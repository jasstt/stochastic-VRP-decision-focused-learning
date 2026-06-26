// =============================================================
// ARUTE CIT-SVRP -- AŞAMA 2c
// QAOA Devresi — Q# (Microsoft QDK)
// =============================================================
//
// Bu dosya, Phase 2b'de üretilen QUBO formülasyonunu
// bir QAOA (Quantum Approximate Optimization Algorithm) devresi
// olarak Q# ile uygular.
//
// QAOA ÇERÇEVESI:
//   |ψ(γ,β)⟩ = [∏_p Ub(βp) Uc(γp)] |+⟩^⊗n
//
//   Uc(γ) = e^{-iγH_C}  → Maliyet (QUBO) Hamiltonian'ı uygular
//   Ub(β) = e^{-iβH_B}  → Mixer Hamiltonian'ı uygular
//
// KISITLAMALAR:
//   - Bu simülasyon küçük bir alt-problem üzerinde çalışır
//     (5 ATM, 2 araç, ~20 qubit) — tam 20 ATM problemi
//     hali hazırdaki klasik simülatörlerde ~1680 qubit gerektirir
//     ve simüle edilemez.
//   - Klasik COBYLA optimizasyonu ile γ/β parametreleri güncellenir.
//
// NASIL ÇALIŞTIRILIR:
//   dotnet run --project phase2c_qaoa_qsharp
// =============================================================

namespace Arute.CIT.QAOA {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;

    // ──────────────────────────────────────────────────────────
    // 1. YARDIMCI: Uniform Süperpozisyon Başlatma
    // ──────────────────────────────────────────────────────────

    operation PrepareUniformSuperposition(qubits : Qubit[]) : Unit {
        ApplyToEach(H, qubits);
    }

    // ──────────────────────────────────────────────────────────
    // 2. MALİYET HAMİLTONİAN KATMANI: Uc(γ)
    //    QUBO: H_C = Σ_{ij} Q_ij · z_i · z_j
    //    z_i = (1 - σ_z^i) / 2  (0/1 temsil)
    //    ZZ rotasyonu: Rzz(2γ·Q_ij, q_i, q_j)
    // ──────────────────────────────────────────────────────────

    operation ApplyCostLayer(
        qubits      : Qubit[],
        qubo_diag   : Double[],    // Diyagonal elemanlar Q_ii
        qubo_edges  : (Int, Int, Double)[],  // (i, j, Q_ij) -- sıfır olmayanlar
        gamma       : Double
    ) : Unit {
        let n = Length(qubits);

        // Diyagonal terimler: Rz(2γ·Q_ii) her qubit üzerine
        for idx in 0 .. n-1 {
            let angle = 2.0 * gamma * qubo_diag[idx];
            if AbsD(angle) > 1e-10 {
                Rz(angle, qubits[idx]);
            }
        }

        // Çapraz terimler: ZZ rotasyonu
        for (i, j, q_ij) in qubo_edges {
            let angle = 2.0 * gamma * q_ij;
            if AbsD(angle) > 1e-10 {
                CNOT(qubits[i], qubits[j]);
                Rz(angle, qubits[j]);
                CNOT(qubits[i], qubits[j]);
            }
        }
    }

    // ──────────────────────────────────────────────────────────
    // 3. MİXER HAMİLTONİAN KATMANI: Ub(β)
    //    H_B = Σ_i σ_x^i  →  Rx(2β) her qubit üzerine
    // ──────────────────────────────────────────────────────────

    operation ApplyMixerLayer(qubits : Qubit[], beta : Double) : Unit {
        ApplyToEach(Rx(2.0 * beta, _), qubits);
    }

    // ──────────────────────────────────────────────────────────
    // 4. p-KATMANLI QAOA DEVRESİ
    // ──────────────────────────────────────────────────────────

