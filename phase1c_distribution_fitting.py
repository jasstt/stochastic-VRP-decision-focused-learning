# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 1c
Talep Dagilimi Fitting: Normal vs LogNormal vs Gamma
=============================================================

MANTIK:
-------
Stochastic VRP'nin kalbinde su soru var:
    "Yarin bu ATM'nin talebi kac TL olacak?"

Bunu yanıtlamak icin talebin hangi olasilik dagilimina
uydugunu bulmamiz lazim. Dagilimi bilince:
    1. Olasilik yogunluk fonksiyonu (PDF) hesaplayabiliriz
    2. Belirli bir stok seviyesinde stockout olasiliini verebiliriz
    3. SAA icin senaryo ornekleyebiliriz (ASAMA 1d)
    4. Stochastic VRP modelinde xi_i ~ F_i yazabiliriz

Karsilastiracagimiz dagilimlari:
    - Normal     : Simetrik, negatif deger alabiliyor (ATM icin kotu)
    - LogNormal  : Sag-kuyruklu, hep pozitif -- ATM talebine teorik olarak uygun
    - Gamma      : Esnek, hep pozitif, sag-kuyruk -- LogNormal rakibi

Hangisinin kazandigina su kriterlerle karar veriyoruz:
    1. KS-test p-degeri (Kolmogorov-Smirnov) -- veri dagilimdan mi geliyor?
    2. AIC (Akaike Information Criterion) -- daha dusuk = daha iyi fit
    3. BIC (Bayesian Information Criterion) -- AIC gibi ama parametre sayisini daha sert cezalandirir
    4. Gorsel Q-Q plot -- gozle dogrulama

CIKTI:
    - fit_results: her ATM icin kazanan dagilim + parametreler (dict)
    - Bu ASAMA 1d'de senaryo ornekleme icin kullanilacak
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from scipy.stats import norm, lognorm, gamma, kstest
import warnings
import sys, io, os

warnings.filterwarnings('ignore')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix


# ─────────────────────────────────────────────
# 1. DAGILIM FITTING FONKSIYONLARI
# ─────────────────────────────────────────────

DISTRIBUTIONS = {
    "Normal":    stats.norm,
    "LogNormal": stats.lognorm,
    "Gamma":     stats.gamma,
}


def fit_distribution(data: np.ndarray, dist_name: str) -> dict:
    """
    Verilen veriyi belirtilen dagilima MLE ile fit eder.
    AIC ve BIC hesaplar, KS testi yapar.

    AIC = 2k - 2*ln(L)     (k = parametre sayisi, L = likelihood)
    BIC = k*ln(n) - 2*ln(L)

    Daha kucuk AIC/BIC = daha iyi fit.
    """
    dist = DISTRIBUTIONS[dist_name]
    n    = len(data)

    # MLE ile parametre tahmini
    params = dist.fit(data)
    k      = len(params)   # parametre sayisi

    # Log-likelihood
    log_lik = np.sum(dist.logpdf(data, *params))

    # AIC / BIC
    aic = 2 * k - 2 * log_lik
    bic = k * np.log(n) - 2 * log_lik

    # Kolmogorov-Smirnov testi
    # H0: veri bu dagilimdan geliyor
    # p > 0.05 -> reddedemeyiz (iyi fit)
    ks_stat, ks_p = kstest(data, dist.cdf, args=params)

    return {
        "dist_name": dist_name,
        "params":    params,
        "log_lik":   log_lik,
        "aic":       aic,
        "bic":       bic,
        "ks_stat":   ks_stat,
        "ks_p":      ks_p,
        "k":         k,
    }


