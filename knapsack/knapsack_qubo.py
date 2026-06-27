# -*- coding: utf-8 -*-
"""
=============================================================
KNAPSACK — GÖREV 2
QUBO Formülasyonu + λ Validasyonu
=============================================================

QUBO hedefi (maximizasyon → minimizasyon çevirisi):
  H(x) = -Σ v_i·x_i  +  λ·(Σ w_i·x_i - W)²

Hibrit mimari:
  - LP relaxation'dan gelen kilitli nesneler (x=0 veya x=1) sabit tutulur.
  - Sadece sınır bölgesindeki (fraksiyonel) nesneler QUBO'ya girer.
  - Kilitli nesnelerin katkısı kapasite ve değer bütçesinden düşülür.

λ Validasyonu (önceki projeden ders — baştan uygulandı):
  Kural: λ  >  max(v_i) / min(w_i²)
  Sezgisel: en değerli nesneyi seçmenin getirisinden (v_max/w_min²)
  kapasite ihlal cezası büyük olmalı ki QAOA kısıtı "görsün".
  Bu eşiğin altında λ seçmek, ceza terimini rota maliyetinin yanında
  görünmez kılar (önceki projede λ_C=0.5 ile yaşanan bug'ın tekrarını önler).
"""

import numpy as np
import pandas as pd
import sys, io, os
import json

BASE = os.path.dirname(__file__)

sys.path.insert(0, BASE)
from knapsack_classical import generate_knapsack, solve_lp_relaxation, validate_solution


# ─────────────────────────────────────────────────────────────────────
# λ VALİDASYONU (baştan önlenmiş bug)
# ─────────────────────────────────────────────────────────────────────

def compute_lambda_threshold(data: dict, subset_indices=None) -> dict:
    """
    Gerekli minimum λ eşiğini hesaplar.

    Türetme:
      1 ihlal birimi cezası: λ · w_min²  (en hafif nesne bir kez fazla seçilir)
      Bu cezanın en değerli nesneyi seçmekten BÜYÜK olması gerekir: v_max
      → λ · w_min² > v_max
      → λ > v_max / w_min²

    Güvenlik katsayısı: 3× (QAOA'nın stokastik doğası için marj)
    """
    if subset_indices is not None:
        v_sub = data["values"][subset_indices]
        w_sub = data["weights"][subset_indices]
    else:
        v_sub = data["values"]
        w_sub = data["weights"]

    v_max  = float(v_sub.max())
    w_min  = float(w_sub.min())
    w_max  = float(w_sub.max())

    # Minimum eşik
    lambda_min = v_max / (w_min ** 2)
    # En büyük olası ihlal: tüm nesneleri seç
    W_sub      = data["W"]
    max_violation = float(np.sum(w_sub))  # en kötü: hepsini seç → toplam ağırlık
    # Güvenlik katsayısı: ceza, tam ihlalde, değer farkından 2× büyük olsun
    lambda_safe = v_max / (w_min ** 2) * 3.0

    return {
        "v_max":        v_max,
        "w_min":        w_min,
        "lambda_min_required": round(lambda_min, 4),
        "lambda_safe_3x":      round(lambda_safe, 4),
        "max_violation":       max_violation,
    }


def validate_lambda(lambda_val: float, threshold: dict) -> dict:
    """
    [L1 uygulaması] λ seçimini açıkça doğrula ve raporla.
    Sessiz 'etkisiz λ' bug'ını önler.
    """
    is_valid   = lambda_val >= threshold["lambda_min_required"]
    is_safe    = lambda_val >= threshold["lambda_safe_3x"]
    pen_at_min = lambda_val * threshold["w_min"] ** 2
    status = ("✅ Güvenli (3×)" if is_safe else
              "⚠️ Eşik üstü ama marjsız" if is_valid else
              "❌ EŞİĞİN ALTINDA — kısıt görülmeyebilir!")
    return {
        "lambda_val":              lambda_val,
        "lambda_min_required":     threshold["lambda_min_required"],
        "lambda_safe_3x":          threshold["lambda_safe_3x"],
        "pen_for_min_violation":   round(pen_at_min, 4),
        "v_max":                   threshold["v_max"],
        "ratio_pen_to_value":      round(pen_at_min / threshold["v_max"], 4),
        "is_valid":                is_valid,
        "status":                  status,
    }


# ─────────────────────────────────────────────────────────────────────
# QUBO MATRISI (sınır bölgesi için)
# ─────────────────────────────────────────────────────────────────────

