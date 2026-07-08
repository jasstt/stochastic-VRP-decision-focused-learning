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
| X-n120-k6  | 119       | True                     | True                  | True                   | 6                    | 6                 | True             |
| X-n125-k30 | 124       | False                    | True                  | False                  | 0                    | 30                | False            |
| X-n129-k18 | 128       | True                     | True                  | True                   | 18                   | 18                | True             |
| X-n134-k13 | 133       | True                     | True                  | True                   | 13                   | 13                | True             |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.008922 |
| OR-Tools route + VROOM allocation | 0.000917 | 0.008004 |
| VROOM route + VROOM allocation | 0.008922 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.005658 | 0.003501 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 12   | 12            | 12               | 0.4527        | 0.0000                        | 0.0089                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 12   | 12            | 12               | 0.4518        | 0.0009                        | 0.0080                     | 1.0000                | 0.0000             | 0.0000                         | 1.0000                    | 0.0394                               |
| VROOM route + VROOM allocation       | baseline      | 12   | 12            | 12               | 0.4440        | 0.0089                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 12   | 12            | 12               | 0.4475        | 0.0057                        | 0.0035                     | 0.1667                | 0.8333             | 0.1667                         | 0.8333                    | 0.1503                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4547        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4547        | 0.0000                         | 1.0000                    | 0.0000                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4460        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4460        | 0.0000                         | 1.0000                    | 0.0000                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4546        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4532        | 0.0000                         | 1.0000                    | 0.0626                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4446        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4504        | 0.3333                         | 0.6667                    | 0.2470                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4515        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4515        | 0.0000                         | 1.0000                    | 0.0000                               |
| cargo      | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4446        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4446        | 0.0000                         | 1.0000                    | 0.0000                               |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 3    | 3             | 3                | 0.4501        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 3    | 3             | 3                | 0.4479        | 0.0000                         | 1.0000                    | 0.0949                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 3    | 3             | 3                | 0.4409        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 3    | 3             | 3                | 0.4491        | 0.3333                         | 0.6667                    | 0.3540                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.083, route-source closer share 0.917, movement fraction 0.095. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
