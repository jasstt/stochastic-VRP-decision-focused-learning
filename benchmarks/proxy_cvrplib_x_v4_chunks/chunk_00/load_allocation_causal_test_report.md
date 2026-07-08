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
| X-n101-k25 | 100       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n106-k14 | 105       | True                     | True                  | True                   | 14                   | 14                | True             |
| X-n110-k13 | 109       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n115-k10 | 114       | True                     | True                  | True                   | 10                   | 10                | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.024812 |
| OR-Tools route + VROOM allocation | 0.010219 | 0.019514 |
| VROOM route + VROOM allocation | 0.024812 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.023922 | 0.000938 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 12   | 12            | 12               | 0.4097        | 0.0000                        | 0.0248                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 12   | 12            | 12               | 0.4199        | 0.0102                        | 0.0195                     | 0.5000                | 0.5000             | 0.5000                         | 0.5000                    | 0.6902                               |
| VROOM route + VROOM allocation       | baseline      | 12   | 12            | 12               | 0.4345        | 0.0248                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 12   | 12            | 12               | 0.4336        | 0.0239                        | 0.0009                     | 0.0000                | 1.0000             | 0.0000                         | 1.0000                    | 0.0586                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4099        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4186        | 0.3333                         | 0.6667                    | 0.6391                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4361        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4361        | 0.0000                         | 1.0000                    | 0.0021                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4083        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4183        | 0.3333                         | 0.6667                    | 0.5964                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4348        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4332        | 0.0000                         | 1.0000                    | 0.1046                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4143        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4202        | 0.3333                         | 0.6667                    | 0.5955                               |
| cargo      | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4394        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4395        | 0.0000                         | 1.0000                    | -0.0097                              |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4065        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4227        | 1.0000                         | 0.0000                    | 0.9299                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4278        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4258        | 0.0000                         | 1.0000                    | 0.1375                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.250, route-source closer share 0.750, movement fraction 0.374. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
