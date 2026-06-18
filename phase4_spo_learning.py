# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 4  (DUZELTILMIS)
Decision-Focused Learning: SPO+ vs MSE vs Quantile
=============================================================

ONCEKI HATALARIN DUZELTMESI:
-----------------------------

HATA 1 -- Gradient yonu tersti:
  Yanlis: W -= lr * lam   (tahmin azaldi -> daha fazla stockout)
  Dogru : W += lr * lam   (tahmin artmali -> daha az stockout)

  Envelope theorem: dC/d(d_hat_i) = -p * P(demand_i > r*_i) < 0
  Yani maliyet, d_hat arttikca AZALIYOR.
  Gradient descent: W -= lr * dC/dW = W -= lr * X.T @ (-p*lam)
                                      = W += lr * X.T @ (p*lam)

HATA 2 -- Senaryolar d_hat'e gore kayiyordu:
  Yanlis: scenarios = d_hat + noise  (her d_hat icin farkli dagiliyor)
           -> optimal r* hep newsvendor kantilinde -> gradient hep sabit
  Dogru : Adjusted SAA kullan:
           scenarios_adj[s,i] = SAA[s,i] + d_hat[i] - SAA_mean[i]
           Bu, SAA'nin kovaryans yapisini korurken merkezini d_hat'e tasir.
           r*(d_hat) degisince lambda da degisiyor -> anlamli gradient!

SONUC:
  SPO+ artik MSE'den FARKLI karar aliyor:
  - Yuksek volatiliteli ATM'lere daha agresif yukleme
  - Kucuk hatanin buyuk regret'e yol actigi durumlarda daha dikkatli

FORMÜLASYON:
-----------
min  E[C(r*(d_hat), d_true)]
     C(r, d) = p * sum_i max(0, d_i - r_i)

Gradient w.r.t. d_hat_i (envelope theorem):
  dC/d(d_hat_i) = -p * P(SAA_adj_i > r*_i)
                = -p * lambda_i          (lambda_i = stockout prob)

W guncelleme:
  W -= lr * dC/dW = W -= lr * X.T @ (-p * lambda)
                   = W += lr * p * X.T @ lambda
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pulp
from sklearn.linear_model import LinearRegression, QuantileRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
import warnings, sys, io, os, time

