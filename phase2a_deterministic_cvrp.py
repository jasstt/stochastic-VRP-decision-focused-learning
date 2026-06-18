# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP PROJESI -- ASAMA 2a
Deterministik CVRP Baseline (PuLP + CBC)
=============================================================

MANTIK:
-------
Arute'nin mevcut sisteminin basit temsili:
    "Her ATM'nin ortalama talebini al,
     o taleplere gore optimal rotalar planla."

Bu deterministik yaklasim su sorulari cevaplamaz:
    - Ya talep tahmininin 2 kati gelirse?
    - Ya bayram gununde tum ATM'ler aynı anda boslalirsa?

Biz bu baseline'i kurup, ASAMA 2c'de "gercek talepte test edecegiz"
ve stockout oranini olcecegiz. Bu oran, ASAMA 3'teki
Stochastic VRP'nin neden daha iyi oldugunu kanitlayacak.

MODEL (3-indisli MTZ formülasyonu):
------------------------------------
Karar degiskenleri:
    x_ijk ∈ {0,1}  : araç k, i'den j'ye gidiyorsa 1
    u_ik  ≥ 0      : MTZ subtour elmn. yardimci degisken (kumulatif yuk)

Amac:
    min Σ_k Σ_ij c_ij * x_ijk

Kisitlar:
    (1) Her ATM tam bir kez ziyaret edilsin:
        Σ_k Σ_j x_ijk = 1,  ∀i ∈ ATM'ler
    (2) Arac k depodan en fazla bir kez cikar:
        Σ_j x_0jk ≤ 1,  ∀k
    (3) Akis dengesi (her dusumde giren = cikan):
        Σ_j x_ijk = Σ_j x_jik,  ∀i, ∀k
    (4) MTZ kapasite + alttur eliminasyonu:
        u_jk ≥ u_ik + d_j * x_ijk - Q*(1-x_ijk),  ∀(i,j), ∀k
        d_i ≤ u_ik ≤ Q,  ∀i ∈ ATM'ler, ∀k

Nokta tahmin: d_i = ATM i'nin ortalama talebi (ASAMA 1b'den)
Cozucu: PuLP + CBC (acik kaynak)
Zaman limiti: 300 saniye (5 dakika) -- en iyi bulunan cozumu al
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import pulp
import time
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))
from phase1a_network_setup import (create_istanbul_network,
                                    build_distance_matrix,
                                    build_time_matrix)

# Maliyet parametreleri
COST_PER_KM     = 8.5    # TL/km -- yakit + amortiman
SERVICE_TIME    = 15     # dakika / ATM ziyareti
TIME_LIMIT_SEC  = 300    # CBC icin max sure


# ─────────────────────────────────────────────
# 1. NOKTA TAHMİN (deterministik talep)
# ─────────────────────────────────────────────

def get_point_estimates(demand_df: pd.DataFrame, network) -> np.ndarray:
    """
    Her ATM icin tek bir talep degeri: 365 gunluk ortalama.
    Bu, deterministik VRP'nin 'd_i' parametresi olacak.

    Donus: shape (N,) array -- ATM siralamasina gore
    """
    demands = np.array([demand_df[col].mean()
                        for col in demand_df.columns])
    print("  Nokta tahmin talepleri (TL):")
    for i, (atm, d) in enumerate(zip(network.atms, demands)):
        print(f"    ATM {atm.id:02d} {atm.name:<22}: {d:>10,.0f} TL")
    print(f"    {'TOPLAM':<28}: {demands.sum():>10,.0f} TL")
    return demands


# ─────────────────────────────────────────────
# 2. CVRP MIP MODELI
# ─────────────────────────────────────────────

