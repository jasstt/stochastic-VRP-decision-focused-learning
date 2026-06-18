# -*- coding: utf-8 -*-
# IMPORTANT: set backend before any other matplotlib import
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- saves to file, no GUI window
"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 1a
ATM Agi Kurulumu: Koordinatlar, Parametreler, Gorsellestirme
=============================================================

MANTIK:
-------
İstanbul'da bir CIT (Cash-In-Transit) filosunun her sabah bir
depodan çıkıp ATM noktalarını ziyaret ettiğini düşün.
Bu aşamada sadece şunu soruyoruz:
    "Noktalarımız nerede ve her birinin özellikleri neler?"

Yapacaklarımız:
    1. Gerçekçi İstanbul koordinatlarıyla 20 ATM noktası tanımla
    2. Merkezi bir depo (Maslak/İTÜ Teknokent) belirle
    3. Her ATM için şu parametreleri ayarla:
        - Günlük ortalama nakit talebi (TL)
        - Zaman penceresi [a_i, b_i] — en erken / en geç ziyaret saati
        - Minimum yenileme miktarı r_min
    4. 4 CIT aracı için araç kapasitesini (Q) tanımla
    5. Haritada görselleştir
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import math

# ─────────────────────────────────────────────
# 1. VERİ YAPILARI (Dataclass'lar)
# ─────────────────────────────────────────────

@dataclass
class ATMNode:
    """
    Bir ATM noktasını temsil eder.
    
    Parametreler:
        id          : Benzersiz kimlik (0 = depo)
        name        : İlçe / lokasyon adı
        lat, lon    : GPS koordinatları
        mean_demand : Ortalama günlük nakit talebi (TL)
        std_demand  : Talebin standart sapması (TL) — belirsizlik buradan geliyor
        time_open   : Erken açılış saati (dakika, gece yarısından itibaren)
        time_close  : Son ziyaret saati (dakika)
        r_min       : Minimum yenileme miktarı (TL) — çok az doldurmak mantıklı değil
        atm_type    : Lokasyon tipi (AVM, cadde, hastane, vb.)
    """
    id: int
    name: str
    lat: float
    lon: float
    mean_demand: float      # TL
    std_demand: float       # TL
    time_open: int          # dakika (örn. 480 = 08:00)
    time_close: int         # dakika (örn. 1020 = 17:00)
    r_min: float            # TL — minimum yükleme
    atm_type: str = "cadde"

@dataclass
class Depot:
    """CIT araçlarının sabah çıkıp akşam döndüğü merkez nokta."""
    id: int = 0
    name: str = "Maslak Depo (İTÜ Teknokent)"
    lat: float = 41.1082
    lon: float = 29.0209

@dataclass
class Vehicle:
    """Bir CIT aracını temsil eder."""
    id: int
    capacity: float         # TL — araçta taşınabilecek max nakit
    speed_kmh: float = 40.0  # İstanbul trafiği için ortalama hız

@dataclass
class CITNetwork:
    """
    Tüm ağ yapısını bir arada tutan ana konteyner.
    Bu nesne bir sonraki aşamalara doğrudan input olarak verilecek.
    """
    depot: Depot
    atms: List[ATMNode]
    vehicles: List[Vehicle]
    distance_matrix: np.ndarray = field(default=None, repr=False)
    time_matrix: np.ndarray = field(default=None, repr=False)


# ─────────────────────────────────────────────
# 2. İSTANBUL ATM NOKTALARI
# ─────────────────────────────────────────────

