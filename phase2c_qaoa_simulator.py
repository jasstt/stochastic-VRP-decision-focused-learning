# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

"""
=============================================================
ARUTE CIT-SVRP -- AŞAMA 2c (Python Tarafı)
QAOA Simülatörü — SciPy + Qiskit Statevector Simülatörü
=============================================================

Bu script, QUBO formülasyonunu klasik bir kuantum devre
simülatörüyle (Qiskit Statevector veya NumPy tabanlı) çalıştırır.
Q# yerine Python tabanında tutuldu çünkü:
  1. .NET kurulumu gerektirmez
  2. Doğrudan NumPy entegrasyonu sağlar
  3. COBYLA parametresi döngüsü daha kolay kurulur

Bu simülatör gerçek kuantum donanımını taklit eder;
gürültü modeli olmadan çalışır (ideal quantum simulator).

Azaltılmış Problem Boyutu:
  Tam problem: 20 ATM × 4 araç → ~1680 qubit (klasik bile simüle edilemez)
  Bu demo:     5 ATM × 2 araç  → 30 qubit (statevector = 2^30 = imkansız)
  QAOA demo:   5 kenar değişkeni → 5 qubit (COBYLA çalışır, anlam sınırlı)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize as scipy_minimize
import time
import sys, io, os
import warnings
warnings.filterwarnings('ignore')

BASE = os.path.dirname(__file__)

# ─────────────────────────────────────────────────────────────────────
# 1. KÜÇÜK QUBO ALT-PROBLEMİ (demo için 5 qubit)
#    5 ATM'nin 1 araçla optimizasyonu: x_ij ∈ {0,1}
#    i: 0=depo, 1..5=ATM;  x_ij=1 ↔ "depodan j'ye git sonra depoya dön"
# ─────────────────────────────────────────────────────────────────────

# Demo maliyet matrisi (normalize, 5 ATM + depo)
C_DEMO = np.array([
    [0.0, 0.60, 0.80, 0.55, 0.70, 0.90],
    [0.60, 0.0, 0.45, 0.70, 0.50, 0.65],
    [0.80, 0.45, 0.0, 0.55, 0.60, 0.40],
    [0.55, 0.70, 0.55, 0.0, 0.35, 0.75],
    [0.70, 0.50, 0.60, 0.35, 0.0, 0.50],
    [0.90, 0.65, 0.40, 0.75, 0.50, 0.0],
])
DEMANDS_DEMO = np.array([50_000, 80_000, 65_000, 45_000, 90_000])  # TL
Q_CAP        = 250_000  # araç kapasitesi (TL)
LAMBDA_V     = 1.0      # ziyaret ceza katsayısı
LAMBDA_C     = 0.5      # kapasite ceza katsayısı
N_QUBITS     = 5        # depodan her ATM'ye gidip gitmeyeceği (tek araç, basit)


def build_demo_qubo() -> np.ndarray:
    """
    5-qubit demo QUBO:
      x_j = 1: araç depodan ATM j'ye gider (j=1..5)
      Maliyet: Σ_j (c_{0j} + c_{j0}) × x_j
      Kapasite: (Σ_j d_j × x_j - Q)²
      Ziyaret:  Σ_j (1-x_j)² — her ATM en az 1 kez
    """
    Q = np.zeros((N_QUBITS, N_QUBITS))
    c_max = C_DEMO.max()

    # Maliyet terimleri (lineer → diyagonal)
    for j in range(N_QUBITS):
        trip_cost = (C_DEMO[0][j+1] + C_DEMO[j+1][0]) / c_max
        Q[j, j] += trip_cost

    # Kapasite penalty: (Σ d_j x_j - Q)^2
    # Genişleme: Σ_j d_j² x_j² + 2Σ_{j<k} d_j d_k x_j x_k - 2Q Σ d_j x_j + Q²
    d_n = DEMANDS_DEMO / Q_CAP   # normalize
    for j in range(N_QUBITS):
        Q[j, j] += LAMBDA_C * (d_n[j]**2 - 2 * d_n[j])
    for j in range(N_QUBITS):
        for k in range(j+1, N_QUBITS):
            Q[j, k] += 2 * LAMBDA_C * d_n[j] * d_n[k]

    # Ziyaret penalty: her ATM ziyaret edilmeli (1-x_j)^2 → -2λx_j + λ
    for j in range(N_QUBITS):
        Q[j, j] -= 2 * LAMBDA_V    # diyagonal: -2λ (lineer terim)
    # +λ sabit terim QUBO matrisine girmez (offset)

    return Q


# ─────────────────────────────────────────────────────────────────────
# 2. NUMPY TABANLI QAOA SİMÜLATÖRÜ
#    (Qiskit kurulu değilse bile çalışır)
# ─────────────────────────────────────────────────────────────────────

def pauli_z_expectation(state: np.ndarray, qubit: int, n: int) -> float:
    """Qubit üzerindeki <Z> beklenti değerini hesaplar."""
    exp_val = 0.0
    for idx in range(2**n):
        bit = (idx >> qubit) & 1
        sign = 1 - 2 * bit    # 0 → +1, 1 → -1
        exp_val += sign * abs(state[idx])**2
    return exp_val


def apply_cost_unitary(state: np.ndarray, Q_mat: np.ndarray,
                        gamma: float, n: int) -> np.ndarray:
    """e^{-iγH_C} operatörünü durum vektörüne uygular."""
    new_state = np.zeros(2**n, dtype=complex)
    for x in range(2**n):
        bits = [(x >> q) & 1 for q in range(n)]
        energy = 0.0
        # Diyagonal terimler
        for i in range(n):
            energy += Q_mat[i, i] * bits[i]
        # Çapraz terimler
        for i in range(n):
            for j in range(i+1, n):
                energy += Q_mat[i, j] * bits[i] * bits[j]
        new_state[x] = state[x] * np.exp(-1j * gamma * energy)
    return new_state


def apply_mixer_unitary(state: np.ndarray, beta: float, n: int) -> np.ndarray:
    """e^{-iβH_B} = ∏_i Rx(2β) operatörünü uygular."""
    Rx = np.array([[np.cos(beta), -1j * np.sin(beta)],
                   [-1j * np.sin(beta), np.cos(beta)]])
    for qubit in range(n):
        new_state = np.zeros(2**n, dtype=complex)
        for x in range(2**n):
            bit = (x >> qubit) & 1
            partner = x ^ (1 << qubit)
            new_state[x] += Rx[bit, bit] * state[x]
            new_state[x] += Rx[bit, 1-bit] * state[partner]
        state = new_state
    return state


def qaoa_energy(params: np.ndarray, Q_mat: np.ndarray, n: int, p: int) -> float:
    """
    p-katmanlı QAOA'nın QUBO enerjisini döndürür.
    params: [γ₁, γ₂, ..., γₚ, β₁, β₂, ..., βₚ]
    """
    gammas = params[:p]
    betas  = params[p:]

    # Başlangıç: |+⟩^⊗n = eşit süperpozisyon
    state = np.ones(2**n, dtype=complex) / np.sqrt(2**n)

    for layer in range(p):
        state = apply_cost_unitary(state, Q_mat, gammas[layer], n)
        state = apply_mixer_unitary(state, betas[layer], n)

    # Beklenti değeri ⟨ψ|H_C|ψ⟩
    energy = 0.0
    probs  = np.abs(state)**2
    for x in range(2**n):
        bits = [(x >> q) & 1 for q in range(n)]
        e = sum(Q_mat[i,i]*bits[i] for i in range(n))
        for i in range(n):
            for j in range(i+1, n):
                e += Q_mat[i,j] * bits[i] * bits[j]
        energy += probs[x] * e
    return energy


def run_qaoa(Q_mat: np.ndarray, p: int = 3, n_restarts: int = 5) -> dict:
    """
    COBYLA ile γ/β parametrelerini optimize eder, en iyi çözümü döndürür.
    """
    n = Q_mat.shape[0]
    best_result = None
    best_energy = np.inf

    t0 = time.time()
    for restart in range(n_restarts):
        # Rastgele başlangıç noktası
        x0 = np.random.uniform(0, np.pi, 2*p)
        res = scipy_minimize(
            qaoa_energy, x0, args=(Q_mat, n, p),
            method='COBYLA',
            options={'maxiter': 500, 'rhobeg': 0.5}
        )
        if res.fun < best_energy:
            best_energy = res.fun
            best_result = res

    elapsed = time.time() - t0

    # En iyi parametrelerle durum vektörü
    gammas = best_result.x[:p]
    betas  = best_result.x[p:]
    state  = np.ones(2**n, dtype=complex) / np.sqrt(2**n)
    for layer in range(p):
        state = apply_cost_unitary(state, Q_mat, gammas[layer], n)
        state = apply_mixer_unitary(state, betas[layer], n)

    # En yüksek olasılıklı bit dizisi → çözüm
    probs   = np.abs(state)**2
    best_x  = int(np.argmax(probs))
    sol_bits = [(best_x >> q) & 1 for q in range(n)]

    return {
        "energy":    best_energy,
        "gammas":    gammas.tolist(),
        "betas":     betas.tolist(),
        "solution":  sol_bits,
        "elapsed":   elapsed,
        "probs":     probs,
    }


def compute_qubo_energy(bits: list, Q_mat: np.ndarray) -> float:
    """Verilen bit vektörü için QUBO enerjisini hesaplar."""
    n   = len(bits)
    e   = sum(Q_mat[i,i]*bits[i] for i in range(n))
    for i in range(n):
        for j in range(i+1, n):
            e += Q_mat[i,j] * bits[i] * bits[j]
    return e


def brute_force_optimal(Q_mat: np.ndarray) -> dict:
    """Kaba kuvvetle tüm 2^n durumları dener (sadece küçük n için)."""
    n = Q_mat.shape[0]
    best_e   = np.inf
    best_x   = None
    for x in range(2**n):
        bits = [(x >> q) & 1 for q in range(n)]
        e    = compute_qubo_energy(bits, Q_mat)
        if e < best_e:
            best_e, best_x = e, bits
    return {"energy": best_e, "solution": best_x}


# ─────────────────────────────────────────────────────────────────────
# 3. GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_qaoa_results(probs: np.ndarray, optimal_bits: list,
                      qaoa_bits: list, n_qubits: int, save_path: str):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#0d1117')

    # Sol: Olasılık dağılımı
    ax1 = axes[0]
    ax1.set_facecolor('#161b27')
    top_k = 16
    top_idx = np.argsort(probs)[-top_k:][::-1]
    labels  = [format(i, f'0{n_qubits}b') for i in top_idx]
    colors  = ['#ffe66d' if list((i >> q) & 1 for q in range(n_qubits)) == qaoa_bits
               else '#4ecdc4' for i in top_idx]
    ax1.bar(range(len(top_idx)), probs[top_idx], color=colors, width=0.7)
    ax1.set_xticks(range(len(top_idx)))
    ax1.set_xticklabels(labels, rotation=45, color='#aaaaaa', fontsize=8)
    ax1.set_title("QAOA Ölçüm Olasılıkları (Top-16)", color='white', fontweight='bold')
    ax1.set_ylabel("Olasılık", color='#aaaaaa')
    ax1.tick_params(colors='#aaaaaa')
    ax1.grid(True, axis='y', alpha=0.15, color='gray', ls='--')
    for sp in ax1.spines.values(): sp.set_edgecolor('#333355')

    import matplotlib.patches as mpatches
    legend_h = [mpatches.Patch(color='#ffe66d', label='QAOA Çözümü'),
                mpatches.Patch(color='#4ecdc4', label='Diğer Durumlar')]
    ax1.legend(handles=legend_h, facecolor='#161b27', edgecolor='#444466',
               labelcolor='white', fontsize=9)

    # Sağ: ATM seçim barları
    ax2 = axes[1]
    ax2.set_facecolor('#161b27')
    atm_labels = [f"ATM{j+1}" for j in range(n_qubits)]
    ax2.bar(atm_labels, qaoa_bits, color='#ffe66d', label='QAOA', width=0.35,
            alpha=0.9, align='center')
    ax2.bar([f"ATM{j+1}" for j in range(n_qubits)],
            optimal_bits, color='#4ecdc4', label='Optimal', width=0.35,
            alpha=0.9, align='edge')
    ax2.set_title("ATM Seçimi: QAOA vs Optimal", color='white', fontweight='bold')
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Gitmez', 'Gider'], color='#aaaaaa')
    ax2.tick_params(colors='#aaaaaa')
    ax2.legend(facecolor='#161b27', edgecolor='#444466', labelcolor='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#333355')

    fig.suptitle("AŞAMA 2c — QAOA Simülatör Sonuçları (5 Qubit Demo)",
                 color='white', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    print(f"  [SAVED] {save_path}")


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n[*] AŞAMA 2c — QAOA Simülatörü (5 Qubit Demo Problemi)\n")

    np.random.seed(42)

    # QUBO oluştur
    Q_demo = build_demo_qubo()
    print(f"  Demo QUBO matrisi ({N_QUBITS}×{N_QUBITS}):")
    with np.printoptions(precision=3, suppress=True):
        print(Q_demo)

    # Kaba kuvvet optimal
    print("\n  [..] Kaba kuvvet (2^5=32 durum) optimal aranıyor...")
    t0 = time.time()
    bf_result = brute_force_optimal(Q_demo)
    bf_time   = time.time() - t0
    print(f"  [OK] Optimal enerji  : {bf_result['energy']:.4f}")
    print(f"       Optimal çözüm  : {bf_result['solution']} (ATM seçimi)")
    print(f"       Süre           : {bf_time*1000:.1f} ms")

    # QAOA simülasyon (p=3, 5 restart)
    print("\n  [..] QAOA simülatörü çalışıyor (p=3, COBYLA)...")
    qaoa_result = run_qaoa(Q_demo, p=3, n_restarts=5)
    qaoa_energy_val  = compute_qubo_energy(qaoa_result["solution"], Q_demo)
    approx_ratio = bf_result["energy"] / qaoa_energy_val if qaoa_energy_val != 0 else np.nan

    print(f"  [OK] QAOA enerji     : {qaoa_result['energy']:.4f}")
    print(f"       QAOA çözüm      : {qaoa_result['solution']}")
    print(f"       Optimal enerji  : {bf_result['energy']:.4f}")
    print(f"       Yaklaşıklık ort.: {approx_ratio:.4f}  (1.0 = optimal)")
    print(f"       Süre            : {qaoa_result['elapsed']:.2f} sn")
    print(f"       γ parametreleri : {[round(g,3) for g in qaoa_result['gammas']]}")
    print(f"       β parametreleri : {[round(b,3) for b in qaoa_result['betas']]}")

    # Görselleştir
    print("\n  [..] Grafik oluşturuluyor...")
    plot_qaoa_results(
        probs       = qaoa_result["probs"],
        optimal_bits= bf_result["solution"],
        qaoa_bits   = qaoa_result["solution"],
        n_qubits    = N_QUBITS,
        save_path   = os.path.join(BASE, "phase2c_qaoa_results.png")
    )

    # Sonuçları kaydet
    results_df = pd.DataFrame([{
        "yontem":         "Kaba Kuvvet (Klasik)",
        "qubo_enerji":    round(bf_result["energy"], 4),
        "sure_sn":        round(bf_time, 4),
        "cozum":          str(bf_result["solution"]),
    }, {
        "yontem":         "QAOA Simülatör (p=3)",
        "qubo_enerji":    round(qaoa_energy_val, 4),
        "sure_sn":        round(qaoa_result["elapsed"], 4),
        "cozum":          str(qaoa_result["solution"]),
    }])
    results_df.to_csv(os.path.join(BASE, "data_qaoa_results.csv"), index=False)
    print(f"  [SAVED] data_qaoa_results.csv")

    print("\n[OK] AŞAMA 2c tamamlandı.")
    print("     Bir sonraki: AŞAMA 2d — Adil Karşılaştırma (MILP vs QAOA)")