def build_cvrp_model(network, demands: np.ndarray):
    """
    PuLP ile 3-indisli MTZ-CVRP modelini kurar.

    Donus: (prob, x_vars, u_vars) -- cozum icin hazir PuLP nesneleri
    """
    n_atms     = len(network.atms)
    n_vehicles = len(network.vehicles)
    Q          = network.vehicles[0].capacity    # tum araclar esit kapasiteli
    D          = network.distance_matrix         # (n+1) x (n+1), satir/sutun 0 = depo
    C          = D * COST_PER_KM                 # maliyet matrisi

    # Dugum indisleri: 0 = depo, 1..n = ATM'ler
    N_all  = list(range(n_atms + 1))   # [0, 1, ..., 20]
    N_atms = list(range(1, n_atms + 1)) # [1, 2, ..., 20]
    K      = list(range(n_vehicles))    # [0, 1, 2, 3]

    prob = pulp.LpProblem("CVRP_Deterministic", pulp.LpMinimize)

    # ── Karar degiskenleri ──
    # x[i][j][k] = 1 eger araç k, i->j gidiyorsa
    x = pulp.LpVariable.dicts(
        "x",
        [(i, j, k) for i in N_all for j in N_all for k in K
         if i != j],
        cat='Binary'
    )

    # u[i][k] = araç k'nin i dugumunu ziyaret ettiginde kumulatif yuku
    u = pulp.LpVariable.dicts(
        "u",
        [(i, k) for i in N_atms for k in K],
        lowBound=0, upBound=Q, cat='Continuous'
    )

    # ── Amac fonksiyonu ──
    prob += pulp.lpSum(
        C[i][j] * x[(i, j, k)]
        for i in N_all for j in N_all for k in K
        if i != j
    ), "Toplam_Rota_Maliyeti"

    # ── Kisit 1: Her ATM tam bir kez ziyaret ──
    for i in N_atms:
        prob += (
            pulp.lpSum(x[(i, j, k)]
                       for j in N_all for k in K if j != i) == 1,
            f"Ziyaret_{i}"
        )

    # ── Kisit 2: Her araç depodan en fazla bir kez cikar ──
    for k in K:
        prob += (
            pulp.lpSum(x[(0, j, k)] for j in N_atms) <= 1,
            f"Depo_Cikis_{k}"
        )

    # ── Kisit 3: Akis dengesi (her dugumde giren = cikan) ──
    for i in N_all:
        for k in K:
            prob += (
                pulp.lpSum(x[(i, j, k)] for j in N_all if j != i) ==
                pulp.lpSum(x[(j, i, k)] for j in N_all if j != i),
                f"Akis_{i}_{k}"
            )

    # ── Kisit 4: MTZ kapasite + alttur eliminasyonu ──
    # Dogru form: u[j] >= u[i] + d[j] - Q*(1 - x[ij])
    # Esit anlam: u[j] - u[i] + Q*(1 - x[ij]) >= d[j]
    # => u[j] - u[i] + Q - Q*x[ij] >= d[j]
    #
    # x[ij]=1 ise: u[j] >= u[i] + d[j]  (yuk artar -- DOGRU)
    # x[ij]=0 ise: u[j] >= u[i] + d[j] - Q  (trivially ok)
    for k in K:
        for i in N_all:
            for j in N_atms:
                if i != j:
                    d_j = demands[j - 1]
                    if i in N_atms:
                        # u[j] - u[i] + Q - Q*x[ij] >= d[j]
                        prob += (
                            u[(j, k)] - u[(i, k)] + Q - Q * x[(i, j, k)] >= d_j,
                            f"MTZ_{i}_{j}_{k}"
                        )
                    else:
                        # i = depo => u[depo] = 0
                        # u[j] + Q - Q*x[0j] >= d[j]
                        prob += (
                            u[(j, k)] + Q - Q * x[(0, j, k)] >= d_j,
                            f"MTZ_dep_{j}_{k}"
                        )

    # Alt sinir: u[i] >= d[i]  (her ATM'ye yuklenecek min nakit)
    for k in K:
        for i in N_atms:
            prob += (
                u[(i, k)] >= demands[i - 1],
                f"Umin_{i}_{k}"
            )

    print(f"\n  Model kuruldu:")
    print(f"    Degisken sayisi : {len(prob.variables())}")
    print(f"    Kisit sayisi    : {len(prob.constraints)}")

    return prob, x, u, N_all, N_atms, K


# ─────────────────────────────────────────────
# 3. COZUM VE ROTA EXTRACTION
# ─────────────────────────────────────────────