def fit_all_distributions(demand_df: pd.DataFrame, network) -> dict:
    """
    Tum ATM'ler icin tum dagilim kombinasyonlarini fit eder.
    Her ATM icin AIC'ye gore en iyi dagilimi secer.

    Donus: {atm_col: {"best": {...}, "all": {...}}}
    """
    results = {}
    atm_cols = demand_df.columns

    for col in atm_cols:
        data = demand_df[col].values.astype(float)
        atm_fits = {}

        for dist_name in DISTRIBUTIONS:
            try:
                fit = fit_distribution(data, dist_name)
                atm_fits[dist_name] = fit
            except Exception as e:
                atm_fits[dist_name] = None

        # AIC'ye gore en iyiyi sec
        valid_fits = {k: v for k, v in atm_fits.items() if v is not None}
        best_name  = min(valid_fits, key=lambda x: valid_fits[x]["aic"])

        results[col] = {
            "best": valid_fits[best_name],
            "all":  valid_fits,
        }

    return results


# ─────────────────────────────────────────────
# 2. OZET TABLO
# ─────────────────────────────────────────────

def print_fit_summary(fit_results: dict, network) -> None:
    print("\n" + "="*80)
    print("  ASAMA 1c -- DAGILIM FITTING SONUCLARI")
    print("="*80)
    print(f"  {'ATM':<30} {'En Iyi Dagilim':<14} {'AIC':>10} {'BIC':>10} {'KS-p':>8} {'KS gecti?':>10}")
    print("  " + "-"*82)

    winner_counts = {"Normal": 0, "LogNormal": 0, "Gamma": 0}

    for col, res in fit_results.items():
        best = res["best"]
        ks_ok = "EVET" if best["ks_p"] > 0.05 else "HAYIR"
        ks_marker = "" if best["ks_p"] > 0.05 else " (!)"
        print(f"  {col:<30} {best['dist_name']:<14} "
              f"{best['aic']:>10.1f} {best['bic']:>10.1f} "
              f"{best['ks_p']:>8.4f} {ks_ok + ks_marker:>10}")
        winner_counts[best["dist_name"]] += 1

    print("="*80)
    print("\n  Kazanan Dagilim Sayilari:")
    for d, c in winner_counts.items():
        bar = "█" * c
        print(f"    {d:<12}: {c:>2} ATM  {bar}")

    print()
    print("  NOT: LogNormal ve Gamma teorik olarak ATM talebi icin")
    print("       daha uygun (hep pozitif, sag-kuyruklu).")
    print("="*80)


