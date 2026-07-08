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
| X-n233-k16 | 232       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n237-k14 | 236       | True                     | True                  | True                   | 14                   | 14                | True             |
| X-n242-k48 | 241       | True                     | True                  | True                   | 48                   | 48                | True             |
| X-n247-k50 | 246       | False                    | True                  | False                  | 0                    | 50                | False            |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.003062 |
| OR-Tools route + VROOM allocation | 0.006233 | 0.007727 |
| VROOM route + VROOM allocation | 0.003062 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.013774 | 0.011799 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 8    | 8             | 8                | 0.4714        | 0.0000                        | 0.0031                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 8    | 8             | 8                | 0.4669        | 0.0062                        | 0.0077                     | 0.7500                | 0.2500             | 0.2500                         | 0.7500                    | -1.2298                              |
| VROOM route + VROOM allocation       | baseline      | 8    | 8             | 8                | 0.4745        | 0.0031                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 8    | 8             | 8                | 0.4627        | 0.0138                        | 0.0118                     | 0.3750                | 0.6250             | 0.3750                         | 0.6250                    | 11.6074                              |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4737        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4741        | 0.5000                         | 0.5000                    | 0.5860                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4765        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4612        | 0.5000                         | 0.5000                    | 35.9660                              |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4723        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4726        | 0.0000                         | 1.0000                    | 0.0946                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4743        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4742        | 0.0000                         | 1.0000                    | 0.0338                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4696        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4503        | 0.0000                         | 1.0000                    | -6.7498                              |
| cargo      | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4767        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4450        | 0.5000                         | 0.5000                    | 10.2011                              |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4700        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4705        | 0.5000                         | 0.5000                    | 1.1500                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4704        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4703        | 0.5000                         | 0.5000                    | 0.2286                               |

## Nedensellik Değerlendirmesi

Müdahale sonucu karışık çıktı. Ortalama allocation-source closer share 0.312, route-source closer share 0.688, movement fraction 5.189. Bu, load allocation'ın kısmi etkisi olabileceğini ama tek faktör olarak yeterli açıklama olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 kısmen açık kalır: load allocation etkili bir mekanizma olabilir, fakat route topology veya solver heuristic farklarıyla birlikte çalışıyor gibi görünmektedir.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