def solve_cvrp(prob, time_limit: int = TIME_LIMIT_SEC):
    """
    CBC cozucusuyle modeli cozer.
    Zaman limiti asildiysa en iyi bulunan feasible cozumu doner.
    """
    solver = pulp.PULP_CBC_CMD(
        msg=1,
        timeLimit=time_limit,
        gapRel=0.05    # %5 optimality gap yeterli (arastirma prototipi)
    )
    print(f"\n  [..] CBC cozuyor (max {time_limit}s, gap<%5)...")
    t0     = time.time()
    status = prob.solve(solver)
    elapsed = time.time() - t0

    print(f"\n  Cozum durumu : {pulp.LpStatus[prob.status]}")
    print(f"  Sure         : {elapsed:.1f} saniye")
    print(f"  Amac degeri  : {pulp.value(prob.objective):,.2f} TL (rota maliyeti)")

    return status, elapsed


def extract_routes(x, N_all, N_atms, K, network):
    """
    x degiskenlerinden her araç icin rota listesi cikarir.

    Donus: {k: [0, i1, i2, ..., 0]} -- depodan cikip donuyor
    """
    routes = {}
    n_nodes = len(N_all)  # sonsuz dongü icin güvenlik siniri

    for k in K:
        start_arcs = [(i, j) for i in N_all for j in N_all
                      if i != j and
                      pulp.value(x.get((i, j, k), 0) or 0) > 0.5]

        if not start_arcs:
            routes[k] = []
            continue

        # Arclari zincire donustur
        arc_dict = {i: j for (i, j) in start_arcs}
        route    = [0]
        current  = arc_dict.get(0)
        visited  = {0}

        while current is not None and current != 0:
            if current in visited or len(route) > n_nodes + 2:
                # Alttur veya bozuk cozum -- guvende kes
                break
            route.append(current)
            visited.add(current)
            current = arc_dict.get(current)

        route.append(0)
        routes[k] = route

    return routes


def print_routes(routes, demands, network):
    """Rotalari insan-okunabilir formatta yazdir."""
    print("\n  Optimal Rotalar:")
    print("  " + "="*65)
    total_cost = 0
    total_load = 0
    D = network.distance_matrix

    for k, route in routes.items():
        if len(route) <= 2:   # sadece depo-depo = bos
            continue

        atm_ids   = [r for r in route if r > 0]
        load      = sum(demands[i-1] for i in atm_ids)
        cap       = network.vehicles[k].capacity
        dist_km   = sum(D[route[t]][route[t+1]]
                        for t in range(len(route)-1))
        cost      = dist_km * COST_PER_KM
        total_cost += cost
        total_load += load

        atm_names = " -> ".join(
            f"ATM{i}({network.atms[i-1].name.split()[0]})"
            for i in atm_ids
        )
        print(f"  Araç {k+1}: {len(atm_ids)} ATM | "
              f"Yuk: {load:,.0f}/{cap:,.0f} TL ({load/cap*100:.0f}%) | "
              f"Dist: {dist_km:.1f} km | Maliyet: {cost:,.0f} TL")
        print(f"    DEPO -> {atm_names} -> DEPO")

    print("  " + "="*65)
    print(f"  TOPLAM ROTA MALIYETI : {total_cost:,.0f} TL")
    print(f"  TOPLAM YUK           : {total_load:,.0f} TL")
    return total_cost


# ─────────────────────────────────────────────
# 4. EX-POST STOCKOUT ANALIZI
# ─────────────────────────────────────────────

