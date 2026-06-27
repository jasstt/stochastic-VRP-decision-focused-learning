# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — GÖREV 3 (Python QAOA Simülatörü)
=============================================================
Q# statevector simülatörü (Qiskit/Q# yoksa NumPy ile).
Önceki projeden öğrenilen 3 ders baştan uygulandı:
  [L1] λ validasyonu — knapsack_qubo.py'de gerçekleşti, burada kullanılır
  [L2] Sessiz INFEASIBLE yok — her çözüm kısıta karşı açıkça doğrulanır
  [L3] ⟨H⟩ beklenti enerjisi VE argmax-bit ayrı ayrı raporlanır
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time, sys, io, os, json
from scipy.optimize import minimize as scipy_minimize

BASE = os.path.dirname(__file__)

sys.path.insert(0, BASE)
from knapsack_classical import generate_knapsack, solve_lp_relaxation, validate_solution
from knapsack_qubo import (
    build_knapsack_qubo, compute_qubo_energy_decomposed,
    compute_lambda_threshold, validate_lambda
)


# ─────────────────────────────────────────────────────────────────────
# NUMPY STATEVECTOR QAOA (Qiskit/Q# gerektirmez)
# ─────────────────────────────────────────────────────────────────────

def apply_cost_unitary_ks(state: np.ndarray, Q_mat: np.ndarray,
                           gamma: float, n: int) -> np.ndarray:
    """e^{-iγH_C} — QUBO Hamiltonian maliyet katmanı."""
    new_state = np.zeros(2**n, dtype=complex)
    for x_int in range(2**n):
        bits   = np.array([(x_int >> q) & 1 for q in range(n)])
        energy = float(np.dot(bits, Q_mat.diagonal()))
        for i in range(n):
            for j in range(i+1, n):
                energy += Q_mat[i, j] * bits[i] * bits[j]
        new_state[x_int] = state[x_int] * np.exp(-1j * gamma * energy)
    return new_state


def apply_mixer_unitary_ks(state: np.ndarray, beta: float, n: int) -> np.ndarray:
    """e^{-iβH_B} = ∏ Rx(2β) karıştırıcı."""
    Rx = np.array([[np.cos(beta), -1j * np.sin(beta)],
                   [-1j * np.sin(beta), np.cos(beta)]])
    for qubit in range(n):
        new_state = np.zeros(2**n, dtype=complex)
        for x_int in range(2**n):
            bit     = (x_int >> qubit) & 1
            partner = x_int ^ (1 << qubit)
            new_state[x_int] += Rx[bit, bit]   * state[x_int]
            new_state[x_int] += Rx[bit, 1-bit] * state[partner]
        state = new_state
    return state


def qaoa_expectation(params: np.ndarray, Q_mat: np.ndarray, n: int, p: int) -> float:
    """
    [L3] ⟨H⟩ beklenti enerjisi.
    params = [γ₁,...,γₚ, β₁,...,βₚ]
    """
    gammas = params[:p]
    betas  = params[p:]
    state  = np.ones(2**n, dtype=complex) / np.sqrt(2**n)
    for layer in range(p):
        state = apply_cost_unitary_ks(state, Q_mat, gammas[layer], n)
        state = apply_mixer_unitary_ks(state, betas[layer], n)
    probs  = np.abs(state)**2
    energy = 0.0
    for x_int in range(2**n):
        bits = np.array([(x_int >> q) & 1 for q in range(n)])
        e    = float(np.dot(bits, Q_mat.diagonal()))
        for i in range(n):
            for j in range(i+1, n):
                e += Q_mat[i, j] * bits[i] * bits[j]
        energy += probs[x_int] * e
    return energy


