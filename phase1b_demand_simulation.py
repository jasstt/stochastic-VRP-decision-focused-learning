# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 1b
Gecmis Talep Verisi Simulasyonu (365 gun, 20 ATM)
=============================================================

MANTIK:
-------
Bir ATM'nin her gunku nakit talebi tek bir sabit sayi degil.
Cumartesi bir AVM'de farkli, sali sabahi bir hastanede farkli.
Ramazan ayinda farkli, yaz tatilinde farkli.

Gercek ATM talep serisini olusturan bilesenler:

    talep(i, t) = baz_talep(i)
                x mevsimsellik(t)       <- yil ici ay etkisi
                x haftalik_etki(t)      <- pazartesi vs cuma
                x atm_tipi_etkisi(i,t)  <- AVM/hastane/cadde davranisi
                x trend(t)              <- yillik bume trendi
                + epsilon(i,t)          <- rastgele gurultu (log-normal)

Bu bilesenler Arute'nin kendi makalelerinden extract edilen
gercek davranis kaliplariyla kalibre edilmistir:
    - AVM ATM'leri: yuksek varyans, hafta sonu zirve
    - Hastane ATM'leri: dusuk varyans, stabil
    - Kurumsal (plaza): hafta ici zirve, hafta sonu dusus
    - Cadde: orta varyans, Cuma-Cumartesi zirve

CIKTI:
    - demand_df: (365 x 20) DataFrame -- her satir bir gun, her sutun bir ATM
    - Bu DataFrame ASAMA 1c'de dagilim fitting'e, ASAMA 3'te SAA senaryolarina girecek
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Asama 1a'yi import et
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix

# ─────────────────────────────────────────────
# 1. ARUTE MAKALESINDEN EXTRACT EDILEN PARAMETRELER
# ─────────────────────────────────────────────

# Aylik mevsimsellik katsayilari (Ocak=1 ... Aralik=12)
# Kaynak: Arute ATM analizi + Turkiye turizm/enflasyon pattern'i
# Yaz aylarinda nakit artisi (turizm), Ocak-Subat dusuk, Aralik yuksek (yilbasi)
MONTHLY_SEASONALITY = {
    1:  0.82,   # Ocak    -- en dusuk (yeni yil sonrasi durgunluk)
    2:  0.85,   # Subat   -- hala dusuk
    3:  0.92,   # Mart    -- canlanma
    4:  0.95,   # Nisan   -- bahar, alis-veris artisi
    5:  1.02,   # Mayis   -- Ramazan/bayram etkisi (ortalama)
    6:  1.08,   # Haziran -- yaz baslangici
    7:  1.15,   # Temmuz  -- turizm zirve (yabanci doviz de dahil)
    8:  1.18,   # Agustos -- tatil zirve
    9:  1.05,   # Eylul   -- okul acilisi, canlanma
    10: 0.98,   # Ekim    -- normal
    11: 0.93,   # Kasim   -- dusus
    12: 1.10,   # Aralik  -- yilbasi, hediye alverioi
}

# Haftalik etki katsayilari (0=Pazartesi ... 6=Pazar)
# Arute: Cuma-Cumartesi zirve, Pazar dusuk (banka subesi kapali, ATM yogun)
# Pazartesi orta (hafta baslangici nakit ihtiyaci)
WEEKDAY_FACTORS = {
    0: 0.88,   # Pazartesi
    1: 0.85,   # Sali      -- en dusuk hafta ici
    2: 0.90,   # Carsamba
    3: 0.95,   # Persembe
    4: 1.18,   # Cuma      -- hafta sonu oncesi nakit cekim zirve
    5: 1.22,   # Cumartesi -- AVM, alis-veris zirve
    6: 0.92,   # Pazar     -- AVM acik ama sube kapali -> ATM yogun
}

# ATM tipine gore haftalik profil multiplier'i
# AVM Cumartesi daha da yukarida, hastane haftasonunda da stabil
ATM_TYPE_WEEKEND_BOOST = {
    "avm":     {"weekday": 1.0, "weekend": 1.35},  # AVM hafta sonu cok yogun
    "plaza":   {"weekday": 1.15, "weekend": 0.60}, # Plaza hafta ici aktif, haftasonu bos
    "hastane": {"weekday": 1.0, "weekend": 1.05},  # Hastane her zaman acik, stabil
    "cadde":   {"weekday": 1.0, "weekend": 1.10},  # Cadde hafta sonu biraz artar
}

# Arute: post-COVID Istanbul'da %10 yillik artis trendi
ANNUAL_TREND_RATE = 0.10   # %10 yillik bume -- 365 gune yayilir

