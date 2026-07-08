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
| X-n251-k28 | 250       | True                     | True                  | True                   | 28                   | 28                | True             |
| X-n256-k16 | 255       | False                    | False                 | False                  | 0                    | 0                 | False            |
| X-n261-k13 | 260       | True                     | True                  | True                   | 13                   | 13                | True             |
| X-n266-k58 | 265       | False                    | False                 | False                  | 0                    | 0                 | False            |

## Müdahale Sonucu

| Senaryo | Stockout (gerçek OR-Tools'a benzerlik) | Stockout (gerçek VROOM'a benzerlik) |
|---|---:|---:|
| OR-Tools route + OR-Tools allocation | 0.000000 | 0.013949 |
| OR-Tools route + VROOM allocation | 0.003269 | 0.015757 |
| VROOM route + VROOM allocation | 0.013949 | 0.000000 |
| VROOM route + OR-Tools allocation | 0.001680 | 0.004656 |

Ayrıntılı scenario özeti:

| Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Mean Abs Distance to OR-Tools | Mean Abs Distance to VROOM | OR-Tools Closer Share | VROOM Closer Share | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ----------------------------- | -------------------------- | --------------------- | ------------------ | ------------------------------ | ------------------------- | ------------------------------------ |
| OR-Tools route + OR-Tools allocation | baseline      | 8    | 8             | 8                | 0.4406        | 0.0000                        | 0.0139                     | 1.0000                | 0.0000             | 1.0000                         | 1.0000                    |                                      |
| OR-Tools route + VROOM allocation    | intervention  | 8    | 8             | 8                | 0.4373        | 0.0033                        | 0.0158                     | 0.7500                | 0.2500             | 0.2500                         | 0.7500                    | 0.1560                               |
| VROOM route + VROOM allocation       | baseline      | 8    | 8             | 8                | 0.4453        | 0.0139                        | 0.0000                     | 0.0000                | 1.0000             | 1.0000                         | 1.0000                    |                                      |
| VROOM route + OR-Tools allocation    | intervention  | 8    | 7             | 7                | 0.4477        | 0.0017                        | 0.0047                     | 0.5714                | 0.4286             | 0.5714                         | 0.4286                    | 0.8192                               |

Domain bazlı özet:

| Domain     | Scenario                             | Scenario Type | Rows | Feasible Rows | Informative Rows | Mean Stockout | Allocation Source Closer Share | Route Source Closer Share | Mean Movement Fraction to Allocation |
| ---------- | ------------------------------------ | ------------- | ---- | ------------- | ---------------- | ------------- | ------------------------------ | ------------------------- | ------------------------------------ |
| atm        | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4534        | 1.0000                         | 1.0000                    |                                      |
| atm        | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4532        | 0.0000                         | 1.0000                    | 0.0093                               |
| atm        | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4470        | 1.0000                         | 1.0000                    |                                      |
| atm        | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4535        | 0.5000                         | 0.5000                    | 0.5312                               |
| grocery    | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4528        | 1.0000                         | 1.0000                    |                                      |
| grocery    | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4516        | 0.5000                         | 0.5000                    | 0.3487                               |
| grocery    | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4457        | 1.0000                         | 1.0000                    |                                      |
| grocery    | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4500        | 0.5000                         | 0.5000                    | 1.1870                               |
| cargo      | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4099        | 1.0000                         | 1.0000                    |                                      |
| cargo      | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.3998        | 0.0000                         | 1.0000                    | -0.1387                              |
| cargo      | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4472        | 1.0000                         | 1.0000                    |                                      |
| cargo      | VROOM route + OR-Tools allocation    | intervention  | 2    | 1             | 1                | 0.4335        | 0.0000                         | 1.0000                    | 0.0000                               |
| cold_chain | OR-Tools route + OR-Tools allocation | baseline      | 2    | 2             | 2                | 0.4464        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | OR-Tools route + VROOM allocation    | intervention  | 2    | 2             | 2                | 0.4447        | 0.5000                         | 0.5000                    | 0.4046                               |
| cold_chain | VROOM route + VROOM allocation       | baseline      | 2    | 2             | 2                | 0.4414        | 1.0000                         | 1.0000                    |                                      |
| cold_chain | VROOM route + OR-Tools allocation    | intervention  | 2    | 2             | 2                | 0.4468        | 1.0000                         | 0.0000                    | 1.1492                               |

## Nedensellik Değerlendirmesi

Müdahale sonucu karışık çıktı. Ortalama allocation-source closer share 0.411, route-source closer share 0.589, movement fraction 0.488. Bu, load allocation'ın kısmi etkisi olabileceğini ama tek faktör olarak yeterli açıklama olmadığını gösterir.

Bu değerlendirme `r` veya p-value kullanmaz. Ana ölçü, hibrit stockout'un route kaynağına mı yoksa allocation kaynağına mı daha yakın olduğudur.

## A.8'in Nihai Durumu

A.8 kısmen açık kalır: load allocation etkili bir mekanizma olabilir, fakat route topology veya solver heuristic farklarıyla birlikte çalışıyor gibi görünmektedir.

## Doğru Cümle

Müdahale hibritleri ortalamada route kaynağına daha yakın kaldı; load allocation tek başına nedensel açıklama değildir.

## Henüz Doğru Olmayan Cümle

Load allocation, her domain ve her instance için tek başına stockout farkını tamamen belirler.

## Sonraki Adım

Müdahale sonucu kısmi veya belirsiz kaldıysa, sıradaki test route topology'nin daha ince özelliklerini ayırmalıdır: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, first-improvement/best-improvement benzeri solver heuristic farkları ve route-level marginal capacity slack birlikte ölçülmelidir.