def run_qaoa_knapsack(Q_mat: np.ndarray, qubo_meta: dict,
                       p: int = 2, n_restarts: int = 8,
                       seed: int = 42) -> dict:
    """
    COBYLA ile p-katmanlı QAOA parametrelerini optimize eder.

    [L3] HEM ⟨H⟩ (beklenti) HEM argmax-bit enerjisi ayrı raporlanır.
    [L2] Çözüm kısıta karşı açıkça doğrulanır.
    """
    np.random.seed(seed)
    n = Q_mat.shape[0]
    best_result = None
    best_expect = np.inf
    convergence_history = []

    t0 = time.perf_counter()
    for restart in range(n_restarts):
        x0  = np.random.uniform(0, np.pi, 2 * p)
        call_log = []

        def tracked(params):
            e = qaoa_expectation(params, Q_mat, n, p)
            call_log.append(e)
            return e

        res = scipy_minimize(tracked, x0, method='COBYLA',
                             options={'maxiter': 500, 'rhobeg': 0.5})
        if res.fun < best_expect:
            best_expect = res.fun
            best_result = res
            convergence_history = call_log

    elapsed = time.perf_counter() - t0

    # Durum vektörü ile olasılıklar
    gammas = best_result.x[:p]
    betas  = best_result.x[p:]
    state  = np.ones(2**n, dtype=complex) / np.sqrt(2**n)
    for layer in range(p):
        state = apply_cost_unitary_ks(state, Q_mat, gammas[layer], n)
        state = apply_mixer_unitary_ks(state, betas[layer], n)

    probs    = np.abs(state)**2
    argmax_x = int(np.argmax(probs))
    argmax_bits = np.array([(argmax_x >> q) & 1 for q in range(n)])

    # [L3] Her ikisini de ayrı hesapla
    expect_dec = compute_qubo_energy_decomposed(
        np.zeros(n),  # placeholder için sıfır, aşağıda düzeltildi
        Q_mat, qubo_meta
    )
    argmax_dec = compute_qubo_energy_decomposed(argmax_bits, Q_mat, qubo_meta)

    # [L2] Kısıt açıkça doğrulanır
    feasible   = argmax_dec["feasible"]
    feas_label = "✅ FEASIBLE" if feasible else f"❌ INFEASIBLE (ihlal: {argmax_dec['violation']:.2f})"

    return {
        "p":               p,
        "gammas":          gammas.tolist(),
        "betas":           betas.tolist(),
        "expect_energy":   round(best_expect, 6),   # [L3] beklenti
        "argmax_bits":     argmax_bits.tolist(),
        "argmax_energy":   argmax_dec["total_qubo"], # [L3] argmax-bit
        "argmax_value":    argmax_dec["knapsack_value"],
        "argmax_value_term":  argmax_dec["value_term"],
        "argmax_penalty_term": argmax_dec["penalty_term"],
        "argmax_total_qubo":   argmax_dec["total_qubo"],
        "feasible":        feasible,
        "feasibility":     feas_label,
        "n_iterations":    len(convergence_history),
        "init_energy":     round(convergence_history[0], 6) if convergence_history else None,
        "probs":           probs,
        "elapsed_s":       round(elapsed, 3),
        "gate_layers":     2 * p,
    }


# ─────────────────────────────────────────────────────────────────────
# GÖRSELLEŞTİRME
# ─────────────────────────────────────────────────────────────────────