    operation QAOACircuit(
        n_qubits    : Int,
        qubo_diag   : Double[],
        qubo_edges  : (Int, Int, Double)[],
        gammas      : Double[],   // uzunluk p
        betas       : Double[]    // uzunluk p
    ) : Result[] {

        use qubits = Qubit[n_qubits];

        // Başlangıç: |+⟩^⊗n
        PrepareUniformSuperposition(qubits);

        let p = Length(gammas);
        for layer in 0 .. p-1 {
            // Maliyet katmanı
            ApplyCostLayer(qubits, qubo_diag, qubo_edges, gammas[layer]);
            // Mixer katmanı
            ApplyMixerLayer(qubits, betas[layer]);
        }

        // Ölçüm (hesaplama tabanında)
        return MeasureEachZ(qubits);
    }

    // ──────────────────────────────────────────────────────────
    // 5. BEKLENEN ENERJİ ÖRNEKLEME
    //    Klasik optimizasyon (COBYLA) bu fonksiyonu çağırır
    // ──────────────────────────────────────────────────────────

    operation EstimateEnergy(
        n_qubits    : Int,
        qubo_diag   : Double[],
        qubo_edges  : (Int, Int, Double)[],
        gammas      : Double[],
        betas       : Double[],
        n_shots     : Int
    ) : Double {

        mutable total_energy = 0.0;

        for _ in 1 .. n_shots {
            let results = QAOACircuit(n_qubits, qubo_diag, qubo_edges, gammas, betas);

            // Bit dizisinden QUBO enerjisini hesapla
            let bits = ResultArrayAsBoolArray(results);
            mutable energy = 0.0;

            // Diyagonal terimler
            for i in 0 .. n_qubits-1 {
                if bits[i] {
                    set energy += qubo_diag[i];
                }
            }

            // Çapraz terimler
            for (i, j, q_ij) in qubo_edges {
                if bits[i] and bits[j] {
                    set energy += q_ij;
                }
            }

            set total_energy += energy;
        }

        return total_energy / IntAsDouble(n_shots);
    }

    // ──────────────────────────────────────────────────────────
    // 6. GİRİŞ NOKTASI (Q# programı)
    // ──────────────────────────────────────────────────────────

    @EntryPoint()
    operation RunQAOA() : Unit {

        // Alt-problem: 5 ATM, 2 araç, ~20 qubit (demo boyutu)
        // Gerçek QUBO katsayıları Python tarafından üretilip
        // JSON olarak okunur. Burada demo değerleri kullanıyoruz.
        let n_qubits = 20;

        // Demo: küçük QUBO diyagonali (Python'dan gelen normalize değerler)
        // Gerçek uygulamada: data_qubo_matrix.npy okunur
        let qubo_diag = [
            0.85, 0.72, 0.91, 0.60, 0.78,
            0.83, 0.69, 0.95, 0.74, 0.80,
            0.88, 0.65, 0.92, 0.71, 0.77,
            0.86, 0.68, 0.93, 0.75, 0.81
        ];

        // Demo kenarlar (i, j, Q_ij) - penalty terimlerinden gelen
        let qubo_edges = [
            (0, 1, -0.15), (0, 5, -0.12), (1, 6, -0.10),
            (2, 7,  0.08), (3, 8, -0.09), (4, 9,  0.07),
            (5, 10,-0.14), (6, 11, 0.11), (7, 12,-0.08),
            (8, 13, 0.09), (9, 14,-0.13), (10, 15, 0.10)
        ];

        // QAOA derinliği p=3, parametreler (Python COBYLA ile optimize edilir)
        let gammas = [0.1, 0.3, 0.5];
        let betas  = [0.5, 0.4, 0.3];
        let n_shots = 1000;

        Message("Arute CIT-SVRP QAOA Simülatörü Başlıyor...");
        Message($"  Qubit sayısı : {n_qubits}");
        Message($"  QAOA derinliği (p) : {Length(gammas)}");
        Message($"  Shot sayısı : {n_shots}");
        Message("");

        let energy = EstimateEnergy(
            n_qubits, qubo_diag, qubo_edges,
            gammas, betas, n_shots
        );

        Message($"  [OK] Tahmini QUBO Enerjisi : {energy}");
        Message("");
        Message("Detaylı optimizasyon için phase2c_qaoa_simulator.py dosyasını çalıştırın.");
        Message("(Python COBYLA döngüsü γ/β parametrelerini günceller.)");
    }
}
