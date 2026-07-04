# Ordering vs Grouping Divergence Report

## Ayrıştırılmış Bulgu

Grouping divergence ve ordering divergence ayrı metriklere bölündü. Ordering divergence yalnızca OR-Tools ve VROOM'da aynı rota grubunda kalan müşteri çiftleri üzerinden hesaplandı; farklı rotaya düşen çiftler bu hesaba dahil edilmedi.

| Instance  | Grouping Divergence | Ordering Divergence | Kendall Tau | Common Co-route Pairs |
| --------- | ------------------- | ------------------- | ----------- | --------------------- |
| A-n32-k5  | 0.0000              | 0.6250              | -0.2500     | 96                    |
| A-n33-k5  | 0.6190              | 0.6458              | -0.2917     | 48                    |
| A-n45-k6  | 0.6742              | 0.6806              | -0.3611     | 72                    |
| A-n60-k9  | 0.8048              | 0.4912              | 0.0175      | 57                    |
| B-n31-k5  | 0.6752              | 0.1053              | 0.7895      | 38                    |
| B-n34-k5  | 0.3884              | 0.8514              | -0.7027     | 74                    |
| B-n38-k6  | 0.3719              | 0.3421              | 0.3158      | 76                    |
| B-n78-k10 | 0.6634              | 0.3043              | 0.3913      | 138                   |
| E-n23-k3  | 0.2435              | 1.0000              | -1.0000     | 87                    |
| E-n51-k5  | 0.7218              | 0.5446              | -0.0891     | 101                   |
| E-n76-k7  | 0.4277              | 0.4542              | 0.0916      | 273                   |
| P-n16-k8  | 0.0000              | 0.2500              | 0.5000      | 8                     |
| P-n19-k2  | 0.0000              | 0.5000              | 0.0000      | 72                    |
| P-n20-k2  | 0.0000              | 0.5556              | -0.1111     | 81                    |
| P-n21-k2  | 0.0000              | 0.3956              | 0.2088      | 91                    |
| P-n50-k8  | 0.6853              | 0.3387              | 0.3226      | 62                    |
| P-n55-k7  | 0.4421              | 0.2667              | 0.4667      | 135                   |
| P-n60-k10 | 0.7686              | 0.7500              | -0.5000     | 56                    |
| P-n65-k10 | 0.6968              | 0.5476              | -0.0952     | 84                    |
| P-n76-k4  | 0.6823              | 0.2178              | 0.5644      | 326                   |

Beklenen ara bulgu doğrulandı: `A-n32-k5` ve `P-n19-k2` için grouping divergence 0.0, fakat ordering divergence sıfır değil. Yani aynı müşteri grupları korunabiliyor ama rota içi ziyaret sırası değişebiliyor.

Domain başına stockout farkı ile korelasyonlar:

| Domain     | n  | Grouping r | Grouping p-value | Ordering r | Ordering p-value | Grouping abs r | Grouping abs p-value | Ordering abs r | Ordering abs p-value | Stronger Abs Metric |
| ---------- | -- | ---------- | ---------------- | ---------- | ---------------- | -------------- | -------------------- | -------------- | -------------------- | ------------------- |
| atm        | 20 | 0.1052     | 0.6589           | 0.1037     | 0.6635           | 0.1832         | 0.4396               | -0.0335        | 0.8886               | grouping            |
| cargo      | 20 | 0.1772     | 0.4547           | 0.0033     | 0.9889           | 0.2624         | 0.2637               | 0.0059         | 0.9804               | grouping            |
| cold_chain | 20 | 0.0994     | 0.6768           | 0.0008     | 0.9974           | -0.0476        | 0.8420               | 0.2164         | 0.3595               | ordering            |
| grocery    | 20 | 0.0984     | 0.6797           | -0.0221    | 0.9264           | 0.1217         | 0.6092               | 0.0387         | 0.8714               | grouping            |

Cold-chain özelinde:

- grouping abs r = -0.0476, p = 0.8420
- ordering abs r = 0.2164, p = 0.3595
- daha güçlü mutlak ilişki: `ordering`

Bu sonuç cold-chain için "ordering grouping'den daha açıklayıcıdır" hipotezini bu 4 instance üzerinde desteklemiyor. Hatta mutlak stockout farkında grouping korelasyonu daha güçlü görünüyor. Ancak n=4 olduğu için bu kesin sonuç değildir.

