# Ordering vs Grouping Divergence Report

## Ayrıştırılmış Bulgu

Grouping divergence ve ordering divergence ayrı metriklere bölündü. Ordering divergence yalnızca OR-Tools ve VROOM'da aynı rota grubunda kalan müşteri çiftleri üzerinden hesaplandı; farklı rotaya düşen çiftler bu hesaba dahil edilmedi.

| Instance | Grouping Divergence | Ordering Divergence | Kendall Tau | Common Co-route Pairs |
| -------- | ------------------- | ------------------- | ----------- | --------------------- |
| A-n32-k5 | 0.0000              | 0.6250              | -0.2500     | 96                    |
| B-n31-k5 | 0.6752              | 0.1053              | 0.7895      | 38                    |
| E-n13-k4 | 0.8095              | 0.5000              | 0.0000      | 4                     |
| P-n19-k2 | 0.0000              | 0.5000              | 0.0000      | 72                    |

Beklenen ara bulgu doğrulandı: `A-n32-k5` ve `P-n19-k2` için grouping divergence 0.0, fakat ordering divergence sıfır değil. Yani aynı müşteri grupları korunabiliyor ama rota içi ziyaret sırası değişebiliyor.

Domain başına stockout farkı ile korelasyonlar:

| Domain     | n | Grouping r | Grouping p-value | Ordering r | Ordering p-value | Grouping abs r | Grouping abs p-value | Ordering abs r | Ordering abs p-value | Stronger Abs Metric |
| ---------- | - | ---------- | ---------------- | ---------- | ---------------- | -------------- | -------------------- | -------------- | -------------------- | ------------------- |
| atm        | 4 | 0.6401     | 0.3599           | 0.2446     | 0.7554           | 0.7121         | 0.2879               | 0.1512         | 0.8488               | grouping            |
| cargo      | 4 | 0.7094     | 0.2906           | 0.1550     | 0.8450           | 0.7094         | 0.2906               | 0.1550         | 0.8450               | grouping            |
| cold_chain | 4 | 0.5784     | 0.4216           | 0.2919     | 0.7081           | 0.5784         | 0.4216               | 0.2919         | 0.7081               | grouping            |
| grocery    | 4 | 0.6699     | 0.3301           | 0.2072     | 0.7928           | 0.6827         | 0.3173               | 0.1906         | 0.8094               | grouping            |

Cold-chain özelinde:

- grouping abs r = 0.5784, p = 0.4216
- ordering abs r = 0.2919, p = 0.7081
- daha güçlü mutlak ilişki: `grouping`

Bu sonuç cold-chain için "ordering grouping'den daha açıklayıcıdır" hipotezini bu 4 instance üzerinde desteklemiyor. Hatta mutlak stockout farkında grouping korelasyonu daha güçlü görünüyor. Ancak n=4 olduğu için bu kesin sonuç değildir.

## Exposure Rank Kaynağı

Exposure rank farkı iki kaynağa ayrıldı:

- `Exposure Rank Diff From Grouping`: farklı rotaya atanan müşteriler
- `Exposure Rank Diff From Ordering`: aynı rotada kalıp rota içi pozisyonu değişen müşteriler

| Instance | Domain     | Exposure Rank Diff From Grouping | Grouping Customer Count | Exposure Rank Diff From Ordering | Ordering Customer Count | Exposure Rank Diff Other |
| -------- | ---------- | -------------------------------- | ----------------------- | -------------------------------- | ----------------------- | ------------------------ |
| A-n32-k5 | atm        |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5 | cargo      |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5 | cold_chain |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| A-n32-k5 | grocery    |                                  | 0                       | 0.3417                           | 20                      | 0.0576                   |
| B-n31-k5 | atm        | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5 | cargo      | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5 | cold_chain | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| B-n31-k5 | grocery    | 0.0772                           | 25                      |                                  | 0                       | 0.0000                   |
| E-n13-k4 | atm        | 0.3333                           | 12                      |                                  | 0                       |                          |
| E-n13-k4 | cargo      | 0.3333                           | 12                      |                                  | 0                       |                          |
| E-n13-k4 | cold_chain | 0.3333                           | 12                      |                                  | 0                       |                          |
| E-n13-k4 | grocery    | 0.3333                           | 12                      |                                  | 0                       |                          |
| P-n19-k2 | atm        |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2 | cargo      |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2 | cold_chain |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |
| P-n19-k2 | grocery    |                                  | 0                       | 0.5882                           | 8                       | 0.0353                   |

Exposure kaynakları ile stockout farkı korelasyonları:

| Domain     | Grouping Exposure r | Grouping Exposure p-value | Ordering Exposure r | Ordering Exposure p-value | Grouping Exposure abs r | Grouping Exposure abs p-value | Ordering Exposure abs r | Ordering Exposure abs p-value | Stronger Abs Exposure Source |
| ---------- | ------------------- | ------------------------- | ------------------- | ------------------------- | ----------------------- | ----------------------------- | ----------------------- | ----------------------------- | ---------------------------- |
| atm        | 0.9609              | 0.0391                    | -0.5032             | 0.4968                    | 0.9834                  | 0.0166                        | -0.5780                 | 0.4220                        | grouping                     |
| cargo      | 0.9826              | 0.0174                    | -0.5751             | 0.4249                    | 0.9826                  | 0.0174                        | -0.5751                 | 0.4249                        | grouping                     |
| cold_chain | 0.9335              | 0.0665                    | -0.4082             | 0.5918                    | 0.9335                  | 0.0665                        | -0.4082                 | 0.5918                        | grouping                     |
| grocery    | 0.9711              | 0.0289                    | -0.5339             | 0.4661                    | 0.9751                  | 0.0249                        | -0.5473                 | 0.4527                        | grouping                     |

Cold-chain exposure kaynağı özelinde:

- grouping exposure abs r = 0.9335, p = 0.0665
- ordering exposure abs r = -0.4082, p = 0.5918
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

Bu koşuda 4 domain'de grouping metriği, 0 domain'de ordering metriği daha güçlü çıktı; 0 domain'de eşitlik görüldü. Cold-chain için de grouping metriği ordering metriğinden daha güçlü göründü. Bu, önceki "route-exposure domain'ler ordering'e daha hassastır" beklentisini n=4 üzerinde doğrulamıyor.

## Doğru Cümle

Grouping ve ordering divergence ayrı etkiler üretir; aynı müşteri grupları korunsa bile rota içi sıra değişimi exposure_rank'i değiştirebilir. Ancak bu 4 instance üzerinde stockout farkını açıklamada ordering divergence'ın grouping divergence'dan genel olarak daha güçlü olduğu gözlemlenmemiştir.

## Henüz Doğru Olmayan Cümle

Cold-chain stockout'u routing motoru değişiminde esas olarak ordering divergence tarafından açıklanır.

## Sonraki Adım

15-20 instance'a çıkarken grouping divergence ve ordering divergence ayrı raporlanmalı. Tek bir "divergence" skoruna geri dönülmemeli. Cold-chain için ayrıca stockout yanında `mean_load_penalty_loss` korelasyonu da hesaplanmalı; çünkü exposure etkisi stokout'tan çok bozulma/kalite maliyetinde görünür olabilir.

Not: n=4 olduğu için tüm Pearson p-value'ları düşük istatistiksel güçle okunmalıdır; bu rapor kesin kanıt değil, tanı analizidir.