def build_knapsack_qubo(data: dict, subset_indices: np.ndarray,
                         lambda_val: float,
                         W_residual: float) -> tuple[np.ndarray, dict]:
    """
    Sınır bölgesindeki nesneler için QUBO matrisi.

    Değişkenler: x_j ∈ {0,1} sadece subset_indices içindeki nesneler için.
    W_residual: kilitli=1 nesneler sonrası kalan kapasite.

    H(x) = -Σ_j v_j·x_j + λ·(Σ_j w_j·x_j - W_residual)²

    Açılım:
      Diyagonal: -v_j + λ·w_j²  - 2λ·W_residual·w_j
      Çapraz:    2λ·w_j·w_k   (j<k)
      Sabit:     λ·W_residual²  (QUBO matrisine girmez)
    """
    m      = len(subset_indices)
    w_sub  = data["weights"][subset_indices].astype(float)
    v_sub  = data["values"][subset_indices].astype(float)
    W_res  = float(W_residual)

    Q = np.zeros((m, m))

    # Diyagonal: -v_j + λ(w_j² - 2W_res·w_j)
    for j in range(m):
        Q[j, j] = -v_sub[j] + lambda_val * (w_sub[j]**2 - 2.0 * W_res * w_sub[j])

    # Çapraz: 2λ·w_j·w_k
    for j in range(m):
        for k in range(j+1, m):
            Q[j, k] = 2.0 * lambda_val * w_sub[j] * w_sub[k]

    # QUBO sabit offset (raporlama için)
    const_offset = lambda_val * W_res**2

    return Q, {
        "n_qubits":      m,
        "lambda":        lambda_val,
        "W_residual":    W_res,
        "const_offset":  const_offset,
        "subset_w":      w_sub,
        "subset_v":      v_sub,
        "subset_indices": subset_indices,
    }


def compute_qubo_energy_decomposed(bits: np.ndarray, Q_mat: np.ndarray,
                                    qubo_meta: dict) -> dict:
    """
    [L3 uygulaması] QUBO enerjisini 3 bileşene ayır:
      value_term   = -Σ v_j·x_j
      penalty_term = λ·(Σ w_j·x_j - W_residual)²
      total        = value_term + penalty_term
    Ayrıca gerçek Knapsack değerini ve kısıt durumunu raporla.
    """
    v_sub  = qubo_meta["subset_v"]
    w_sub  = qubo_meta["subset_w"]
    W_res  = qubo_meta["W_residual"]
    lam    = qubo_meta["lambda"]

    value_term   = -float(np.dot(v_sub, bits))
    cap_usage    = float(np.dot(w_sub, bits))
    violation    = cap_usage - W_res
    penalty_term = lam * violation**2

    # QUBO matris enerjisi (doğrulama)
    n = len(bits)
    mat_e = sum(Q_mat[i, i] * bits[i] for i in range(n))
    for i in range(n):
        for j in range(i+1, n):
            mat_e += Q_mat[i, j] * bits[i] * bits[j]

    return {
        "value_term":   round(value_term, 6),
        "penalty_term": round(penalty_term, 6),
        "total_qubo":   round(value_term + penalty_term, 6),
        "mat_energy":   round(mat_e, 6),    # bu iki aynı olmalı
        "knapsack_value": round(-value_term, 2),
        "cap_usage":    cap_usage,
        "W_residual":   W_res,
        "violation":    round(violation, 4),
        "feasible":     violation <= 0,
    }


def brute_force_qubo(Q_mat: np.ndarray, qubo_meta: dict) -> dict:
    """
    2^m tüm kombinasyonlar (sadece küçük m için).
    QUBO enerjisini hem matris hem bileşen bazlı hesaplar.
    """
    m = Q_mat.shape[0]
    best_e   = np.inf
    best_bits = None
    all_results = []

    for x in range(2**m):
        bits = np.array([(x >> q) & 1 for q in range(m)])
        dec  = compute_qubo_energy_decomposed(bits, Q_mat, qubo_meta)
        if dec["total_qubo"] < best_e:
            best_e, best_bits = dec["total_qubo"], bits.copy()
        all_results.append(dec)

    best_dec = compute_qubo_energy_decomposed(best_bits, Q_mat, qubo_meta)
    return {"bits": best_bits, **best_dec, "all_results": all_results}


