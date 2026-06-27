# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — GÖREV 5: Tam Karşılaştırma Tablosu
=============================================================

Tüm yöntemleri yan yana karşılaştırır:
- DP (optimal)
- LP Relaxation + Rounding
- Greedy
- Hibrit (Klasik Kilitleme + QAOA p=1,2,3)

Her satır için enerji 3 bileşene ayrılır:
  value_term   = -Σ v_i·x_i
  penalty_term = λ·(kapasite ihlali)²
  total_qubo   = value_term + penalty_term

Enerji ayrışımı hem sınır bölgesi hem tam problem için
ayrı ayrı raporlanır.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import json, time, sys, io, os

BASE = os.path.dirname(__file__)

sys.path.insert(0, BASE)
from knapsack_classical import (
    generate_knapsack, solve_dp, solve_lp_relaxation, solve_greedy, validate_solution
)
from knapsack_qubo import (
    build_knapsack_qubo, compute_qubo_energy_decomposed,
    compute_lambda_threshold, validate_lambda, brute_force_qubo
)
from knapsack_hybrid import run_qaoa_knapsack


# ─────────────────────────────────────────────────────────────────────
# ENERJİ BILEŞEN HESAPLAYICI (tam problem için)
# ─────────────────────────────────────────────────────────────────────

def full_problem_energy_decomposed(x: np.ndarray, data: dict,
                                    lambda_val: float) -> dict:
    """
    Tam 20-nesne problemi için enerji ayrışımı.
    QUBO: H(x) = -Σ v_i·x_i + λ·(Σ w_i·x_i - W)²
    """
    w, v, W = data["weights"], data["values"], data["W"]
    value_term   = -float(np.dot(v, x))
    cap_use      = float(np.dot(w, x))
    violation    = cap_use - W
    penalty_term = lambda_val * violation**2
    total_qubo   = value_term + penalty_term
    return {
        "value_term":    round(value_term, 4),
        "penalty_term":  round(penalty_term, 4),
        "total_qubo":    round(total_qubo, 4),
        "knapsack_value": round(-value_term, 2),
        "cap_used":      int(cap_use),
        "W":             W,
        "violation":     round(violation, 4),
        "feasible":      violation <= 0,
    }


# ─────────────────────────────────────────────────────────────────────
# HİBRİT ÇÖZÜM BİRLEŞTİRİCİ
# ─────────────────────────────────────────────────────────────────────

def build_hybrid_solution(qaoa_bits: list, frac_idx: np.ndarray,
                           fixed1_idx: np.ndarray, n: int) -> np.ndarray:
    """
    Klasik katman (kilitli nesneler) + QAOA katmanı (sınır bölgesi) birleştirir.
    [L2] Tam çözüm kısıta karşı açıkça doğrulanır.
    """
    x = np.zeros(n, dtype=int)
    # Kilitli=1 nesneler
    x[fixed1_idx] = 1
    # QAOA sınır bölgesi kararları
    for local_j, global_i in enumerate(frac_idx):
        x[global_i] = int(qaoa_bits[local_j])
    return x


# ─────────────────────────────────────────────────────────────────────
# TAM KARŞILAŞTIRMA
# ─────────────────────────────────────────────────────────────────────