def evaluate_stockout(routes, demands_det, network,
                      scenario_matrix: np.ndarray) -> dict:
    """
    Deterministik plan SAA senaryolarinda test edilir.

    Her senaryo s icin:
        - ATM i'ye yüklenen miktar = deterministik plan (r_i = d_i_det)
        - Gercek talep = xi_i^s (senaryodan)
        - Stockout_i^s = max(0, xi_i^s - r_i)

    Stockout orani = kac ATM'de kac senaryoda stockout var?
    """
    S, N   = scenario_matrix.shape
    r_det  = demands_det.copy()   # deterministik yukleme = nokta tahmin

    stockout_matrix = np.zeros((S, N))   # her hucre = o senaryoda o ATM'nin stockout'u

    for s in range(S):
        for j in range(N):
            shortfall = scenario_matrix[s, j] - r_det[j]
            stockout_matrix[s, j] = max(0.0, shortfall)

    # Metrikler
    n_stockout_events = np.sum(stockout_matrix > 0)
    stockout_rate     = n_stockout_events / (S * N)          # % hucre
    atm_stockout_rate = np.mean(stockout_matrix > 0, axis=0) # her ATM icin
    scenario_stockout = np.mean(np.any(stockout_matrix > 0, axis=1)) # senaryo bazli

    total_shortfall   = stockout_matrix.sum()
    avg_shortfall_per_event = (total_shortfall / n_stockout_events
                               if n_stockout_events > 0 else 0)

    # Ceza maliyeti (p = 5x tasima maliyeti -- Arute parametre referansi)
    p_penalty = COST_PER_KM * 5
    total_penalty = total_shortfall * p_penalty / 1e6   # milyon TL

    print("\n  Ex-Post Stockout Analizi (deterministik plan, SAA senaryolarinda):")
    print("  " + "="*65)
    print(f"  Senaryo sayisi              : {S}")
    print(f"  ATM sayisi                  : {N}")
    print(f"  Toplam test edilecek olay   : {S * N}")
    print(f"  Stockout olan olay sayisi   : {n_stockout_events}")
    print(f"  Genel stockout orani        : %{stockout_rate*100:.1f}")
    print(f"  Senaryo bazli stockout orani: %{scenario_stockout*100:.1f}")
    print(f"    (en az 1 ATM'de stockout olan senaryo yuzdesi)")
    print(f"  Toplam eksik nakit          : {total_shortfall:,.0f} TL")
    print(f"  Ortalama eksik / olay       : {avg_shortfall_per_event:,.0f} TL")
    print(f"  Tahmini ceza maliyeti       : {total_penalty:.2f}M TL")
    print("  " + "="*65)

    print("\n  En yuksek stockout riski olan ATM'ler:")
    top_atms = np.argsort(atm_stockout_rate)[::-1][:5]
    for rank, j in enumerate(top_atms, 1):
        print(f"    {rank}. ATM {j+1:02d}: %{atm_stockout_rate[j]*100:.1f} "
              f"stockout riski -- ort eksik: {stockout_matrix[:,j].mean():,.0f} TL")

    return {
        "stockout_matrix":       stockout_matrix,
        "stockout_rate":         stockout_rate,
        "scenario_stockout":     scenario_stockout,
        "atm_stockout_rate":     atm_stockout_rate,
        "total_shortfall":       total_shortfall,
        "avg_shortfall":         avg_shortfall_per_event,
        "total_penalty_TL":      total_penalty * 1e6,
        "n_stockout_events":     n_stockout_events,
    }


# ─────────────────────────────────────────────
# 5. GORSELLESTIRME
# ─────────────────────────────────────────────

