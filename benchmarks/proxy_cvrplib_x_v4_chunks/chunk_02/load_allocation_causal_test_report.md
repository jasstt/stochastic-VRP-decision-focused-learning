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

Ortak anchor-feasible instance sayısı: 2.

Aktif route sayısı eşit olan ortak anchor-feasible instance sayısı: 2.

| Instance   | Customers | OR-Tools Anchor Feasible | VROOM Anchor Feasible | Common Anchor Feasible | OR-Tools Route Count | VROOM Route Count | Same Route Count |
| ---------- | --------- | ------------------------ | --------------------- | ---------------------- | -------------------- | ----------------- | ---------------- |
| X-n139-k10 | 138       | True                     | True                  | True                   | 10                   | 10                | True             |
| X-n143-k7  | 142       | True                     | True                  | True                   | 7                    | 7                 | True             |
| X-n148-k46 | 147       | False                    | True                  | False                  | 0                    | 46                | False            |
| X-n153-k22 | 152       | False                    | True                  | False                  | 0                    | 22                | False            |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.000873 |
| OR-Tools route + VROOM allocation | 0.000000 | 0.000873 |
| VROOM route + VROOM allocation | 0.000873 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.000873 | 0.000000 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 8    | 8             | 8                | 0.3603        | 0.0000                        | 0.0009                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 8    | 8             | 8                | 0.3603        | 0.0000                        | 0.0009                     | 1.0000                | 0.0000             | 0.0000                         | 1.0000                    | 0.0000                               |
| VROOM route + VROOM allocation       | baseline      | 8    | 8             | 8                | 0.3606        | 0.0009                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 8    | 8             | 8                | 0.3606        | 0.0009                        | 0.0000                     | 0.0000                | 1.0000             | 0.0000                         | 1.0000                    | 0.0000                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.3627        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.3627        | 0.0000                         | 1.0000                    | 0.0000                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.3631        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.3631        | 0.0000                         | 1.0000                    | 0.0000                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.3625        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.3625        | 0.0000                         | 1.0000                    | 0.0000                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.3625        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.3625        | 0.0000                         | 1.0000                    | 0.0000                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.3613        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.3613        | 0.0000                         | 1.0000                    | 0.0000                               |
| cargo      | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.3619        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.3619        | 0.0000                         | 1.0000                    | 0.0000                               |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.3547        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.3547        | 0.0000                         | 1.0000                    | 0.0000                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.3551        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.3551        | 0.0000                         | 1.0000                    | 0.0000                               |

## Nedensellik Değerlendirmesi

Hibritler allocation kaynağına değil route kaynağına yakın kaldı. Ortalama allocation-source closer share 0.000, route-source closer share 1.000, movement fraction 0.000. Bu, load allocation'ın tek başına nedensel mekanizma olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 açık kalır: beş korelasyonel aday ve load-allocation müdahalesi kök nedeni kapatmadı. Routing algoritmasının daha ince topology/heuristic farkları araştırılmalıdır.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
