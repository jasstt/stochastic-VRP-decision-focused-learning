# -*- coding: utf-8 -*-
"""
=============================================================
ARUTE CIT-SVRP -- AŞAMA 2b
CVRP → QUBO Dönüşümü
=============================================================

Bu script:
  1. Mevcut CVRP modelini (phase2a) matematiksel olarak özetler.
  2. Problemi QUBO (Quadratic Unconstrained Binary Optimization)
     formuna dönüştürür.
  3. Kubit sayısı ve ceza katsayısı (λ) analizini yapar.

NOT: QAOA/kuantum simülatörü bu dosyayı giriş olarak kullanır.
"""

import numpy as np
import pandas as pd
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import create_istanbul_network, build_distance_matrix

# ─────────────────────────────────────────────────────────────────────
# BÖLÜM 1 — MEVCUT MILP FORMÜLASYONU (ÖZETİ)
# ─────────────────────────────────────────────────────────────────────
MILP_SUMMARY = """
╔══════════════════════════════════════════════════════════════════════╗
║  AŞAMA 2a — 3-İndisli MTZ-CVRP (PuLP/CBC)  FORMÜLASYON ÖZETİ       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  KÜME TANIMLARI                                                      ║
║    N = {1,...,20}      ATM düğümleri                                 ║
║    N₀= {0,1,...,20}    Depo (0) + ATM'ler                            ║
║    K = {0,1,2,3}       CIT araçları (4 adet)                         ║
║                                                                      ║
║  KARAR DEĞİŞKENLERİ                                                  ║
║    x_ijk ∈ {0,1}  : Araç k, düğüm i'den j'ye gidiyorsa 1            ║
║    u_ik  ∈ [d_i,Q]: Araç k'nin i'yi ziyaretindeki kümülatif yükü    ║
║                                                                      ║
║  AMAÇ FONKSİYONU                                                     ║
║    min  Σ_k Σ_{i≠j} c_ij · x_ijk                                    ║
║    c_ij = 8.5 TL/km · dist(i,j)                                      ║
║                                                                      ║
║  KISITLAR                                                            ║
║    (C1) Her ATM tam 1 kez ziyaret:                                   ║
║         Σ_k Σ_{j≠i} x_ijk = 1,   ∀i ∈ N                             ║
║    (C2) Araç depodan max 1 kez çıkar:                                ║
║         Σ_{j∈N} x_{0jk} ≤ 1,     ∀k ∈ K                             ║
║    (C3) Akış dengesi (giren = çıkan):                                ║
║         Σ_j x_ijk = Σ_j x_jik,   ∀i ∈ N₀, ∀k ∈ K                   ║
║    (C4) MTZ – Kapasite + Alt-tur Eliminasyonu:                       ║
║         u_jk ≥ u_ik + d_j - Q(1-x_ijk),  ∀i∈N, j∈N, k∈K            ║
║         u_{jk} + Q - Q·x_{0jk} ≥ d_j,    ∀j∈N (depodan çıkış)      ║
║         d_i ≤ u_ik ≤ Q                                               ║
║                                                                      ║
║  BOYUT ANALIZI (20 ATM, 4 araç, Q=500.000 TL)                       ║
║    İkili değişken   x: 20×21×4 = 1.680 binary variables              ║
║    Sürekli değişken u: 20×4    = 80 continuous variables             ║
║    Kısıt sayısı       : ~8.500                                       ║
║    PuLP/CBC süresi    : ~60-180 sn                                   ║
║    Optimal maliyet    : 3.394 TL/gün (rota)                          ║
║    + Stokout cezası   : 477.297 TL/gün → TOPLAM: 480.691 TL/gün     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────────────────
# BÖLÜM 2 — QUBO FORMÜLASYONU
# ─────────────────────────────────────────────────────────────────────
# QUBO formu: min  x^T Q x  (x ∈ {0,1}^n, Q ∈ R^{n×n} )
#
# Orijinal CVRP → QUBO dönüşümü için her x_ijk değişkeni bir qubit'e
# karşılık gelir. Kapasite kısıtları ve ziyaret kısıtları ceza terimi
# olarak amaç fonksiyonuna eklenir (λ parametresiyle).
#
# TAM QUBO:
#   H(x) = H_cost + λ₁·H_visit + λ₂·H_cap + λ₃·H_flow
#
# H_cost  = Σ_{i,j,k} c_ij · x_ijk
#
# H_visit = Σ_i (1 - Σ_{j,k} x_ijk)²   [C1: her ATM 1 kez]
#
# H_cap   = Σ_k (Σ_i d_i·Σ_j x_ijk - Q)²  [C4'ün yumuşatılmış hali]
#           NOT: MTZ'nin kuadratik tam karşılığı ancak yardımcı
#           değişkenler + slack bits ile yapılabilir. Burada
#           kapasite ihlalini yaklaşık olarak penalize ediyoruz.
#
# H_flow  = Σ_{i,k} (Σ_j x_ijk - Σ_j x_jik)²  [C3: akış dengesi]
# ─────────────────────────────────────────────────────────────────────


def build_qubo_matrix(network, demands: np.ndarray,
                      lambda_visit: float = 1.0,
                      lambda_cap: float   = 0.5,
                      lambda_flow: float  = 0.8,
                      n_vehicles: int     = None,
                      reduce_size: bool   = True) -> tuple[np.ndarray, dict, int]:
    """
    CVRP modelini QUBO matrisine (Q) çevirir.

    Parametreler
    -----------
    network       : Phase 1a'dan gelen ağ nesnesi
    demands       : ATM talepleri, shape (N,)
    lambda_visit  : Ziyaret kısıtı ceza katsayısı
    lambda_cap    : Kapasite kısıtı ceza katsayısı
    lambda_flow   : Akış dengesi ceza katsayısı
    n_vehicles    : Kullanılacak araç sayısı (None → ağdaki tam sayı)
    reduce_size   : True → alt-problem boyutunu küçültmek için sadece
                    gerçekçi kenarları al (depo-ATM + ATM-ATM)

    Dönüş
    -----
    Q_matrix  : QUBO matrisi (n_qubits × n_qubits)
    var_map   : {(i,j,k): qubit_index} sözlüğü
    n_qubits  : Toplam kubit sayısı
    """
    N_atm  = len(demands)
    N_all  = list(range(N_atm + 1))    # 0=depo, 1..N=ATM
    N_atms = list(range(1, N_atm + 1))
    K      = list(range(n_vehicles or len(network.vehicles)))
    C      = network.distance_matrix * 8.5   # maliyet matrisi (TL/km)
    Q_cap  = float(network.vehicles[0].capacity)

    # ── Değişken haritası ──
    var_map = {}
    idx = 0
    for k in K:
        for i in N_all:
            for j in N_all:
                if i != j:
                    var_map[(i, j, k)] = idx
                    idx += 1

    n_qubits = idx
    Q_mat = np.zeros((n_qubits, n_qubits))

    # Normalize için maksimum maliyet
    c_max = C.max()

    # ── H_cost: rota maliyetleri (diyagonal) ──
    for (i, j, k), qi in var_map.items():
        Q_mat[qi, qi] += C[i][j] / c_max   # normalize

    # ── H_visit: her ATM tam 1 kez ziyaret edilmeli ──
    # (1 - Σ_{j≠i, k} x_ijk)² = 1 - 2·Σx_ijk + (Σx_ijk)²
    for i in N_atms:
        visit_vars = [(i, j, k) for j in N_all for k in K
                      if j != i and (i, j, k) in var_map]
        # Diyagonal: -2λ₁ (lineer terim)
        for v in visit_vars:
            Q_mat[var_map[v], var_map[v]] -= 2 * lambda_visit
        # Off-diyagonal: +2λ₁ (kuadratik çift)
        for a in range(len(visit_vars)):
            for b in range(a + 1, len(visit_vars)):
                qa = var_map[visit_vars[a]]
                qb = var_map[visit_vars[b]]
                Q_mat[qa, qb] += 2 * lambda_visit
        # Sabit terim: +λ₁ (QUBO matrisine yansımaz, offset)

    # ── H_cap: kapasite kısıtı (her araç için) ──
    # (Σ_i d_i·Σ_j x_ijk - Q)² → ikili genişleme
    for k in K:
        for i in N_atms:
            out_vars = [(i, j, k) for j in N_all if j != i and (i, j, k) in var_map]
            d_i = demands[i - 1] / Q_cap    # normalize
            for v in out_vars:
                Q_mat[var_map[v], var_map[v]] += lambda_cap * d_i * (d_i - 2)
                for v2 in out_vars:
                    if v != v2:
                        Q_mat[var_map[v], var_map[v2]] += lambda_cap * d_i * d_i

    # ── H_flow: akış dengesi kısıtı ──
    # (Σ_j x_ijk - Σ_j x_jik)² = lineer + kuadratik cezalar
    for i in N_all:
        for k in K:
            out_vars = [(i, j, k) for j in N_all if j != i and (i, j, k) in var_map]
            in_vars  = [(j, i, k) for j in N_all if j != i and (j, i, k) in var_map]
            for v in out_vars:
                Q_mat[var_map[v], var_map[v]] += lambda_flow
            for v in in_vars:
                Q_mat[var_map[v], var_map[v]] += lambda_flow
            for v_out in out_vars:
                for v_in in in_vars:
                    qa = var_map[v_out]
                    qb = var_map[v_in]
                    if qa != qb:
                        Q_mat[min(qa,qb), max(qa,qb)] -= 2 * lambda_flow

    return Q_mat, var_map, n_qubits


def analyze_qubit_scaling(n_nodes_list: list, n_vehicles_list: list) -> pd.DataFrame:
    """
    Farklı ağ boyutları için kubit ve QUBO büyüklüğü analizini hesaplar.
    n_nodes_list: ATM sayısı [20, 50, 100, 200]
    """
    rows = []
    for n_nodes, n_veh in zip(n_nodes_list, n_vehicles_list):
        n_all      = n_nodes + 1        # depo dahil
        n_edges    = n_all * (n_all-1)  # yönlü kenarlar
        n_qubits   = n_edges * n_veh    # x_{ijk} değişkenleri
        n_slack    = n_nodes * n_veh * 10  # kapasite slack bits (yaklaşık)
        total_q    = n_qubits + n_slack
        qubo_size  = total_q ** 2 / 1e6  # MB (float64)
        n_terms    = n_qubits * (n_qubits - 1) // 2  # QUBO off-diag eleman
        rows.append({
            "ATM Sayısı":      n_nodes,
            "Araç Sayısı":     n_veh,
            "Karar x-Qubits":  n_qubits,
            "Slack Qubits":    n_slack,
            "Toplam Qubits":   total_q,
            "QUBO Boyutu (MB)": round(qubo_size, 1),
            "QUBO Terim Sayısı": f"{n_terms:,}",
        })
    return pd.DataFrame(rows)


def penalty_tradeoff_analysis(costs: np.ndarray, demands: np.ndarray,
                               lambda_range: np.ndarray) -> pd.DataFrame:
    """
    Farklı λ değerleri için tahmini kısıt ihlali sayısını gösterir.
    Sezgisel analiz: λ çok küçük → ihlal baskın, λ çok büyük → arama bozulur.
    """
    c_mean   = costs.mean()
    d_mean   = demands.mean()
    Q_cap    = 500_000.0
    rows = []
    for lam in lambda_range:
        # Bir kısıt ihlalinin maliyeti ≈ λ × (ihlal büyüklüğü)
        # İhlal yaratmak ≠ avantajlı olduğu eşik: λ > c_max
        violation_cost  = lam * d_mean     # 1 ATM atlama cezası
        c_saving        = c_mean           # atlayınca kazanılan rota maliyeti
        violation_ratio = c_saving / violation_cost if violation_cost > 0 else np.inf
        search_quality  = "İyi" if 0.1 < violation_ratio < 10 else (
                           "Fazla serbest (ihlal olur)" if violation_ratio >= 10
                           else "Fazla sıkı (arama bozulur)")
        rows.append({
            "λ (penalty)": round(lam, 3),
            "1 ihlal ceza (TL)": round(violation_cost),
            "Rota tasarrufu (TL)": round(c_saving),
            "Oran (tasarruf/ceza)": round(violation_ratio, 3),
            "Durum": search_quality
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    BASE = os.path.dirname(__file__)

    print(MILP_SUMMARY)

    # Network yükle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)

    # Talep yükle
    demand_df = pd.read_csv(os.path.join(BASE, "data_demand_365.csv"),
                            index_col="tarih", parse_dates=True)
    demands = demand_df.mean().values
    N       = len(demands)
    n_veh   = len(network.vehicles)

    # ── QUBO Matrisi ──
    print("\n[1] QUBO matrisi oluşturuluyor (20 ATM, 4 araç)...")
    λ1, λ2, λ3 = 1.0, 0.5, 0.8
    Q_mat, var_map, n_qubits = build_qubo_matrix(
        network, demands,
        lambda_visit=λ1, lambda_cap=λ2, lambda_flow=λ3
    )
    print(f"    Toplam qubit       : {n_qubits:,}")
    print(f"    QUBO matris boyutu : {n_qubits}×{n_qubits} = {n_qubits**2:,} eleman")
    print(f"    Sıfır olmayan oran : {np.count_nonzero(Q_mat)/n_qubits**2*100:.1f}%")

    # ── Ceza Katsayısı Trade-off ──
    print("\n[2] Ceza katsayısı (λ) trade-off analizi:")
    costs_arr = network.distance_matrix.flatten() * 8.5
    costs_arr = costs_arr[costs_arr > 0]
    lambda_range = np.array([0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0])
    df_penalty = penalty_tradeoff_analysis(costs_arr, demands, lambda_range)
    print(df_penalty.to_string(index=False))
    df_penalty.to_csv(os.path.join(BASE, "data_qubo_penalty_analysis.csv"), index=False)
    print(f"\n    [SAVED] data_qubo_penalty_analysis.csv")
    print(f"\n    Tavsiye: λ₁={λ1}, λ₂={λ2}, λ₃={λ3}")
    print("    λ₁ (ziyaret kısıtı) en kritik → en yüksek tutulmalı")
    print("    λ₂ (kapasite) ≈ 0.5×λ₁ iyi denge noktası")
    print("    λ₃ (akış) ≈ 0.8×λ₁ akış ihlallerini baskılar")

    # ── Kubit Ölçekleme Analizi ──
    print("\n[3] Ağ boyutuna göre Kubit ölçekleme analizi:")
    n_nodes_list   = [20, 50, 100, 200]
    n_vehicles_list = [4,  8,  15,  30]
    df_scale = analyze_qubit_scaling(n_nodes_list, n_vehicles_list)
    print(df_scale.to_string(index=False))
    df_scale.to_csv(os.path.join(BASE, "data_qubo_qubit_scaling.csv"), index=False)
    print(f"\n    [SAVED] data_qubo_qubit_scaling.csv")

    # QUBO matrisini binary formatında kaydet (sonraki aşamalar kullanır)
    np.save(os.path.join(BASE, "data_qubo_matrix.npy"), Q_mat)
    print(f"    [SAVED] data_qubo_matrix.npy ({n_qubits}×{n_qubits})")

    # Var_map kaydet
    import json
    var_map_str = {str(k): v for k, v in var_map.items()}
    with open(os.path.join(BASE, "data_qubo_varmap.json"), "w") as f:
        json.dump({"var_map": var_map_str, "n_qubits": n_qubits, "N_atm": N}, f)
    print(f"    [SAVED] data_qubo_varmap.json")

    print("\n[OK] AŞAMA 2b (QUBO Formülasyonu) tamamlandı.")
    print("     Bir sonraki: AŞAMA 2c — QAOA Simülatörü")
