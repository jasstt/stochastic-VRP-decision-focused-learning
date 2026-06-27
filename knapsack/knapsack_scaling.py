# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — GÖREV 6: Ölçekleme Analizi
=============================================================

n'i kademeli artır: 10 → 20 → 50 → 100
Her n için:
  - Sınır bölgesi boyutu (LP fraksiyonel nesneler)
  - QUBO qubit sayısı
  - Azure Quantum kaynak tahmini (analitik model)
  - NISQ uygulanabilirliği
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time, sys, io, os

BASE = os.path.dirname(__file__)

sys.path.insert(0, BASE)
from knapsack_classical import generate_knapsack, solve_lp_relaxation
from knapsack_qubo import compute_lambda_threshold


# ─────────────────────────────────────────────────────────────────────
# KAYNAK TAHMİN MODELİ
# ─────────────────────────────────────────────────────────────────────

def estimate_resources(m_boundary: int, n_total: int,
                        p_qaoa: int = 3, t_gate_ns: float = 100.0) -> dict:
    """
    m_boundary qubit için QAOA kaynak tahmini.

    Formüller (phase2e'den alındı, knapsack için uyarlandı):
      - T-gate/katman: m*(m+1)/2 terim × 10 T-gate/Rz
      - Toplam T-gate: p × katman_T_gate
      - Mantıksal qubit: m_boundary (QUBO boyutu)
      - Fiziksel qubit: m × (2d²-1) surface code d=15
      - Runtime: Toplam_T × t_gate_ns
    """
    d_surface  = 15
    logical_q  = m_boundary
    physical_q = logical_q * (2 * d_surface**2 - 1)

    # QUBO çapraz terim sayısı: m*(m-1)/2
    n_cross_terms  = m_boundary * (m_boundary - 1) // 2
    t_gates_layer  = (m_boundary + n_cross_terms) * 10    # Rz→10 T-gate
    total_t_gates  = t_gates_layer * p_qaoa

    runtime_s = total_t_gates * t_gate_ns / 1e9
    runtime_h = runtime_s / 3600

    # DP için klasik referans: O(n × W) ≈ O(n^2 × 0.6 × n_w_range)
    # yaklaşık: n_total × (n_total * 5) = 5n²
    dp_ops_estimate = n_total * (n_total * 5)
    dp_time_ms = dp_ops_estimate * 1e-7   # ~100ns/op

    # NISQ uygulanabilirliği
    if logical_q <= 50:
        nisq_status = "✅ NISQ mevcut (2024)"
    elif logical_q <= 200:
        nisq_status = "⚠️ NISQ sınırında (~2026)"
    elif logical_q <= 1000:
        nisq_status = "⏳ Erken FT (~2028-2030)"
    elif logical_q <= 10000:
        nisq_status = "⏳ Gelişmiş FT (~2030-2035)"
    else:
        nisq_status = "❌ Fiziksel sınır aşıldı (2035+)"

    def _fmt(s):
        if s < 1e-3: return f"{s*1e6:.0f} µs"
        if s < 1:    return f"{s*1e3:.0f} ms"
        if s < 60:   return f"{s:.1f} sn"
        if s < 3600: return f"{s/60:.1f} dk"
        if s < 86400: return f"{s/3600:.1f} sa"
        return f"{s/86400:.1f} gün"

    return {
        "n_total":        n_total,
        "m_boundary":     m_boundary,
        "logical_qubits": logical_q,
        "physical_qubits": physical_q,
        "total_t_gates":  total_t_gates,
        "qaoa_runtime":   _fmt(runtime_s),
        "dp_runtime":     _fmt(dp_time_ms / 1000),
        "nisq_status":    nisq_status,
    }


# ─────────────────────────────────────────────────────────────────────
# ÖLÇEKLEME DÖNGÜSÜ
# ─────────────────────────────────────────────────────────────────────