## Exposure Rank Kaynağı

Exposure rank farkı iki kaynağa ayrıldı:

- `Exposure Rank Diff From Grouping`: farklı rotaya atanan müşteriler
- `Exposure Rank Diff From Ordering`: aynı rotada kalıp rota içi pozisyonu değişen müşteriler

| Instance  | Domain     | Exposure Rank Diff From Grouping | Grouping Customer Count | Exposure Rank Diff From Ordering | Ordering Customer Count | Exposure Rank Diff Other |
| --------- | ---------- | -------------------------------- | ----------------------- | -------------------------------- | ----------------------- | ------------------------ |
| A-n32-k5  | atm        |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5  | cargo      |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5  | cold_chain |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5  | grocery    |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n33-k5  | atm        | 0.3044                           | 32                      |                                  | 0                       |                          |
| A-n33-k5  | cargo      | 0.3044                           | 32                      |                                  | 0                       |                          |
| A-n33-k5  | cold_chain | 0.3044                           | 32                      |                                  | 0                       |                          |
| A-n33-k5  | grocery    | 0.3044                           | 32                      |                                  | 0                       |                          |
| A-n45-k6  | atm        | 0.3520                           | 44                      |                                  | 0                       |                          |
| A-n45-k6  | cargo      | 0.3520                           | 44                      |                                  | 0                       |                          |
| A-n45-k6  | cold_chain | 0.3520                           | 44                      |                                  | 0                       |                          |
| A-n45-k6  | grocery    | 0.3520                           | 44                      |                                  | 0                       |                          |
| A-n60-k9  | atm        | 0.2262                           | 59                      |                                  | 0                       |                          |
| A-n60-k9  | cargo      | 0.2262                           | 59                      |                                  | 0                       |                          |
| A-n60-k9  | cold_chain | 0.2262                           | 59                      |                                  | 0                       |                          |
| A-n60-k9  | grocery    | 0.2262                           | 59                      |                                  | 0                       |                          |
| B-n31-k5  | atm        | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5  | cargo      | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5  | cold_chain | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5  | grocery    | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n34-k5  | atm        | 0.3887                           | 25                      | 0.1914                           | 8                       |                          |
| B-n34-k5  | cargo      | 0.3887                           | 25                      | 0.1914                           | 8                       |                          |
| B-n34-k5  | cold_chain | 0.3887                           | 25                      | 0.1914                           | 8                       |                          |
| B-n34-k5  | grocery    | 0.3887                           | 25                      | 0.1914                           | 8                       |                          |
| B-n38-k6  | atm        | 0.1082                           | 29                      | 0.1111                           | 2                       | 0.0972                   |
| B-n38-k6  | cargo      | 0.1082                           | 29                      | 0.1111                           | 2                       | 0.0972                   |
| B-n38-k6  | cold_chain | 0.1082                           | 29                      | 0.1111                           | 2                       | 0.0972                   |
| B-n38-k6  | grocery    | 0.1082                           | 29                      | 0.1111                           | 2                       | 0.0972                   |
| B-n78-k10 | atm        | 0.2496                           | 67                      |                                  | 0                       | 0.0513                   |
| B-n78-k10 | cargo      | 0.2496                           | 67                      |                                  | 0                       | 0.0513                   |
| B-n78-k10 | cold_chain | 0.2496                           | 67                      |                                  | 0                       | 0.0513                   |
| B-n78-k10 | grocery    | 0.2496                           | 67                      |                                  | 0                       | 0.0513                   |
| E-n23-k3  | atm        | 0.4286                           | 22                      |                                  | 0                       |                          |
| E-n23-k3  | cargo      | 0.4286                           | 22                      |                                  | 0                       |                          |
| E-n23-k3  | cold_chain | 0.4286                           | 22                      |                                  | 0                       |                          |
| E-n23-k3  | grocery    | 0.4286                           | 22                      |                                  | 0                       |                          |
| E-n51-k5  | atm        | 0.3429                           | 50                      |                                  | 0                       |                          |
| E-n51-k5  | cargo      | 0.3429                           | 50                      |                                  | 0                       |                          |
| E-n51-k5  | cold_chain | 0.3429                           | 50                      |                                  | 0                       |                          |
| E-n51-k5  | grocery    | 0.3429                           | 50                      |                                  | 0                       |                          |
| E-n76-k7  | atm        | 0.3092                           | 75                      |                                  | 0                       |                          |
| E-n76-k7  | cargo      | 0.3092                           | 75                      |                                  | 0                       |                          |
| E-n76-k7  | cold_chain | 0.3092                           | 75                      |                                  | 0                       |                          |
| E-n76-k7  | grocery    | 0.3092                           | 75                      |                                  | 0                       |                          |
| P-n16-k8  | atm        |                                  | 0                       | 0.3214                           | 4                       | 0.0390                   |
| P-n16-k8  | cargo      |                                  | 0                       | 0.3214                           | 4                       | 0.0390                   |
| P-n16-k8  | cold_chain |                                  | 0                       | 0.3214                           | 4                       | 0.0390                   |
| P-n16-k8  | grocery    |                                  | 0                       | 0.3214                           | 4                       | 0.0390                   |
| P-n19-k2  | atm        |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2  | cargo      |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2  | cold_chain |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2  | grocery    |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n20-k2  | atm        |                                  | 0                       | 0.5444                           | 10                      | 0.0123                   |
| P-n20-k2  | cargo      |                                  | 0                       | 0.5444                           | 10                      | 0.0123                   |
| P-n20-k2  | cold_chain |                                  | 0                       | 0.5444                           | 10                      | 0.0123                   |
| P-n20-k2  | grocery    |                                  | 0                       | 0.5444                           | 10                      | 0.0123                   |
| P-n21-k2  | atm        |                                  | 0                       | 0.5066                           | 8                       | 0.0132                   |
| P-n21-k2  | cargo      |                                  | 0                       | 0.5066                           | 8                       | 0.0132                   |
| P-n21-k2  | cold_chain |                                  | 0                       | 0.5066                           | 8                       | 0.0132                   |
| P-n21-k2  | grocery    |                                  | 0                       | 0.5066                           | 8                       | 0.0132                   |
| P-n50-k8  | atm        | 0.2126                           | 49                      |                                  | 0                       |                          |
| P-n50-k8  | cargo      | 0.2126                           | 49                      |                                  | 0                       |                          |
| P-n50-k8  | cold_chain | 0.2126                           | 49                      |                                  | 0                       |                          |
| P-n50-k8  | grocery    | 0.2126                           | 49                      |                                  | 0                       |                          |
| P-n55-k7  | atm        | 0.1995                           | 40                      | 0.4969                           | 6                       | 0.0590                   |
| P-n55-k7  | cargo      | 0.1995                           | 40                      | 0.4969                           | 6                       | 0.0590                   |
| P-n55-k7  | cold_chain | 0.1995                           | 40                      | 0.4969                           | 6                       | 0.0590                   |
| P-n55-k7  | grocery    | 0.1995                           | 40                      | 0.4969                           | 6                       | 0.0590                   |
| P-n60-k10 | atm        | 0.3425                           | 59                      |                                  | 0                       |                          |
| P-n60-k10 | cargo      | 0.3425                           | 59                      |                                  | 0                       |                          |
| P-n60-k10 | cold_chain | 0.3425                           | 59                      |                                  | 0                       |                          |
| P-n60-k10 | grocery    | 0.3425                           | 59                      |                                  | 0                       |                          |
| P-n65-k10 | atm        | 0.3194                           | 64                      |                                  | 0                       |                          |
| P-n65-k10 | cargo      | 0.3194                           | 64                      |                                  | 0                       |                          |
| P-n65-k10 | cold_chain | 0.3194                           | 64                      |                                  | 0                       |                          |
| P-n65-k10 | grocery    | 0.3194                           | 64                      |                                  | 0                       |                          |
| P-n76-k4  | atm        | 0.2728                           | 75                      |                                  | 0                       |                          |
| P-n76-k4  | cargo      | 0.2728                           | 75                      |                                  | 0                       |                          |
| P-n76-k4  | cold_chain | 0.2728                           | 75                      |                                  | 0                       |                          |
| P-n76-k4  | grocery    | 0.2728                           | 75                      |                                  | 0                       |                          |

