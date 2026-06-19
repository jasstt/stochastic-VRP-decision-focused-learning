# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 3b (GAMSPy Versiyonu)
Two-Stage Stochastic VRP -- SAA ile Optimal Yukleme LP
=============================================================

Bu script, AŞAMA 3a'daki "Two-Stage Stochastic Loading" probleminin
PuLP yerine **GAMSPy** kütüphanesi ile modellenmiş alternatif versiyonudur.
GAMSPy, Endüstri standardı olan GAMS optimizasyon motorunu Python üzerinden
çağırmamızı sağlar ve matris-vektör operasyonlarını daha hızlı derler.

Not: Bu betiği çalıştırmak için `gamspy` kütüphanesinin yüklü olması gerekir.
Yüklemek için: `pip install gamspy`
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import sys, io, os

try:
    import gamspy as gp
except ImportError:
    print("HATA: 'gamspy' modulu bulunamadi. Lutfen 'pip install gamspy' komutuyla yukleyin.")
    sys.exit(1)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

# Phase 1a'dan bazi yardimci fonksiyonlari iceri aliyoruz
from phase1a_network_setup import create_istanbul_network, build_distance_matrix, build_time_matrix
# Phase 3a'daki islevleri yeniden kullanmak icin
from phase3a_stochastic_loading import (
    load_routes_from_csv, get_route_groups, compute_det_cost,
    compare_and_print, visualize_comparison, save_results
)

# Maliyet parametreleri
COST_PER_KM   = 8.5    # TL/km
PENALTY_RATIO = 3.0    # her 1 TL eksik nakit -> 3 TL ceza

# ─────────────────────────────────────────────
# 1. GAMSPY ILE STOCHASTIC YUKLEME LP
# ─────────────────────────────────────────────