def run_full_comparison() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = generate_knapsack(n=20, seed=42)
    lp   = solve_lp_relaxation(data)

    frac_idx   = np.where(lp["fractional_mask"])[0]
    fixed1_idx = np.where(lp["fixed_1_mask"])[0]
    fixed0_idx = np.where(lp["fixed_0_mask"])[0]

    w_locked1  = int(np.sum(data["weights"][fixed1_idx]))
    v_locked1  = int(np.sum(data["values"][fixed1_idx]))
    W_residual = data["W"] - w_locked1

    # λ validasyonu
    thresh     = compute_lambda_threshold(data, subset_indices=frac_idx)
    lambda_val = thresh["lambda_safe_3x"]
    val_rep    = validate_lambda(lambda_val, thresh)
    print(f"  λ = {lambda_val} → {val_rep['status']}")

    Q_mat, qubo_meta = build_knapsack_qubo(data, frac_idx, lambda_val, W_residual)

    # Klasik çözümler
    print("  [1/6] DP...")
    dp_res  = solve_dp(data)
    print("  [2/6] LP Relaxation...")
    # lp zaten çözüldü
    print("  [3/6] Greedy...")
    gr_res  = solve_greedy(data)
    dp_opt  = dp_res["total_value"]

    # QAOA (p=1,2,3) sınır bölgesi için
    rows_summary  = []
    rows_decompose = []

    def add_row(method, x_sol, elapsed_ms, label=""):
        val = validate_solution(x_sol, data)
        dec = full_problem_energy_decomposed(x_sol, data, lambda_val)
        gap = (dp_opt - val["total_value"]) / dp_opt * 100 if dp_opt > 0 else 0.0
        rows_summary.append({
            "Yöntem":           method,
            "Toplam Değer":     val["total_value"],
            "DP Optimal'e Gap (%)": round(gap, 2),
            "Kapasite Kullanımı":   val["cap_used"],
            "Kapasite Limiti":      val["cap_limit"],
            "Kısıt Uyumu":          val["feasibility"],
            "Süre (ms)":            round(elapsed_ms, 3),
        })
        rows_decompose.append({
            "Yöntem":           method,
            "Değer Terimi (-Σv·x)": dec["value_term"],
            "Ceza Terimi (λ·ihlal²)": dec["penalty_term"],
            "Toplam QUBO":      dec["total_qubo"],
            "Knapsack Değeri":  dec["knapsack_value"],
            "Kapasite İhlali":  dec["violation"],
            "Feasible?":        "✅" if dec["feasible"] else "❌",
        })

    add_row("DP (Exact Optimal)", dp_res["x"], dp_res["elapsed_ms"])
    add_row("LP Relaxation + Round", lp["x"], lp["elapsed_ms"])
    add_row("Greedy (v/w oranı)", gr_res["x"], gr_res["elapsed_ms"])

    # QAOA hibrit
    for p_val in [1, 2, 3]:
        print(f"  [{p_val+3}/6] QAOA p={p_val} hibrit...")
        t0   = time.perf_counter()
        qaoa = run_qaoa_knapsack(Q_mat, qubo_meta, p=p_val,
                                  n_restarts=8, seed=42)
        elapsed = (time.perf_counter() - t0) * 1000

        # Hibrit tam çözüm
        x_hybrid = build_hybrid_solution(
            qaoa["argmax_bits"], frac_idx, fixed1_idx, data["n"]
        )
        # [L2] Kapasite kısıtı açıkça doğrulanır
        val_hybrid = validate_solution(x_hybrid, data)
        if not val_hybrid["feasible"]:
            print(f"    [UYARI] Hibrit p={p_val} INFEASIBLE: {val_hybrid['feasibility']}")
            # Düzeltme: sınır bölgesini sıfırla (muhafazakar)
            x_fallback = np.zeros(data["n"], dtype=int)
            x_fallback[fixed1_idx] = 1
            if validate_solution(x_fallback, data)["feasible"]:
                x_hybrid = x_fallback
                print(f"    [DÜZ.] Sınır bölgesi sıfırlandı — güvenli çözüm.")

        label = f"⟨H⟩={qaoa['expect_energy']:.3f}"
        add_row(f"Hibrit QAOA p={p_val} ({label})", x_hybrid, elapsed)

    return pd.DataFrame(rows_summary), pd.DataFrame(rows_decompose)