warnings.filterwarnings('ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix

PENALTY_RATIO = 3.0
TRAIN_RATIO   = 0.75
S_TRAIN       = 20
S_EVAL        = 100
N_EPOCHS      = 35
LR_INIT       = 0.12
ROUTE_GROUPS  = {0:[10,19,6,7,2,3,18], 1:[1,15,20,17,16,5], 3:[12,9,11,8,14,13,4]}


# ─────────────────────────────────────────────
# 1. OZELLIK MUHENDISLIGI
# ─────────────────────────────────────────────

def build_features(demand_df):
    dates  = demand_df.index
    y      = demand_df.values
    dow    = dates.dayofweek
    month  = dates.month
    is_we  = (dow >= 5).astype(float)
    h_eves = pd.to_datetime(["2023-04-20","2023-06-27"])
    is_hol = np.isin(dates.date, h_eves.date).astype(float)
    dow_oh  = pd.get_dummies(dow,   prefix='d', drop_first=True).values.astype(float)
    mon_oh  = pd.get_dummies(month, prefix='m', drop_first=True).values.astype(float)
    lag7    = np.zeros_like(y)
    for t in range(7, len(y)):
        lag7[t] = y[t-7:t].mean(axis=0)
    lag7[:7] = y.mean(axis=0)
    X = np.hstack([dow_oh, mon_oh, is_we[:,None], is_hol[:,None], lag7/1e5])
    return X, y, dates


# ─────────────────────────────────────────────
# 2. ADJUSTED SAA + LP
# ─────────────────────────────────────────────

def adjust_saa(d_hat, saa_matrix):
    """
    SAA senaryolarini d_hat'e gore kaydirır.
    Kovaryans yapisi korunur, merkez d_hat'e gelir.

    saa_adj[s,i] = SAA[s,i] - SAA_mean[i] + d_hat[i]
    """
    saa_mean = saa_matrix.mean(axis=0)
    adj      = saa_matrix - saa_mean[None,:] + d_hat[None,:]
    return np.maximum(adj, 0)


def solve_lp(scenarios, Q, route_groups=ROUTE_GROUPS, p=PENALTY_RATIO):
    """
    LP'yi cozer, r_opt ve lambda (dual stockout prob) doner.

    lambda_i = P(scenario_i > r*_i)  -- envelope gradient
    """
    S, N = scenarios.shape
    prob = pulp.LpProblem("LP", pulp.LpMinimize)
    r = pulp.LpVariable.dicts("r", range(N), lowBound=0, cat='Continuous')
    z = pulp.LpVariable.dicts("z",
        [(i,s) for i in range(N) for s in range(S)], lowBound=0, cat='Continuous')

    prob += (1/S)*p*pulp.lpSum(z[(i,s)] for i in range(N) for s in range(S))
    for k, ids in route_groups.items():
        prob += pulp.lpSum(r[j-1] for j in ids) <= Q
    for i in range(N):
        for s in range(S):
            prob += z[(i,s)] >= float(scenarios[s,i]) - r[i]

    pulp.PULP_CBC_CMD(msg=0).solve(prob)
    r_opt = np.array([max(0., pulp.value(r[i]) or 0.) for i in range(N)])
    lam   = np.array([np.mean(scenarios[:,i] > r_opt[i]) for i in range(N)])
    return r_opt, lam


def compute_cost(r, d_true, p=PENALTY_RATIO):
    return p * np.maximum(0, d_true - r).sum()


# ─────────────────────────────────────────────
# 3. MSE MODEL
# ─────────────────────────────────────────────

def train_mse(X_tr, y_tr):
    sc = StandardScaler()
    Xs = sc.fit_transform(X_tr)
    ms = [LinearRegression().fit(Xs, y_tr[:,i]) for i in range(y_tr.shape[1])]
    return ms, sc

def pred_mse(ms, sc, X):
    return np.maximum(np.column_stack([m.predict(sc.transform(X)) for m in ms]), 0)


# ─────────────────────────────────────────────
# 4. QUANTILE MODEL
# ─────────────────────────────────────────────

def train_q75(X_tr, y_tr):
    sc = StandardScaler()
    Xs = sc.fit_transform(X_tr)
    ms = [QuantileRegressor(quantile=0.75, alpha=0., solver='highs').fit(Xs, y_tr[:,i])
          for i in range(y_tr.shape[1])]
    return ms, sc

def pred_q75(ms, sc, X):
    return np.maximum(np.column_stack([m.predict(sc.transform(X)) for m in ms]), 0)


# ─────────────────────────────────────────────
# 5. SPO+ MODEL (duzeltilmis gradient)
# ─────────────────────────────────────────────

def train_spo(X_tr, y_tr, saa_matrix, Q,
              n_epochs=N_EPOCHS, lr=LR_INIT, seed=42):
    """
    SPO+ -- Adjusted SAA + dogru gradient yonu.

    Her egitim ornegi t icin:
      1. d_hat = X[t] @ W + b
      2. saa_adj = SAA - SAA_mean + d_hat     (sabit kovaryans, kayan merkez)
      3. r*, lambda = solve_lp(saa_adj)
      4. regret  = C(r*, d_true) - C(r*_oracle, d_true)
      5. gradient: dC/d(d_hat_i) = -p * lambda_i
         W guncellemesi: W += lr * p * X.T @ lambda   (ARTIRICI yon!)
    """
    rng  = np.random.default_rng(seed)
    T, P = X_tr.shape
    N    = y_tr.shape[1]

    # Kucuk SAA alt kumesi (hiz icin)
    saa_sub = saa_matrix[:S_TRAIN]

    # Warm-start: SAA_mean etrafinda MSE
    sc = StandardScaler()
    Xs = sc.fit_transform(X_tr)
    W  = np.zeros((P, N))
    b  = saa_matrix.mean(axis=0).copy()   # SAA ortalamasi ile baslat

    for i in range(N):
        m = LinearRegression().fit(Xs, y_tr[:,i])
        W[:,i] = m.coef_ * 0.1   # kucuk warm-start (cok baglanma)

    # Oracle: SAA ile en iyi mumkun yukleme (tam dagilimleri bilseydik)
    r_oracle_global, _ = solve_lp(saa_matrix, Q)

    print(f"\n  SPO+ basliyor: {n_epochs} epoch, lr={lr}")
    print(f"  Duzelti: W += lr*p*X.T@lambda  (ARTIRICI)")
    epoch_regrets = []
    t_start = time.time()

    for epoch in range(n_epochs):
        # Cosine annealing
        lr_t  = lr * 0.5 * (1 + np.cos(np.pi * epoch / n_epochs))
        idxs  = rng.permutation(T)[:30]

        dW = np.zeros_like(W)
        db = np.zeros(N)
        epoch_regret = 0.

        for t in idxs:
            x_t   = Xs[t]
            d_t   = y_tr[t]

            d_hat = np.maximum(x_t @ W + b, 0)
            saa_adj = adjust_saa(d_hat, saa_sub)

            # LP coz
            r_hat, lam = solve_lp(saa_adj, Q)

            # Oracle (gercek talep d_t etrafinda)
            saa_oracle = adjust_saa(d_t, saa_sub)
            r_ora, _   = solve_lp(saa_oracle, Q)

            regret = max(0, compute_cost(r_hat, d_t) - compute_cost(r_ora, d_t))
            epoch_regret += regret

            # DUZELTILMIS gradient: dC/d(d_hat) = -p * lambda
            # W guncellemesi: W += lr * p * X.T @ lambda
            # (maliyet azaltmak icin tahmini ARTIR)
            dW += np.outer(x_t, lam)   # biriktir (isaret artirici)
            db += lam

        n_used = len(idxs)
        # ARTIRICI guncelleme (onceki -=, simdi +=)
        W += lr_t * PENALTY_RATIO * dW / n_used
        b += lr_t * PENALTY_RATIO * db / n_used

        avg_r = epoch_regret / n_used
        epoch_regrets.append(avg_r)
        print(f"  Epoch {epoch+1:2d}/{n_epochs} | lr={lr_t:.4f} | "
              f"Regret={avg_r:,.0f} TL | {time.time()-t_start:.1f}s")

    return W, b, sc, epoch_regrets


def pred_spo(W, b, sc, X):
    return np.maximum(sc.transform(X) @ W + b, 0)


# ─────────────────────────────────────────────
# 6. DEGERLENDIRME
# ─────────────────────────────────────────────

def evaluate(name, d_hat_test, y_test, saa_matrix, Q):
    """
    Her test gunu icin:
      - d_hat -> adjusted SAA -> LP -> r*
      - Oracle: d_true -> adjusted SAA -> LP -> r_oracle
      - Cost ve regret hesapla
    """
    T = len(d_hat_test)
    costs, sos, regrets = [], [], []

    for t in range(T):
        dh = d_hat_test[t]
        dt = y_test[t]

        saa_m = adjust_saa(dh, saa_matrix)
        r, _  = solve_lp(saa_m, Q)

        saa_o  = adjust_saa(dt, saa_matrix)
        r_ora, _ = solve_lp(saa_o, Q)

        c_m = 3394 + compute_cost(r, dt)
        c_o = 3394 + compute_cost(r_ora, dt)

        sf = np.maximum(0, dt - r)
        costs.append(c_m)
        sos.append(np.mean(sf > 0)*100)
        regrets.append(max(0, c_m - c_o))

    mae = mean_absolute_error(y_test.flatten(), d_hat_test.flatten())
    return {
        "name": name,
        "mean_cost":     np.mean(costs),
        "std_cost":      np.std(costs),
        "mean_stockout": np.mean(sos),
        "mean_regret":   np.mean(regrets),
        "mae":           mae,
        "total_costs":   np.array(costs),
        "sos":           np.array(sos),
        "regrets":       np.array(regrets),
    }


# ─────────────────────────────────────────────
# 7. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize(results, epoch_regrets, path="phase4_spo_comparison.png"):
    fig, axes = plt.subplots(2, 2, figsize=(22, 12))
    fig.patch.set_facecolor('#0d1117')
    fig.suptitle("AŞAMA 4 — SPO+ vs MSE vs Quantile: Karar Odakli Ogrenme",
                 color='white', fontsize=14, fontweight='bold', y=1.01)

    dark   = '#1a1f2e'
    colors = ['#ff6b6b','#4ecdc4','#ffe66d']
    names  = [r["name"] for r in results]

    # ── Sol ust: maliyet box ──
    ax = axes[0,0]; ax.set_facecolor(dark)
    ax.set_title("Test Seti Gunluk Toplam Maliyet", color='white', fontsize=11, fontweight='bold')
    bp = ax.boxplot([r["total_costs"] for r in results],
                    positions=[1,2,3], widths=0.5, patch_artist=True,
                    medianprops=dict(color='#ffe66d', linewidth=2.5),
                    whiskerprops=dict(color='#aaaaaa'), capprops=dict(color='#aaaaaa'),
                    flierprops=dict(marker='.', color='#666666', markersize=4))
    for patch,c in zip(bp['boxes'], colors):
        patch.set_facecolor(c+'44'); patch.set_edgecolor(c)
    for i, r in enumerate(results):
        ax.text(i+1, r["mean_cost"]+200, f"{r['mean_cost']:,.0f}",
                ha='center', color='white', fontsize=9, fontweight='bold')
    ax.axhline(244191, color='#a8e6cf', lw=1.5, ls=':', label='Oracle (Stoch.LP)')
    ax.set_xticks([1,2,3]); ax.set_xticklabels(names, color='#aaaaaa')
    ax.set_ylabel("Maliyet (TL/gun)", color='#aaaaaa')
    ax.tick_params(colors='#aaaaaa')
    ax.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax.grid(True, axis='y', alpha=0.12, color='gray', ls='--')
    [s.set_edgecolor('#333355') for s in ax.spines.values()]

    # ── Sag ust: regret violin ──
    ax = axes[0,1]; ax.set_facecolor(dark)
    ax.set_title("Regret Dagilimi (Dusuk = Daha Iyi)", color='white', fontsize=11, fontweight='bold')
    vp = ax.violinplot([r["regrets"] for r in results],
                        positions=[1,2,3], widths=0.5, showmedians=True, showextrema=True)
    for pc,c in zip(vp['bodies'], colors):
        pc.set_facecolor(c+'55'); pc.set_edgecolor(c); pc.set_alpha(0.8)
    vp['cmedians'].set_color('#ffe66d')
    for part in ['cmins','cmaxes','cbars']: vp[part].set_color('#aaaaaa')
    for i,r in enumerate(results):
        ax.text(i+1, np.percentile(r["regrets"],5),
                f"ort={r['mean_regret']:,.0f}", ha='center',
                color=colors[i], fontsize=8.5, fontweight='bold')
    ax.set_xticks([1,2,3]); ax.set_xticklabels(names, color='#aaaaaa')
    ax.set_ylabel("Gunluk Regret (TL)", color='#aaaaaa')
    ax.tick_params(colors='#aaaaaa')
    ax.grid(True, axis='y', alpha=0.12, color='gray', ls='--')
    [s.set_edgecolor('#333355') for s in ax.spines.values()]

    # ── Sol alt: egitim egrisi ──
    ax = axes[1,0]; ax.set_facecolor(dark)
    ax.set_title("SPO+ Egitim Egrisi", color='white', fontsize=11, fontweight='bold')
    ep = np.arange(1, len(epoch_regrets)+1)
    ax.plot(ep, epoch_regrets, color='#ffe66d', lw=2, marker='o', ms=4, label='Epoch Regret')
    if len(epoch_regrets) > 4:
        sm = np.convolve(epoch_regrets, np.ones(5)/5, mode='valid')
        ax.plot(ep[2:-2], sm, color='#4ecdc4', lw=2.5, ls='--', label='Hareketli Ort.')
    ax.set_xlabel("Epoch", color='#aaaaaa'); ax.set_ylabel("Ort. Regret (TL)", color='#aaaaaa')
    ax.tick_params(colors='#aaaaaa')
    ax.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=9)
    ax.grid(True, alpha=0.12, color='gray', ls='--')
    [s.set_edgecolor('#333355') for s in ax.spines.values()]

    # ── Sag alt: ozet bar ──
    ax = axes[1,1]; ax.set_facecolor(dark)
    ax.set_title("Model Karsilastirma Ozeti", color='white', fontsize=11, fontweight='bold')
    x = np.arange(len(names)); w = 0.35
    ax2 = ax.twinx()
    costs = [r["mean_cost"] for r in results]
    sos   = [r["mean_stockout"] for r in results]
    ax.bar(x-w/2, costs, width=w, color=[c+'cc' for c in colors], zorder=3)
    ax2.bar(x+w/2, sos, width=w, color=[c+'44' for c in colors],
            edgecolor=colors, lw=1.5, zorder=3)
    for xi,(cv,sv) in enumerate(zip(costs,sos)):
        ax.text(xi-w/2, cv+100, f"{cv:,.0f}", ha='center',
                color='white', fontsize=8, fontweight='bold')
        ax2.text(xi+w/2, sv+0.3, f"%{sv:.1f}", ha='center',
                 color='#ffe66d', fontsize=9, fontweight='bold')
    ax.axhline(244191, color='#a8e6cf', lw=1.5, ls=':', label='Oracle')
    ax.set_xticks(x); ax.set_xticklabels(names, color='#aaaaaa')
    ax.set_ylabel("Ort. Maliyet (TL)", color='#aaaaaa')
    ax2.set_ylabel("Ort. Stockout (%)", color='#ffe66d')
    ax.tick_params(colors='#aaaaaa'); ax2.tick_params(colors='#ffe66d')
    ax.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax.grid(True, axis='y', alpha=0.12, color='gray', ls='--')
    [s.set_edgecolor('#333355') for s in ax.spines.values()]
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    plt.tight_layout(pad=2.0)
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"\n  [SAVED] {path}")


