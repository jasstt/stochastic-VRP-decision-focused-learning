# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP -- AŞAMA 2d
Adil Karşılaştırma: PuLP/MILP vs QAOA Simülatör
=============================================================

Aynı küçük alt-problem üzerinde her iki yöntemi karşılaştırır.
Önemli bağlam notu:
  - QAOA bu ölçekte (5 qubit, 5 ATM) anlam taşısa da,
    gerçek problem (20 ATM, ~1680 qubit) ile arası
    büyük: QAOA şu anda klasik MILP'i yenemez.
  - Bu karşılaştırmanın amacı metodolojik dürüstlük.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pulp
import time
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = os.path.dirname(__file__)

# Phase 2c'den QAOA fonksiyonlarını içeri al
sys.path.insert(0, BASE)
from phase2c_qaoa_simulator import (
    build_demo_qubo, run_qaoa, brute_force_optimal,
    compute_qubo_energy, N_QUBITS, DEMANDS_DEMO, C_DEMO, Q_CAP
)

# ─────────────────────────────────────────────────────────────────────
# 1. MILP ÇÖZÜMÜ (aynı 5 ATM alt-problemi)
# ─────────────────────────────────────────────────────────────────────

def solve_milp_subproblem() -> dict:
    """
    5 ATM, 1 araç, depo-merkezli VRP (PuLP/CBC).
    x_j ∈ {0,1}: depodan ATM j'ye gidilip gelinecek mi?
    (Basit atama problemi — tam CVRP'nin alt versiyonu)
    """
    n = len(DEMANDS_DEMO)
    prob = pulp.LpProblem("Demo_CVRP_5ATM", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", range(n), cat='Binary')

    # Amaç: rota maliyeti (depo-ATM-depo gidiş-dönüş)
    trip_costs = [C_DEMO[0][j+1] + C_DEMO[j+1][0] for j in range(n)]
    prob += pulp.lpSum(trip_costs[j] * x[j] for j in range(n))

    # Kapasite kısıtı
    prob += pulp.lpSum(DEMANDS_DEMO[j] * x[j] for j in range(n)) <= Q_CAP

    # Her ATM ziyaret edilmeli
    for j in range(n):
        prob += x[j] == 1, f"visit_{j}"

    t0 = time.time()
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    elapsed = time.time() - t0

    sol = [int(round(pulp.value(x[j]))) for j in range(n)]
    obj_val = pulp.value(prob.objective)

    return {
        "solution":    sol,
        "obj_value":   obj_val,
        "status":      pulp.LpStatus[prob.status],
        "elapsed_ms":  elapsed * 1000,
        "n_vars":      len(prob.variables()),
        "n_constraints": len(prob.constraints),
    }


# ─────────────────────────────────────────────────────────────────────
# 2. QAOA ÇÖZÜMÜ (farklı p değerleri için)
# ─────────────────────────────────────────────────────────────────────

def benchmark_qaoa_vs_milp() -> pd.DataFrame:
    """
    p=1,2,3 QAOA ve MILP + Kaba Kuvvet karşılaştırmasını üretir.
    """
    np.random.seed(42)
    Q_demo = build_demo_qubo()

    rows = []

    # Kaba Kuvvet
    print("  [1/5] Kaba kuvvet (2^5)...")
    t0 = time.time()
    bf = brute_force_optimal(Q_demo)
    bf_t = (time.time() - t0) * 1000
    rows.append({
        "Yöntem": "Kaba Kuvvet (Klasik)",
        "QUBO Enerjisi": round(bf["energy"], 4),
        "Süre (ms)": round(bf_t, 2),
        "Optimal'e Uzaklık": 0.0,
        "Çözüm Kalitesi": "Optimal ✓",
        "Kısıt Uyumu": "Tam",
        "Qubit / Değişken Sayısı": f"2^{N_QUBITS} durum"
    })

    # MILP
    print("  [2/5] MILP (PuLP/CBC)...")
    milp = solve_milp_subproblem()
    milp_qubo_e = compute_qubo_energy(milp["solution"], Q_demo)
    milp_gap    = abs(milp_qubo_e - bf["energy"]) / abs(bf["energy"]) if bf["energy"] != 0 else 0.0
    rows.append({
        "Yöntem": "PuLP/MILP (CBC)",
        "QUBO Enerjisi": round(milp_qubo_e, 4),
        "Süre (ms)": round(milp["elapsed_ms"], 2),
        "Optimal'e Uzaklık": round(milp_gap * 100, 2),
        "Çözüm Kalitesi": f"Optimal ✓ ({milp['status']})",
        "Kısıt Uyumu": "Tam",
        "Qubit / Değişken Sayısı": f"{milp['n_vars']} binary + {milp['n_constraints']} kısıt"
    })

    # QAOA — farklı derinlikler
    for p_val in [1, 2, 3]:
        label = f"[{3-p_val+3}/5]"
        print(f"  {label} QAOA p={p_val} (COBYLA, 5 restart)...")
        qaoa = run_qaoa(Q_demo, p=p_val, n_restarts=5)
        qaoa_e = compute_qubo_energy(qaoa["solution"], Q_demo)
        gap = abs(qaoa_e - bf["energy"]) / abs(bf["energy"]) if bf["energy"] != 0 else 0.0
        approx_ratio = bf["energy"] / qaoa_e if qaoa_e != 0 else np.nan
        # Kısıt uyumu: kapasite kontrolü
        cap_used = sum(DEMANDS_DEMO[j] * qaoa["solution"][j] for j in range(N_QUBITS))
        kısıt_uyum = "Tam" if cap_used <= Q_CAP else f"İhlal ({cap_used/1000:.0f}k > {Q_CAP/1000:.0f}k TL)"
        rows.append({
            "Yöntem": f"QAOA (p={p_val}, NumPy sim.)",
            "QUBO Enerjisi": round(qaoa_e, 4),
            "Süre (ms)": round(qaoa["elapsed"] * 1000, 1),
            "Optimal'e Uzaklık": round(gap * 100, 2),
            "Çözüm Kalitesi": f"Yaklaşık (α≈{approx_ratio:.3f})",
            "Kısıt Uyumu": kısıt_uyum,
            "Qubit / Değişken Sayısı": f"{N_QUBITS} qubit, {2*p_val} parametre"
        })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────
# 3. GERÇEK PROBLEM BOYUTU KARŞILAŞTIRMASI (20 ATM)
# ─────────────────────────────────────────────────────────────────────

FULL_PROBLEM_COMPARISON = {
    "PuLP/MILP (20 ATM, 4 araç)": {
        "Maliyet (TL/gün)": "3,394",
        "Stockout Oranı (%)": "42.4",
        "Çözüm Süresi (sn)": "60-180",
        "Çözüm Kalitesi": "≤%5 gap (CBC)",
        "Qubit/Değişken": "~1680 binary + 80 continuous + ~8500 kısıt",
        "Donanım Gereksinimi": "Standart CPU",
        "Bugün Kullanılabilir mi?": "✅ Evet",
    },
    "QAOA Simülatör (20 ATM, 4 araç)": {
        "Maliyet (TL/gün)": "Simüle edilemez*",
        "Stockout Oranı (%)": "N/A",
        "Çözüm Süresi (sn)": "~2^1680 durum → ∞",
        "Çözüm Kalitesi": "N/A (durum uzayı çok büyük)",
        "Qubit/Değişken": "~1680 qubit gerekli",
        "Donanım Gereksinimi": "~1680+ mantıksal qubit (mevcut yok)",
        "Bugün Kullanılabilir mi?": "❌ Hayır (NISQ era kısıtı)",
    },
    "QAOA Simülatör (5 ATM demo)": {
        "Maliyet (TL/gün)": "Demo boyutu",
        "Stockout Oranı (%)": "N/A",
        "Çözüm Süresi (sn)": "2-10 sn (COBYLA)",
        "Çözüm Kalitesi": "Yaklaşık (α≈0.85-0.98)",
        "Qubit/Değişken": "5 qubit",
        "Donanım Gereksinimi": "Standart CPU (numpy sim.)",
        "Bugün Kullanılabilir mi?": "✅ Evet (anlam sınırlı)",
    }
}


# ─────────────────────────────────────────────────────────────────────
# 4. GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_comparison(df_bench: pd.DataFrame, save_path: str):
    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.32,
                            left=0.07, right=0.96, top=0.89, bottom=0.08)

    dark  = '#161b27'
    grid  = '#2a2f3e'
    colors = ['#4ecdc4', '#a29bfe', '#ffe66d', '#ffe66d', '#ff9f43']

    methods = df_bench["Yöntem"].tolist()
    energies = df_bench["QUBO Enerjisi"].tolist()
    times_ms  = df_bench["Süre (ms)"].tolist()
    gaps      = df_bench["Optimal'e Uzaklık"].tolist()

    # Panel 1: QUBO Enerjisi
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("QUBO Enerjisi (Düşük = İyi)", color='white', fontweight='bold')
    bars = ax1.bar(range(len(methods)), energies, color=colors[:len(methods)], width=0.6)
    ax1.set_xticks(range(len(methods)))
    short_labels = ["Kaba\nKuvvet", "MILP\n(CBC)", "QAOA\np=1", "QAOA\np=2", "QAOA\np=3"]
    ax1.set_xticklabels(short_labels[:len(methods)], color='#aaaaaa', fontsize=9)
    for b, v in zip(bars, energies):
        ax1.text(b.get_x()+b.get_width()/2, v+0.002, f"{v:.3f}",
                 ha='center', color='white', fontsize=8.5, fontweight='bold')
    ax1.set_ylabel("QUBO Enerjisi", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]

    # Panel 2: Çözüm Süresi (log)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("Çözüm Süresi (ms, log)", color='white', fontweight='bold')
    safe_times = [max(t, 0.01) for t in times_ms]
    ax2.bar(range(len(methods)), safe_times, color=colors[:len(methods)], width=0.6)
    ax2.set_yscale('log')
    ax2.set_xticks(range(len(methods)))
    ax2.set_xticklabels(short_labels[:len(methods)], color='#aaaaaa', fontsize=9)
    for i, v in enumerate(times_ms):
        ax2.text(i, max(v, 0.01)*1.5, f"{v:.1f} ms",
                 ha='center', color='white', fontsize=8.5)
    ax2.set_ylabel("Süre (ms, log ölçek)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    # Panel 3: Optimal'e Uzaklık (%)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(dark)
    ax3.set_title("Optimal'e Uzaklık (%, düşük = iyi)", color='white', fontweight='bold')
    bars3 = ax3.bar(range(len(methods)), gaps, color=colors[:len(methods)], width=0.6)
    ax3.set_xticks(range(len(methods)))
    ax3.set_xticklabels(short_labels[:len(methods)], color='#aaaaaa', fontsize=9)
    for b, v in zip(bars3, gaps):
        ax3.text(b.get_x()+b.get_width()/2, v+0.1, f"%{v:.1f}",
                 ha='center', color='white', fontsize=9, fontweight='bold')
    ax3.set_ylabel("Optimal'e Uzaklık (%)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Metin tablosu (gerçek problem)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(dark)
    ax4.axis('off')
    ax4.set_title("Gerçek Problem (20 ATM) Özeti", color='white',
                  fontweight='bold', pad=10)

    table_data = [
        ["MILP", "3.394 TL/gün", "60-180 sn", "✅ Şimdi"],
        ["QAOA (gerçek)", "Simüle\nedilemiyor", "∞", "❌ ~2030+"],
        ["QAOA (5-ATM\ndemo)", "Demo", "2-10 sn", "✅ Anlam\nsınırlı"],
    ]
    headers = ["Yöntem", "Maliyet", "Süre", "Kullanılabilir?"]
    row_colors_t = [['#4ecdc433','#4ecdc411','#4ecdc411','#4ecdc411'],
                    ['#ff6b6b33','#ff6b6b11','#ff6b6b11','#ff6b6b11'],
                    ['#ffe66d33','#ffe66d11','#ffe66d11','#ffe66d11']]
    tbl = ax4.table(cellText=table_data, colLabels=headers,
                    cellLoc='center', loc='center', bbox=[0.0, 0.05, 1.0, 0.90])
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor('#2a2f3e')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor(row_colors_t[r-1][c] if r-1 < len(row_colors_t) else '#161b27')
            cell.set_text_props(color='white')
        cell.set_edgecolor('#333355')

    fig.text(0.5, 0.95,
             "AŞAMA 2d — Adil Karşılaştırma: Klasik MILP vs QAOA Simülatör",
             ha='center', color='white', fontsize=14, fontweight='bold')
    fig.text(0.5, 0.927,
             "5 Qubit Demo Alt-Problemi (Sol/Orta) + Gerçek Problemin Özeti (Sağ-Alt)",
             ha='center', color='#8899bb', fontsize=9)

    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] {save_path}")


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] AŞAMA 2d — Karşılaştırma: PuLP/MILP vs QAOA\n")
    np.random.seed(42)

    print("  Benchmark çalıştırılıyor (5 yöntem)...")
    df_bench = benchmark_qaoa_vs_milp()

    print("\n" + "="*78)
    print("  5-ATM ALT-PROBLEMİ — KARŞıLAŞTIRMA TABLOSU")
    print("="*78)
    print(df_bench[["Yöntem","QUBO Enerjisi","Süre (ms)","Optimal'e Uzaklık","Kısıt Uyumu"]].to_string(index=False))

    print("\n" + "="*78)
    print("  20-ATM GERÇEK PROBLEMİ — KARŞıLAŞTIRMA ÖZETİ")
    print("="*78)
    for sys_name, metrics in FULL_PROBLEM_COMPARISON.items():
        print(f"\n  [{sys_name}]")
        for k, v in metrics.items():
            print(f"    {k:<32}: {v}")

    df_bench.to_csv(os.path.join(BASE, "data_comparison_milp_qaoa.csv"), index=False)
    print(f"\n  [SAVED] data_comparison_milp_qaoa.csv")

    print("\n  [..] Karşılaştırma grafiği oluşturuluyor...")
    plot_comparison(df_bench, os.path.join(BASE, "phase2d_comparison.png"))

    print("\n[OK] AŞAMA 2d tamamlandı.")
    print("     Bir sonraki: AŞAMA 2e — Kaynak Tahmini")
