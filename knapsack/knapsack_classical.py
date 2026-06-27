# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — GÖREV 1
Klasik Temel Çizgiler: DP, LP Relaxation, Greedy
=============================================================

Sentetik veri: n=20, seed=42, W=%60 toplam ağırlık
Üretilen veri tüm modüller tarafından paylaşılır.

Önceki projeden alınan dersler, baştan uygulandı:
  [L1] Kısıt her çözüm için açıkça doğrulanır
  [L2] LP INFEASIBLE sessizce geçilmez, kontrol zorunlu
  [L3] Çözüm kalitesi hem değer hem kapasite ile birlikte raporlanır
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import sys, io, os

BASE = os.path.dirname(__file__)

# ─────────────────────────────────────────────────────────────────────
# VERİ ÜRETİMİ (tüm modüller bu fonksiyonu içeri alır)
# ─────────────────────────────────────────────────────────────────────

def generate_knapsack(n: int = 20, seed: int = 42,
                      w_range=(1, 10), v_range=(1, 20),
                      capacity_ratio: float = 0.60) -> dict:
    """
    Tekrar üretilebilir Knapsack örneği.
    W = toplam ağırlığın %60'ı → sınır bölgesini zorlaştırır.
    """
    rng = np.random.default_rng(seed)
    weights = rng.integers(w_range[0], w_range[1] + 1, size=n)
    values  = rng.integers(v_range[0], v_range[1] + 1, size=n)
    W       = int(np.sum(weights) * capacity_ratio)
    return {
        "n": n, "weights": weights, "values": values,
        "W": W, "seed": seed,
        "total_weight": int(np.sum(weights)),
        "total_value":  int(np.sum(values)),
    }


def validate_solution(x: np.ndarray, data: dict) -> dict:
    """
    [L1] Her çözümü kısıta karşı açıkça doğrula.
    Sessiz INFEASIBLE veya görünmez kısıt ihlali engellenir.
    """
    w, v, W = data["weights"], data["values"], data["W"]
    cap_used   = int(np.sum(w * x))
    total_val  = int(np.sum(v * x))
    feasible   = bool(cap_used <= W)
    n_selected = int(np.sum(x))
    return {
        "total_value":  total_val,
        "cap_used":     cap_used,
        "cap_limit":    W,
        "cap_slack":    W - cap_used,
        "n_selected":   n_selected,
        "feasible":     feasible,
        "feasibility":  "✅ FEASIBLE" if feasible else f"❌ INFEASIBLE ({cap_used-W} fazla)",
    }


# ─────────────────────────────────────────────────────────────────────
# YÖNTEM A — DİNAMİK PROGRAMLAMA (exact optimal)
# ─────────────────────────────────────────────────────────────────────

def solve_dp(data: dict) -> dict:
    """
    O(n×W) DP tablosu ile exact çözüm.
    """
    n, w, v, W = data["n"], data["weights"], data["values"], data["W"]
    # dp[i][c] = i nesneden c kapasite ile elde edilebilecek maksimum değer
    dp = np.zeros((n + 1, W + 1), dtype=np.int64)

    t0 = time.perf_counter()
    for i in range(1, n + 1):
        wi, vi = int(w[i-1]), int(v[i-1])
        dp[i, :] = dp[i-1, :]
        if wi <= W:
            dp[i, wi:] = np.maximum(dp[i, wi:],
                                     dp[i-1, :W-wi+1] + vi)
    elapsed = time.perf_counter() - t0

    # Traceback
    x = np.zeros(n, dtype=int)
    cap = W
    for i in range(n, 0, -1):
        if dp[i, cap] != dp[i-1, cap]:
            x[i-1] = 1
            cap -= int(w[i-1])

    check = validate_solution(x, data)
    assert check["feasible"], f"DP BUG: {check['feasibility']}"   # [L1]

    return {
        "method":  "Dinamik Programlama (DP)",
        "x":       x,
        "elapsed_ms": elapsed * 1000,
        "dp_table": dp,
        **check,
    }


# ─────────────────────────────────────────────────────────────────────
# YÖNTEM B — LP RELAXATION + ROUNDING
# ─────────────────────────────────────────────────────────────────────

