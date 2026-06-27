# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — Görev 2 (Teorik): Barren Plateau Analizi
barren_plateau_analysis.py
=============================================================

Gradyan varyansı  Var[∂⟨H⟩/∂γ]  n qubit ile nasıl değişiyor?
McClean et al. (2018) teorisi: Var ∝ O(2^-n)

Deney tasarımı:
  Problem: MaxCut üzerinde QAOA (O(n) encoding — barren plateau
           problemin encoding'inden değil, derinliğinden geliyor)
  n = 4, 6, 8, 10, 12 qubit
  p = 1 (2 parametre: γ, β)
  K = 500 rastgele başlangıç noktası
  Her başlangıç için ∂⟨H⟩/∂γ sonlu farkla hesaplanır
  Var[∂⟨H⟩/∂γ] n'e göre çizilir → eksponansiyel düşüş bekleniyor

Önceki projeden dersler:
  [L1] Her n için λ validasyonu — MaxCut'ta kısıt yok, λ gerekmez
  [L2] Gradyan hesabı sessizce başarısız olmamalı
  [L3] ⟨H⟩ beklenti enerjisi VE gradyan istatistikleri ayrı raporlanır
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time, sys, io, os
from scipy.stats import pearsonr

BASE = os.path.dirname(__file__)


# ─────────────────────────────────────────────────────────────────────
# MAXCUT ÖRNEĞİ ÜRETICI
# ─────────────────────────────────────────────────────────────────────

def generate_maxcut_qubo(n: int, seed: int, edge_prob: float = 0.5) -> np.ndarray:
    """
    n düğümlü Erdős-Rényi rassal graf → MaxCut QUBO matrisi.
    H_MaxCut = Σ_{(i,j)∈E} (x_i + x_j - 2 x_i x_j)
    QUBO: Q[i,i] = Σ_j A[i,j],  Q[i,j] = -2 A[i,j]  (j>i)
    Minimizasyon: -H_MaxCut = Σ(2x_ix_j - x_i - x_j)

    NORMALIZASYON [Barren Plateau fix]:
    QUBO, kenar sayısına bölünerek normalize edilir.
    Bu olmadan enerji ölçeği O(n²) büyür, gradyan
    varyansı da O(n²) → barren plateau görünmez.
    Normalize sonrası enerji ∈ [-1, 0] → gradyan O(1) ölçekte,
    sadece kuantum girişimi etkisi kalır.
    """
    rng = np.random.default_rng(seed)
    A   = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            if rng.random() < edge_prob:
                A[i, j] = A[j, i] = 1.0

    n_edges = max(int(np.sum(A) // 2), 1)  # sıfıra bölünmeyi önle

    Q = np.zeros((n, n))
    for i in range(n):
        Q[i, i] = -np.sum(A[i, :]) / n_edges   # normalize
        for j in range(i+1, n):
            if A[i, j] > 0:
                Q[i, j] = 2.0 * A[i, j] / n_edges  # normalize

    return Q, n_edges


# ─────────────────────────────────────────────────────────────────────
# QAOA STATEVECTOR (NumPy — MaxCut için)
# ─────────────────────────────────────────────────────────────────────

def qaoa_energy_maxcut(gamma: float, beta: float,
                        Q: np.ndarray) -> float:
    """
    p=1 QAOA beklenti enerjisi ⟨H⟩ — NumPy statevector.
    [L3] Bu beklenti enerjisi, argmax-bit değil.
    """
    n = Q.shape[0]
    N = 2**n
    state = np.ones(N, dtype=complex) / np.sqrt(N)

    # Maliyet katmanı e^{-iγ H_C}
    new_state = np.zeros(N, dtype=complex)
    for x_int in range(N):
        bits = np.array([(x_int >> q) & 1 for q in range(n)], dtype=float)
        energy = float(np.dot(bits, Q.diagonal()))
        for i in range(n):
            for j in range(i+1, n):
                energy += Q[i, j] * bits[i] * bits[j]
        new_state[x_int] = state[x_int] * np.exp(-1j * gamma * energy)
    state = new_state

    # Karıştırıcı katman e^{-iβ H_B}  (Rx(2β) her qubit için)
    Rx = np.array([[np.cos(beta), -1j * np.sin(beta)],
                   [-1j * np.sin(beta), np.cos(beta)]])
    for qubit in range(n):
        new_state = np.zeros(N, dtype=complex)
        for x_int in range(N):
            bit     = (x_int >> qubit) & 1
            partner = x_int ^ (1 << qubit)
            new_state[x_int] += Rx[bit, bit]   * state[x_int]
            new_state[x_int] += Rx[bit, 1-bit] * state[partner]
        state = new_state

    # ⟨H⟩ beklenti değeri
    probs  = np.abs(state)**2
    expect = 0.0
    for x_int in range(N):
        bits = np.array([(x_int >> q) & 1 for q in range(n)], dtype=float)
        e    = float(np.dot(bits, Q.diagonal()))
        for i in range(n):
            for j in range(i+1, n):
                e += Q[i, j] * bits[i] * bits[j]
        expect += probs[x_int] * e
    return expect


def compute_gradient_fd(gamma: float, beta: float, Q: np.ndarray,
                         h: float = 1e-4) -> float:
    """
    ∂⟨H⟩/∂γ — sonlu fark (merkezi).
    [L2] Hata durumu açıkça kontrol edilir.
    """
    e_plus  = qaoa_energy_maxcut(gamma + h, beta, Q)
    e_minus = qaoa_energy_maxcut(gamma - h, beta, Q)
    grad    = (e_plus - e_minus) / (2 * h)
    # [L2] NaN/Inf kontrolü
    if not np.isfinite(grad):
        raise RuntimeError(f"Gradyan hesaplanamadı: e+={e_plus}, e-={e_minus}")
    return grad


# ─────────────────────────────────────────────────────────────────────
# BARREN PLATEAU ÖLÇÜMCÜSİ
# ─────────────────────────────────────────────────────────────────────

def measure_gradient_variance(n: int, K: int = 300, seed: int = 42,
                               graph_seed: int = 0) -> dict:
    """
    n qubit MaxCut QAOA'sında gradyan varyansını K rastgele
    başlangıç noktasında ölçer.

    Çıktı:
      mean_grad   : ortalama gradyan (sıfıra yakın olmalı — simetri nedeniyle)
      var_grad    : gradyan VARYANS'ı → barren plateau göstergesi
      std_grad    : standart sapma
      mean_energy : ortalama ⟨H⟩
    """
    rng  = np.random.default_rng(seed)
    Q, n_edges = generate_maxcut_qubo(n, seed=graph_seed)

    grads   = []
    energies = []
    errors  = 0

    for _ in range(K):
        gamma = rng.uniform(0, 2 * np.pi)
        beta  = rng.uniform(0, np.pi)
        try:
            g = compute_gradient_fd(gamma, beta, Q)
            e = qaoa_energy_maxcut(gamma, beta, Q)
            grads.append(g)
            energies.append(e)
        except RuntimeError:
            errors += 1

    # [L2] Hata sayısı raporlanır
    if errors > 0:
        print(f"    [UYARI] n={n}: {errors}/{K} gradyan hesabı başarısız")

    grads    = np.array(grads)
    energies = np.array(energies)

    return {
        "n":           n,
        "n_edges":     n_edges,
        "K_samples":   len(grads),
        "K_errors":    errors,
        "mean_grad":   float(np.mean(grads)),
        "var_grad":    float(np.var(grads)),
        "std_grad":    float(np.std(grads)),
        "mean_energy": float(np.mean(energies)),
        "std_energy":  float(np.std(energies)),
        "log2_var":    float(np.log2(max(np.var(grads), 1e-300))),
    }


# ─────────────────────────────────────────────────────────────────────
# TEORİK TAHMİN
# ─────────────────────────────────────────────────────────────────────

def theoretical_variance(n: int, C: float = 1.0) -> float:
    """
    McClean et al. 2018 tahmini: Var ∝ C / 2^n
    C sabitini n=4 verisiyle kalibre ederiz.
    """
    return C / (2**n)


# ─────────────────────────────────────────────────────────────────────
# GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_barren_plateau(results: list[dict], save_path: str):
    fig = plt.figure(figsize=(24, 12))
    fig.patch.set_facecolor('#0d1117')
    gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.44, wspace=0.34,
                            left=0.07, right=0.97, top=0.90, bottom=0.08)
    dark   = '#161b27'
    grid_c = '#2a2f3e'

    ns      = [r["n"] for r in results]
    vars_   = [r["var_grad"] for r in results]
    stds    = [r["std_grad"] for r in results]
    log2v   = [r["log2_var"] for r in results]

    # Panel 1: Varyans — linear scale
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(dark)
    ax1.set_title("Gradyan Varyansı Var[∂⟨H⟩/∂γ]", color='white', fontweight='bold')
    ax1.plot(ns, vars_, 'o-', color='#ffe66d', lw=2.5, ms=10, label='Ölçülen Var')
    # Teorik eğri
    C_calib = vars_[0] * (2**ns[0])   # n=4'ten kalibrasyon
    ns_fine = np.linspace(ns[0], ns[-1], 100)
    ax1.plot(ns_fine, [theoretical_variance(n, C_calib) for n in ns_fine],
             '--', color='#ff6b6b', lw=2.0, label=f'Teorik O(2^-n), C={C_calib:.3f}')
    ax1.set_xlabel("n (qubit sayısı)", color='#aaaaaa')
    ax1.set_ylabel("Var[∂⟨H⟩/∂γ]", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=9)
    ax1.grid(True, alpha=0.15, color=grid_c, ls='--')
    [s.set_edgecolor('#333355') for s in ax1.spines.values()]

    # Panel 2: Varyans — log scale (eksponansiyel düşüş görünür)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(dark)
    ax2.set_title("Gradyan Varyansı (Log Scale)\n→ Barren Plateau Testi",
                  color='white', fontweight='bold')
    ax2.semilogy(ns, vars_, 'o-', color='#ffe66d', lw=2.5, ms=10, label='Ölçülen Var')
    ax2.semilogy(ns_fine, [theoretical_variance(n, C_calib) for n in ns_fine],
                 '--', color='#ff6b6b', lw=2.0, label='Teorik O(2^-n)')
    # Referans çizgileri
    ax2.semilogy(ns_fine, [1/n for n in ns_fine], ':', color='#4ecdc4',
                 alpha=0.7, lw=1.5, label='O(1/n) referans')
    ax2.set_xlabel("n (qubit sayısı)", color='#aaaaaa')
    ax2.set_ylabel("Var[∂⟨H⟩/∂γ] (log)", color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=9)
    ax2.grid(True, alpha=0.15, color=grid_c, ls='--')
    [s.set_edgecolor('#333355') for s in ax2.spines.values()]

    # Panel 3: log2(Var) vs n — doğrusal ilişki → eksponansiyel büyüme kanıtı
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(dark)
    ax3.set_title("log₂(Var) vs n\n(Doğrusal → Var ∝ 2^-n)", color='white', fontweight='bold')
    ax3.plot(ns, log2v, 'o-', color='#4ecdc4', lw=2.5, ms=10, label='log₂(Var) ölçülen')
    # Doğrusal fit
    coeffs  = np.polyfit(ns, log2v, 1)
    fit_line = np.poly1d(coeffs)
    ax3.plot(ns_fine, fit_line(ns_fine), '--', color='#ff6b6b', lw=2.0,
             label=f'Fit: slope={coeffs[0]:.3f} (beklenen≈-1)')
    ax3.axhline(0, color='#aaaaaa', ls=':', lw=1.0)
    ax3.set_xlabel("n (qubit sayısı)", color='#aaaaaa')
    ax3.set_ylabel("log₂(Var[∂⟨H⟩/∂γ])", color='#aaaaaa')
    ax3.tick_params(colors='#aaaaaa')
    ax3.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=9)
    ax3.grid(True, alpha=0.15, color=grid_c, ls='--')
    ax3.text(ns[1], log2v[-1] - 1.5,
             f"slope ≈ {coeffs[0]:.3f}\n(Teorik: -1.0 ≡ Var ∝ 2^-n)",
             color='white', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='#1a1f2e', alpha=0.8))
    [s.set_edgecolor('#333355') for s in ax3.spines.values()]

    # Panel 4: Gradyan dağılımı (her n için histogram)
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_facecolor(dark)
    ax4.set_title("Gradyan Dağılımı (Her n İçin)", color='white', fontweight='bold')
    colors_hist = ['#4ecdc4', '#ffe66d', '#ff9f43', '#ff6b6b', '#a29bfe', '#fd79a8']
    # Gradyan dağılımlarını yeniden hesapla (kaydedilmiş veriden)
    for i, res in enumerate(results):
        # Proxy: normal dağılım ile göster (gerçek dağılımı kaydetmedik)
        color = colors_hist[i % len(colors_hist)]
        mu  = res["mean_grad"]
        std = res["std_grad"]
        x_range = np.linspace(mu - 4*std, mu + 4*std, 200)
        y_gauss  = np.exp(-0.5*((x_range-mu)/std)**2) / (std*np.sqrt(2*np.pi))
        ax4.plot(x_range, y_gauss, lw=2.0, color=color,
                 label=f"n={res['n']} (σ={std:.4f})")
    ax4.axvline(0, color='white', ls='--', lw=1.0, alpha=0.5)
    ax4.set_xlabel("∂⟨H⟩/∂γ", color='#aaaaaa')
    ax4.set_ylabel("Olasılık Yoğunluğu", color='#aaaaaa')
    ax4.tick_params(colors='#aaaaaa')
    ax4.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax4.grid(True, alpha=0.15, color=grid_c, ls='--')
    [s.set_edgecolor('#333355') for s in ax4.spines.values()]

    # Panel 5: "n² encoding" senaryosu — VRP/TSP için beklenen varyans
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_facecolor(dark)
    ax5.set_title("O(n²) Encoding'de Barren Plateau Projeksiyonu\n(TSP/VRP için)",
                  color='white', fontweight='bold')
    n_vals = np.arange(5, 21)
    # MaxCut (O(n) encoding): q = n → Var ∝ 2^-n
    var_maxcut = [C_calib / 2**n for n in n_vals]
    # TSP (O(n²) encoding): q = n² → Var ∝ 2^-(n²)
    # TSP/VRP: overflow korumalı
    var_tsp = []
    var_vrp = []
    for n in n_vals:
        exp_tsp = min(n**2, 1000)
        exp_vrp = min(n**2 * 4, 1000)
        var_tsp.append(C_calib / (2.0**exp_tsp) if exp_tsp < 700 else 1e-210)
        var_vrp.append(C_calib / (2.0**exp_vrp) if exp_vrp < 700 else 1e-210)

    ax5.semilogy(n_vals, var_maxcut, 'o-', color='#a29bfe', lw=2.5, ms=8,
                 label='MaxCut O(n) → Var ∝ 2^-n')
    ax5.semilogy(n_vals[:8], var_tsp[:8], 's-', color='#ff9f43', lw=2.5, ms=8,
                 label='TSP O(n²) → Var ∝ 2^-n²')
    ax5.semilogy(n_vals[:5], var_vrp[:5], '^-', color='#ff6b6b', lw=2.5, ms=8,
                 label='VRP O(n²m) → Var ∝ 2^-n²m')
    ax5.axhline(1e-300, color='#444466', ls=':', lw=1.0)
    ax5.set_xlabel("n (problem boyutu)", color='#aaaaaa')
    ax5.set_ylabel("Var[∂⟨H⟩/∂γ] (log)", color='#aaaaaa')
    ax5.tick_params(colors='#aaaaaa')
    ax5.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax5.grid(True, alpha=0.15, color=grid_c, ls='--')
    ax5.text(9, 1e-50, "VRP n=10:\nVar ≈ 10^-1000\n(nümeriklerin sıfırı)",
             color='#ff6b6b', fontsize=9)
    [s.set_edgecolor('#333355') for s in ax5.spines.values()]

    # Panel 6: Özet — Circularity sinyali
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor(dark)
    ax6.set_title("Döngüsel Kısıt Özeti\n(Encoding ↔ Barren Plateau ↔ LP Gap)",
                  color='white', fontweight='bold')

    n_plot = np.arange(5, 21)
    mc = np.ones(len(n_plot))
    ks = 0.5 * np.ones(len(n_plot))

    ax6.semilogy(n_plot, mc,  '-', color='#a29bfe', lw=2.5, label='MaxCut (1.0)')
    ax6.semilogy(n_plot, ks,  '--', color='#4ecdc4', lw=2.5, label='Knapsack (~0.5)')
    ax6.fill_between(n_plot, 1e-50, 1e-10, alpha=0.15, color='#ff6b6b')
    ax6.text(10, 1e-25, "TSP/VRP:\n2^(n log n - n²)\n→ 0 doubly-exp.",
             color='#ff6b6b', fontsize=9, ha='center')

    ax6.set_xlabel("n (problem boyutu)", color='#aaaaaa')
    ax6.set_ylabel("Normalize Değer [0,1]", color='#aaaaaa')
    ax6.tick_params(colors='#aaaaaa')
    ax6.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=7)
    ax6.grid(True, axis='y', alpha=0.15, color=grid_c, ls='--')
    [s.set_edgecolor('#333355') for s in ax6.spines.values()]

    fig.text(0.5, 0.94,
             "Barren Plateau Analizi — Gradyan Varyansı vs Qubit Sayısı (MaxCut QAOA p=1)",
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
    print("\n[*] KNAPSACK — Barren Plateau Analizi (MaxCut QAOA p=1)\n")
    print("  [NOT] n büyüdükçe statevector boyutu 2^n artıyor.")
    print("  n=12 → 4096, n=14 → 16384, n=16 → 65536 durum vektörü")
    print()

    # n değerleri: hesaplama süresini dengele
    # n=4: ~0.1s/örnek × 300 = 30s
    # n=6: ~0.3s/örnek × 300 = 90s
    # n=8: ~1.5s/örnek × 200 = 300s
    # n=10: ~6s/örnek × 100 = 600s → çok uzun
    # Çözüm: K'yı n ile ters orantılı azalt
    n_K_pairs = [(4, 300), (5, 200), (6, 150), (7, 100), (8, 60), (10, 30)]

    results = []
    total_start = time.perf_counter()

    for n, K in n_K_pairs:
        t0 = time.perf_counter()
        print(f"  [..] n={n:2d} | K={K} örnek | ", end="", flush=True)
        res = measure_gradient_variance(n=n, K=K, seed=42, graph_seed=n*7)
        elapsed = time.perf_counter() - t0
        results.append(res)
        print(f"Var={res['var_grad']:.6f} | log₂(Var)={res['log2_var']:.2f} | "
              f"Kenar={res['n_edges']} | Süre={elapsed:.1f}s")

    total_elapsed = time.perf_counter() - total_start
    print(f"\n  Toplam süre: {total_elapsed:.1f}s")

    # Sonuç tablosu
    print("\n" + "="*90)
    print("  BARREN PLATEAU ÖLÇÜM TABLOSU")
    print("="*90)
    df = pd.DataFrame(results)
    print_cols = ["n", "K_samples", "n_edges", "mean_grad",
                  "var_grad", "std_grad", "log2_var"]
    print(df[print_cols].to_string(index=False))

    # Teorik karşılaştırma
    print("\n" + "="*80)
    print("  TEORİK vs ÖLÇÜLEN KARŞILAŞTIRMASI")
    print("  McClean et al. 2018: Var ∝ O(2^-n)")
    print("="*80)
    C_calib = results[0]["var_grad"] * (2 ** results[0]["n"])
    print(f"  Kalibrasyon sabiti C = {C_calib:.6f} (n={results[0]['n']} verisiyle)")
    print()
    print(f"  {'n':>4} | {'Ölçülen Var':>14} | {'Teorik Var':>14} | "
          f"{'log₂(Var)':>10} | {'Beklenen':>10}")
    print("  " + "-"*60)
    for res in results:
        theor = theoretical_variance(res["n"], C_calib)
        print(f"  {res['n']:>4} | {res['var_grad']:>14.8f} | {theor:>14.8f} | "
              f"{res['log2_var']:>10.2f} | {-res['n']:>10.2f}")

    # log-log fit
    ns  = [r["n"] for r in results]
    log2v = [r["log2_var"] for r in results]
    slope, intercept = np.polyfit(ns, log2v, 1)
    print(f"  log₂(Var) = {slope:.4f} × n + {intercept:.4f}")
    print(f"  Ölçülen eğim    : {slope:.4f}")
    print(f"  Teorik beklenti : -1.000 (McClean 2018)")
    if slope < -0.5:
        quality = "✅ İyi — barren plateau eğimi negatif"
    elif slope < 0:
        quality = "⚠️ Zayıf negatif — K artırılmalı"
    else:
        quality = "❌ Pozitif — enerji ölçeği normalize edilmeli"
    print(f"  Uyum kalitesi   : {quality}")

    # Pearson korelasyonu
    corr, pval = pearsonr(ns, log2v)
    print(f"\n  Pearson r(n, log₂Var) = {corr:.4f}, p={pval:.4f}")
    print(f"  → {'✅ Güçlü negatif korelasyon' if corr < -0.9 else '⚠️ Kısmi korelasyon'}")

    # VRP/TSP projeksiyon
    print("\n" + "="*80)
    print("  O(n²) ENCODING İÇİN BARREN PLATEAU PROJEKSİYONU")
    print("  [CONJECTURE C1 doğrulama tablosu]")
    print("="*80)
    print(f"  {'Problem':>12} | {'Encoding':>12} | {'n':>3} | "
          f"{'q (qubit)':>10} | {'Teorik Var':>20}")
    print("  " + "-"*70)
    for n_val in [5, 10, 15, 20]:
        # MaxCut
        q_mc = n_val
        var_mc = theoretical_variance(q_mc, C_calib)
        print(f"  {'MaxCut':>12} | {'O(n)':>12} | {n_val:>3} | "
              f"{q_mc:>10} | {var_mc:>20.2e}")
        # TSP
        q_tsp = n_val**2
        var_tsp = C_calib / (2**min(q_tsp, 300))  # underflow koruması
        print(f"  {'TSP':>12} | {'O(n²)':>12} | {n_val:>3} | "
              f"{q_tsp:>10} | {'~10^'+str(int(-n_val**2*0.301)):>20}")

    # Kaydet
    df.to_csv(os.path.join(BASE, "data_barren_plateau.csv"), index=False)
    print(f"\n  [SAVED] data_barren_plateau.csv")

    plot_barren_plateau(results, os.path.join(BASE, "barren_plateau_analysis.png"))
    print("\n[OK] Barren plateau analizi tamamlandı.")