def create_istanbul_network() -> CITNetwork:
    """
    İstanbul'un hem Avrupa hem Anadolu yakasından gerçekçi
    ilçe konumlarında 20 ATM noktası oluşturur.
    
    Talep parametreleri gerçek ATM davranışına yakın:
        - AVM ATM'leri: yüksek talep, yüksek varyans
        - Hastane ATM'leri: orta talep, düşük varyans (sabit hasta trafiği)
        - Cadde ATM'leri: orta-düşük talep, orta varyans
    
    Zaman pencereleri:
        - Tüm ATM'ler mesai saatlerinde erişilebilir (08:00–17:00)
        - Bazı AVM'ler daha geniş pencere (09:00–20:00)
    """

    depot = Depot()

    # Her ATM için: (id, isim, lat, lon, ort_talep, std_talep, açılış, kapanış, r_min, tip)
    # Talep birimi: TL (x1000 — binler cinsinden düşün)
    atm_data = [
        # ── AVRUPA YAKASI ──
        ( 1, "Levent (AVM)",         41.0820, 29.0120, 85_000, 25_000, 480, 1200, 10_000, "avm"),
        ( 2, "Beşiktaş Meydan",      41.0430, 29.0050, 60_000, 18_000, 480, 1020, 8_000,  "cadde"),
        ( 3, "Şişli Merkez",         41.0607, 28.9870, 70_000, 20_000, 480, 1020, 8_000,  "cadde"),
        ( 4, "Fatih Aksaray",        41.0082, 28.9502, 55_000, 15_000, 480, 1020, 7_000,  "cadde"),
        ( 5, "Bağcılar AVM",         41.0375, 28.8570, 90_000, 28_000, 540, 1200, 12_000, "avm"),
        ( 6, "Bakırköy Hastane",     40.9795, 28.8720, 45_000, 10_000, 480,  960, 6_000,  "hastane"),
        ( 7, "Zeytinburnu Cadde",    41.0005, 28.9050, 50_000, 14_000, 480, 1020, 7_000,  "cadde"),
        ( 8, "Eyüpsultan",           41.0730, 28.9350, 42_000, 12_000, 480, 1020, 5_000,  "cadde"),
        ( 9, "Sarıyer",              41.1670, 29.0510, 38_000, 11_000, 480, 1020, 5_000,  "cadde"),
        (10, "Maslak Plaza",         41.1150, 29.0280, 75_000, 22_000, 480, 1020, 10_000, "plaza"),
        # ── ANADOLU YAKASI ──
        (11, "Kadıköy Meydan",       40.9925, 29.0262, 72_000, 21_000, 480, 1020, 9_000,  "cadde"),
        (12, "Üsküdar Merkez",       41.0236, 29.0165, 58_000, 16_000, 480, 1020, 7_000,  "cadde"),
        (13, "Ataşehir AVM",         40.9890, 29.1295, 95_000, 30_000, 540, 1260, 12_000, "avm"),
        (14, "Maltepe Hastane",      40.9342, 29.1300, 48_000, 12_000, 480,  960, 6_000,  "hastane"),
        (15, "Kartal Cadde",         40.8922, 29.1890, 52_000, 14_000, 480, 1020, 7_000,  "cadde"),
        (16, "Pendik",               40.8770, 29.2400, 40_000, 11_000, 480, 1020, 5_000,  "cadde"),
        (17, "Tuzla Organize San.",  40.8490, 29.3100, 35_000,  9_000, 480, 1020, 5_000,  "plaza"),
        (18, "Beykoz",               41.1270, 29.1080, 30_000,  8_000, 480, 1020, 4_000,  "cadde"),
        (19, "Ümraniye Merkez",      41.0220, 29.1180, 62_000, 18_000, 480, 1020, 8_000,  "cadde"),
        (20, "Sultanbeyli",          40.9640, 29.2650, 33_000,  9_000, 480, 1020, 4_000,  "cadde"),
    ]

    atms = [
        ATMNode(
            id=row[0], name=row[1], lat=row[2], lon=row[3],
            mean_demand=row[4], std_demand=row[5],
            time_open=row[6], time_close=row[7],
            r_min=row[8], atm_type=row[9]
        )
        for row in atm_data
    ]

    # 4 CIT aracı — her biri 500.000 TL nakit kapasiteli
    vehicles = [
        Vehicle(id=k, capacity=500_000, speed_kmh=40.0)
        for k in range(1, 5)
    ]

    network = CITNetwork(depot=depot, atms=atms, vehicles=vehicles)
    return network


