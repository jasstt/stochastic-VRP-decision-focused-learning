# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP -- AŞAMA 2e
Microsoft Quantum Kaynak Tahmini (Resource Estimation)
=============================================================

Azure Quantum Resource Estimator'ı (ücretsiz, hesap gerekmez)
simüle eden analitik tahmin modeli.

Gerçek kaynak tahmincisi için:
  pip install azure-quantum
  (Azure hesabı olmadan sadece kaynak tahmini yapılabilir)

Bu script, gerçek Azure RE çağrılarını
analitik formüllerle modelleyip aynı tablo/grafikleri üretir.

Formüller kaynağı:
  - Bravyi-Haah T-gate synthesis: ~10 T-gates/Rz
  - Surface code: 1 mantıksal qubit ≈ 1000 fiziksel qubit (d=15)
  - QAOA devresindeki Rz sayısı: n_qubits × p + n_edges × p kapı
  - T-clock: ~100 ns/T-gate (surface code)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = os.path.dirname(__file__)


# ─────────────────────────────────────────────────────────────────────
# 1. KAYNAK TAHMİNİ FORMÜLLERI
# ─────────────────────────────────────────────────────────────────────

def estimate_qubit_count(n_nodes: int, n_vehicles: int) -> dict:
    """
    CVRP → QUBO → QAOA için kubit sayısı tahmini.

    Formül:
      Karar değişkenleri (x_{ijk}):
        n_edges × n_vehicles = (n+1)×n × n_vehicles
      Kapasite slack qubits (MTZ linearizasyonu):
        n_nodes × n_vehicles × ceil(log2(Q/d_min))
        ≈ n_nodes × n_vehicles × 10
      Toplam mantıksal qubit: x_qubits + slack_qubits
      Fiziksel qubit (surface code, d=15):
        ~1000 × mantıksal_qubit
    """
    n_all   = n_nodes + 1
    x_bits  = n_all * n_nodes * n_vehicles    # yönlü kenar × araç
    slack   = n_nodes * n_vehicles * 10       # kapasite encoding
    anc     = x_bits // 10                    # CNOT yardımcı qubits
    logical = x_bits + slack + anc

    # Surface code (code distance d=15, 2d²-1 fiziksel/mantıksal)
    d_surface = 15
    physical  = logical * (2 * d_surface**2 - 1)

    return {
        "x_qubits":       x_bits,
        "slack_qubits":   slack,
        "ancilla_qubits": anc,
        "logical_qubits": logical,
        "physical_qubits": physical,
    }


def estimate_runtime(n_nodes: int, n_vehicles: int, p_qaoa: int = 5,
                     t_gate_ns: float = 100.0) -> dict:
    """
    QAOA çalışma zamanı (fault-tolerant).

    QAOA devresi derinliği:
      - Her katman: (n_edges × ZZ rotasyon) + (n_qubits × Rx) kapıları
      - Her Rz kapısı: ~10 T-gate
      - Toplam T-gate: p × (n_edges + n_qubits) × 10
      - Sıralı T-gate zamanı: T × t_gate_ns
    """
    n_all    = n_nodes + 1
    n_edges  = n_all * n_nodes * n_vehicles
    n_qubits = n_edges + n_nodes * n_vehicles * 10

    t_gates_per_layer = (n_edges + n_qubits) * 10    # Rz → ~10 T-gate
    total_t_gates      = t_gates_per_layer * p_qaoa

    # Paralel T-gate sayısı (yüzey kodunda genellikle sıralı)
    runtime_ns = total_t_gates * t_gate_ns
    runtime_s  = runtime_ns / 1e9
    runtime_h  = runtime_s / 3600

    return {
        "T_gates_total":   total_t_gates,
        "runtime_ns":      runtime_ns,
        "runtime_seconds": runtime_s,
        "runtime_hours":   runtime_h,
    }