# ─────────────────────────────────────────────
# 3. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize_fits(demand_df: pd.DataFrame, fit_results: dict, network,
                   save_path: str = "phase1c_distribution_fits.png") -> None:
    """
    4x5 grid: her ATM icin histogram + 3 dagilim PDF overlay.

    Her panelde:
        - Gri histogram: gercek verinin frekans dagilimi
        - Kirmizi: Normal fit
        - Mavi: LogNormal fit
        - Yesil: Gamma fit
        - Kalin cizgi: AIC'ye gore kazanan dagilim
        - Baslik: Kazanan dagilim ve KS p-degeri
    """
    atm_cols = list(demand_df.columns)
    n_atms   = len(atm_cols)
    ncols    = 4
    nrows    = (n_atms + ncols - 1) // ncols  # 5

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(22, nrows * 4.2))
    fig.patch.set_facecolor('#0d1117')
    fig.suptitle("ATM Talep Dagilimi Fitting: Normal / LogNormal / Gamma",
                 color='white', fontsize=15, fontweight='bold', y=1.01)

    dist_colors = {
        "Normal":    "#ff6b6b",
        "LogNormal": "#4ecdc4",
        "Gamma":     "#ffe66d",
    }

    axes_flat = axes.flatten()

    for idx, col in enumerate(atm_cols):
        ax = axes_flat[idx]
        ax.set_facecolor('#1a1f2e')

        data  = demand_df[col].values / 1000   # bin TL goster
        res   = fit_results[col]
        best  = res["best"]

        # Histogram
        ax.hist(data, bins=30, density=True,
                color='#445566', alpha=0.7, edgecolor='#667788', linewidth=0.3,
                label='Gercek veri')

        # PDF overlay
        x = np.linspace(data.min() * 0.8, data.max() * 1.2, 300)

        for dist_name, dist_obj in DISTRIBUTIONS.items():
            fit = res["all"].get(dist_name)
            if fit is None:
                continue

            # Parametreleri bin TL'ye donustur (veriyi scale ettik)
            # Parametreleri direkt kullanamayiz cunku scale degistirdik
            # Yeniden fit et (sadece gorsel icin)
            try:
                params_scaled = dist_obj.fit(data)
                y = dist_obj.pdf(x, *params_scaled)
                is_best = (dist_name == best["dist_name"])
                ax.plot(x, y,
                        color=dist_colors[dist_name],
                        linewidth=2.8 if is_best else 1.0,
                        alpha=1.0 if is_best else 0.45,
                        linestyle='-' if is_best else '--',
                        label=f"{dist_name}{'*' if is_best else ''}")
            except Exception:
                pass

        # Baslik: ATM ismi + kazanan + KS p
        short_name = col.replace("ATM_", "").replace("_", " ")
        ks_str     = f"KS-p={best['ks_p']:.3f}"
        ax.set_title(f"{short_name}\n[{best['dist_name']}] {ks_str}",
                     color='white', fontsize=7.5, fontweight='bold')

        ax.set_xlabel("Talep (bin TL)", color='#999999', fontsize=7)
        ax.tick_params(colors='#888888', labelsize=6)
        ax.legend(fontsize=5.5, facecolor='#0d1117',
                  edgecolor='#333355', labelcolor='white')
        ax.grid(True, alpha=0.10, color='gray', linestyle='--')
        for sp in ax.spines.values():
            sp.set_edgecolor('#333355')

    # Bos panelleri kapat
    for idx in range(n_atms, len(axes_flat)):
        axes_flat[idx].set_visible(False)

    plt.tight_layout(pad=1.5)
    plt.savefig(save_path, dpi=130, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Gorsel kaydedildi: {save_path}")


def visualize_qq(demand_df: pd.DataFrame, fit_results: dict,
                 save_path: str = "phase1c_qqplots.png") -> None:
    """
    Q-Q plot: teorik kantiller vs gercek veri kantilleri.
    Duz diagonal cizgi = mukemmel fit.
    Sadece her ATM icin KAZANAN dagilimin Q-Q'sunu goster.
    """
    atm_cols = list(demand_df.columns)
    n_atms   = len(atm_cols)
    ncols    = 4
    nrows    = (n_atms + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(22, nrows * 4.0))
    fig.patch.set_facecolor('#0d1117')
    fig.suptitle("Q-Q Plot: Kazanan Dagilim vs Gercek Veri",
                 color='white', fontsize=15, fontweight='bold', y=1.01)

    axes_flat = axes.flatten()

    for idx, col in enumerate(atm_cols):
        ax  = axes_flat[idx]
        ax.set_facecolor('#1a1f2e')
        data = demand_df[col].values / 1000

        res  = fit_results[col]
        best = res["best"]

        dist_obj = DISTRIBUTIONS[best["dist_name"]]
        # scale'li fit
        params = dist_obj.fit(data)

        # Teorik kantiller
        n = len(data)
        probabilities   = (np.arange(1, n + 1) - 0.5) / n
        theoretical_q   = dist_obj.ppf(probabilities, *params)
        empirical_q     = np.sort(data)

        # Scatter
        ax.scatter(theoretical_q, empirical_q,
                   color='#4ecdc4', alpha=0.55, s=8, zorder=3)

        # Ideal cizgi (45 derece)
        mn = min(theoretical_q.min(), empirical_q.min())
        mx = max(theoretical_q.max(), empirical_q.max())
        ax.plot([mn, mx], [mn, mx], color='#ff6b6b',
                linewidth=1.5, zorder=4, label='Ideal fit')

        short_name = col.replace("ATM_", "").replace("_", " ")
        ax.set_title(f"{short_name}\n[{best['dist_name']}]",
                     color='white', fontsize=7.5, fontweight='bold')
        ax.set_xlabel("Teorik", color='#999999', fontsize=7)
        ax.set_ylabel("Gercek", color='#999999', fontsize=7)
        ax.tick_params(colors='#888888', labelsize=6)
        ax.grid(True, alpha=0.10, color='gray', linestyle='--')
        for sp in ax.spines.values():
            sp.set_edgecolor('#333355')

    for idx in range(n_atms, len(axes_flat)):
        axes_flat[idx].set_visible(False)

    plt.tight_layout(pad=1.5)
    plt.savefig(save_path, dpi=130, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] Q-Q plot kaydedildi: {save_path}")


# ─────────────────────────────────────────────
# 4. SONUCLARI KAYDET (ASAMA 1d icin)
# ─────────────────────────────────────────────

def save_fit_params(fit_results: dict,
                    path: str = "data_fit_params.csv") -> pd.DataFrame:
    """
    Her ATM'nin kazanan dagilimini ve parametrelerini CSV'ye yazar.
    ASAMA 1d bu CSV'yi okuyarak senaryo ornekleyecek.
    """
    rows = []
    for col, res in fit_results.items():
        best = res["best"]
        row  = {
            "atm_col":   col,
            "dist_name": best["dist_name"],
            "aic":       best["aic"],
            "bic":       best["bic"],
            "ks_stat":   best["ks_stat"],
            "ks_p":      best["ks_p"],
        }
        # Parametreler dagilima gore degisken sayida
        for pi, pval in enumerate(best["params"]):
            row[f"param_{pi}"] = pval

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"  [SAVED] Fit parametreleri: {path}  ({len(df)} satir)")
    return df


