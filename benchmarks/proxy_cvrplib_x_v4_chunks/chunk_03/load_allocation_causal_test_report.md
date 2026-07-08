# Load Allocation Causal Test Report

## Müdahale Tasarımı

Bu test korelasyon değil, müdahale testidir. Önce OR-Tools ve VROOM route setleri aynı instance üzerinde çözüldü. Sonra her domain için baseline stochastic engine tekrar çalıştırıldı ve her provider'ın route-level planlanan yük toplamları çıkarıldı.

Müdahale şu şekilde uygulandı:

- `OR-Tools route + VROOM allocation`: OR-Tools route grupları sabit kaldı, route-level toplam yük hedefleri VROOM baseline çözümünden alındı.
- `VROOM route + OR-Tools allocation`: VROOM route grupları sabit kaldı, route-level toplam yük hedefleri OR-Tools baseline çözümünden alındı.
- Route etiketleri provider'lar arasında anlamsız olduğu için allocation vektörleri büyükten küçüğe sıralanıp hedef provider'ın büyükten küçüğe route yüklerine eşlendi.
- Aktif route sayısı eşit olmayan instance-domain satırları müdahale için elendi; aksi halde "allocation kaynağı" ile "route sayısı" karışacaktı.

## Dataset ve Feasibility

Çalıştırılan set: 4 CVRPLIB X instance.

Ortak anchor-feasible instance sayısı: 3.

Aktif route sayısı eşit olan ortak anchor-feasible instance sayısı: 3.

| Instance   | Customers | OR-Tools Anchor Feasible | VROOM Anchor Feasible | Common Anchor Feasible | OR-Tools Route Count | VROOM Route Count | Same Route Count |
| ---------- | --------- | ------------------------ | --------------------- | ---------------------- | -------------------- | ----------------- | ---------------- |
| X-n157-k13 | 156       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n162-k11 | 161       | True                     | True                  | True                   | 11                   | 11                | True             |
| X-n167-k10 | 166       | True                     | True                  | True                   | 10                   | 10                | True             |
| X-n172-k51 | 171       | False                    | True                  | False                  | 0                    | 51                | False            |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.019665 |
| OR-Tools route + VROOM allocation | 0.000000 | 0.001474 |
| VROOM route + VROOM allocation | 0.019665 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.000321 | 0.001154 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 12   | 12            | 12               | 0.2810        | 0.0000                        | 0.0197                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 12   | 1             | 1                | 0.4858        | 0.0000                        | 0.0015                     | 1.0000                | 0.0000             | 0.0000                         | 1.0000                    | 0.0000                               |
| VROOM route + VROOM allocation       | baseline      | 12   | 12            | 12               | 0.2618        | 0.0197                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 12   | 1             | 1                | 0.4854        | 0.0003                        | 0.0012                     | 1.0000                | 0.0000             | 1.0000                         | 0.0000                    | 0.7826                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.2841        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 3    | 1             | 1                | 0.4858        | 0.0000                         | 1.0000                    | 0.0000                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.2715        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 3    | 1             | 1                | 0.4854        | 1.0000                         | 0.0000                    | 0.7826                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.3146        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| grocery    | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.3064        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.1895        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cargo      | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.1701        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.3357        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.2990        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |

## Nedensellik Değerlendirmesi

Müdahale sonucu karışık çıktı. Ortalama allocation-source closer share 0.500, route-source closer share 0.500, movement fraction 0.391. Bu, load allocation'ın kısmi etkisi olabileceğini ama tek faktör olarak yeterli açıklama olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 kısmen açık kalır: load allocation etkili bir mekanizma olabilir, fakat route topology veya solver heuristic farklarıyla birlikte çalışıyor gibi görünmektedir.

## Doğru Cümle

Müdahale hibritleri allocation ve route kaynakları arasında net ayrışmadı; sonuç kısmi/belirsizdir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
