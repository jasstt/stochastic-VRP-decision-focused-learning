# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 3a
Two-Stage Stochastic VRP -- SAA ile Optimal Yukleme LP
=============================================================

MANTIK:
-------
Two-Stage Stochastic VRP'nin iki karari var:

AŞAMA 1 (Burada-ve-Simdi, belirsizlik gelmeden):
    x_ijk  -- hangi arac hangi ATM'ye gider? (rota)
    r_i    -- o ATM'ye ne kadar nakit yüklenir? (yukleme miktari)

AŞAMA 2 (Bekle-ve-Gor, talep xi_i^s geldikten sonra):
    z_i^s  -- ATM i'de senaryo s'de kac TL eksik kaldi? (recourse)

Pratikte:
    Rotalar cok degismez (operasyonel kural),
    ama YUKLEME MIKTARLARI her gun optimize edilir.

Bu bolumde rotalar Phase 2a'dan sabit alinir,
yukleme miktarlari r_i LP ile stochastic optimize edilir.

Bu yaklasim "Expected Value with Recourse" veya
"Stochastic Loading Problem" olarak da bilinir.

FORMÜLASYON:
-----------
min  (1/S) * Σ_s Σ_i  p * z_i^s     (beklenen ceza)

s.t.
    Σ_{i ∈ R_k}  r_i  ≤  Q_k,         ∀k   (araç kapasite)
    z_i^s  ≥  xi_i^s  -  r_i,         ∀s,i (eksik nakit = recourse)
    z_i^s  ≥  0,                       ∀s,i
    r_i    ≥  0,                       ∀i

Burada:
    R_k     = arac k'nin servise girdigi ATM kumesi (Phase 2a'dan)
    Q_k     = araç k'nin nakit kapasitesi (500.000 TL)
    xi_i^s  = senaryo s'de ATM i'nin talebi (SAA matrisinden)
    p       = ceza katsayisi (TL eksik basina TL maliyet)

DEĞİŞKEN SAYISI:
    r_i  : N = 20 (surekli)
    z_i^s: S * N = 100 * 20 = 2.000 (surekli)
    Toplam 2.020 degisken -- LP oldugundan MILISANIYEDE cozer!

KIYASLAMA:
----------
Det. plan  : r_i = d_i (ortalama),  ceza hesaplanir
Stochastic : r_i = optimized         ceza minimize edildi

VSS = Value of Stochastic Solution = Det.maliyet - Stoch.maliyet
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pulp
import time
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix

# Maliyet parametreleri (Phase 2a ile tutarli)
COST_PER_KM   = 8.5    # TL/km
PENALTY_RATIO = 3.0    # her 1 TL eksik nakit -> 3 TL ceza (operasyonel maliyet)


# ─────────────────────────────────────────────
# 1. PHASE 2a ROTALARINI OKU
# ─────────────────────────────────────────────

def load_routes_from_csv(base: str) -> dict:
    """
    Phase 2a'nin ciktisi data_det_routes.csv'den rotalari yukler.
    Donus: {vehicle_id: [0, atm1, atm2, ..., 0]}
    """
    df = pd.read_csv(os.path.join(base, "data_det_routes.csv"))
    routes = {}
    for k, grp in df.groupby("vehicle"):
        route = grp.sort_values("position")["node"].tolist()
        if len(route) > 2:   # bos rotayi atla
            routes[int(k)] = route
    return routes


def get_route_groups(routes: dict) -> dict:
    """
    Her araç icin hangi ATM'leri servis ettigini cikarir.
    Donus: {vehicle_id: [atm_id1, atm_id2, ...]}  (0=depo haric)
    """
    groups = {}
    for k, route in routes.items():
        groups[k] = [n for n in route if n > 0]
    return groups


# ─────────────────────────────────────────────
# 2. DETERMINISTIK REFERANS MALIYETI
# ─────────────────────────────────────────────