def solve_lp_relaxation(data: dict) -> dict:
    """
    LP relaxation: x_i ∈ [0,1] (binary yerine sürekli).
    Çözüm: greedy fraksiyonel (analitik — scipy LP ile de yapılabilir).
    Ardından basit rounding uygulanır.

    [L2] LP INFEASIBLE kontrolü açıkça yapılır.
    """
    n, w, v, W = data["n"], data["weights"], data["values"], data["W"]

    t0 = time.perf_counter()
    # LP relaxation: v/w oranına göre sırala, fraksiyonel doldur
    ratio  = v / w
    order  = np.argsort(-ratio)   # azalan sıra
    x_frac = np.zeros(n, dtype=float)
    cap    = W

    for i in order:
        if w[i] <= cap:
            x_frac[i] = 1.0
            cap -= w[i]
        elif cap > 0:
            x_frac[i] = cap / w[i]   # fraksiyonel doldur
            cap = 0
            break

    lp_value = float(np.dot(v, x_frac))

    # Fraksiyonel nesneleri tespit et (sınır bölgesi)
    eps = 1e-9
    fractional_mask = (x_frac > eps) & (x_frac < 1 - eps)
    fixed_0_mask    = x_frac < eps
    fixed_1_mask    = x_frac > 1 - eps

    # Rounding: fraksiyonel nesneyi 0 veya 1'e yuvarlayarak feasibility koru
    x_rounded = x_frac.copy()
    x_rounded[fractional_mask] = 0.0   # muhafazakar rounding

    # [L2] Açık INFEASIBLE kontrolü
    cap_check = int(np.sum(w * np.round(x_rounded)))
    if cap_check > W:
        # Eğer yine de infeasible → en az değerliden çıkar
        for i in order[::-1]:
            if x_rounded[i] == 1:
                x_rounded[i] = 0
                if int(np.sum(w * x_rounded)) <= W:
                    break

    x_int = x_rounded.astype(int)
    elapsed = time.perf_counter() - t0

    check = validate_solution(x_int, data)
    if not check["feasible"]:
        print(f"  [UYARI] LP rounding sonrası INFEASIBLE: {check['feasibility']}")  # [L2]

    return {
        "method":           "LP Relaxation + Rounding",
        "x":                x_int,
        "x_frac":           x_frac,
        "lp_upper_bound":   lp_value,
        "fractional_mask":  fractional_mask,
        "fixed_0_mask":     fixed_0_mask,
        "fixed_1_mask":     fixed_1_mask,
        "n_fractional":     int(fractional_mask.sum()),
        "elapsed_ms":       (time.perf_counter() - t0) * 1000,
        **check,
    }


# ─────────────────────────────────────────────────────────────────────
# YÖNTEM C — GREEDY (değer/ağırlık oranı)
# ─────────────────────────────────────────────────────────────────────

def solve_greedy(data: dict) -> dict:
    """
    Greedy: v/w oranına göre azalan sırada tam nesneleri seç.
    """
    n, w, v, W = data["n"], data["weights"], data["values"], data["W"]
    ratio = v / w
    order = np.argsort(-ratio)
    x = np.zeros(n, dtype=int)
    cap = W

    t0 = time.perf_counter()
    for i in order:
        if w[i] <= cap:
            x[i] = 1
            cap -= w[i]
    elapsed = time.perf_counter() - t0

    check = validate_solution(x, data)
    assert check["feasible"], f"Greedy BUG: {check['feasibility']}"  # [L1]

    return {
        "method":     "Greedy (v/w oranı)",
        "x":          x,
        "elapsed_ms": elapsed * 1000,
        **check,
    }