def full_resource_table(n_nodes_list: list, n_vehicles_list: list,
                        p_qaoa: int = 5) -> pd.DataFrame:
    """
    Farklı problem boyutları için tam kaynak tahmini tablosu.
    """
    rows = []
    for n_nodes, n_veh in zip(n_nodes_list, n_vehicles_list):
        q = estimate_qubit_count(n_nodes, n_veh)
        r = estimate_runtime(n_nodes, n_veh, p_qaoa)

        # Klasik MILP için referans zaman (deneysel ölçekleme)
        # ~O(n^2.5) CBC ölçeklemesi
        milp_time_s = 0.5 * (n_nodes / 20)**2.5 * 120   # 20 ATM ≈ 120 sn baseline

        rows.append({
            "ATM Sayısı":          n_nodes,
            "Araç Sayısı":         n_veh,
            "Mantıksal Qubit":     f"{q['logical_qubits']:,}",
            "Fiziksel Qubit":      f"{q['physical_qubits']:,}",
            "Toplam T-Gate":       f"{r['T_gates_total']:,}",
            "QAOA Çalışma Süresi": _fmt_time(r['runtime_seconds']),
            "MILP Çalışma Süresi": _fmt_time(milp_time_s),
            "Kuantum Avantajlı?":  _is_advantageous(q['logical_qubits'],
                                                       r['runtime_seconds'],
                                                       milp_time_s),
        })
    return pd.DataFrame(rows)


def _fmt_time(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds*1000:.0f} ms"
    elif seconds < 60:
        return f"{seconds:.1f} sn"
    elif seconds < 3600:
        return f"{seconds/60:.1f} dk"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} sa"
    else:
        return f"{seconds/86400:.1f} gün"


def _is_advantageous(logical_q: int, qaoa_s: float, milp_s: float) -> str:
    """Basit karar: QAOA mevcut donanımda avantajlı mı?"""
    # 2024 itibarıyla en büyük fault-tolerant sistemler ~1000 mantıksal qubit hedefliyor
    if logical_q > 50_000:
        return "❌ Fiziksel sınır (donanım yok)"
    if logical_q > 5_000:
        return "⏳ ~2035+ (gelişmiş FT donanım)"
    if logical_q > 1_000:
        return "⏳ ~2030+ (erken FT donanım)"
    if qaoa_s > milp_s * 10:
        return "⚠️ Mümkün ama daha yavaş"
    return "✅ Potansiyel avantaj"


# ─────────────────────────────────────────────────────────────────────
# 2. ÖLÇEKLEME GRAFİKLERİ
# ─────────────────────────────────────────────────────────────────────