def compute_det_cost(demands_det: np.ndarray,
                     route_groups: dict,
                     scenario_matrix: np.ndarray,
                     network) -> dict:
    """
    Phase 2a'nin deterministik yukleme planinin beklenen toplam maliyetini hesaplar.
    r_i = d_i (nokta tahmin) -> ceza = p * max(0, xi^s - r_i)
    Rota maliyeti Phase 2a'dan sabit: 3394 TL/gun
    """
    S, N = scenario_matrix.shape
    r_det = demands_det.copy()

    # Ceza maliyeti
    shortfall_matrix = np.maximum(0, scenario_matrix - r_det[np.newaxis, :])
    expected_penalty = PENALTY_RATIO * shortfall_matrix.mean(axis=0).sum()

    # Rota maliyeti (Phase 2a'dan)
    route_cost_det = 3394.0

    total_cost_det = route_cost_det + expected_penalty

    return {
        "route_cost":     route_cost_det,
        "expected_penalty": expected_penalty,
        "total_cost":     total_cost_det,
        "shortfall_matrix": shortfall_matrix,
        "r_values":       r_det,
    }


# ─────────────────────────────────────────────
# 3. STOCHASTIC YUKLEME LP
# ─────────────────────────────────────────────

def solve_stochastic_loading(route_groups: dict,
                              scenario_matrix: np.ndarray,
                              network,
                              penalty: float = PENALTY_RATIO) -> dict:
    """
    r_i yukleme miktarlarini minimize ederek stochastic LP cozumu.

    LP degiskenleri:
        r[i]    : ATM i'ye yuklenen nakit (TL)
        z[i][s] : ATM i'nin senaryo s'deki eksigi (TL)

    Amaç: (1/S) * p * Σ_s Σ_i z[i][s]   minimize et
    """
    S, N = scenario_matrix.shape
    Q    = network.vehicles[0].capacity
    prob = pulp.LpProblem("Stochastic_Loading_LP", pulp.LpMinimize)

    # ── Degiskenler ──
    r = pulp.LpVariable.dicts("r", range(N), lowBound=0, cat='Continuous')
    z = pulp.LpVariable.dicts("z",
                               [(i, s) for i in range(N) for s in range(S)],
                               lowBound=0, cat='Continuous')

    # ── Amac: beklenen ceza ──
    prob += (1/S) * penalty * pulp.lpSum(
        z[(i, s)] for i in range(N) for s in range(S)
    ), "Beklenen_Ceza"

    # ── Kisit 1: araç kapasitesi (her rota grubu) ──
    for k, atm_ids in route_groups.items():
        atm_idxs = [aid - 1 for aid in atm_ids]   # 1-indexed -> 0-indexed
        prob += (
            pulp.lpSum(r[j] for j in atm_idxs) <= Q,
            f"Kapasite_Arac_{k}"
        )

    # ── Kisit 2: shortfall linearizasyonu z[i][s] >= xi_i^s - r_i ──
    for i in range(N):
        for s in range(S):
            xi_is = float(scenario_matrix[s, i])
            prob += (
                z[(i, s)] >= xi_is - r[i],
                f"Shortfall_{i}_{s}"
            )

    # ── Coz (LP -- cok hizli) ──
    solver = pulp.PULP_CBC_CMD(msg=0)
    t0     = time.time()
    prob.solve(solver)
    elapsed = time.time() - t0

    # ── Sonuclari topla ──
    r_opt  = np.array([pulp.value(r[i]) for i in range(N)])
    z_vals = np.array([[pulp.value(z[(i, s)]) for s in range(S)]
                        for i in range(N)])

    expected_penalty = (1/S) * penalty * z_vals.sum()
    route_cost_stoch  = 3394.0   # rotalar ayni (Phase 2a)
    total_cost_stoch  = route_cost_stoch + expected_penalty

    shortfall_matrix  = np.maximum(0, scenario_matrix - r_opt[np.newaxis, :])

    print(f"\n  [OK] LP cozuldu: {pulp.LpStatus[prob.status]} "
          f"({elapsed:.2f} sn, {len(prob.variables())} degisken, {len(prob.constraints)} kisit)")

    return {
        "route_cost":       route_cost_stoch,
        "expected_penalty": expected_penalty,
        "total_cost":       total_cost_stoch,
        "r_values":         r_opt,
        "shortfall_matrix": shortfall_matrix,
        "status":           pulp.LpStatus[prob.status],
        "elapsed":          elapsed,
    }