def print_aic_comparison_table(fit_results: dict) -> None:
    """
    Tum ATM'ler icin 3 dagilimin AIC degerlerini tablo halinde goster.
    Kucuk AIC = iyi fit.
    """
    print("\n  AIC Karsilastirma Tablosu (dusuk = daha iyi fit):")
    print(f"  {'ATM':<28} {'Normal':>12} {'LogNormal':>12} {'Gamma':>12} {'Kazanan':>12}")
    print("  " + "-"*80)

    for col, res in fit_results.items():
        short = col.replace("ATM_", "A").replace("_", "-")[:24]
        aics  = {d: res["all"][d]["aic"] for d in res["all"] if res["all"][d]}
        best  = res["best"]["dist_name"]
        n_aic = aics.get("Normal",    float('inf'))
        l_aic = aics.get("LogNormal", float('inf'))
        g_aic = aics.get("Gamma",     float('inf'))

        # Kazanani kalin goster (ASCII icin *)
        def fmt(v, name):
            s = f"{v:12.1f}"
            return f"{'*':>1}{s[1:]}" if name == best else s

        print(f"  {short:<28}"
              f"{fmt(n_aic, 'Normal')}"
              f"{fmt(l_aic, 'LogNormal')}"
              f"{fmt(g_aic, 'Gamma')}"
              f"  {best:>12}")


# ─────────────────────────────────────────────
# 5. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 1c -- Dagilim Fitting Basliyor...\n")

    # Network yukle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)

    # ASAMA 1b ciktisini oku
    demand_path = os.path.join(os.path.dirname(__file__), "data_demand_365.csv")
    demand_df   = pd.read_csv(demand_path, index_col="tarih", parse_dates=True)
    print(f"  [OK] Talep verisi yuklendi: {demand_df.shape}")

    # Fitting
    print("  [..] 3 dagilim x 20 ATM fitting yapiliyor (MLE)...")
    fit_results = fit_all_distributions(demand_df, network)
    print("  [OK] Fitting tamamlandi.")

    # Ozet tablo
    print_fit_summary(fit_results, network)
    print_aic_comparison_table(fit_results)

    # Gorseller
    print("\n  [..] Histogram + PDF overlay grafigi uretiliyor...")
    visualize_fits(demand_df, fit_results, network)

    print("  [..] Q-Q plot grafigi uretiliyor...")
    visualize_qq(demand_df, fit_results)

    # Kaydet
    fit_params_df = save_fit_params(fit_results)

    print("\n[OK] ASAMA 1c tamamlandi.")
    print("     fit_results  -> ASAMA 1d'ye (SAA senaryo ornekleme) hazir.")
    print("     data_fit_params.csv kaydedildi.")