# Gurultu seviyesi: log-normal sigma parametresi ATM tipine gore
# AVM yuksek varyans, hastane dusuk varyans
NOISE_SIGMA = {
    "avm":     0.22,
    "plaza":   0.18,
    "hastane": 0.12,
    "cadde":   0.17,
}


# ─────────────────────────────────────────────
# 2. BAYRAM / OZEL GUN ANOMALILERI
# ─────────────────────────────────────────────

def get_special_day_multiplier(date: pd.Timestamp) -> float:
    """
    Bayram ve ozel gunlerde talep normalin cok disina cikar.
    Ramazan Bayrami oncesi: ATM'ler bos kaliyor -> stockout riski en yuksek an.
    
    Arute icin en kritik operasyonel gun = Kurban Bayrami arifesi.
    
    Gercek tarih yerine sim yilindaki yaklasik gunleri kullaniyoruz.
    """
    month, day = date.month, date.day
    
    # Kurban Bayrami arifesi (yaklasik Haziran sonu - Temmuz)
    if month == 6 and day in [27, 28, 29]:
        return 2.10   # %110 artis -- Arute'nin en kritik senaryosu

    # Ramazan Bayrami arifesi (yaklasik Nisan)
    if month == 4 and day in [8, 9, 10]:
        return 1.85

    # Yilbasi gecesi oncesi (31 Aralik)
    if month == 12 and day == 31:
        return 1.60

    # Ramazan ayinin son haftasi (ortalama)
    if month == 3 and day >= 20:
        return 1.25

    # Milli bayramlar (29 Ekim, 19 Mayis, 23 Nisan)
    if (month == 10 and day == 29) or \
       (month == 5 and day == 19) or \
       (month == 4 and day == 23):
        return 1.30   # Tatil -> nakit

    return 1.0   # Normal gun


# ─────────────────────────────────────────────
# 3. ANA SIMULASYON FONKSIYONU
# ─────────────────────────────────────────────