# ─────────────────────────────────────────────
# 4. KIYASLAMA VE VSS
# ─────────────────────────────────────────────

def compare_and_print(det: dict, stoch: dict,
                      demands_det: np.ndarray,
                      scenario_matrix: np.ndarray,
                      network) -> None:

    S, N = scenario_matrix.shape
    Q    = network.vehicles[0].capacity

    def stockout_stats(sfm):
        n_events  = np.sum(sfm > 0)
        rate      = n_events / (S * N)
        scen_rate = np.mean(np.any(sfm > 0, axis=1))
        total_sf  = sfm.sum()
        return n_events, rate, scen_rate, total_sf

    det_ev,   det_rate,   det_scen,   det_sf   = stockout_stats(det["shortfall_matrix"])
    stoch_ev, stoch_rate, stoch_scen, stoch_sf = stockout_stats(stoch["shortfall_matrix"])

    vss_abs = det["total_cost"] - stoch["total_cost"]
    vss_pct = vss_abs / det["total_cost"] * 100

    print("\n" + "="*70)
    print("  KIYASLAMA: DETERMINİSTIK vs STOCHASTIC YUKLEME PLANI")
    print("="*70)
    print(f"\n  {'Metrik':<35} {'Deterministik':>15} {'Stochastic':>15} {'Fark':>12}")
    print("  " + "-"*77)

    rows = [
        ("Rota Maliyeti (TL/gun)",       det['route_cost'],       stoch['route_cost'],       False),
        ("Beklenen Ceza (TL/gun)",        det['expected_penalty'], stoch['expected_penalty'], True),
        ("TOPLAM Maliyet (TL/gun)",       det['total_cost'],       stoch['total_cost'],       True),
        ("Stockout Orani (%)",            det_rate*100,            stoch_rate*100,            True),
        ("Senaryo Riski (%)",             det_scen*100,            stoch_scen*100,            True),
        ("Toplam Eksik Nakit (TL)",       det_sf,                  stoch_sf,                  True),
    ]
    for label, dv, sv, lower_better in rows:
        diff     = sv - dv
        diff_str = f"{diff:+,.1f}" if abs(diff) < 1e6 else f"{diff/1e6:+.2f}M"
        if lower_better:
            color_tag = " ✓" if sv < dv else " ✗"
        else:
            color_tag = ""
        print(f"  {label:<35} {dv:>15,.1f} {sv:>15,.1f} {diff_str:>12}{color_tag}")

    print("  " + "-"*77)
    print(f"\n  VSS (Value of Stochastic Solution):")
    print(f"    Mutlak tasarruf   : {vss_abs:>10,.2f} TL/gun")
    print(f"    Yuzde tasarruf    : %{vss_pct:.1f}")
    print(f"    Yillik tasarruf   : {vss_abs * 365 / 1e6:>10.2f} milyon TL")
    print()
    print(f"  Stockout azalmasi  : %{det_rate*100:.1f} -> %{stoch_rate*100:.1f}")
    print(f"  Senaryo riski      : %{det_scen*100:.1f} -> %{stoch_scen*100:.1f}")
    print()

    # Per-ATM yukleme karsilastirma
    print(f"  Per-ATM Yukleme Karsilastirmasi (r_i):")
    print(f"  {'ATM':<28} {'Det. Yukl (TL)':>15} {'Stoch. Yukl (TL)':>18} {'Delta%':>8} {'P90 Talep':>12}")
    print("  " + "-"*85)
    for i in range(N):
        atm_name  = network.atms[i].name[:24]
        r_d   = det["r_values"][i]
        r_s   = stoch["r_values"][i]
        delta = (r_s - r_d) / r_d * 100
        p90   = np.percentile(scenario_matrix[:, i], 90)
        print(f"  {atm_name:<28} {r_d:>15,.0f} {r_s:>18,.0f} {delta:>+7.1f}% {p90:>12,.0f}")
    print("="*70)