Exposure kaynakları ile stockout farkı korelasyonları:

| Domain     | Grouping Exposure r | Grouping Exposure p-value | Ordering Exposure r | Ordering Exposure p-value | Grouping Exposure abs r | Grouping Exposure abs p-value | Ordering Exposure abs r | Ordering Exposure abs p-value | Stronger Abs Exposure Source |
| ---------- | ------------------- | ------------------------- | ------------------- | ------------------------- | ----------------------- | ----------------------------- | ----------------------- | ----------------------------- | ---------------------------- |
| atm        | -0.1114             | 0.6399                    | -0.1529             | 0.5200                    | 0.3507                  | 0.1295                        | -0.0414                 | 0.8623                        | grouping                     |
| cargo      | -0.1328             | 0.5767                    | -0.2081             | 0.3787                    | 0.3813                  | 0.0971                        | -0.0902                 | 0.7053                        | grouping                     |
| cold_chain | -0.2364             | 0.3155                    | -0.1111             | 0.6409                    | 0.3063                  | 0.1890                        | 0.1451                  | 0.5418                        | grouping                     |
| grocery    | -0.2201             | 0.3512                    | -0.1572             | 0.5080                    | 0.3693                  | 0.1091                        | 0.0107                  | 0.9644                        | grouping                     |