def solve_stochastic_loading_gamspy(route_groups: dict,
                                    scenario_matrix: np.ndarray,
                                    network,
                                    penalty: float = PENALTY_RATIO) -> dict:
    """
    r_i yukleme miktarlarini minimize ederek stochastic LP cozumu (GAMSPy ile).
    """
    S, N = scenario_matrix.shape
    Q    = float(network.vehicles[0].capacity)
    
    # GAMS Container baslat
    m = gp.Container()
    
    # ── Kümeler (Sets) ──
    i = gp.Set(m, name="i", records=[str(idx) for idx in range(N)], description="ATMs")
    s = gp.Set(m, name="s", records=[str(scn) for scn in range(S)], description="Scenarios")
    
    k_list = [str(k_id) for k_id in route_groups.keys()]
    k = gp.Set(m, name="k", records=k_list, description="Vehicles")
    
    # Araç -> ATM atama haritasi (2D Kume)
    route_map_records = []
    for k_id, atm_ids in route_groups.items():
        for aid in atm_ids:
            route_map_records.append((str(k_id), str(aid - 1)))
            
    route_map = gp.Set(m, name="route_map", domain=[k, i], records=route_map_records)
    
    # ── Parametreler (Parameters) ──
    xi_records = []
    for scn in range(S):
        for atm in range(N):
            xi_records.append((str(scn), str(atm), float(scenario_matrix[scn, atm])))
            
    xi = gp.Parameter(m, name="xi", domain=[s, i], records=xi_records)
    Q_param = gp.Parameter(m, name="Q", records=Q)
    p_param = gp.Parameter(m, name="penalty", records=penalty)
    prob_s  = gp.Parameter(m, name="prob", records=1.0/S)
    
    # ── Degiskenler (Variables) ──
    r = gp.Variable(m, name="r", type="Positive", domain=[i], description="Yuklenen Nakit")
    z = gp.Variable(m, name="z", type="Positive", domain=[i, s], description="Eksik Nakit")
    obj = gp.Variable(m, name="obj", type="Free", description="Toplam Beklenen Ceza")
    
    # ── Kisitlar (Equations) ──
    # 1. Arac kapasite kisiti
    cap_eq = gp.Equation(m, name="cap_eq", domain=[k], description="Arac kapasitesi asilamaz")
    cap_eq[k] = gp.Sum(i.where[route_map[k, i]], r[i]) <= Q_param
    
    # 2. Eksik nakit (shortfall) kisiti
    shortfall_eq = gp.Equation(m, name="shortfall_eq", domain=[i, s], description="Z kisiti linearizasyonu")
    shortfall_eq[i, s] = z[i, s] >= xi[s, i] - r[i]
    
    # 3. Amac fonksiyonu
    obj_eq = gp.Equation(m, name="obj_eq", description="Amac")
    obj_eq[...] = obj == prob_s * p_param * gp.Sum((i, s), z[i, s])
    
    # ── Model ──
    stoch_model = gp.Model(
        m,
        name="StochasticLoadingGAMSPy",
        equations=[cap_eq, shortfall_eq, obj_eq],
        problem="LP",
        sense=gp.Sense.MIN,
        objective=obj
    )
    
    # ── Cozum ──
    t0 = time.time()
    # output_sys_out=False yapildi ki ekrani GAMS loglari ile doldurmasin
    stoch_model.solve() 
    elapsed = time.time() - t0
    
    # ── Sonuclari Ayiklama ──
    # r.records bir DataFrame dondurur (i, level, marginal, lower, upper, scale)
    r_df = r.records.set_index("i") if r.records is not None else pd.DataFrame()
    r_opt = np.array([r_df.loc[str(idx), "level"] if str(idx) in r_df.index else 0.0 for idx in range(N)])
    
    # Amac degeri = Beklenen ceza
    expected_penalty = float(obj.records["level"].iloc[0]) if obj.records is not None else 0.0
    
    route_cost_stoch  = 3394.0   # Phase 2a'dan gelen sabit rota maliyeti
    total_cost_stoch  = route_cost_stoch + expected_penalty
    shortfall_matrix  = np.maximum(0, scenario_matrix - r_opt[np.newaxis, :])
    
    status_str = str(stoch_model.status)
    
    print(f"\n  [OK] GAMSPy LP cozuldu: {status_str} ({elapsed:.2f} sn)")
    
    return {
        "route_cost":       route_cost_stoch,
        "expected_penalty": expected_penalty,
        "total_cost":       total_cost_stoch,
        "r_values":         r_opt,
        "shortfall_matrix": shortfall_matrix,
        "status":           status_str,
        "elapsed":          elapsed,
    }


# ─────────────────────────────────────────────
# 2. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 3b -- Two-Stage Stochastic Loading LP (GAMSPy Versiyonu) Basliyor...\n")

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
    routes       = load_routes_from_csv(base)
    route_groups = get_route_groups(routes)
    print(f"  [OK] {len(route_groups)} aktif rota grubu yuklendi (Phase 2a).")

    # Deterministik referans maliyeti (PuLP versiyonundaki fonksiyonu cagiriyoruz)
    print("\n  [..] Deterministik referans maliyeti hesaplaniyor...")
    det_result = compute_det_cost(demands_det, route_groups, scenario_matrix, network)
    print(f"  [OK] Det. beklenen ceza   : {det_result['expected_penalty']:,.2f} TL/gun")

    # Stochastic LP coz (GAMSPy ile)
    print(f"\n  [..] GAMSPy Stochastic Loading LP cozuluyor (S={S}, N={N})...")
    stoch_result = solve_stochastic_loading_gamspy(
        route_groups, scenario_matrix, network, penalty=PENALTY_RATIO
    )
    print(f"  [OK] Stoch. beklenen ceza : {stoch_result['expected_penalty']:,.2f} TL/gun")

    # Kiyaslama tablosu (ayni fonksiyon)
    compare_and_print(det_result, stoch_result, demands_det, scenario_matrix, network)

    print("\n[OK] ASAMA 3b (GAMSPy) tamamlandi.")
