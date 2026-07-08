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
| X-n270-k35 | 269       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n275-k28 | 274       | True                     | True                  | True                   | 28                   | 28                | True             |
| X-n280-k17 | 279       | True                     | True                  | True                   | 17                   | 17                | True             |
| X-n284-k15 | 283       | True                     | True                  | True                   | 15                   | 15                | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.019580 |
| OR-Tools route + VROOM allocation | 0.012694 | 0.005273 |
| VROOM route + VROOM allocation | 0.019580 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.017539 | 0.003053 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 12   | 12            | 12               | 0.3859        | 0.0000                        | 0.0196                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 12   | 6             | 6                | 0.4451        | 0.0127                        | 0.0053                     | 0.3333                | 0.6667             | 0.6667                         | 0.3333                    | 0.6053                               |
| VROOM route + VROOM allocation       | baseline      | 12   | 12            | 12               | 0.3842        | 0.0196                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 12   | 7             | 7                | 0.4536        | 0.0175                        | 0.0031                     | 0.0000                | 1.0000             | 0.0000                         | 1.0000                    | 0.0343                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.3784        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| atm        | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.3425        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 3    | 1             | 1                | 0.4596        | 0.0000                         | 1.0000                    | 0.4595                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4263        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4433        | 0.6667                         | 0.3333                    | 0.5337                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4529        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4581        | 0.0000                         | 1.0000                    | -0.0580                              |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.3003        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cargo      | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.2946        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 3    | 0             | 0                |               |                                |                           |                                      |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4385        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4469        | 0.6667                         | 0.3333                    | 0.6769                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4469        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4471        | 0.0000                         | 1.0000                    | -0.0150                              |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.333, route-source closer share 0.667, movement fraction 0.320. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
