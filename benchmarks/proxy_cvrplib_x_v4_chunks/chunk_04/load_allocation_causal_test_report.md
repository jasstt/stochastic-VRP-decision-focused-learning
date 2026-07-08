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
| X-n176-k26 | 175       | False                    | True                  | False                  | 0                    | 26                | False            |
| X-n181-k23 | 180       | True                     | True                  | True                   | 23                   | 23                | True             |
| X-n186-k15 | 185       | True                     | True                  | True                   | 15                   | 15                | True             |
| X-n190-k8  | 189       | True                     | True                  | True                   | 8                    | 8                 | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.011872 |
| OR-Tools route + VROOM allocation | 0.022278 | 0.026198 |
| VROOM route + VROOM allocation | 0.011872 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.032167 | 0.027591 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 12   | 12            | 12               | 0.4159        | 0.0000                        | 0.0119                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 12   | 10            | 10               | 0.4118        | 0.0223                        | 0.0262                     | 0.8000                | 0.2000             | 0.2000                         | 0.8000                    | 2.7172                               |
| VROOM route + VROOM allocation       | baseline      | 12   | 12            | 12               | 0.4159        | 0.0119                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 12   | 10            | 10               | 0.4124        | 0.0322                        | 0.0276                     | 0.2000                | 0.8000             | 0.2000                         | 0.8000                    | -1.9994                              |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4166        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 3    | 2             | 2                | 0.4237        | 0.0000                         | 1.0000                    | 0.0278                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4127        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 3    | 2             | 2                | 0.4163        | 0.0000                         | 1.0000                    | 0.0806                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4253        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4264        | 0.0000                         | 1.0000                    | 0.2270                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4236        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4250        | 0.3333                         | 0.6667                    | 0.2194                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.3933        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 3    | 2             | 2                | 0.3344        | 0.5000                         | 0.5000                    | 12.5802                              |
| cargo      | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4012        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 3    | 2             | 2                | 0.3250        | 0.0000                         | 1.0000                    | -12.6985                             |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4285        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4408        | 0.3333                         | 0.6667                    | 0.4251                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4260        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4554        | 0.3333                         | 0.6667                    | 1.5278                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.200, route-source closer share 0.800, movement fraction 0.359. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
