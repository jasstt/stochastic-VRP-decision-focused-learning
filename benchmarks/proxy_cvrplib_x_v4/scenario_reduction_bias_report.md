# Scenario Reduction Bias Report

## Bulgu

X40 setinden OR-Tools anchor-feasible 9 instance seçildi: 3 küçük, 3 orta, 3 büyük. Full LP planning history, X40 için 180 senaryodur; hızlı mod `limit=60` kullanır. Routing anchor ve evaluation senaryoları sabit tutuldu, sadece LP training senaryoları değiştirildi.

Instance bazında domain-maksimum göreli stockout sapması en fazla 1.88%; instance-ortalama göreli sapma ortalaması 0.67%. %5 eşiğini herhangi bir domain'de aşan instance sayısı: 0/9.

Sistematik yön: limited-full stockout farkı 25 domain-row'da pozitif, 10 domain-row'da negatif, 1 row'da sıfır; ortalama signed fark 0.002356.

Instance büyüklüğü korelasyonu: en güçlü tanı sinyali Mean_Abs_Stockout_Diff için r=0.378, p=0.318, bootstrap CI=[-0.192, 0.921], diagnostic signal only: n<15.

### Instance Özeti

| Instance | Customers | Size Bucket | Mean_Relative_Stockout_Diff | Max_Relative_Stockout_Diff | Mean_Signed_Stockout_Diff | Runtime Speedup | Exceeds 5pct Any Domain |
| --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 105 | small | 0.00178169 | 0.00308422 | 0.000285714 | 7.92806 | no |
| X-n120-k6 | 119 | small | 0.00214748 | 0.00487329 | 0.000672269 | 8.84214 | no |
| X-n143-k7 | 142 | small | 0.00540043 | 0.00921447 | -0.000246479 | 6.5517 | no |
| X-n157-k13 | 156 | medium | 0.00517141 | 0.0078239 | 0.0025 | 10.3087 | no |
| X-n190-k8 | 189 | medium | 0.0177105 | 0.0187902 | 0.00763228 | 7.85627 | no |
| X-n214-k11 | 213 | medium | 0.010567 | 0.0144045 | 0.00495305 | 9.28876 | no |
| X-n237-k14 | 236 | large | 0.00242525 | 0.00385962 | -0.00095339 | 8.82432 | no |
| X-n261-k13 | 260 | large | 0.00377242 | 0.00719601 | 0.001625 | 7.43334 | no |
| X-n284-k15 | 283 | large | 0.0113889 | 0.0130752 | 0.00473498 | 9.06771 | no |

### Korelasyonlar

| Metric | n | Unique X Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | A.5 Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mean_Relative_Stockout_Diff | 9 | 9 | 0.354291 | 0.354605 | -0.249399 | 0.945133 | diagnostic signal only: n<15 |
| Max_Relative_Stockout_Diff | 9 | 9 | 0.357564 | 0.340658 | -0.265649 | 0.906539 | diagnostic signal only: n<15 |
| Mean_Abs_Stockout_Diff | 9 | 9 | 0.378129 | 0.317642 | -0.19197 | 0.921153 | diagnostic signal only: n<15 |

## Güvenli Kullanım Kuralı

Hızlı mod güvenli: X40 üzerinde OR-Tools anchor-feasible, küçük/orta/büyük dengeli tanı koşularında her instance için domain-maksimum göreli stockout sapması %5'in altında kaldığında keşif ve debug koşularında `--lp-planning-scenario-limit 60` kullanılabilir. Full scenario zorunlu: final README/rapor sonuçları, yayınlanacak yüzdeler ve karar verdiren karşılaştırmalar.

## Üç Branch'e Etkisi

Bu test push öncesi altyapı kontrolüdür. Bias küçük ve sistematik görünmediği için üç branch'i bloke etmeye gerek yok. Yine de nihai README/rapor sayıları full scenario ile teyit edilmeli; hızlı mod sadece keşif, debug ve aday hipotez eleme için varsayılan olabilir.

## Doğru Cümle

`limit=60` hızlı modu bu 9-instance X40 tanı koşusunda büyük veya sistematik bir stockout bias üretmedi; ancak n=9 olduğu için bu bir kesin kanıt değil, pratik güvenlik sinyalidir.

## Henüz Doğru Olmayan Cümle

`limit=60` her instance ve her domain için full scenario yerine bilimsel olarak eşdeğerdir.
