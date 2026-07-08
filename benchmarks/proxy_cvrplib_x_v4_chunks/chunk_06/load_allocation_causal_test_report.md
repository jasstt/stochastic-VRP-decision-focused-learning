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

Ortak anchor-feasible instance sayısı: 4.

Aktif route sayısı eşit olan ortak anchor-feasible instance sayısı: 4.

| Instance   | Customers | OR-Tools Anchor Feasible | VROOM Anchor Feasible | Common Anchor Feasible | OR-Tools Route Count | VROOM Route Count | Same Route Count |
| ---------- | --------- | ------------------------ | --------------------- | ---------------------- | -------------------- | ----------------- | ---------------- |
| X-n214-k11 | 213       | True                     | True                  | True                   | 11                   | 11                | True             |
| X-n219-k73 | 218       | True                     | True                  | True                   | 73                   | 73                | True             |
| X-n223-k34 | 222       | True                     | True                  | True                   | 34                   | 34                | True             |
| X-n228-k23 | 227       | True                     | True                  | True                   | 23                   | 23                | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.004506 |
| OR-Tools route + VROOM allocation | 0.001218 | 0.004318 |
| VROOM route + VROOM allocation | 0.004506 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.003289 | 0.000238 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 16   | 16            | 16               | 0.4623        | 0.0000                        | 0.0045                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 16   | 14            | 14               | 0.4612        | 0.0012                        | 0.0043                     | 1.0000                | 0.0000             | 0.0000                         | 1.0000                    | -0.6593                              |
| VROOM route + VROOM allocation       | baseline      | 16   | 16            | 16               | 0.4607        | 0.0045                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 16   | 14            | 14               | 0.4610        | 0.0033                        | 0.0002                     | 0.0000                | 1.0000             | 0.0000                         | 1.0000                    | -5.2857                              |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 4    | 4             | 4                | 0.4657        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 4    | 4             | 4                | 0.4616        | 0.0000                         | 1.0000                    | -2.3158                              |
| atm        | VROOM route + VROOM allocation       | baseline      | 4    | 4             | 4                | 0.4656        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 4    | 3             | 3                | 0.4632        | 0.0000                         | 1.0000                    | 0.0000                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 4    | 4             | 4                | 0.4640        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 4    | 4             | 4                | 0.4640        | 0.0000                         | 1.0000                    | 0.0000                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 4    | 4             | 4                | 0.4622        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 4    | 4             | 4                | 0.4622        | 0.0000                         | 1.0000                    | 0.0000                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 4    | 4             | 4                | 0.4608        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 4    | 2             | 2                | 0.4604        | 0.0000                         | 1.0000                    | 0.0168                               |
| cargo      | VROOM route + VROOM allocation       | baseline      | 4    | 4             | 4                | 0.4582        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 4    | 3             | 3                | 0.4626        | 0.0000                         | 1.0000                    | -24.6667                             |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 4    | 4             | 4                | 0.4585        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 4    | 4             | 4                | 0.4585        | 0.0000                         | 1.0000                    | 0.0000                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 4    | 4             | 4                | 0.4570        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 4    | 4             | 4                | 0.4570        | 0.0000                         | 1.0000                    | 0.0000                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.000, route-source closer share 1.000, movement fraction -2.972. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
