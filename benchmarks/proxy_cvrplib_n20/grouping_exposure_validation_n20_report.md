# Grouping Exposure Validation n20 Report

## n=4 -> n=20 Karşılaştırması

Bu rapor, `exposure_rank_diff_from_grouping -> stockout_diff` ilişkisini 20 coordinate-capable CVRPLIB instance üzerinde yeniden test eder. `stockout_diff`, OR-Tools stockout minus VROOM stockout olarak hesaplandı. n=4 sonuçları geçmiş küçük koşudan, n=20 sonuçları yeni validation setinden alınmıştır.

| Domain     | n4 r   | n4 p   | n20 n | n20 r   | n20 p  | Direction preserved? | n20 mean grouping exposure diff | n20 mean signed stockout diff |
| ---------- | ------ | ------ | ----- | ------- | ------ | -------------------- | ------------------------------- | ----------------------------- |
| atm        | 0.9609 | 0.0391 | 20    | -0.1114 | 0.6399 | no                   | 0.2067                          | -0.0030                       |
| cargo      | 0.9826 | 0.0174 | 20    | -0.1328 | 0.5767 | no                   | 0.2067                          | -0.0025                       |
| cold_chain | 0.9335 | 0.0665 | 20    | -0.2364 | 0.3155 | no                   | 0.2067                          | -0.0007                       |
| grocery    | 0.9711 | 0.0289 | 20    | -0.2201 | 0.3512 | no                   | 0.2067                          | -0.0036                       |

Yön koruması: 0/4 domain.

## Bootstrap Güven Aralıkları

Her domain için Pearson r, 1000 bootstrap resample ile %95 güven aralığına alındı.

| Domain     | n  | Observed r | Observed p-value | Bootstrap CI low | Bootstrap CI high | Valid bootstrap samples | CI contains zero | Interpretation                            |
| ---------- | -- | ---------- | ---------------- | ---------------- | ----------------- | ----------------------- | ---------------- | ----------------------------------------- |
| atm        | 20 | -0.1114    | 0.6399           | -0.5002          | 0.2196            | 1000                    | True             | correlation not distinguishable from zero |
| cargo      | 20 | -0.1328    | 0.5767           | -0.5051          | 0.1830            | 1000                    | True             | correlation not distinguishable from zero |
| cold_chain | 20 | -0.2364    | 0.3155           | -0.6136          | 0.1387            | 1000                    | True             | correlation not distinguishable from zero |
| grocery    | 20 | -0.2201    | 0.3512           | -0.5775          | 0.0511            | 1000                    | True             | correlation not distinguishable from zero |

## Doğru Cümle

Grouping-kaynaklı exposure rank farkı ile stockout arasındaki ilişki n=20 koşusunda kesin istatistiksel destek kazanmadı; bootstrap %95 güven aralıkları sıfırı içeriyor.

## Henüz Doğru Olmayan Cümle

Bu bulgu farklı VRP problem ailelerine genellenir. Bu hâlâ doğru değil; VRPTW, multi-depot, pickup-delivery ve gerçek yol zamanı belirsizliği ayrı test edilmedi.

## Sonraki Adım

Öncelik artık bu iddiayı büyütmek değil, n=4 koşusundaki güçlü p-value'ların neden şiştiğini açıklamak olmalı. Bunun için instance ailesi, kapasite baskısı ve signed/absolute stockout farkı ayrı ayrı stratify edilmeli. Cold-chain için stockout yanında `mean_load_penalty_loss` korelasyonu ayrıca test edilmeli.