# ─────────────────────────────────────────────
# 3. MESAFİ MATRİSİ (Haversine)
# ─────────────────────────────────────────────

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    İki GPS koordinatı arasındaki yüzey mesafesini hesaplar (km).
    VRP için c_ij parametresi buradan gelecek.
    
    Basit yaklaşım: gerçek sürüş mesafesi ≈ haversine * 1.35
    (İstanbul'un çarpık yol ağı için eklenen katsayı)
    """
    R = 6371.0
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    a = math.sin(Δφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(Δλ/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) * 1.35  # yol katsayısı


def build_distance_matrix(network: CITNetwork) -> np.ndarray:
    """
    (n+1) x (n+1) boyutlu mesafe matrisi oluşturur.
    Satır/sütun 0 = depo, 1..n = ATM'ler.
    
    Bu matris VRP'nin temel girdisi — c_ij buradan hesaplanacak.
    """
    n = len(network.atms) + 1  # +1 depo için
    lats = [network.depot.lat] + [a.lat for a in network.atms]
    lons = [network.depot.lon] + [a.lon for a in network.atms]

    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i, j] = haversine_km(lats[i], lons[i], lats[j], lons[j])
    return D


def build_time_matrix(distance_matrix: np.ndarray, speed_kmh: float = 40.0) -> np.ndarray:
    """
    Mesafe matrisinden süre matrisi türetir (dakika cinsinden).
    ATM ziyareti süresi = sürüş süresi + 15 dakika servis süresi.
    """
    service_time = 15  # dakika — para sayma, makbuz alma vb.
    travel_time = (distance_matrix / speed_kmh) * 60  # dakikaya çevir
    # Sadece seyahat süresi (servis süresi ayrıca node'da işlenir)
    return travel_time


# ─────────────────────────────────────────────
# 4. ÖZET İSTATİSTİKLER
# ─────────────────────────────────────────────

def print_network_summary(network: CITNetwork) -> None:
    """Ağ hakkında özet istatistikler yazdırır."""
    print("=" * 60)
    print("  ARUTE CIT-SVRP — AĞ ÖZETİ")
    print("=" * 60)
    print(f"  Depo          : {network.depot.name}")
    print(f"  ATM Sayısı    : {len(network.atms)}")
    print(f"  Araç Sayısı   : {len(network.vehicles)}")
    print(f"  Araç Kapasitesi: {network.vehicles[0].capacity:,.0f} TL")
    print()

    demands = [a.mean_demand for a in network.atms]
    print(f"  Talep İstatistikleri (günlük, TL):")
    print(f"    Toplam (ort. talep): {sum(demands):,.0f} TL")
    print(f"    Ortalama per ATM  : {np.mean(demands):,.0f} TL")
    print(f"    Min / Max         : {min(demands):,.0f} / {max(demands):,.0f} TL")
    print()

    total_capacity = sum(v.capacity for v in network.vehicles)
    total_demand   = sum(demands)
    print(f"  Filo Toplam Kapasitesi: {total_capacity:,.0f} TL")
    print(f"  Toplam Ort. Talep     : {total_demand:,.0f} TL")
    print(f"  Kapasite / Talep Oranı: {total_capacity/total_demand:.2f}x")
    print()

    types = {}
    for a in network.atms:
        types[a.atm_type] = types.get(a.atm_type, 0) + 1
    print("  ATM Tipleri:")
    for t, c in sorted(types.items()):
        print(f"    {t:<12}: {c} adet")
    print("=" * 60)

    # Mesafe matrisi özeti
    D = network.distance_matrix
    off_diag = D[D > 0]
    print(f"\n  Mesafe Matrisi:")
    print(f"    Ort. mesafe  : {off_diag.mean():.1f} km")
    print(f"    Max mesafe   : {off_diag.max():.1f} km")
    print(f"    Min mesafe   : {off_diag.min():.1f} km")
    print("=" * 60)


# ─────────────────────────────────────────────
# 5. GÖRSELLEŞTİRME
# ─────────────────────────────────────────────

def visualize_network(network: CITNetwork, save_path: str = "phase1a_atm_network.png") -> None:
    """
    ATM noktalarını ve depoyu İstanbul haritası üzerinde gösterir.
    
    Renk kodu:
        ★ Kırmızı yıldız = Depo (Maslak)
        🔴 Kırmızı daire = AVM ATM'leri (yüksek talep)
        🟠 Turuncu kare  = Plaza ATM'leri
        🟢 Yeşil üçgen   = Hastane ATM'leri
        🔵 Mavi daire    = Cadde ATM'leri
    
    Daire boyutu = ortalama talep miktarıyla orantılı
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.patch.set_facecolor('#0d1117')

    # ── Sol panel: Harita ──
    ax = axes[0]
    ax.set_facecolor('#1a1f2e')
    ax.set_title("İstanbul CIT Ağı — ATM Lokasyonları", 
                 color='white', fontsize=14, fontweight='bold', pad=12)

    # Tip → renk/marker eşlemesi
    style_map = {
        "avm":     {"color": "#ff4444", "marker": "o", "zorder": 5},
        "plaza":   {"color": "#ff9933", "marker": "s", "zorder": 4},
        "hastane": {"color": "#44ff88", "marker": "^", "zorder": 4},
        "cadde":   {"color": "#4499ff", "marker": "o", "zorder": 3},
    }

    # Arka plan ızgara
    ax.grid(True, alpha=0.15, color='gray', linestyle='--', linewidth=0.5)

    # ATM noktaları
    max_demand = max(a.mean_demand for a in network.atms)
    for atm in network.atms:
        style = style_map.get(atm.atm_type, style_map["cadde"])
        size  = 80 + 300 * (atm.mean_demand / max_demand)  # talebe göre boyut

        ax.scatter(atm.lon, atm.lat,
                   c=style["color"], marker=style["marker"],
                   s=size, alpha=0.90, zorder=style["zorder"],
                   edgecolors='white', linewidths=0.6)

        # ATM ID etiketi
        ax.annotate(str(atm.id),
                    xy=(atm.lon, atm.lat),
                    xytext=(3, 3), textcoords='offset points',
                    color='white', fontsize=7, fontweight='bold',
                    zorder=6)

    # Depo
    ax.scatter(network.depot.lon, network.depot.lat,
               c='#ffdd00', marker='*', s=500, zorder=10,
               edgecolors='white', linewidths=1.0, label='Depo')
    ax.annotate('DEPO\n(Maslak)',
                xy=(network.depot.lon, network.depot.lat),
                xytext=(5, 8), textcoords='offset points',
                color='#ffdd00', fontsize=8, fontweight='bold', zorder=11)

    # Boğaz çizgisi (yaklaşık)
    ax.axvline(x=29.025, color='#3388ff', alpha=0.3,
               linewidth=2, linestyle=':', label='Boğaz (yaklaşık)')

    ax.text(28.95, 41.14, 'AVRUPA\nYAKASI', color='#aaccff',
            fontsize=9, alpha=0.6, ha='center')
    ax.text(29.15, 41.14, 'ANADOLU\nYAKASI', color='#aaccff',
            fontsize=9, alpha=0.6, ha='center')

    # Eksen formatı
    ax.set_xlabel('Boylam (°E)', color='#aaaaaa', fontsize=10)
    ax.set_ylabel('Enlem (°N)', color='#aaaaaa', fontsize=10)
    ax.tick_params(colors='#aaaaaa')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')

    # Legend
    legend_handles = [
        mpatches.Patch(color='#ff4444', label='AVM'),
        mpatches.Patch(color='#ff9933', label='Plaza'),
        mpatches.Patch(color='#44ff88', label='Hastane'),
        mpatches.Patch(color='#4499ff', label='Cadde'),
        plt.Line2D([0],[0], marker='*', color='w', markerfacecolor='#ffdd00',
                   markersize=12, label='Depo'),
    ]
    ax.legend(handles=legend_handles, loc='lower right',
              facecolor='#1a1f2e', edgecolor='#444466',
              labelcolor='white', fontsize=9)

    # ── Sağ panel: Talep çubuğu grafiği ──
    ax2 = axes[1]
    ax2.set_facecolor('#1a1f2e')
    ax2.set_title("ATM Ortalama Günlük Talep ve Belirsizlik",
                  color='white', fontsize=14, fontweight='bold', pad=12)

    names   = [f"ATM {a.id}\n{a.name.split()[0]}" for a in network.atms]
    demands = [a.mean_demand / 1000 for a in network.atms]   # bin TL
    stds    = [a.std_demand  / 1000 for a in network.atms]
    colors  = [style_map[a.atm_type]["color"] for a in network.atms]

    bars = ax2.barh(names, demands, xerr=stds,
                    color=colors, alpha=0.8,
                    error_kw={'ecolor': 'white', 'alpha': 0.5, 'linewidth': 1})

    ax2.set_xlabel("Ortalama Günlük Talep (bin TL) ± 1σ",
                   color='#aaaaaa', fontsize=10)
    ax2.tick_params(colors='#aaaaaa', labelsize=8)
    for spine in ax2.spines.values():
        spine.set_edgecolor('#333355')
    ax2.grid(True, axis='x', alpha=0.15, color='gray', linestyle='--')
    ax2.invert_yaxis()

    # Değer etiketleri
    for bar, d in zip(bars, demands):
        ax2.text(d + 1, bar.get_y() + bar.get_height()/2,
                 f'{d:.0f}k', va='center', color='white', fontsize=7)

    # Araç kapasitesi referans çizgisi
    per_vehicle_share = network.vehicles[0].capacity / 1000 / len(network.atms) * len(network.vehicles)
    ax2.axvline(x=network.vehicles[0].capacity / 1000,
                color='#ffdd00', linewidth=1.5, linestyle='--', alpha=0.7,
                label=f'Araç Kapasitesi (500k TL)')
    ax2.legend(facecolor='#1a1f2e', edgecolor='#444466',
               labelcolor='white', fontsize=9)

    plt.tight_layout(pad=2.0)
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Gorsel kaydedildi: {save_path}")


# ─────────────────────────────────────────────
# 6. ANA AKIŞ
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n[*] ASAMA 1a -- ATM Agi Kuruluyor...\n")

    # Ağı oluştur
    network = create_istanbul_network()

    # Mesafe ve zaman matrislerini hesapla
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)

    # Özet yazdır
    print_network_summary(network)

    # Görselleştir
    visualize_network(network)

    # Sonraki asamalara aktarilacak nesneyi hazirla
    print("\n[OK] network nesnesi ASAMA 1b'ye hazir.")
    print(f"   network.atms          → {len(network.atms)} ATM")
    print(f"   network.vehicles      → {len(network.vehicles)} araç")
    print(f"   network.distance_matrix → shape {network.distance_matrix.shape}")
    print(f"   network.time_matrix     → shape {network.time_matrix.shape}")