def plot_resource_scaling(n_nodes_list, n_vehicles_list,
                          n_qubits_log, n_phys_log, qaoa_time_s, milp_time_s,
                          save_path: str):

    fig = plt.figure(figsize=(22, 14))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32,
                            left=0.07, right=0.97, top=0.90, bottom=0.07)
    dark  = '#161b27'
    grid  = '#2a2f3e'

    labels = [f"{n}ATM\n{v}araç" for n, v in zip(n_nodes_list, n_vehicles_list)]

    # Panel 1: Mantıksal Qubit Ölçekleme
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("Mantıksal Qubit Sayısı (log)", color='white', fontweight='bold')
    ax1.semilogy(n_nodes_list, n_qubits_log, 'o-', color='#4ecdc4', lw=2.5,
                 ms=9, label='Mantıksal Qubit')
    # Mevcut hedef çizgisi
    ax1.axhline(1000, color='#ffe66d', ls='--', lw=1.5, label='~2030 hedef (~1000)')
    ax1.axhline(100,  color='#a8e6cf', ls='--', lw=1.5, label='~2027 hedef (~100)')
    ax1.set_xticks(n_nodes_list)
    ax1.set_xticklabels(labels, color='#aaaaaa', fontsize=9)
    ax1.set_ylabel("Mantıksal Qubit (log)", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax1.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]

    # Panel 2: Fiziksel Qubit
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("Fiziksel Qubit Sayısı (log, d=15 surface code)", color='white',
                  fontweight='bold')
    ax2.semilogy(n_nodes_list, n_phys_log, 's-', color='#ff9f43', lw=2.5,
                 ms=9, label='Fiziksel Qubit')
    ax2.axhline(1_000_000, color='#ff6b6b', ls='--', lw=1.5, label='1M qubit (uzak hedef)')
    ax2.set_xticks(n_nodes_list)
    ax2.set_xticklabels(labels, color='#aaaaaa', fontsize=9)
    ax2.set_ylabel("Fiziksel Qubit (log)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax2.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    # Panel 3: Çalışma Süresi Karşılaştırması
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(dark)
    ax3.set_title("Çalışma Süresi: MILP vs QAOA (FT) (log)", color='white',
                  fontweight='bold')
    ax3.semilogy(n_nodes_list, milp_time_s, 'o-', color='#4ecdc4', lw=2.5,
                 ms=9, label='MILP (CBC)')
    ax3.semilogy(n_nodes_list, qaoa_time_s, 's-', color='#ffe66d', lw=2.5,
                 ms=9, label='QAOA (FT sim.)')
    ax3.set_xticks(n_nodes_list)
    ax3.set_xticklabels(labels, color='#aaaaaa', fontsize=9)
    ax3.set_ylabel("Süre (saniye, log)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=9)
    ax3.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Kuantum Avantaj Haritası
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(dark)
    ax4.set_title("Kuantum Avantaj Bölgesi", color='white', fontweight='bold')
    for i, (n, v, q_l, q_t, m_t) in enumerate(zip(
            n_nodes_list, n_vehicles_list, n_qubits_log, qaoa_time_s, milp_time_s)):
        color = '#4ecdc4' if q_l < 1000 and q_t < m_t else (
                '#ffe66d' if 1000 <= q_l < 50_000 else '#ff6b6b')
        ax4.scatter(q_l, q_t / max(m_t, 1e-6), s=200, color=color,
                    zorder=5, edgecolors='white', lw=1.5)
        ax4.annotate(f"{n} ATM", (q_l, q_t/max(m_t,1e-6)),
                     textcoords="offset points", xytext=(5,5),
                     color='white', fontsize=9)

    ax4.axhline(1.0, color='#aaaaaa', ls='--', lw=1.5,
                label='QAOA=MILP eşik (oran=1.0)')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlabel("Mantıksal Qubit (log)", color='#aaaaaa')
    ax4.set_ylabel("QAOA/MILP Süre Oranı (log)", color='#aaaaaa')
    ax4.tick_params(colors='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax4.grid(True, alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax4.spines.values()]

    # Renk açıklamaları
    import matplotlib.patches as mpatches
    legend_patches = [
        mpatches.Patch(color='#4ecdc4', label='Potansiyel avantaj (<1000 qubit)'),
        mpatches.Patch(color='#ffe66d', label='Yakın gelecek (2030-2035)'),
        mpatches.Patch(color='#ff6b6b', label='Uzak gelecek (2035+)'),
    ]
    ax4.legend(handles=legend_patches, facecolor=dark, edgecolor='#444466',
               labelcolor='white', fontsize=8, loc='lower right')

    fig.text(0.5, 0.94,
             "AŞAMA 2e — Kuantum Kaynak Tahmini: CVRP Ölçekleme Analizi",
             ha='center', color='white', fontsize=14, fontweight='bold')
    fig.text(0.5, 0.92,
             "Surface code (d=15) + T-gate synthesis varsayımı | QAOA p=5",
             ha='center', color='#8899bb', fontsize=9)

    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] {save_path}")


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[*] AŞAMA 2e — Kuantum Kaynak Tahmini\n")

    n_nodes_list   = [5, 10, 20, 50, 100, 200]
    n_veh_list     = [1,  2,  4,  8,  15,  30]
    P_QAOA         = 5

    # Ölçekleme hesapla
    n_qubits_log = []
    n_phys_log   = []
    qaoa_time_s  = []
    milp_time_s  = []

    for n_nodes, n_veh in zip(n_nodes_list, n_veh_list):
        q = estimate_qubit_count(n_nodes, n_veh)
        r = estimate_runtime(n_nodes, n_veh, P_QAOA)
        milp_t = 0.5 * (n_nodes / 20)**2.5 * 120
        n_qubits_log.append(q["logical_qubits"])
        n_phys_log.append(q["physical_qubits"])
        qaoa_time_s.append(r["runtime_seconds"])
        milp_time_s.append(max(milp_t, 0.01))

    # Tam tablo (sadece ana boyutlar)
    main_nodes = [20, 50, 100, 200]
    main_veh   = [4,   8,  15,  30]
    df_resource = full_resource_table(main_nodes, main_veh, P_QAOA)

    print("="*90)
    print("  KAYNAK TAHMİNİ TABLOSU (p=5 QAOA, Surface Code d=15)")
    print("="*90)
    print(df_resource.to_string(index=False))
    print("="*90)

    df_resource.to_csv(os.path.join(BASE, "data_resource_estimates.csv"), index=False)
    print(f"\n  [SAVED] data_resource_estimates.csv")

    # Görselleştir
    print("\n  [..] Kaynak ölçekleme grafikleri oluşturuluyor...")
    plot_resource_scaling(
        n_nodes_list, n_veh_list,
        n_qubits_log, n_phys_log, qaoa_time_s, milp_time_s,
        save_path=os.path.join(BASE, "phase2e_resource_estimate.png")
    )

    print("\n[OK] AŞAMA 2e tamamlandı.")
    print("     Bir sonraki: AŞAMA 2f — Kuantum Uygulanabilirlik Raporu")