# ─────────────────────────────────────────────
# 5. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize_comparison(det: dict, stoch: dict,
                         demands_det: np.ndarray,
                         scenario_matrix: np.ndarray,
                         network,
                         save_path: str = "phase3a_stochastic_loading.png") -> None:
    """
    4 panel:
    Sol ust   : Per-ATM yukleme miktarlari (Det vs Stoch grouped bar)
    Sag ust   : Toplam maliyet dagilimi (box: Det vs Stoch)
    Sol alt   : Stockout orani per-ATM karsilastirmasi
    Sag alt   : Araç kapasite kullanimi (Det vs Stoch)
    """
    S, N = scenario_matrix.shape
    Q    = network.vehicles[0].capacity

    fig, axes = plt.subplots(2, 2, figsize=(22, 12))
    fig.patch.set_facecolor('#0d1117')
    fig.suptitle("AŞAMA 3a — Stochastic Loading Planı vs Deterministik Baseline",
                 color='white', fontsize=14, fontweight='bold', y=1.01)

    dark = '#1a1f2e'
    C_DET   = '#ff6b6b'
    C_STOCH = '#4ecdc4'
    atm_labels = [f"A{i+1:02d}" for i in range(N)]
    x = np.arange(N)
    w = 0.38

    # ── Sol üst: Per-ATM yukleme ──
    ax1 = axes[0, 0]
    ax1.set_facecolor(dark)
    ax1.set_title("Per-ATM Yukleme Miktari: Det. vs Stochastic",
                  color='white', fontsize=11, fontweight='bold')

    ax1.bar(x - w/2, det["r_values"]/1000,   width=w, color=C_DET,
            alpha=0.85, label='Deterministik (ort.)', zorder=3)
    ax1.bar(x + w/2, stoch["r_values"]/1000, width=w, color=C_STOCH,
            alpha=0.85, label='Stochastic (LP opt.)', zorder=3)

    # P90 referans cizgisi
    p90_arr = np.percentile(scenario_matrix, 90, axis=0) / 1000
    ax1.plot(x, p90_arr, color='#ffe66d', linewidth=1.5,
             linestyle='--', label='P90 Talep', zorder=5)

    ax1.set_xticks(x)
    ax1.set_xticklabels(atm_labels, color='#aaaaaa', fontsize=7, rotation=45)
    ax1.set_ylabel("Nakit Yuklemesi (bin TL)", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8)
    ax1.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax1.spines.values():
        sp.set_edgecolor('#333355')

    # ── Sag üst: Maliyet dagilimi (senaryo bazli) ──
    ax2 = axes[0, 1]
    ax2.set_facecolor(dark)
    ax2.set_title("Senaryo Bazli Toplam Maliyet Dagilimi",
                  color='white', fontsize=11, fontweight='bold')

    # Her senaryo icin toplam maliyet = rota + ceza o senaryoda
    det_costs_per_scen   = (3394.0 + PENALTY_RATIO *
                             det["shortfall_matrix"].sum(axis=1))
    stoch_costs_per_scen = (3394.0 + PENALTY_RATIO *
                             stoch["shortfall_matrix"].sum(axis=1))

    bp1 = ax2.boxplot([det_costs_per_scen, stoch_costs_per_scen],
                       positions=[1, 2], widths=0.4,
                       patch_artist=True,
                       medianprops=dict(color='#ffe66d', linewidth=2.5),
                       whiskerprops=dict(color='#aaaaaa'),
                       capprops=dict(color='#aaaaaa'),
                       flierprops=dict(marker='.', color='#888888', markersize=4))

    bp1['boxes'][0].set_facecolor('#ff6b6b44')
    bp1['boxes'][0].set_edgecolor(C_DET)
    bp1['boxes'][1].set_facecolor('#4ecdc444')
    bp1['boxes'][1].set_edgecolor(C_STOCH)

    ax2.set_xticks([1, 2])
    ax2.set_xticklabels(['Deterministik', 'Stochastic'],
                        color='#aaaaaa', fontsize=10)
    ax2.set_ylabel("Gunluk Toplam Maliyet (TL)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax2.spines.values():
        sp.set_edgecolor('#333355')

    # VSS annotasyon
    mean_d = det_costs_per_scen.mean()
    mean_s = stoch_costs_per_scen.mean()
    ax2.annotate(f"VSS = {mean_d - mean_s:,.0f} TL/gun",
                 xy=(1.5, (mean_d + mean_s) / 2),
                 ha='center', color='#ffe66d', fontsize=10, fontweight='bold')

    # ── Sol alt: Stockout orani per-ATM ──
    ax3 = axes[1, 0]
    ax3.set_facecolor(dark)
    ax3.set_title("Per-ATM Stockout Orani: Det. vs Stochastic",
                  color='white', fontsize=11, fontweight='bold')

    det_so   = np.mean(det["shortfall_matrix"]   > 0, axis=0) * 100
    stoch_so = np.mean(stoch["shortfall_matrix"] > 0, axis=0) * 100

    ax3.bar(x - w/2, det_so,   width=w, color=C_DET,
            alpha=0.85, label='Deterministik', zorder=3)
    ax3.bar(x + w/2, stoch_so, width=w, color=C_STOCH,
            alpha=0.85, label='Stochastic', zorder=3)

    ax3.axhline(y=5, color='#ffe66d', linewidth=1.5, linestyle='--',
                label='%5 kabul edilebilir esik')

    ax3.set_xticks(x)
    ax3.set_xticklabels(atm_labels, color='#aaaaaa', fontsize=7, rotation=45)
    ax3.set_ylabel("Stockout Orani (%)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8)
    ax3.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax3.spines.values():
        sp.set_edgecolor('#333355')

    # ── Sag alt: Araç kapasite kullanimi ──
    ax4 = axes[1, 1]
    ax4.set_facecolor(dark)
    ax4.set_title("Araç Kapasite Kullanimi: Det. vs Stochastic",
                  color='white', fontsize=11, fontweight='bold')

    # Route groups (Phase 2a'dan)
    route_groups_for_plot = {1: [10,19,6,7,2,3,18],
                              2: [1,15,20,17,16,5],
                              4: [12,9,11,8,14,13,4]}

    vehicle_labels, det_pcts, stoch_pcts = [], [], []
    for k, atm_ids in route_groups_for_plot.items():
        idxs = [aid - 1 for aid in atm_ids]
        det_load   = sum(det["r_values"][j]   for j in idxs)
        stoch_load = sum(stoch["r_values"][j] for j in idxs)
        vehicle_labels.append(f"Araç {k}\n({len(atm_ids)} ATM)")
        det_pcts.append(det_load / Q * 100)
        stoch_pcts.append(stoch_load / Q * 100)

    xv = np.arange(len(vehicle_labels))
    ax4.bar(xv - 0.2, det_pcts,   width=0.35, color=C_DET,   alpha=0.85,
            label='Deterministik', zorder=3)
    ax4.bar(xv + 0.2, stoch_pcts, width=0.35, color=C_STOCH, alpha=0.85,
            label='Stochastic', zorder=3)
    ax4.axhline(y=100, color='#ff4444', linewidth=1.5, linestyle='--',
                label='Kapasite Limiti')

    for xi, (dp, sp) in enumerate(zip(det_pcts, stoch_pcts)):
        ax4.text(xi - 0.2, dp + 1, f'%{dp:.0f}', ha='center',
                 color='white', fontsize=9, fontweight='bold')
        ax4.text(xi + 0.2, sp + 1, f'%{sp:.0f}', ha='center',
                 color='white', fontsize=9, fontweight='bold')

    ax4.set_xticks(xv)
    ax4.set_xticklabels(vehicle_labels, color='#aaaaaa', fontsize=10)
    ax4.set_ylabel("Kapasite Kullanimi (%)", color='#aaaaaa')
    ax4.tick_params(colors='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8)
    ax4.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    ax4.set_ylim(0, 115)
    for sp in ax4.spines.values():
        sp.set_edgecolor('#333355')

    plt.tight_layout(pad=2.0)
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Gorsel: {save_path}")


# ─────────────────────────────────────────────
# 6. KAYDET
# ─────────────────────────────────────────────

def save_results(stoch: dict, det: dict,
                 scenario_matrix: np.ndarray, base: str) -> None:
    S, N  = scenario_matrix.shape
    vss   = det["total_cost"] - stoch["total_cost"]

    summary = {
        "det_route_cost":       det["route_cost"],
        "det_penalty":          det["expected_penalty"],
        "det_total":            det["total_cost"],
        "stoch_route_cost":     stoch["route_cost"],
        "stoch_penalty":        stoch["expected_penalty"],
        "stoch_total":          stoch["total_cost"],
        "vss_abs":              vss,
        "vss_pct":              vss / det["total_cost"] * 100,
        "det_stockout_rate":    np.mean(det["shortfall_matrix"] > 0) * 100,
        "stoch_stockout_rate":  np.mean(stoch["shortfall_matrix"] > 0) * 100,
    }
    pd.DataFrame([summary]).to_csv(
        os.path.join(base, "data_stoch_summary.csv"), index=False)

    # Optimal yukleme miktarlari
    load_df = pd.DataFrame({
        "atm_id":        range(1, N+1),
        "r_det_TL":      det["r_values"],
        "r_stoch_TL":    stoch["r_values"],
        "delta_TL":      stoch["r_values"] - det["r_values"],
        "delta_pct":     (stoch["r_values"] - det["r_values"]) / det["r_values"] * 100,
    })
    load_df.to_csv(os.path.join(base, "data_stoch_loads.csv"), index=False)

    print(f"  [SAVED] Ozet : data_stoch_summary.csv")
    print(f"  [SAVED] Yuklemeler : data_stoch_loads.csv")


# ─────────────────────────────────────────────
# 7. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 3a -- Two-Stage Stochastic Loading LP Basliyor...\n")

    base = os.path.dirname(__file__)

    # Network yukle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)
    print("  [OK] Network yuklendi.")

    # Talep ve SAA verileri
    demand_df = pd.read_csv(os.path.join(base, "data_demand_365.csv"),
                            index_col="tarih", parse_dates=True)
    demands_det     = demand_df.mean().values
    scenario_matrix = np.load(os.path.join(base, "data_saa_scenarios.npy"))
    S, N = scenario_matrix.shape
    print(f"  [OK] SAA matrisi: {scenario_matrix.shape}")

    # Phase 2a rota gruplarini yukle
    routes      = load_routes_from_csv(base)
    route_groups = get_route_groups(routes)
    print(f"  [OK] {len(route_groups)} aktif rota grubu yuklendi (Phase 2a).")
    for k, atm_ids in route_groups.items():
        print(f"    Arac {k}: {atm_ids}")

    # Deterministik referans maliyeti
    print("\n  [..] Deterministik referans maliyeti hesaplaniyor...")
    det_result = compute_det_cost(demands_det, route_groups,
                                   scenario_matrix, network)
    print(f"  [OK] Det. beklenen ceza   : {det_result['expected_penalty']:,.2f} TL/gun")
    print(f"  [OK] Det. toplam maliyet  : {det_result['total_cost']:,.2f} TL/gun")

    # Stochastic LP coz
    print(f"\n  [..] Stochastic Loading LP cozuluyor "
          f"(p={PENALTY_RATIO}x, S={S}, N={N})...")
    stoch_result = solve_stochastic_loading(
        route_groups, scenario_matrix, network,
        penalty=PENALTY_RATIO
    )
    print(f"  [OK] Stoch. beklenen ceza : {stoch_result['expected_penalty']:,.2f} TL/gun")
    print(f"  [OK] Stoch. toplam maliyet: {stoch_result['total_cost']:,.2f} TL/gun")

    # Kiyaslama tablosu
    compare_and_print(det_result, stoch_result,
                      demands_det, scenario_matrix, network)

    # Gorsel
    print("\n  [..] Karsilastirma grafigi uretiliyor...")
    visualize_comparison(det_result, stoch_result,
                          demands_det, scenario_matrix, network)

    # Kaydet
    save_results(stoch_result, det_result, scenario_matrix, base)

    vss = det_result["total_cost"] - stoch_result["total_cost"]
    print("\n[OK] ASAMA 3a tamamlandi.")
    print(f"  VSS (Value of Stochastic Solution) = {vss:,.2f} TL/gun")
    print(f"  Yillik tasarruf potansiyeli         = {vss*365/1e6:.2f} milyon TL")
    print()
    print("  Bir sonraki: ASAMA 4 -- SPO+ / Decision-Focused Learning")