# ─────────────────────────────────────────────────────────────────────
# ANA AKIŞ
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("\n[*] KNAPSACK — Görev 2: QUBO Formülasyonu + λ Validasyonu\n")

    # Veri yükle
    data = generate_knapsack(n=20, seed=42)
    lp   = solve_lp_relaxation(data)

    frac_idx  = np.where(lp["fractional_mask"])[0]
    fixed1_idx = np.where(lp["fixed_1_mask"])[0]
    fixed0_idx = np.where(lp["fixed_0_mask"])[0]

    print(f"  LP sınır bölgesi: {len(frac_idx)} nesne → {frac_idx.tolist()}")
    print(f"  Kilitli=1: {fixed1_idx.tolist()}")
    print(f"  Kilitli=0: {fixed0_idx.tolist()}")

    # Kilitli=1 nesnelerin katkısı
    w_locked1 = int(np.sum(data["weights"][fixed1_idx]))
    v_locked1 = int(np.sum(data["values"][fixed1_idx]))
    W_residual = data["W"] - w_locked1

    print(f"\n  Kilitli=1 kapasite tüketimi: {w_locked1}")
    print(f"  Kilitli=1 değer katkısı    : {v_locked1}")
    print(f"  QUBO için kalan kapasite    : {W_residual}")
    print(f"  QUBO için nesne sayısı (m)  : {len(frac_idx)}")

    # λ validasyonu
    print("\n  [λ VALİDASYONU]")
    thresh = compute_lambda_threshold(data, subset_indices=frac_idx)
    print(f"  v_max (sınır bölgesi)  : {thresh['v_max']}")
    print(f"  w_min (sınır bölgesi)  : {thresh['w_min']}")
    print(f"  λ minimum eşik         : v_max/w_min² = {thresh['lambda_min_required']}")
    print(f"  λ güvenli (3× marj)    : {thresh['lambda_safe_3x']}")

    lambda_val = thresh["lambda_safe_3x"]
    val_report = validate_lambda(lambda_val, thresh)
    print(f"\n  Seçilen λ              : {lambda_val}")
    print(f"  Min. ihlal cezası      : {val_report['pen_for_min_violation']}")
    print(f"  v_max'a oran           : {val_report['ratio_pen_to_value']}×")
    print(f"  Durum                  : {val_report['status']}")

    # QUBO matrisi
    if len(frac_idx) > 0:
        Q_mat, qubo_meta = build_knapsack_qubo(data, frac_idx, lambda_val, W_residual)
        print(f"\n  QUBO Matrisi ({qubo_meta['n_qubits']}×{qubo_meta['n_qubits']}):")
        with np.printoptions(precision=3, suppress=True, linewidth=120):
            print(Q_mat)

        # Kaba kuvvet (küçük m için)
        if len(frac_idx) <= 15:
            print(f"\n  [..] Kaba kuvvet optimal aranıyor (2^{len(frac_idx)}={2**len(frac_idx)} kombinasyon)...")
            bf = brute_force_qubo(Q_mat, qubo_meta)
            print(f"  [OK] Optimal sınır bölgesi çözümü: {bf['bits'].tolist()}")
            print(f"       Değer terimi   : {bf['value_term']}")
            print(f"       Ceza terimi    : {bf['penalty_term']} (λ={lambda_val})")
            print(f"       Toplam QUBO    : {bf['total_qubo']}")
            print(f"       Kısıt durumu   : {'✅ FEASIBLE' if bf['feasible'] else '❌ INFEASIBLE'}")
            print(f"       Knapsack değeri: {bf['knapsack_value']}")
    else:
        print("\n  Sınır bölgesi boş — QAOA gerekmez!")

    # Kaydet
    np.save(os.path.join(BASE, "data_qubo_matrix.npy"), Q_mat)
    with open(os.path.join(BASE, "data_qubo_meta.json"), "w") as f:
        meta_save = {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                     for k, v in qubo_meta.items()}
        json.dump({"qubo_meta": meta_save,
                   "lambda_val": lambda_val,
                   "lambda_thresh": thresh,
                   "W_residual": W_residual,
                   "frac_idx": frac_idx.tolist(),
                   "fixed1_idx": fixed1_idx.tolist(),
                   "v_locked1": v_locked1,
                   "w_locked1": w_locked1}, f, indent=2)
    print(f"\n  [SAVED] data_qubo_matrix.npy")
    print(f"  [SAVED] data_qubo_meta.json")
    print("\n[OK] Görev 2 tamamlandı.")
