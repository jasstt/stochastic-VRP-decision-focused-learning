# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 1d
SAA Senaryo Uretimi (S=100 Senaryo)
=============================================================

MANTIK:
-------
Two-Stage Stochastic VRP'nin cozum yontemi SAA'dir:
    Sample Average Approximation (Ornek Ortalama Yaklasimi)

Gercek problemde xi_i (ATM i'nin talebi) bilinmiyor.
SAA'nin mantigi: 
    "Dagilimdan cok sayida senaryo ornekle,
     o senaryolarin ortalamasini minimize et,
     bu ortalama gercek beklentiye yaklasir."

Matematiksel olarak:
    min Σ c_ij x_ijk  +  (1/S) * Σ_s Q(x, xi^s)
    
Burada xi^s = senaryo s'deki talep vektoru.
Her xi_i^s bagimsiz olarak F_i dagilimından orneklenir.

S = 100 seciminin sebebi:
    - S cok kucuk -> yaklasim gurultulu, optimal cozum yaniltici
    - S cok buyuk -> MIP cok buyur, Gurobi yavaslar
    - Literaturde ATM problemi icin S=50-200 standart aralik
    - Biz 100 ile baslarız, 3. asamada sensitivity analizi yapariz

CIKTI:
    - scenarios: np.ndarray shape (S, N) -- S senaryo, N ATM
    - scenario_probs: np.ndarray shape (S,) -- esit olasilik (1/S)
    - Bu dogrudan ASAMA 2 ve 3'e input olacak
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix


# ─────────────────────────────────────────────
# 1. FIT PARAMETRELERINI OKU
# ─────────────────────────────────────────────

DIST_MAP = {
    "Normal":    stats.norm,
    "LogNormal": stats.lognorm,
    "Gamma":     stats.gamma,
}


def load_fit_params(path: str = "data_fit_params.csv") -> dict:
    """
    ASAMA 1c'nin ciktisi olan CSV'yi okur.
    Her ATM icin dagilim adi + parametreler doner.

    Donus: {atm_col: {"dist": scipy.stats obje, "params": tuple}}
    """
    df  = pd.read_csv(path)
    out = {}

    for _, row in df.iterrows():
        col       = row["atm_col"]
        dist_name = row["dist_name"]
        # param_0, param_1, ... sutunlarini topla (NaN olmayanlar)
        param_cols = sorted([c for c in df.columns if c.startswith("param_")])
        params     = tuple(row[c] for c in param_cols if pd.notna(row[c]))

        out[col] = {
            "dist_name": dist_name,
            "dist":      DIST_MAP[dist_name],
            "params":    params,
        }

    return out


# ─────────────────────────────────────────────
# 2. SAA SENARYO URETICI
# ─────────────────────────────────────────────

def generate_saa_scenarios(fit_params: dict,
                            demand_df: pd.DataFrame,
                            network,
                            n_scenarios: int = 100,
                            seed: int = 123) -> dict:
    """
    Her ATM icin kazanan dagilimdan n_scenarios adet bagımsız
    talep ornegi ceker.

    Onemli: Senaryolar BAGIMSIZ orneklenir.
    Gercekte ATM talepleri arasinda korelasyon olabilir
    (ornek: Cuma gunu tum ATM'ler yuksek). Bu basitlestirme
    ASAMA 4'te (SPO+) ele alinabilir.

    Donus dict icerigi:
        "matrix"  : (S x N) ndarray -- ham senaryo degerleri (TL)
        "probs"   : (S,) ndarray    -- esit agirlik p_s = 1/S
        "atm_cols": list            -- sutun siralama bilgisi
        "stats"   : DataFrame       -- senaryo istatistikleri
        "n_scenarios": int
        "n_atms"  : int
    """
    rng      = np.random.default_rng(seed)
    atm_cols = list(fit_params.keys())
    n_atms   = len(atm_cols)

    scenario_matrix = np.zeros((n_scenarios, n_atms))

    for j, col in enumerate(atm_cols):
        fp     = fit_params[col]
        dist   = fp["dist"]
        params = fp["params"]

        # n_scenarios adet ornekle
        samples = dist.rvs(*params, size=n_scenarios, random_state=rng)

        # Guvenlik: sifirin altina dusmesi imkansiz (nakit talep hep pozitif)
        # Minimum: ASAMA 1a'daki r_min parametresi
        atm_idx  = int(col.split("_")[1]) - 1   # ATM_01 -> index 0
        r_min    = network.atms[atm_idx].r_min
        samples  = np.maximum(samples, r_min)

        scenario_matrix[:, j] = samples

    # Esit olasilik
    probs = np.ones(n_scenarios) / n_scenarios

    # Senaryo istatistikleri
    stats_rows = []
    for j, col in enumerate(atm_cols):
        col_data = scenario_matrix[:, j]
        fp       = fit_params[col]
        hist_mean = demand_df[col].mean()   # gercek tarihsel ortalama
        stats_rows.append({
            "atm_col":     col,
            "dist_name":   fp["dist_name"],
            "scen_mean":   col_data.mean(),
            "scen_std":    col_data.std(),
            "scen_min":    col_data.min(),
            "scen_max":    col_data.max(),
            "scen_p10":    np.percentile(col_data, 10),
            "scen_p50":    np.percentile(col_data, 50),
            "scen_p90":    np.percentile(col_data, 90),
            "hist_mean":   hist_mean,
            "bias_pct":    (col_data.mean() - hist_mean) / hist_mean * 100,
        })

    stats_df = pd.DataFrame(stats_rows)

    return {
        "matrix":      scenario_matrix,
        "probs":       probs,
        "atm_cols":    atm_cols,
        "stats":       stats_df,
        "n_scenarios": n_scenarios,
        "n_atms":      n_atms,
    }


# ─────────────────────────────────────────────
# 3. SENARYO KALITE KONTROL
# ─────────────────────────────────────────────

def print_scenario_summary(saa: dict, network) -> None:
    """
    Senaryolarin gercek tarihsel veriyle tutarliligini kontrol et.
    'bias_pct' kucukse senaryolar gercekci.
    """
    print("\n" + "="*75)
    print("  ASAMA 1d -- SAA SENARYO OZETI")
    print("="*75)
    print(f"  Senaryo sayisi    : {saa['n_scenarios']}")
    print(f"  ATM sayisi        : {saa['n_atms']}")
    print(f"  Matris boyutu     : {saa['matrix'].shape}  (S x N)")
    print(f"  Olasilik agirlik  : p_s = 1/{saa['n_scenarios']} = {1/saa['n_scenarios']:.4f}")
    print()

    df = saa["stats"]
    total_mean   = saa["matrix"].sum(axis=1).mean()
    total_std    = saa["matrix"].sum(axis=1).std()
    total_p10    = np.percentile(saa["matrix"].sum(axis=1), 10)
    total_p90    = np.percentile(saa["matrix"].sum(axis=1), 90)

    print(f"  Toplam Filo Talebi (tum ATM'ler toplamı, senaryo bazli):")
    print(f"    Senaryo Ort.     : {total_mean:>12,.0f} TL")
    print(f"    Senaryo Std      : {total_std:>12,.0f} TL")
    print(f"    P10 (dusuk gun)  : {total_p10:>12,.0f} TL")
    print(f"    P90 (yuksek gun) : {total_p90:>12,.0f} TL")
    print(f"    P90/P10 orani    : {total_p90/total_p10:.2f}x  (1x = sifir belirsizlik)")
    print()

    # Araç kapasitesi analizi
    vehicle_capacity = network.vehicles[0].capacity
    n_vehicles       = len(network.vehicles)
    total_cap        = vehicle_capacity * n_vehicles

    pct_exceed = np.mean(saa["matrix"].sum(axis=1) > total_cap) * 100
    print(f"  Kapasite Analizi:")
    print(f"    Toplam filo kap. : {total_cap:>12,.0f} TL")
    print(f"    Kap. asim riski  : %{pct_exceed:.1f} senaryo toplam kapasiteyi asiyor")
    print()

    print(f"  Per-ATM Kalite Kontrolu (Bias = Senaryo Ort. vs Tarihsel Ort.):")
    print(f"  {'ATM':<30} {'Dagilim':<12} {'Scen.Ort':>10} {'Tarih.Ort':>10} "
          f"{'Bias%':>7} {'P90':>10}")
    print("  " + "-"*85)

    for _, row in df.iterrows():
        short = row["atm_col"].replace("ATM_", "A").replace("_", "-")[:26]
        bias_flag = " (!)" if abs(row["bias_pct"]) > 10 else ""
        print(f"  {short:<30} {row['dist_name']:<12} "
              f"{row['scen_mean']:>10,.0f} {row['hist_mean']:>10,.0f} "
              f"{row['bias_pct']:>6.1f}%{bias_flag} {row['scen_p90']:>10,.0f}")

    print("="*75)


# ─────────────────────────────────────────────
# 4. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize_scenarios(saa: dict, demand_df: pd.DataFrame, network,
                        save_path: str = "phase1d_saa_scenarios.png") -> None:
    """
    3 panel gorseli:

    Sol: Senaryo "fan" grafigi -- 100 senaryonun ATM bazli dagilimi
         Her ince cizgi bir senaryo, kalin cizgi ortalama.
         Belirsizlik bolgesi = senaryolar arasi yayilim.

    Sag ust: Toplam filo talebi dagilim histogrami
             Araç kapasitesi referans cizgisi ile birlikte.
             Kapasite asimi = kirmizi bolge -> stockout riski.

    Sag alt: P10-P50-P90 box plot -- her ATM icin senaryo yayilimi
    """
    fig = plt.figure(figsize=(22, 13))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.30)

    ax1 = fig.add_subplot(gs[:, 0])    # sol: tam yukseklik
    ax2 = fig.add_subplot(gs[0, 1])   # sag ust
    ax3 = fig.add_subplot(gs[1, 1])   # sag alt

    dark   = '#1a1f2e'
    S      = saa["n_scenarios"]
    matrix = saa["matrix"]           # (S x N)
    atm_cols = saa["atm_cols"]
    n_atms   = saa["n_atms"]

    # ── Sol panel: ATM bazli senaryo fan ──
    ax1.set_facecolor(dark)
    ax1.set_title(f"SAA Senaryo Yelpazesi -- {S} Senaryo (per ATM)",
                  color='white', fontsize=12, fontweight='bold')

    x = np.arange(n_atms)
    atm_labels = [c.replace("ATM_", "A").replace("_", "\n")[:8]
                  for c in atm_cols]

    # Her senaryo ince cizgi
    for s in range(S):
        ax1.plot(x, matrix[s] / 1000, color='#4499ff',
                 alpha=0.08, linewidth=0.7)

    # P10, P50, P90 bantlari
    p10 = np.percentile(matrix, 10, axis=0) / 1000
    p50 = np.percentile(matrix, 50, axis=0) / 1000
    p90 = np.percentile(matrix, 90, axis=0) / 1000
    scen_mean = matrix.mean(axis=0) / 1000

    ax1.fill_between(x, p10, p90, alpha=0.20, color='#4499ff', label='P10-P90 araligi')
    ax1.plot(x, p50,       color='#ffe66d', linewidth=2.0, label='Medyan (P50)', zorder=5)
    ax1.plot(x, scen_mean, color='#ff6b6b', linewidth=2.2,
             linestyle='--', label='Senaryo Ort.', zorder=6)

    # Tarihsel ortalama
    hist_means = demand_df.mean(axis=0).values / 1000
    ax1.scatter(x, hist_means, color='#44ff88', s=40, zorder=7,
                label='Tarihsel Ort.', marker='D')

    ax1.set_xticks(x)
    ax1.set_xticklabels(atm_labels, color='#aaaaaa', fontsize=6.5, rotation=45)
    ax1.set_ylabel("Gunluk Talep (bin TL)", color='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8, loc='upper right')
    ax1.grid(True, alpha=0.12, color='gray', linestyle='--')
    for sp in ax1.spines.values():
        sp.set_edgecolor('#333355')

    # ── Sag ust: Toplam filo talebi dagilimi ──
    ax2.set_facecolor(dark)
    ax2.set_title("Toplam Filo Talebi Dagilimi (S=100 Senaryo)",
                  color='white', fontsize=11, fontweight='bold')

    total_demand = matrix.sum(axis=1) / 1e6   # milyon TL
    total_cap    = (network.vehicles[0].capacity * len(network.vehicles)) / 1e6

    n_exceed = np.sum(total_demand > total_cap)
    # Normal altindaki kisim (mavi) ve asim kismi (kirmizi)
    ax2.hist(total_demand[total_demand <= total_cap], bins=20,
             color='#4499ff', alpha=0.80, label=f'Kapasite alti ({S-n_exceed} senaryo)')
    ax2.hist(total_demand[total_demand > total_cap],  bins=10,
             color='#ff4444', alpha=0.80, label=f'Kapasite asimi ({n_exceed} senaryo)')

    ax2.axvline(x=total_cap, color='#ffdd00', linewidth=2.0,
                linestyle='--', label=f'Filo kap. ({total_cap:.1f}M TL)')
    ax2.axvline(x=np.mean(total_demand), color='#ff9933', linewidth=1.5,
                linestyle=':', label=f'Ort. talep ({np.mean(total_demand):.2f}M TL)')

    ax2.set_xlabel("Toplam Gunluk Talep (milyon TL)", color='#aaaaaa')
    ax2.set_ylabel("Senaryo Sayisi", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8)
    ax2.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax2.spines.values():
        sp.set_edgecolor('#333355')

    # ── Sag alt: ATM bazli P10-P90 Box ──
    ax3.set_facecolor(dark)
    ax3.set_title("ATM Bazli Senaryo Yayilimi (P10 / P50 / P90)",
                  color='white', fontsize=11, fontweight='bold')

    # Manuel box plot (kutu = P25-P75, biyik = P10-P90)
    for j in range(n_atms):
        col_data = matrix[:, j] / 1000
        p10j = np.percentile(col_data, 10)
        p25j = np.percentile(col_data, 25)
        p50j = np.percentile(col_data, 50)
        p75j = np.percentile(col_data, 75)
        p90j = np.percentile(col_data, 90)

        # Kutu
        ax3.bar(j, p75j - p25j, bottom=p25j,
                color='#4499ff', alpha=0.60, width=0.65)
        # Medyan cizgisi
        ax3.plot([j - 0.32, j + 0.32], [p50j, p50j],
                 color='#ffe66d', linewidth=2.0, zorder=5)
        # Biyiklar
        ax3.plot([j, j], [p10j, p25j], color='#4499ff', alpha=0.7, linewidth=1.2)
        ax3.plot([j, j], [p75j, p90j], color='#4499ff', alpha=0.7, linewidth=1.2)

    ax3.set_xticks(range(n_atms))
    ax3.set_xticklabels([f"A{i+1:02d}" for i in range(n_atms)],
                        color='#aaaaaa', fontsize=6.5, rotation=45)
    ax3.set_ylabel("Gunluk Talep (bin TL)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax3.spines.values():
        sp.set_edgecolor('#333355')

    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Gorsel kaydedildi: {save_path}")


# ─────────────────────────────────────────────
# 5. KAYDET (ASAMA 2 ve 3 icin)
# ─────────────────────────────────────────────

def save_scenarios(saa: dict,
                   matrix_path: str = "data_saa_scenarios.npy",
                   stats_path:  str = "data_saa_stats.csv") -> None:
    """
    Senaryo matrisini .npy (numpy binary) olarak kaydet.
    .npy formati cok daha hizli yuklenir (CSV'den 10-20x).
    ASAMA 2a bu dosyayi np.load() ile dogrudan okuyacak.
    """
    np.save(matrix_path, saa["matrix"])
    np.save(matrix_path.replace("scenarios", "probs"), saa["probs"])
    saa["stats"].to_csv(stats_path, index=False)

    print(f"\n  [SAVED] Senaryo matrisi : {matrix_path}")
    print(f"  [SAVED] Olasilik vektoru: {matrix_path.replace('scenarios', 'probs')}")
    print(f"  [SAVED] Senaryo istatist.: {stats_path}")
    print(f"  Matris boyutu : {saa['matrix'].shape}  "
          f"({saa['matrix'].nbytes/1024:.1f} KB)")


# ─────────────────────────────────────────────
# 6. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 1d -- SAA Senaryo Uretimi Basliyor...\n")

    base = os.path.dirname(__file__)

    # Network yukle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)
    print("  [OK] Network yuklendi.")

    # Fit parametreleri yukle (ASAMA 1c ciktisi)
    fit_path   = os.path.join(base, "data_fit_params.csv")
    fit_params = load_fit_params(fit_path)
    print(f"  [OK] Fit parametreleri yuklendi: {len(fit_params)} ATM")

    # Tarihsel veri (bias kontrolu icin)
    demand_df = pd.read_csv(
        os.path.join(base, "data_demand_365.csv"),
        index_col="tarih", parse_dates=True
    )

    # SAA senaryolari uret
    print(f"  [..] S=100 senaryo ornekleniyor...")
    saa = generate_saa_scenarios(
        fit_params, demand_df, network,
        n_scenarios=100, seed=123
    )
    print(f"  [OK] {saa['n_scenarios']} senaryo uretildi.")

    # Ozet ve kalite kontrol
    print_scenario_summary(saa, network)

    # Gorsel
    print("\n  [..] Senaryo yelpazesi grafigi uretiliyor...")
    visualize_scenarios(saa, demand_df, network)

    # Kaydet
    save_scenarios(saa,
                   matrix_path=os.path.join(base, "data_saa_scenarios.npy"),
                   stats_path =os.path.join(base, "data_saa_stats.csv"))

    print("\n[OK] ASAMA 1d tamamlandi.")
    print(f"     SAA matrisi     : shape {saa['matrix'].shape}")
    print(f"     Olasilik        : p_s = {saa['probs'][0]:.4f} (esit agirlik)")
    print()
    print("  ======================================================")
    print("  ASAMA 1 (Veri ve Talep Modelleme) TAMAMLANDI!")
    print("  ======================================================")
    print("  Olusan dosyalar:")
    print("    data_demand_365.csv     -- 365 gunluk tarihsel veri")
    print("    data_fit_params.csv     -- dagilim fit parametreleri")
    print("    data_saa_scenarios.npy  -- (100x20) SAA talep matrisi")
    print("    data_saa_probs.npy      -- (100,) olasilik vektoru")
    print()
    print("  Bir sonraki: ASAMA 2a -- Deterministik VRP Baseline (Gurobi)")