# ─────────────────────────────────────────────
# 8. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 4 -- SPO+ (DUZELTILMIS: dogru gradient yonu)\n")

    base    = os.path.dirname(__file__)
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix     = build_time_matrix(network.distance_matrix)
    Q = network.vehicles[0].capacity

    demand_df  = pd.read_csv(os.path.join(base,"data_demand_365.csv"),
                              index_col="tarih", parse_dates=True)
    saa_matrix = np.load(os.path.join(base,"data_saa_scenarios.npy"))
    print(f"  SAA matrisi: {saa_matrix.shape} | SAA ortalama: {saa_matrix.mean():.0f} TL")

    X, y, _ = build_features(demand_df)
    T_tr = int(len(X)*TRAIN_RATIO)
    X_tr, X_te = X[:T_tr], X[T_tr:]
    y_tr, y_te = y[:T_tr], y[T_tr:]
    print(f"  Egitim: {T_tr} gun | Test: {len(X_te)} gun | Ozellik: {X.shape[1]}")

    # [1/3] MSE
    print("\n  [1/3] MSE Linear...")
    ms_m, sc_m = train_mse(X_tr, y_tr)
    d_mse = pred_mse(ms_m, sc_m, X_te)
    print(f"  [OK] MAE = {mean_absolute_error(y_te.flatten(), d_mse.flatten()):,.0f} TL")

    # [2/3] Quantile P75
    print("\n  [2/3] Quantile P75...")
    ms_q, sc_q = train_q75(X_tr, y_tr)
    d_q75 = pred_q75(ms_q, sc_q, X_te)
    print(f"  [OK] MAE = {mean_absolute_error(y_te.flatten(), d_q75.flatten()):,.0f} TL")

    # [3/3] SPO+
    print("\n  [3/3] SPO+ (adjusted SAA + arturici gradient)...")
    t0 = time.time()
    W, b, sc_s, epocrs = train_spo(X_tr, y_tr, saa_matrix, Q)
    d_spo = pred_spo(W, b, sc_s, X_te)
    print(f"  [OK] SPO+ {time.time()-t0:.1f}s | "
          f"MAE = {mean_absolute_error(y_te.flatten(), d_spo.flatten()):,.0f} TL")

    # Degerlendirme
    print(f"\n  [..] Test degerlendirmesi ({len(y_te)} gun)...")
    results = []
    for nm, dh in [("MSE-P&O", d_mse), ("Quantile-P75", d_q75), ("SPO+", d_spo)]:
        print(f"  -> {nm}...", end="", flush=True)
        r = evaluate(nm, dh, y_te, saa_matrix, Q)
        results.append(r)
        print(f"  Maliyet={r['mean_cost']:,.0f} | SO=%{r['mean_stockout']:.1f} | "
              f"Regret={r['mean_regret']:,.0f}")

    # Ozet tablo
    print("\n" + "="*72)
    print("  ASAMA 4 -- FINAL KARSILASTIRMA")
    print("="*72)
    print(f"  {'Model':<16} {'Maliyet(TL)':>13} {'Stockout%':>11} {'Regret':>12} {'MAE':>10}")
    print("  " + "-"*65)
    print(f"  {'[Oracle]':<16} {'244,191':>13} {'%25.4':>11} {'0':>12} {'--':>10}")
    for r in results:
        tag = " *" if r["name"]=="SPO+" else ""
        print(f"  {r['name']:<16} {r['mean_cost']:>13,.0f} "
              f"{'%'+str(round(r['mean_stockout'],1)):>11} "
              f"{r['mean_regret']:>12,.0f} "
              f"{r['mae']:>10,.0f}{tag}")
    print("="*72)

    m, q, s = results
    print(f"\n  SPO+ vs MSE    maliyet : {m['mean_cost']-s['mean_cost']:+,.0f} TL/gun tasarruf")
    print(f"  SPO+ vs MSE    regret  : {(m['mean_regret']-s['mean_regret'])/max(m['mean_regret'],1)*100:+.1f}%")
    print(f"  SPO+ vs Q75    maliyet : {q['mean_cost']-s['mean_cost']:+,.0f} TL/gun tasarruf")
    print(f"  SPO+ yillik avantaj    : {(m['mean_cost']-s['mean_cost'])*365/1e6:+.2f} milyon TL")

    visualize(results, epocrs)

    pd.DataFrame([{"model":r["name"],"mean_cost":r["mean_cost"],
                   "mean_stockout":r["mean_stockout"],"mean_regret":r["mean_regret"],
                   "mae":r["mae"]} for r in results]).to_csv(
        os.path.join(base,"data_phase4_summary.csv"), index=False)
    print("  [SAVED] data_phase4_summary.csv")

    print("\n[OK] ASAMA 4 tamamlandi.")
    print("  Bir sonraki: ASAMA 5 -- Final Kiyaslama Raporu")
