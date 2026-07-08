# Load Allocation Causal Test Report

## Müdahale Tasarımı

Bu test korelasyon değil, müdahale testidir. Önce OR-Tools ve VROOM route setleri aynı instance üzerinde çözüldü. Sonra her domain için baseline stochastic engine tekrar çalıştırıldı ve her provider'ın route-level planlanan yük toplamları çıkarıldı.

Müdahale şu şekilde uygulandı:

- `OR-Tools route + VROOM allocation`: OR-Tools route grupları sabit kaldı, route-level toplam yük hedefleri VROOM baseline çözümünden alındı.
- `VROOM route + OR-Tools allocation`: VROOM route grupları sabit kaldı, route-level toplam yük hedefleri OR-Tools baseline çözümünden alındı.
- Route etiketleri provider'lar arasında anlamsız olduğu için allocation vektörleri büyükten küçüğe sıralanıp hedef provider'ın büyükten küçüğe route yüklerine eşlendi.
- Aktif route sayısı eşit olmayan instance-domain satırları müdahale için elendi; aksi halde "allocation kaynağı" ile "route sayısı" karışacaktı.

## Dataset ve Feasibility

Çalıştırılan set: 40 CVRPLIB X instance.

Ortak anchor-feasible instance sayısı: 27.

Aktif route sayısı eşit olan ortak anchor-feasible instance sayısı: 27.

| Instance   | Customers | OR-Tools Anchor Feasible | VROOM Anchor Feasible | Common Anchor Feasible | OR-Tools Route Count | VROOM Route Count | Same Route Count |
| ---------- | --------- | ------------------------ | --------------------- | ---------------------- | -------------------- | ----------------- | ---------------- |
| X-n101-k25 | 100       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n106-k14 | 105       | True                     | True                  | True                   | 14                   | 14                | True             |
| X-n110-k13 | 109       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n115-k10 | 114       | True                     | True                  | True                   | 10                   | 10                | True             |
| X-n120-k6  | 119       | True                     | True                  | True                   | 6                    | 6                 | True             |
| X-n125-k30 | 124       | False                    | True                  | False                  | 0                    | 30                | False            |
| X-n129-k18 | 128       | True                     | True                  | True                   | 18                   | 18                | True             |
| X-n134-k13 | 133       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n139-k10 | 138       | True                     | True                  | True                   | 10                   | 10                | True             |
| X-n143-k7  | 142       | True                     | True                  | True                   | 7                    | 7                 | True             |
| X-n148-k46 | 147       | False                    | True                  | False                  | 0                    | 46                | False            |
| X-n153-k22 | 152       | False                    | True                  | False                  | 0                    | 22                | False            |
| X-n157-k13 | 156       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n162-k11 | 161       | True                     | True                  | True                   | 11                   | 11                | True             |
| X-n167-k10 | 166       | True                     | True                  | True                   | 10                   | 10                | True             |
| X-n172-k51 | 171       | False                    | True                  | False                  | 0                    | 51                | False            |
| X-n176-k26 | 175       | False                    | True                  | False                  | 0                    | 26                | False            |
| X-n181-k23 | 180       | True                     | True                  | True                   | 23                   | 23                | True             |
| X-n186-k15 | 185       | True                     | True                  | True                   | 15                   | 15                | True             |
| X-n190-k8  | 189       | True                     | True                  | True                   | 8                    | 8                 | True             |
| X-n195-k51 | 194       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n200-k36 | 199       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n204-k19 | 203       | True                     | True                  | True                   | 19                   | 19                | True             |
| X-n209-k16 | 208       | True                     | True                  | True                   | 16                   | 16                | True             |
| X-n214-k11 | 213       | True                     | True                  | True                   | 11                   | 11                | True             |
| X-n219-k73 | 218       | True                     | True                  | True                   | 73                   | 73                | True             |
| X-n223-k34 | 222       | True                     | True                  | True                   | 34                   | 34                | True             |
| X-n228-k23 | 227       | True                     | True                  | True                   | 23                   | 23                | True             |
| X-n233-k16 | 232       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n237-k14 | 236       | True                     | True                  | True                   | 14                   | 14                | True             |
| X-n242-k48 | 241       | True                     | True                  | True                   | 48                   | 48                | True             |
| X-n247-k50 | 246       | False                    | True                  | False                  | 0                    | 50                | False            |
| X-n251-k28 | 250       | True                     | True                  | True                   | 28                   | 28                | True             |
| X-n256-k16 | 255       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n261-k13 | 260       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n266-k58 | 265       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n270-k35 | 269       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n275-k28 | 274       | True                     | True                  | True                   | 28                   | 28                | True             |
| X-n280-k17 | 279       | True                     | True                  | True                   | 17                   | 17                | True             |
| X-n284-k15 | 283       | True                     | True                  | True                   | 15                   | 15                | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.012388 |
| OR-Tools route + VROOM allocation | 0.006454 | 0.010912 |
| VROOM route + VROOM allocation | 0.012388 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.012310 | 0.005640 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 108  | 108           | 108              | 0.4096        | 0.0000                        | 0.0124                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 108  | 87            | 87               | 0.4329        | 0.0065                        | 0.0109                     | 0.7816                | 0.2184             | 0.2184                         | 0.7816                    | 0.2803                               |
| VROOM route + VROOM allocation       | baseline      | 108  | 108           | 108              | 0.4104        | 0.0124                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 108  | 87            | 87               | 0.4362        | 0.0123                        | 0.0056                     | 0.1379                | 0.8621             | 0.1379                         | 0.8621                    | 0.1004                               |

Müdahale uygulanabilirliği:

| Reason                             | Count |
| ---------------------------------- | ----- |
| allocation_target_exceeds_capacity | 42    |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 27   | 27            | 27               | 0.4114        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 27   | 21            | 21               | 0.4387        | 0.0952                         | 0.9048                    | -0.2905                              |
| atm        | VROOM route + VROOM allocation       | baseline      | 27   | 27            | 27               | 0.4081        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 27   | 21            | 21               | 0.4394        | 0.1429                         | 0.8571                    | 3.5430                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 27   | 27            | 27               | 0.4204        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 27   | 24            | 24               | 0.4375        | 0.2083                         | 0.7917                    | 0.2594                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 27   | 27            | 27               | 0.4244        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 27   | 24            | 24               | 0.4408        | 0.1250                         | 0.8750                    | 0.1765                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 27   | 27            | 27               | 0.3852        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 27   | 18            | 18               | 0.4142        | 0.1111                         | 0.8889                    | 0.7335                               |
| cargo      | VROOM route + VROOM allocation       | baseline      | 27   | 27            | 27               | 0.3892        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 27   | 18            | 18               | 0.4218        | 0.0556                         | 0.9444                    | -4.3912                              |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 27   | 27            | 27               | 0.4214        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 27   | 24            | 24               | 0.4373        | 0.4167                         | 0.5833                    | 0.4606                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 27   | 27            | 27               | 0.4198        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 27   | 24            | 24               | 0.4396        | 0.2083                         | 0.7917                    | 0.3807                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.178, route-source closer share 0.822, movement fraction 0.190. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