Cold-chain exposure kaynağı özelinde:

- grouping exposure abs r = 0.3063, p = 0.1890
- ordering exposure abs r = 0.1451, p = 0.5418
- daha güçlü kaynak: `grouping`

## Model Tasarımından Kaynaklanan Beklenen Sonuçlar

Grocery ve cold-chain adapter'ları aynı route feature tablosunu alıyor, fakat objective içinde aynı feature'ları kullanmıyor:

| Domain     | Uses arrival_exposure_rank | Uses route_features directly | Feature summary                                                                |
| ---------- | -------------------------- | ---------------------------- | ------------------------------------------------------------------------------ |
| grocery    | False                      | False                        | uses demand/distance criticality and distance_rank; no direct exposure feature |
| cold_chain | True                       | True                         | uses arrival_exposure_rank in perishability and load_penalty                   |

`grocery` objective'i `arrival_exposure_rank` kullanmıyor. Bu nedenle grocery'nin ordering/exposure divergence'a doğrudan hassas olmaması bug değil; model tasarımından kaynaklanan beklenen sonuçtur. Grocery stockout değişiyorsa bu daha çok rota kapasite gruplaması ve load allocation üzerinden dolaylı gelir.

`cold_chain` objective'i `arrival_exposure_rank` değerini hem `perishability` hem de `load_penalty` içinde kullanıyor. Bu yüzden exposure/order değişimine hassas olması beklenir; fakat bu küçük örneklemde stockout değil, load-penalty maliyeti tarafında daha görünür olabilir.

## Veriden Çıkan Gerçek Sinyal

Bu koşuda 3 domain'de grouping metriği, 1 domain'de ordering metriği daha güçlü çıktı; 0 domain'de eşitlik görüldü. Cold-chain için de grouping metriği ordering metriğinden daha güçlü göründü. Bu, önceki "route-exposure domain'ler ordering'e daha hassastır" beklentisini n=4 üzerinde doğrulamıyor.

## Doğru Cümle

Grouping ve ordering divergence ayrı etkiler üretir; aynı müşteri grupları korunsa bile rota içi sıra değişimi exposure_rank'i değiştirebilir. Ancak bu 4 instance üzerinde stockout farkını açıklamada ordering divergence'ın grouping divergence'dan genel olarak daha güçlü olduğu gözlemlenmemiştir.

## Henüz Doğru Olmayan Cümle

Cold-chain stockout'u routing motoru değişiminde esas olarak ordering divergence tarafından açıklanır.

## Sonraki Adım

15-20 instance'a çıkarken grouping divergence ve ordering divergence ayrı raporlanmalı. Tek bir "divergence" skoruna geri dönülmemeli. Cold-chain için ayrıca stockout yanında `mean_load_penalty_loss` korelasyonu da hesaplanmalı; çünkü exposure etkisi stokout'tan çok bozulma/kalite maliyetinde görünür olabilir.

Not: n=4 olduğu için tüm Pearson p-value'ları düşük istatistiksel güçle okunmalıdır; bu rapor kesin kanıt değil, tanı analizidir.
