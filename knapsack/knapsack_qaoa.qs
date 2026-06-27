// ============================================================
// KNAPSACK QAOA — Q# Devresi
// Görev 3: Sınır bölgesi nesneleri için p-katmanlı QAOA
// ============================================================
//
// Bu dosya Microsoft QDK ile derlenir.
// Python tarafı (knapsack_hybrid.py) parametreleri gönderir,
// Q# devresi ölçüm sonuçlarını döndürür.
//
// Devre mimarisi:
//   |+⟩^⊗m başlangıç durumu
//   p kez: Uc(γ_l) · Ub(β_l)
//   Uc: QUBO Hamiltonian'ını Rz/CNOT kapılarıyla kodlar
//   Ub: Rx(2β) karıştırıcı
// ============================================================

namespace KnapsackQAOA {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;

    // ─────────────────────────────────────────────────────
    // COST UNITARY: Uc(γ) = exp(-iγ H_C)
    // H_C = Σ_j Q_jj Z_j + Σ_{j<k} Q_jk Z_j Z_k
    // ─────────────────────────────────────────────────────

    operation ApplyCostUnitary(
        qubits   : Qubit[],
        diag     : Double[],     // Q_jj katsayıları
        offdiag  : Double[][],   // Q_jk katsayıları (j<k matris)
        gamma    : Double
    ) : Unit is Adj + Ctl {
        let n = Length(qubits);

        // Diyagonal terimler: Rz(2γ Q_jj)
        for j in 0..n-1 {
            Rz(2.0 * gamma * diag[j], qubits[j]);
        }

        // Çapraz terimler: CNOT + Rz(2γ Q_jk) + CNOT
        for j in 0..n-2 {
            for k in j+1..n-1 {
                if AbsD(offdiag[j][k]) > 1e-10 {
                    CNOT(qubits[j], qubits[k]);
                    Rz(2.0 * gamma * offdiag[j][k], qubits[k]);
                    CNOT(qubits[j], qubits[k]);
                }
            }
        }
    }

    // ─────────────────────────────────────────────────────
    // MIXER UNITARY: Ub(β) = exp(-iβ H_B) = ∏ Rx(2β)
    // ─────────────────────────────────────────────────────

    operation ApplyMixerUnitary(
        qubits : Qubit[],
        beta   : Double
    ) : Unit is Adj + Ctl {
        for q in qubits {
            Rx(2.0 * beta, q);
        }
    }

    // ─────────────────────────────────────────────────────
    // p-KATMANLI QAOA DEVRESİ
    // ─────────────────────────────────────────────────────

    operation RunQAOACircuit(
        n_qubits : Int,
        diag     : Double[],
        offdiag  : Double[][],
        gammas   : Double[],    // uzunluk = p
        betas    : Double[],    // uzunluk = p
        n_shots  : Int
    ) : Result[] {
        let p = Length(gammas);

        use qubits = Qubit[n_qubits];

        // Başlangıç: |+⟩^⊗n eşit süperpozisyon
        ApplyToEach(H, qubits);

        // p QAOA katmanı
        for layer in 0..p-1 {
            ApplyCostUnitary(qubits, diag, offdiag, gammas[layer]);
            ApplyMixerUnitary(qubits, betas[layer]);
        }

        // Ölçüm
        let results = MeasureEachZ(qubits);
        ResetAll(qubits);
        return results;
    }

    // ─────────────────────────────────────────────────────
    // TEK ATIŞ ÇALIŞTIRICISI (Python tarafından çağrılır)
    // ─────────────────────────────────────────────────────

    @EntryPoint()
    operation Main() : Unit {
        // Giriş noktası — gerçek parametreler Python'dan gelir.
        // Bu blok sadece derleme doğrulaması içindir.
        let n = 3;  // demo
        let diag    = [-5.0, -8.0, -6.0];
        let offdiag = [[0.0, 2.0, 2.0],
                       [0.0, 0.0, 2.0],
                       [0.0, 0.0, 0.0]];
        let gammas  = [0.5, 1.2];
        let betas   = [0.8, 0.4];

        Message("KnapsackQAOA: Devre derleme doğrulaması");
        Message($"n_qubits={n}, p={Length(gammas)}");

        use qubits = Qubit[n];
        ApplyToEach(H, qubits);
        for layer in 0..Length(gammas)-1 {
            ApplyCostUnitary(qubits, diag, offdiag, gammas[layer]);
            ApplyMixerUnitary(qubits, betas[layer]);
        }
        let res = MeasureEachZ(qubits);
        Message($"Ölçüm: {res}");
        ResetAll(qubits);
    }
}