def visualize_routes(routes, demands, network,
                     save_path="phase2a_routes.png"):
    """
    ATM konumlarini ve optimal rotalari harita uzerinde gosterir.
    Her araç farkli renkle, oklar rota yonunu gosterir.
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 9))
    fig.patch.set_facecolor('#0d1117')

    ROUTE_COLORS = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#a8e6cf']
    dark = '#1a1f2e'

    # ── Sol: Rota Haritasi ──
    ax = axes[0]
    ax.set_facecolor(dark)
    ax.set_title("Deterministik CVRP -- Optimal Rotalar",
                 color='white', fontsize=13, fontweight='bold')

    ax.axvline(x=29.025, color='#3388ff', alpha=0.2,
               linewidth=2, linestyle=':')
    ax.text(28.94, 41.14, 'AVRUPA', color='#aaccff', fontsize=8, alpha=0.5)
    ax.text(29.12, 41.14, 'ANADOLU', color='#aaccff', fontsize=8, alpha=0.5)

    # ATM'leri ciz
    for atm in network.atms:
        ax.scatter(atm.lon, atm.lat, c='#445566', s=60, zorder=3,
                   edgecolors='#778899', linewidths=0.8)
        ax.annotate(str(atm.id), xy=(atm.lon, atm.lat),
                    xytext=(2, 2), textcoords='offset points',
                    color='#aaaaaa', fontsize=6.5, zorder=4)

    # Depo
    depot = network.depot
    ax.scatter(depot.lon, depot.lat, c='#ffdd00', marker='*',
               s=400, zorder=10, edgecolors='white', linewidths=1.0)

    # Rotalari ciz
    lons = [network.depot.lon] + [a.lon for a in network.atms]
    lats = [network.depot.lat] + [a.lat for a in network.atms]

    for k, route in routes.items():
        if len(route) <= 2:
            continue
        color = ROUTE_COLORS[k % len(ROUTE_COLORS)]
        for t in range(len(route) - 1):
            i, j = route[t], route[t+1]
            xi, yi = lons[i], lats[i]
            xj, yj = lons[j], lats[j]
            dx, dy = xj - xi, yj - yi
            ax.annotate("",
                xy=(xj, yj), xytext=(xi, yi),
                arrowprops=dict(
                    arrowstyle="-|>",
                    color=color, lw=1.8, alpha=0.85,
                    mutation_scale=12,
                )
            )

    # Legend
    legend_handles = [
        mpatches.Patch(color=ROUTE_COLORS[k], label=f"Araç {k+1}")
        for k, route in routes.items() if len(route) > 2
    ]
    legend_handles.append(
        plt.Line2D([0],[0], marker='*', color='w',
                   markerfacecolor='#ffdd00', markersize=12, label='Depo')
    )
    ax.legend(handles=legend_handles, loc='lower right',
              facecolor=dark, edgecolor='#444466',
              labelcolor='white', fontsize=9)

    ax.set_xlabel("Boylam", color='#aaaaaa')
    ax.set_ylabel("Enlem", color='#aaaaaa')
    ax.tick_params(colors='#aaaaaa')
    ax.grid(True, alpha=0.10, color='gray', linestyle='--')
    for sp in ax.spines.values():
        sp.set_edgecolor('#333355')

    # ── Sag: Araç yuk kullanimi ──
    ax2 = axes[1]
    ax2.set_facecolor(dark)
    ax2.set_title("Araç Yuk Kullanimi (Deterministik Plan)",
                  color='white', fontsize=13, fontweight='bold')

    vehicle_labels, loads, capacities = [], [], []
    for k, route in routes.items():
        if len(route) <= 2:
            continue
        atm_ids = [r for r in route if r > 0]
        load    = sum(demands[i-1] for i in atm_ids)
        cap     = network.vehicles[k].capacity
        vehicle_labels.append(f"Araç {k+1}\n({len(atm_ids)} ATM)")
        loads.append(load / 1000)
        capacities.append(cap / 1000)

    x_pos = np.arange(len(vehicle_labels))
    ax2.bar(x_pos, capacities, color='#334455', alpha=0.6,
            label='Kapasite (500k TL)', width=0.5)
    ax2.bar(x_pos, loads, color='#4ecdc4', alpha=0.85,
            label='Gercek Yuk', width=0.5)

    for xi, (l, c) in enumerate(zip(loads, capacities)):
        pct = l / c * 100
        ax2.text(xi, l + 2, f'%{pct:.0f}',
                 ha='center', color='white', fontsize=11, fontweight='bold')

    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(vehicle_labels, color='#aaaaaa', fontsize=10)
    ax2.set_ylabel("Nakit Yuku (bin TL)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=9)
    ax2.grid(True, axis='y', alpha=0.12, color='gray', linestyle='--')
    for sp in ax2.spines.values():
        sp.set_edgecolor('#333355')

    plt.tight_layout(pad=2.0)
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"\n  [SAVED] Rota haritasi: {save_path}")


# ─────────────────────────────────────────────
# 6. SONUCLARI KAYDET
# ─────────────────────────────────────────────

def save_results(routes, demands, eval_results, network, base):
    """ASAMA 2c ve ASAMA 3 icin cikti dosyalari."""
    # Rotalar
    route_rows = []
    for k, route in routes.items():
        for pos, node in enumerate(route):
            route_rows.append({
                "vehicle":   k,
                "position":  pos,
                "node":      node,
                "is_depot":  node == 0,
            })
    pd.DataFrame(route_rows).to_csv(
        os.path.join(base, "data_det_routes.csv"), index=False)

    # Deterministik yukleme miktarlari
    load_rows = [{"atm_id": i+1, "det_load_TL": demands[i]}
                 for i in range(len(demands))]
    pd.DataFrame(load_rows).to_csv(
        os.path.join(base, "data_det_loads.csv"), index=False)

    # Stockout analizi
    so = eval_results
    summary = {
        "stockout_rate_pct":      so["stockout_rate"] * 100,
        "scenario_stockout_pct":  so["scenario_stockout"] * 100,
        "total_shortfall_TL":     so["total_shortfall"],
        "avg_shortfall_TL":       so["avg_shortfall"],
        "total_penalty_TL":       so["total_penalty_TL"],
    }
    pd.DataFrame([summary]).to_csv(
        os.path.join(base, "data_det_stockout_summary.csv"), index=False)

    print(f"  [SAVED] Rotalar           : data_det_routes.csv")
    print(f"  [SAVED] Yukleme miktarlari: data_det_loads.csv")
    print(f"  [SAVED] Stockout ozeti    : data_det_stockout_summary.csv")


# ─────────────────────────────────────────────
# 7. ANA AKIS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] ASAMA 2a -- Deterministik CVRP Baseline Basliyor...\n")

    base = os.path.dirname(__file__)

    # Network yukle
    network = create_istanbul_network()
    network.distance_matrix = build_distance_matrix(network)
    network.time_matrix      = build_time_matrix(network.distance_matrix)
    print("  [OK] Network yuklendi.")

    # Tarihsel veri
    demand_df = pd.read_csv(
        os.path.join(base, "data_demand_365.csv"),
        index_col="tarih", parse_dates=True
    )

    # SAA senaryolari (stockout testi icin)
    scenario_matrix = np.load(os.path.join(base, "data_saa_scenarios.npy"))
    print(f"  [OK] SAA senaryolari yuklendi: {scenario_matrix.shape}")

    # Nokta tahmin
    print("\n  [..] Nokta tahmin hesaplaniyor (365-gun ortalama)...")
    demands_det = get_point_estimates(demand_df, network)

    # Model kur
    print("\n  [..] CVRP MIP modeli kuruluyor...")
    prob, x_vars, u_vars, N_all, N_atms, K = build_cvrp_model(
        network, demands_det
    )

    # Coz
    status, elapsed = solve_cvrp(prob, time_limit=TIME_LIMIT_SEC)

    if pulp.value(prob.objective) is None:
        print("\n  [!!] Feasible cozum bulunamadi. Model veya parametreler kontrol edilmeli.")
        sys.exit(1)

    # Rotalari cikar
    routes = extract_routes(x_vars, N_all, N_atms, K, network)

    # Rotalari yazdir
    total_route_cost = print_routes(routes, demands_det, network)

    # Ex-post stockout analizi
    eval_results = evaluate_stockout(
        routes, demands_det, network, scenario_matrix
    )

    # Gorsellestir
    print("\n  [..] Rota haritasi uretiliyor...")
    visualize_routes(routes, demands_det, network)

    # Kaydet
    print("\n  [..] Sonuclar kaydediliyor...")
    save_results(routes, demands_det, eval_results, network, base)

    print("\n[OK] ASAMA 2a tamamlandi.")
    print(f"  Rota maliyeti    : {total_route_cost:,.0f} TL/gun")
    print(f"  Stockout orani   : %{eval_results['stockout_rate']*100:.1f}")
    print(f"  Senaryo riski    : %{eval_results['scenario_stockout']*100:.1f} senaryoda en az 1 stockout")
    print()
    print("  Bir sonraki: ASAMA 3a -- Two-Stage Stochastic VRP (SAA ile MIP)")