def plot_qaoa_results(results_by_p: dict, qubo_meta: dict,
                      bf_value: float, save_path: str):
    n_p  = len(results_by_p)
    fig  = plt.figure(figsize=(22, 10))
    fig.patch.set_facecolor('#0d1117')
    gs   = gridspec.GridSpec(2, n_p + 1, figure=fig,
                             hspace=0.42, wspace=0.32,
                             left=0.06, right=0.97, top=0.90, bottom=0.08)
    dark = '#161b27'; grid = '#2a2f3e'
    palette = ['#4ecdc4', '#ffe66d', '#ff9f43', '#a29bfe', '#fd79a8']

    for idx, (p_val, res) in enumerate(results_by_p.items()):
        probs = res["probs"]
        n     = int(np.round(np.log2(len(probs))))
        top_k = min(16, 2**n)
        top_idx = np.argsort(probs)[-top_k:][::-1]

        ax = fig.add_subplot(gs[0, idx])
        ax.set_facecolor(dark)
        ax.set_title(f"QAOA p={p_val}\n⟨H⟩={res['expect_energy']:.4f}",
                     color='white', fontweight='bold', fontsize=9)
        colors = [palette[idx] if i == int(np.argmax(probs))
                  else '#333355' for i in top_idx]
        ax.bar(range(len(top_idx)), probs[top_idx], color=colors, width=0.7)
        labels = [format(i, f'0{n}b') for i in top_idx]
        ax.set_xticks(range(len(top_idx)))
        ax.set_xticklabels(labels, rotation=70, fontsize=6, color='#aaaaaa')
        ax.set_ylabel("Olasılık", color='#aaaaaa', fontsize=8)
        ax.tick_params(colors='#aaaaaa', labelsize=7)
        ax.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
        [s.set_edgecolor('#333355') for s in ax.spines.values()]

    # Panel: ⟨H⟩ vs argmax karşılaştırması
    ax_cmp = fig.add_subplot(gs[0, n_p])
    ax_cmp.set_facecolor(dark)
    ax_cmp.set_title("⟨H⟩ vs Argmax Enerji\n(p değerine göre)", color='white',
                      fontweight='bold', fontsize=9)
    p_vals  = list(results_by_p.keys())
    expect  = [results_by_p[p]["expect_energy"]   for p in p_vals]
    argmax  = [results_by_p[p]["argmax_total_qubo"] for p in p_vals]
    x_pos   = np.arange(len(p_vals))
    w       = 0.35
    ax_cmp.bar(x_pos - w/2, expect, w, color='#4ecdc4', label='⟨H⟩ beklenti')
    ax_cmp.bar(x_pos + w/2, argmax, w, color='#ffe66d', label='Argmax-bit')
    ax_cmp.set_xticks(x_pos)
    ax_cmp.set_xticklabels([f"p={p}" for p in p_vals], color='#aaaaaa')
    ax_cmp.tick_params(colors='#aaaaaa')
    ax_cmp.legend(facecolor=dark, edgecolor='#444466', labelcolor='white', fontsize=8)
    ax_cmp.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax_cmp.spines.values()]

    # Alt panel: Knapsack değeri karşılaştırması
    ax_val = fig.add_subplot(gs[1, :])
    ax_val.set_facecolor(dark)
    ax_val.set_title("Sınır Bölgesi Knapsack Değeri (QAOA argmax) vs Optimal",
                      color='white', fontweight='bold')
    vals   = [results_by_p[p]["argmax_value"] for p in p_vals]
    colors = [palette[i] for i in range(len(p_vals))]
    ax_val.bar([f"QAOA p={p}" for p in p_vals], vals, color=colors, width=0.5)
    ax_val.axhline(bf_value, color='#ff6b6b', ls='--', lw=2,
                   label=f"Kaba Kuvvet Optimal ({bf_value:.0f})")
    ax_val.set_ylabel("Sınır Bölgesi Knapsack Değeri", color='#aaaaaa')
    ax_val.tick_params(colors='#aaaaaa')
    ax_val.legend(facecolor=dark, edgecolor='#444466', labelcolor='white')
    ax_val.grid(True, axis='y', alpha=0.15, color=grid, ls='--')
    [s.set_edgecolor('#333355') for s in ax_val.spines.values()]

    fig.text(0.5, 0.94, "KNAPSACK — QAOA Simülatörü (Sınır Bölgesi)",
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
    print("\n[*] KNAPSACK — Görev 3: QAOA Simülatörü (Sınır Bölgesi)\n")

    data = generate_knapsack(n=20, seed=42)
    lp   = solve_lp_relaxation(data)

    frac_idx   = np.where(lp["fractional_mask"])[0]
    fixed1_idx = np.where(lp["fixed_1_mask"])[0]
    w_locked1  = int(np.sum(data["weights"][fixed1_idx]))
    v_locked1  = int(np.sum(data["values"][fixed1_idx]))
    W_residual = data["W"] - w_locked1

    # λ validasyonu (baştan uygulandı)
    thresh     = compute_lambda_threshold(data, subset_indices=frac_idx)
    lambda_val = thresh["lambda_safe_3x"]
    val_report = validate_lambda(lambda_val, thresh)
    print(f"  λ = {lambda_val} → {val_report['status']}")

    Q_mat, qubo_meta = build_knapsack_qubo(data, frac_idx, lambda_val, W_residual)
    m = Q_mat.shape[0]
    print(f"  QUBO boyutu: {m} qubit (sınır bölgesi)")

    # Kaba kuvvet referansı
    best_bf_e  = np.inf
    best_bf_bits = None
    for x_int in range(2**m):
        bits = np.array([(x_int >> q) & 1 for q in range(m)])
        cap  = float(np.dot(qubo_meta["subset_w"], bits))
        if cap > W_residual:
            continue   # [L2] kapasite kısıtı hard
        dec = compute_qubo_energy_decomposed(bits, Q_mat, qubo_meta)
        if dec["total_qubo"] < best_bf_e:
            best_bf_e    = dec["total_qubo"]
            best_bf_bits = bits.copy()
            best_bf_val  = dec["knapsack_value"]

    print(f"  Kaba kuvvet optimal sınır değeri: {best_bf_val}")

    # QAOA p=1,2,3
    results_by_p = {}
    for p_val in [1, 2, 3]:
        print(f"\n  [..] QAOA p={p_val} (COBYLA, 8 restart)...")
        res = run_qaoa_knapsack(Q_mat, qubo_meta, p=p_val,
                                 n_restarts=8, seed=42)
        results_by_p[p_val] = res
        print(f"       [L3] ⟨H⟩ beklenti    : {res['expect_energy']}")
        print(f"       [L3] Argmax-bit enerji: {res['argmax_total_qubo']}")
        print(f"       Argmax-bit çözümü     : {res['argmax_bits']}")
        print(f"       Knapsack değeri       : {res['argmax_value']}")
        print(f"       Gamma parametreleri   : {[round(g, 4) for g in res['gammas']]}")
        print(f"       Beta parametreleri    : {[round(b, 4) for b in res['betas']]}")
        print(f"       İterasyon sayısı      : {res['n_iterations']}")
        print(f"       Devre derinliği       : {res['gate_layers']} katman (p×2)")
        print(f"       [L2] Kısıt durumu     : {res['feasibility']}")
        print(f"       Süre                  : {res['elapsed_s']} sn")

    # Karşılaştırma tablosu
    print("\n" + "="*80)
    print("  QAOA KARŞILAŞTIRMA TABLOSU — ⟨H⟩ ve Argmax ayrı [L3]")
    print("="*80)
    rows = []
    for p_val, res in results_by_p.items():
        rows.append({
            "p": p_val,
            "⟨H⟩ Beklenti": res["expect_energy"],
            "Argmax Enerji": res["argmax_total_qubo"],
            "Değer Terimi": res["argmax_value_term"],
            "Ceza Terimi":  res["argmax_penalty_term"],
            "KS Değeri":    res["argmax_value"],
            "Kısıt":        res["feasibility"],
            "Süre (sn)":    res["elapsed_s"],
        })
    df_qaoa = pd.DataFrame(rows)
    print(df_qaoa.to_string(index=False))

    df_qaoa.to_csv(os.path.join(BASE, "data_qaoa_knapsack.csv"), index=False)
    with open(os.path.join(BASE, "data_qaoa_results.json"), "w") as f:
        save_data = {str(p): {k: (v.tolist() if hasattr(v, 'tolist') else v)
                               for k, v in res.items() if k != "probs"}
                     for p, res in results_by_p.items()}
        json.dump({"qaoa_results": save_data,
                   "bf_optimal_boundary_value": float(best_bf_val),
                   "lambda_val": lambda_val,
                   "W_residual": W_residual,
                   "v_locked1": v_locked1,
                   "frac_idx": frac_idx.tolist(),
                   "fixed1_idx": fixed1_idx.tolist()}, f, indent=2)
    print(f"\n  [SAVED] data_qaoa_knapsack.csv")
    print(f"  [SAVED] data_qaoa_results.json")

    plot_qaoa_results(results_by_p, qubo_meta, best_bf_val,
                      os.path.join(BASE, "knapsack_qaoa_results.png"))

    print("\n[OK] Görev 3 tamamlandı.")