# ─────────────────────────────────────────────────────────────────────
# GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_classical(data, dp_res, lp_res, greedy_res, save_path):
    fig = plt.figure(figsize=(22, 12))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.32,
                            left=0.06, right=0.97, top=0.90, bottom=0.08)
    dark = '#161b27'; grid = '#2a2f3e'
    w, v, W = data["weights"], data["values"], data["W"]
    n  = data["n"]
    x  = np.arange(n)

    # Panel 1: DP seçimleri
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("DP Seçim (Optimal)", color='white', fontweight='bold')
    colors_dp = ['#4ecdc4' if dp_res["x"][i] else '#444466' for i in range(n)]
    ax1.bar(x, v, color=colors_dp, width=0.7, alpha=0.9)
    ax1.set_xlabel("Nesne İndeksi", color='#aaaaaa')
    ax1.set_ylabel("Değer (v_i)", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]
    import matplotlib.patches as mpatches
    ax1.legend(handles=[mpatches.Patch(color='#4ecdc4', label='Seçildi'),
                         mpatches.Patch(color='#444466', label='Seçilmedi')],
               facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)

    # Panel 2: LP fraksiyonel çözüm
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("LP Relaxation (x_i ∈ [0,1])", color='white', fontweight='bold')
    lp_colors = []
    for i in range(n):
        if lp_res["fixed_1_mask"][i]:   lp_colors.append('#4ecdc4')
        elif lp_res["fixed_0_mask"][i]: lp_colors.append('#444466')
        else:                            lp_colors.append('#ffe66d')
    ax2.bar(x, lp_res["x_frac"], color=lp_colors, width=0.7, alpha=0.9)
    ax2.set_ylabel("LP Çözüm (x_frac)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]
    ax2.legend(handles=[mpatches.Patch(color='#4ecdc4', label='Kilitli=1'),
                         mpatches.Patch(color='#ffe66d', label='Sınır bölgesi'),
                         mpatches.Patch(color='#444466', label='Kilitli=0')],
               facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)

    # Panel 3: v/w oranı + greedy seçim
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(dark)
    ax3.set_title("Greedy (v/w Oranı)", color='white', fontweight='bold')
    ratio  = v / w
    colors_gr = ['#ff9f43' if greedy_res["x"][i] else '#444466' for i in range(n)]
    ax3.bar(x, ratio, color=colors_gr, width=0.7, alpha=0.9)
    ax3.set_ylabel("Oran (v_i / w_i)", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Kapasite karşılaştırması
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_facecolor(dark)
    ax4.set_title("Kapasite Kullanımı", color='white', fontweight='bold')
    methods = ["DP", "LP+Round", "Greedy"]
    caps    = [dp_res["cap_used"], lp_res["cap_used"], greedy_res["cap_used"]]
    bars    = ax4.bar(methods, caps, color=['#4ecdc4','#ffe66d','#ff9f43'], width=0.5)
    ax4.axhline(W, color='#ff6b6b', ls='--', lw=2, label=f"Kapasite sınırı ({W})")
    for b, v_ in zip(bars, caps):
        ax4.text(b.get_x()+b.get_width()/2, v_+1, str(v_),
                 ha='center', color='white', fontsize=10, fontweight='bold')
    ax4.set_ylabel("Kapasite Kullanımı", color='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax4.tick_params(colors='#aaaaaa')
    [s.set_edgecolor('#333355') for s in ax4.spines.values()]

    # Panel 5: Toplam değer karşılaştırması
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_facecolor(dark)
    ax5.set_title("Toplam Değer Karşılaştırması", color='white', fontweight='bold')
    vals = [dp_res["total_value"], lp_res["total_value"], greedy_res["total_value"]]
    bars5 = ax5.bar(methods, vals, color=['#4ecdc4','#ffe66d','#ff9f43'], width=0.5)
    ax5.axhline(dp_res["total_value"], color='#4ecdc4', ls='--', lw=1.5,
                label=f"DP Optimal ({dp_res['total_value']})")
    for b, v_ in zip(bars5, vals):
        gap = (dp_res["total_value"] - v_) / dp_res["total_value"] * 100
        ax5.text(b.get_x()+b.get_width()/2, v_+0.5,
                 f"{v_}\n(gap %{gap:.1f})" if gap > 0 else str(v_),
                 ha='center', color='white', fontsize=9, fontweight='bold')
    ax5.set_ylabel("Toplam Değer", color='#aaaaaa')
    ax5.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax5.tick_params(colors='#aaaaaa')
    [s.set_edgecolor('#333355') for s in ax5.spines.values()]

    # Panel 6: Çözüm süresi
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor(dark)
    ax6.set_title("Çözüm Süresi (ms)", color='white', fontweight='bold')
    times = [dp_res["elapsed_ms"], lp_res["elapsed_ms"], greedy_res["elapsed_ms"]]
    ax6.bar(methods, [max(t, 0.001) for t in times],
            color=['#4ecdc4','#ffe66d','#ff9f43'], width=0.5)
    ax6.set_yscale('log')
    for i, (m, t) in enumerate(zip(methods, times)):
        ax6.text(i, max(t, 0.001)*2, f"{t:.3f} ms",
                 ha='center', color='white', fontsize=9)
    ax6.set_ylabel("Süre (ms, log)", color='#aaaaaa')
    ax6.tick_params(colors='#aaaaaa')
    [s.set_edgecolor('#333355') for s in ax6.spines.values()]

    fig.text(0.5, 0.94, "KNAPSACK — Klasik Yöntemler (n=20, seed=42)",
             ha='center', color='white', fontsize=14, fontweight='bold')
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] {save_path}")


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n[*] KNAPSACK — Görev 1: Klasik Temel Çizgiler\n")

    data = generate_knapsack(n=20, seed=42)
    print(f"  Veri: n={data['n']} | W={data['W']} | "
          f"Toplam ağırlık={data['total_weight']} | "
          f"Kapasite oranı={data['W']/data['total_weight']:.1%}")
    print(f"  Ağırlıklar: {data['weights'].tolist()}")
    print(f"  Değerler  : {data['values'].tolist()}")
    print()

    dp_res     = solve_dp(data)
    lp_res     = solve_lp_relaxation(data)
    greedy_res = solve_greedy(data)

    # Özet tablo
    rows = []
    dp_opt = dp_res["total_value"]
    for res in [dp_res, lp_res, greedy_res]:
        gap = (dp_opt - res["total_value"]) / dp_opt * 100
        rows.append({
            "Yöntem":           res["method"],
            "Toplam Değer":     res["total_value"],
            "Gap (%)":          round(gap, 2),
            "Kapasite Kullanımı": res["cap_used"],
            "Kapasite Limiti":  res["cap_limit"],
            "Kısıt Uyumu":      res["feasibility"],
            "Süre (ms)":        round(res["elapsed_ms"], 4),
        })

    df = pd.DataFrame(rows)
    print("=" * 80)
    print("  SONUÇ TABLOSU — Klasik Yöntemler")
    print("=" * 80)
    print(df.to_string(index=False))

    print(f"\n  LP Sınır Bölgesi: {lp_res['n_fractional']} nesne "
          f"→ QUBO/QAOA katmanına gidecek")
    print(f"  Kilitli=1: {lp_res['fixed_1_mask'].sum()} nesne")
    print(f"  Kilitli=0: {lp_res['fixed_0_mask'].sum()} nesne")
    print()
    fractional_indices = np.where(lp_res["fractional_mask"])[0]
    print(f"  Sınır bölgesi indisleri: {fractional_indices.tolist()}")

    # Kaydet
    df.to_csv(os.path.join(BASE, "data_classical_results.csv"), index=False)
    np.save(os.path.join(BASE, "data_knapsack.npy"),
            np.array([data["weights"], data["values"],
                      [data["W"]], [data["n"]]], dtype=object))

    # Veriyi JSON olarak da kaydet (diğer modüller için)
    import json
    with open(os.path.join(BASE, "data_knapsack.json"), "w") as f:
        json.dump({
            "n": int(data["n"]), "W": int(data["W"]),
            "weights": data["weights"].tolist(),
            "values":  data["values"].tolist(),
            "dp_optimal": int(dp_opt),
            "dp_x":       dp_res["x"].tolist(),
            "lp_x_frac":  lp_res["x_frac"].tolist(),
            "fractional_indices": fractional_indices.tolist(),
            "fixed_1_indices":    np.where(lp_res["fixed_1_mask"])[0].tolist(),
            "fixed_0_indices":    np.where(lp_res["fixed_0_mask"])[0].tolist(),
        }, f, indent=2)
    print(f"  [SAVED] data_knapsack.json")
    print(f"  [SAVED] data_classical_results.csv")

    print("\n  [..] Grafik oluşturuluyor...")
    plot_classical(data, dp_res, lp_res, greedy_res,
                   os.path.join(BASE, "knapsack_classical.png"))

    print("\n[OK] Görev 1 tamamlandı.")