def simulate_demand(network, n_days: int = 365,
                    start_date: str = "2023-01-01",
                    seed: int = 42) -> pd.DataFrame:
    """
    Her ATM icin n_days gunluk gercekci nakit talep serisi olusturur.

    Parametreler:
        network    : ASAMA 1a'da olusturulan CITNetwork nesnesi
        n_days     : Simulasyon uzunlugu (varsayilan 365 gun)
        start_date : Seri baslangic tarihi
        seed       : Tekrarlanabilirlik icin random seed

    Donus:
        demand_df  : pd.DataFrame, shape (n_days, n_atms)
                     index = tarihler, columns = ATM isimleri
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')

    # Her ATM icin ayri seri olustur
    demand_matrix = np.zeros((n_days, len(network.atms)))

    for col_idx, atm in enumerate(network.atms):

        baz   = atm.mean_demand     # TL -- ASAMA 1a'dan
        sigma = NOISE_SIGMA[atm.atm_type]
        type_profile = ATM_TYPE_WEEKEND_BOOST[atm.atm_type]

        for row_idx, date in enumerate(dates):

            # --- Bilesenler ---

            # 1) Aylik mevsimsellik
            m_factor = MONTHLY_SEASONALITY[date.month]

            # 2) Haftalik gun etkisi
            wd = date.dayofweek   # 0=Pzt, 6=Paz
            w_factor = WEEKDAY_FACTORS[wd]

            # 3) ATM tipine gore hafta sonu amplifikasyonu
            is_weekend = wd >= 5
            type_factor = (type_profile["weekend"] if is_weekend
                           else type_profile["weekday"])

            # 4) Dogrusal trend (0. gunde 1.0, son gunde 1+rate)
            trend = 1.0 + ANNUAL_TREND_RATE * (row_idx / n_days)

            # 5) Bayram anomalisi
            special = get_special_day_multiplier(date)

            # --- Deterministik beklenti ---
            mu = baz * m_factor * w_factor * type_factor * trend * special

            # --- Log-normal gurultu ---
            # Log-normal kullaniminin sebebi: talep hic negatif olmaz,
            # ve gercek ATM verilerinde sag-tarafli kuyruk gozlemlenir.
            # Log-normal: ln(X) ~ N(mu_ln, sigma^2)
            # mu_ln oyle secilmeli ki E[X] = mu olsun:
            #   mu_ln = ln(mu) - sigma^2 / 2
            mu_ln    = np.log(mu) - (sigma**2) / 2
            raw      = rng.lognormal(mean=mu_ln, sigma=sigma)

            # Minimum gunde en az %20 baz talep (ATM hic kapanmaz)
            demand_matrix[row_idx, col_idx] = max(raw, 0.20 * baz)

    # DataFrame'e donustur
    col_names = [f"ATM_{atm.id:02d}_{atm.name.split()[0]}" for atm in network.atms]
    demand_df = pd.DataFrame(demand_matrix, index=dates, columns=col_names)
    demand_df.index.name = "tarih"

    return demand_df


# ─────────────────────────────────────────────
# 4. OZET ISTATISTIKLER
# ─────────────────────────────────────────────

def print_demand_summary(demand_df: pd.DataFrame, network) -> None:
    print("\n" + "="*60)
    print("  ASAMA 1b -- TALEP SIMULASYONU OZETI")
    print("="*60)
    print(f"  Simulasyon suresi : {len(demand_df)} gun")
    print(f"  ATM sayisi        : {demand_df.shape[1]}")
    print(f"  Baslangic         : {demand_df.index[0].date()}")
    print(f"  Bitis             : {demand_df.index[-1].date()}")
    print()

    total_stats = demand_df.sum(axis=1)   # gunluk toplam filo talebi
    print("  Gunluk TOPLAM Filo Talebi (tum ATM'ler):")
    print(f"    Ortalama : {total_stats.mean():>12,.0f} TL")
    print(f"    Std Dev  : {total_stats.std():>12,.0f} TL")
    print(f"    Min      : {total_stats.min():>12,.0f} TL")
    print(f"    Max      : {total_stats.max():>12,.0f} TL  (bayram?)")
    print()

    print("  Per-ATM Istatistikleri:")
    print(f"  {'ATM':<28} {'Ort (TL)':>12} {'Std':>10} {'CV%':>7} {'Min':>10} {'Max':>10}")
    print("  " + "-"*80)
    for i, col in enumerate(demand_df.columns):
        s = demand_df[col]
        cv = (s.std() / s.mean()) * 100
        print(f"  {col:<28} {s.mean():>12,.0f} {s.std():>10,.0f} "
              f"{cv:>6.1f}% {s.min():>10,.0f} {s.max():>10,.0f}")

    print("="*60)
    print("  CV = Coefficient of Variation (degiskenlik katsayisi)")
    print("  Yuksek CV -> yuksek belirsizlik -> Stochastic VRP daha kritik")
    print("="*60)


# ─────────────────────────────────────────────
# 5. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize_demand(demand_df: pd.DataFrame, network,
                     save_path: str = "phase1b_demand_simulation.png") -> None:
    """
    3 panel:
      Sol ust  : 4 farkli tip ATM icin yillik talep serisi (zaman serisi)
      Sag ust  : Haftalik ortalama profil (bar chart)
      Alt      : Aylik mevsimsellik + ATM tipine gore dagilim (violin)
    """
    fig = plt.figure(figsize=(20, 12))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.28)

    ax1 = fig.add_subplot(gs[0, :])    # ust: tam genislik zaman serisi
    ax2 = fig.add_subplot(gs[1, 0])   # sol alt: haftalik profil
    ax3 = fig.add_subplot(gs[1, 1])   # sag alt: aylik mevsimsellik

    dark_bg = '#1a1f2e'
    colors  = {"avm": "#ff4444", "plaza": "#ff9933",
                "hastane": "#44ff88", "cadde": "#4499ff"}

    # ── PANEL 1: Yillik Zaman Serisi (tip basina 1 ornek ATM) ──
    ax1.set_facecolor(dark_bg)
    ax1.set_title("Yillik ATM Talep Serisi -- Tip Bazli Ornek",
                  color='white', fontsize=13, fontweight='bold')

    type_representatives = {}
    for atm in network.atms:
        if atm.atm_type not in type_representatives:
            type_representatives[atm.atm_type] = atm

    for tip, atm in type_representatives.items():
        col = f"ATM_{atm.id:02d}_{atm.name.split()[0]}"
        series = demand_df[col] / 1000   # bin TL
        ax1.plot(demand_df.index, series,
                 color=colors[tip], alpha=0.85, linewidth=0.9,
                 label=f"{tip.upper()} -- {atm.name}")
        # 7 gunluk hareketli ortalama
        ax1.plot(demand_df.index,
                 series.rolling(7, center=True).mean(),
                 color=colors[tip], linewidth=2.2, alpha=0.5)

    # Bayram anlik cizgisi
    ax1.axvline(pd.Timestamp("2023-06-28"), color='yellow',
                linewidth=1.2, linestyle='--', alpha=0.6, label='Kurban Bayrami arifesi')
    ax1.axvline(pd.Timestamp("2023-04-09"), color='orange',
                linewidth=1.2, linestyle='--', alpha=0.6, label='Ramazan Bayrami arifesi')

    ax1.set_xlabel("Tarih", color='#aaaaaa')
    ax1.set_ylabel("Gunluk Talep (bin TL)", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(loc='upper left', facecolor=dark_bg,
               edgecolor='#444466', labelcolor='white', fontsize=8)
    ax1.grid(True, alpha=0.12, color='gray', linestyle='--')
    for sp in ax1.spines.values():
        sp.set_edgecolor('#333355')

    # ── PANEL 2: Haftalik Profil ──
    ax2.set_facecolor(dark_bg)
    ax2.set_title("Haftalik Talep Profili (Tip Bazli)",
                  color='white', fontsize=12, fontweight='bold')

    days_tr = ['Pzt', 'Sal', 'Car', 'Per', 'Cum', 'Cmt', 'Paz']
    x = np.arange(7)
    width = 0.2
    offsets = np.linspace(-0.3, 0.3, len(type_representatives))

    for (tip, atm), offset in zip(type_representatives.items(), offsets):
        col = f"ATM_{atm.id:02d}_{atm.name.split()[0]}"
        weekly_avg = [demand_df[col][demand_df.index.dayofweek == d].mean() / 1000
                      for d in range(7)]
        ax2.bar(x + offset, weekly_avg, width,
                color=colors[tip], alpha=0.80, label=tip.upper())

    ax2.set_xticks(x)
    ax2.set_xticklabels(days_tr, color='#aaaaaa')
    ax2.set_ylabel("Ort. Gunluk Talep (bin TL)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor=dark_bg, edgecolor='#444466',
               labelcolor='white', fontsize=8)
    ax2.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax2.spines.values():
        sp.set_edgecolor('#333355')

    # ── PANEL 3: Aylik Mevsimsellik ──
    ax3.set_facecolor(dark_bg)
    ax3.set_title("Aylik Mevsimsellik -- Toplam Filo Talebi",
                  color='white', fontsize=12, fontweight='bold')

    monthly_total = demand_df.sum(axis=1).resample('ME').mean() / 1e6  # milyon TL
    bar_colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(monthly_total)))
    bars = ax3.bar(range(len(monthly_total)), monthly_total,
                   color=bar_colors, alpha=0.85, edgecolor='white', linewidth=0.4)

    months_tr = ['Oca', 'Sub', 'Mar', 'Nis', 'May', 'Haz',
                 'Tem', 'Agu', 'Eyl', 'Eki', 'Kas', 'Ara']
    ax3.set_xticks(range(len(monthly_total)))
    ax3.set_xticklabels(months_tr[:len(monthly_total)], color='#aaaaaa')
    ax3.set_ylabel("Ort. Gunluk Toplam Talep (milyon TL)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax3.spines.values():
        sp.set_edgecolor('#333355')
    for bar, val in zip(bars, monthly_total):
        ax3.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                 f'{val:.2f}M', ha='center', va='bottom',
                 color='white', fontsize=7)

    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Gorsel kaydedildi: {save_path}")


# ─────────────────────────────────────────────
# 6. VERIYI KAYDET (ASAMA 1c ve sonrasi icin)
# ─────────────────────────────────────────────

def save_demand_data(demand_df: pd.DataFrame,
                     path: str = "data_demand_365.csv") -> None:
    demand_df.to_csv(path)
    print(f"  [SAVED] CSV kaydedildi : {path}")
    print(f"          Shape          : {demand_df.shape}")
    print(f"          Boyut          : {os.path.getsize(path)/1024:.1f} KB")


# ─────────────────────────────────────────────
# 7. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 1b -- Talep Simulasyonu Basliyor...\n")

    # Asama 1a'dan network'u yukle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)
    print("  [OK] Network yuklendi (ASAMA 1a).")

    # Simulasyonu calistir
    print("  [..] 365 gunluk talep serisi uretiliyor...")
    demand_df = simulate_demand(network, n_days=365,
                                start_date="2023-01-01", seed=42)
    print("  [OK] Simulasyon tamamlandi.")

    # Ozet yazdir
    print_demand_summary(demand_df, network)

    # Gorsellestir
    visualize_demand(demand_df, network)

    # Kaydet
    save_demand_data(demand_df, path="data_demand_365.csv")

    print("\n[OK] ASAMA 1b tamamlandi.")
    print("     demand_df -> ASAMA 1c'ye (dagilim fitting) hazir.")
    print(f"     Shape: {demand_df.shape}  |  Tarih: {demand_df.index[0].date()} -> {demand_df.index[-1].date()}")