def run_scaling_analysis(n_list: list[int], seed: int = 42,
                          p_qaoa: int = 3) -> pd.DataFrame:
    rows = []
    for n in n_list:
        print(f"  n={n:3d} | ", end="", flush=True)
        t0   = time.perf_counter()
        data = generate_knapsack(n=n, seed=seed)
        lp   = solve_lp_relaxation(data)
        elapsed_lp = (time.perf_counter() - t0) * 1000

        frac_idx  = np.where(lp["fractional_mask"])[0]
        fixed1_idx = np.where(lp["fixed_1_mask"])[0]
        m_boundary = len(frac_idx)

        # λ eşiği
        if m_boundary > 0:
            thresh = compute_lambda_threshold(data, subset_indices=frac_idx)
            lambda_min = thresh["lambda_min_required"]
            lambda_safe = thresh["lambda_safe_3x"]
        else:
            lambda_min = lambda_safe = 0.0

        # Kaynak tahmini
        res = estimate_resources(m_boundary, n, p_qaoa)

        # DP referans süresi (gerçek ölçüm)
        from knapsack_classical import solve_dp
        t_dp = time.perf_counter()
        dp   = solve_dp(data)
        dp_ms = (time.perf_counter() - t_dp) * 1000

        print(f"sınır={m_boundary} nesne | λ_min={lambda_min:.2f} | "
              f"qubit={m_boundary} mantıksal / {res['physical_qubits']:,} fiziksel | "
              f"{res['nisq_status']}")

        rows.append({
            "n (Toplam Nesne)":      n,
            "W (Kapasite)":          data["W"],
            "Sınır Bölgesi (m)":    m_boundary,
            "Kilitli=1":             int(lp["fixed_1_mask"].sum()),
            "Kilitli=0":             int(lp["fixed_0_mask"].sum()),
            "λ min. eşik":          round(lambda_min, 3),
            "λ güvenli (3×)":       round(lambda_safe, 3),
            "Mantıksal Qubit":      res["logical_qubits"],
            "Fiziksel Qubit":       f"{res['physical_qubits']:,}",
            "Toplam T-Gate":        f"{res['total_t_gates']:,}",
            "QAOA Runtime (FT)":   res["qaoa_runtime"],
            "DP Runtime (klasik)": f"{dp_ms:.2f} ms",
            "NISQ Durumu":         res["nisq_status"],
            "DP Optimal Değer":    dp["total_value"],
        })

    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────
# GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_scaling(df: pd.DataFrame, save_path: str):
    fig = plt.figure(figsize=(22, 12))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.40, wspace=0.32,
                            left=0.07, right=0.97, top=0.90, bottom=0.08)
    dark = '#161b27'; grid = '#2a2f3e'

    n_vals   = df["n (Toplam Nesne)"].tolist()
    boundary = df["Sınır Bölgesi (m)"].tolist()
    locked1  = df["Kilitli=1"].tolist()
    locked0  = df["Kilitli=0"].tolist()
    phys_q   = df["Fiziksel Qubit"].apply(lambda x: int(x.replace(",",""))).tolist()
    log_q    = df["Mantıksal Qubit"].tolist()

    # Panel 1: Sınır bölgesi büyüklüğü
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("LP Sınır Bölgesi Büyüklüğü vs n", color='white', fontweight='bold')
    ax1.plot(n_vals, boundary, 'o-', color='#ffe66d', lw=2.5, ms=10, label='Sınır (fraksiyonel)')
    ax1.plot(n_vals, locked1,  's-', color='#4ecdc4', lw=2.0, ms=8, label='Kilitli=1')
    ax1.plot(n_vals, locked0,  '^-', color='#ff9f43', lw=2.0, ms=8, label='Kilitli=0')
    ax1.set_xlabel("n (Toplam Nesne)", color='#aaaaaa')
    ax1.set_ylabel("Nesne Sayısı", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax1.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]

    # Panel 2: Sınır oranı (%)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("Sınır Bölgesi Oranı (%)", color='white', fontweight='bold')
    ratio = [b/n*100 for b, n in zip(boundary, n_vals)]
    ax2.bar(n_vals, ratio, color='#ffe66d', width=[n_vals[i]//6 for i in range(len(n_vals))])
    for x, y in zip(n_vals, ratio):
        ax2.text(x, y + 0.3, f"%{y:.0f}", ha='center', color='white', fontsize=9)
    ax2.set_xlabel("n", color='#aaaaaa')
    ax2.set_ylabel("Sınır/Toplam (%)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    # Panel 3: Mantıksal qubit (linear)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(dark)
    ax3.set_title("Mantıksal Qubit (QUBO boyutu)", color='white', fontweight='bold')
    ax3.plot(n_vals, log_q, 'o-', color='#4ecdc4', lw=2.5, ms=10)
    ax3.axhline(50,  color='#4ecdc4', ls='--', lw=1.2, alpha=0.6, label='NISQ ~2024 sınır')
    ax3.axhline(1000, color='#ffe66d', ls='--', lw=1.2, alpha=0.6, label='FT 2028-2030')
    ax3.set_xlabel("n", color='#aaaaaa')
    ax3.set_ylabel("Mantıksal Qubit", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax3.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Fiziksel qubit (log)
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_facecolor(dark)
    ax4.set_title("Fiziksel Qubit (log, d=15 surface code)", color='white', fontweight='bold')
    ax4.semilogy(n_vals, phys_q, 's-', color='#ff9f43', lw=2.5, ms=10)
    ax4.axhline(1_000_000, color='#ff6b6b', ls='--', lw=1.5, label='1M qubit hedef')
    ax4.set_xlabel("n", color='#aaaaaa')
    ax4.set_ylabel("Fiziksel Qubit (log)", color='#aaaaaa')
    ax4.tick_params(colors='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax4.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax4.spines.values()]

    # Panel 5: λ eşiği ölçeklemesi
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_facecolor(dark)
    ax5.set_title("λ Min. Eşiği vs n", color='white', fontweight='bold')
    lam_min  = df["λ min. eşik"].tolist()
    lam_safe = df["λ güvenli (3×)"].tolist()
    ax5.plot(n_vals, lam_min,  'o-', color='#4ecdc4', lw=2.0, ms=8, label='λ minimum')
    ax5.plot(n_vals, lam_safe, 's-', color='#ffe66d', lw=2.0, ms=8, label='λ güvenli (3×)')
    ax5.set_xlabel("n", color='#aaaaaa')
    ax5.set_ylabel("λ değeri", color='#aaaaaa')
    ax5.tick_params(colors='#aaaaaa')
    ax5.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax5.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax5.spines.values()]

    # Panel 6: NISQ Avantaj Haritası
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor(dark)
    ax6.set_title("Hibrit Avantaj Bölgesi", color='white', fontweight='bold')
    for i, (n, m, lq) in enumerate(zip(n_vals, boundary, log_q)):
        if lq <= 50:   color = '#4ecdc4'
        elif lq <= 200: color = '#ffe66d'
        elif lq <= 1000: color = '#ff9f43'
        else:            color = '#ff6b6b'
        ax6.scatter(n, m, s=300, color=color, zorder=5,
                    edgecolors='white', lw=1.5)
        ax6.annotate(f"n={n}\nm={m}", (n, m),
                     textcoords="offset points", xytext=(7, -3),
                     color='white', fontsize=8)
    ax6.set_xlabel("n (Toplam Nesne)", color='#aaaaaa')
    ax6.set_ylabel("m (QUBO Qubit)", color='#aaaaaa')
    ax6.tick_params(colors='#aaaaaa')
    import matplotlib.patches as mpatches
    ax6.legend(handles=[
        mpatches.Patch(color='#4ecdc4', label='NISQ mevcut (2024)'),
        mpatches.Patch(color='#ffe66d', label='NISQ sınırı (~2026)'),
        mpatches.Patch(color='#ff9f43', label='Erken FT (~2030)'),
        mpatches.Patch(color='#ff6b6b', label='Gelişmiş FT (2035+)'),
    ], facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=7)
    ax6.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax6.spines.values()]

    fig.text(0.5, 0.94, "KNAPSACK — Ölçekleme Analizi (n=10→100, p=3 QAOA)",
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
    print("\n[*] KNAPSACK — Görev 6: Ölçekleme Analizi\n")

    n_list = [10, 20, 50, 100]
    df = run_scaling_analysis(n_list, seed=42, p_qaoa=3)

    print("\n" + "="*110)
    print("  ÖLÇEKLEME ANALİZİ TABLOSU")
    print("="*110)
    print(df[["n (Toplam Nesne)", "Sınır Bölgesi (m)", "Kilitli=1",
               "λ min. eşik", "λ güvenli (3×)",
               "Mantıksal Qubit", "Fiziksel Qubit",
               "QAOA Runtime (FT)", "DP Runtime (klasik)", "NISQ Durumu"]].to_string(index=False))

    df.to_csv(os.path.join(BASE, "data_scaling.csv"), index=False)
    print(f"\n  [SAVED] data_scaling.csv")

    plot_scaling(df, os.path.join(BASE, "knapsack_scaling.png"))

    print("\n[OK] Görev 6 tamamlandı.")