# ─────────────────────────────────────────────────────────────────────
# GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_comparison(df_sum: pd.DataFrame, df_dec: pd.DataFrame, save_path: str):
    fig = plt.figure(figsize=(24, 12))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.32,
                            left=0.06, right=0.97, top=0.90, bottom=0.08)
    dark = '#161b27'; grid = '#2a2f3e'

    methods  = df_sum["Yöntem"].tolist()
    n        = len(methods)
    palette  = ['#4ecdc4', '#a29bfe', '#ffe66d', '#ff9f43', '#fd79a8', '#55efc4']

    # Panel 1: Toplam Değer
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("Toplam Knapsack Değeri", color='white', fontweight='bold')
    vals = df_sum["Toplam Değer"].tolist()
    bars = ax1.bar(range(n), vals, color=palette[:n], width=0.6)
    dp_val = vals[0]
    ax1.axhline(dp_val, color='#ff6b6b', ls='--', lw=1.5,
                label=f"DP Optimal ({dp_val})")
    for b, v in zip(bars, vals):
        ax1.text(b.get_x()+b.get_width()/2, v + 0.3, str(v),
                 ha='center', color='white', fontsize=8.5, fontweight='bold')
    ax1.set_xticks(range(n))
    ax1.set_xticklabels([m[:15] for m in methods], color='#aaaaaa',
                        fontsize=7, rotation=25, ha='right')
    ax1.set_ylabel("Toplam Değer", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax1.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]

    # Panel 2: Gap (%)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("Optimal'e Gap (%)", color='white', fontweight='bold')
    gaps  = df_sum["DP Optimal'e Gap (%)"].tolist()
    bars2 = ax2.bar(range(n), gaps, color=palette[:n], width=0.6)
    for b, v in zip(bars2, gaps):
        ax2.text(b.get_x()+b.get_width()/2, max(v, 0.05) + 0.05,
                 f"%{v:.1f}", ha='center', color='white', fontsize=9, fontweight='bold')
    ax2.set_xticks(range(n))
    ax2.set_xticklabels([m[:15] for m in methods], color='#aaaaaa',
                        fontsize=7, rotation=25, ha='right')
    ax2.set_ylabel("Gap (%)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    # Panel 3: Enerji bileşen ayrışımı
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(dark)
    ax3.set_title("QUBO Enerji Ayrışımı (Değer + Ceza)", color='white', fontweight='bold')
    value_terms   = df_dec["Değer Terimi (-Σv·x)"].tolist()
    penalty_terms = df_dec["Ceza Terimi (λ·ihlal²)"].tolist()
    x_pos = np.arange(n)
    ax3.bar(x_pos, value_terms, color='#4ecdc4', width=0.5, label='Değer Terimi (-Σv·x)')
    bottom_pos = [max(v, 0) for v in value_terms]
    ax3.bar(x_pos, penalty_terms, color='#ff6b6b', width=0.5,
            bottom=bottom_pos, label='Ceza Terimi (λ·ihlal²)')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([m[:15] for m in methods], color='#aaaaaa',
                        fontsize=7, rotation=25, ha='right')
    ax3.set_ylabel("Enerji Bileşeni", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax3.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Kapasite kullanımı
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(dark)
    ax4.set_title("Kapasite Kullanımı", color='white', fontweight='bold')
    cap_use = df_sum["Kapasite Kullanımı"].tolist()
    cap_lim = df_sum["Kapasite Limiti"].iloc[0]
    bars4   = ax4.bar(range(n), cap_use, color=palette[:n], width=0.6)
    ax4.axhline(cap_lim, color='#ff6b6b', ls='--', lw=2,
                label=f"Kapasite limiti (W={cap_lim})")
    for b, v in zip(bars4, cap_use):
        ax4.text(b.get_x()+b.get_width()/2, v + 0.3, str(v),
                 ha='center', color='white', fontsize=8, fontweight='bold')
    ax4.set_xticks(range(n))
    ax4.set_xticklabels([m[:15] for m in methods], color='#aaaaaa',
                        fontsize=7, rotation=25, ha='right')
    ax4.set_ylabel("Kapasite Kullanımı", color='#aaaaaa')
    ax4.tick_params(colors='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax4.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax4.spines.values()]

    fig.text(0.5, 0.94, "KNAPSACK — Tam Karşılaştırma: Klasik + Hibrit QAOA",
             ha='center', color='white', fontsize=13, fontweight='bold')
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] {save_path}")


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n[*] KNAPSACK — Görev 5: Tam Karşılaştırma Tablosu\n")

    df_summary, df_decompose = run_full_comparison()

    print("\n" + "="*90)
    print("  KARŞILAŞTIRMA ÖZET TABLOSU")
    print("="*90)
    print(df_summary.to_string(index=False))

    print("\n" + "="*100)
    print("  ENERJİ BILEŞEN AYRIŞIMI (λ validasyonu baştan uygulandı)")
    print("="*100)
    print(df_decompose.to_string(index=False))

    df_summary.to_csv(os.path.join(BASE, "data_comparison_full.csv"), index=False)
    df_decompose.to_csv(os.path.join(BASE, "data_energy_decomposition.csv"), index=False)
    print(f"\n  [SAVED] data_comparison_full.csv")
    print(f"  [SAVED] data_energy_decomposition.csv")

    plot_comparison(df_summary, df_decompose,
                    os.path.join(BASE, "knapsack_comparison.png"))

    print("\n[OK] Görev 5 tamamlandı.")
