# Route Grouping Sensitivity Report

## Bulgu

Route grouping farki ile stockout degisimi arasinda net ama zayif-orneklemli bir yon sinyali gozlemlendi. En onemli sinir: n=4 instance. Bu nedenle sonucu istatistiksel kanit olarak degil, hipotez olusturan bir tani testi olarak okumak gerekir.

Route grouping divergence:

| Instance | Divergence Score |
| -------- | ---------------- |
| A-n32-k5 | 0.0000           |
| B-n31-k5 | 0.6752           |
| E-n13-k4 | 0.8095           |
| P-n19-k2 | 0.0000           |

Exposure rank farki domain bazinda ayni cikti, cunku mevcut adapter'lar ayni route feature uretimini paylasiyor. Cold-chain bu feature'i objective icinde dogrudan kullaniyor; grocery ise mevcut implementasyonda exposure rank'i dogrudan kullanmiyor.

Onemli ayrim: `A-n32-k5` ve `P-n19-k2` icin grouping divergence 0.0 cikti, fakat exposure rank diff sifir degil. Bu, iki motorun ayni musteri gruplarini koruyup rota icindeki ziyaret sirasini degistirebildigini gosterir. Dolayisiyla route grouping divergence tek basina cold-chain etkisini aciklamaya yetmez; route order / exposure divergence da ayrica izlenmelidir.

| Instance | Domain     | Avg Rank Diff | Std Dev |
| -------- | ---------- | ------------- | ------- |
| A-n32-k5 | atm        | 0.2409        | 0.2684  |
| A-n32-k5 | cargo      | 0.2409        | 0.2684  |
| A-n32-k5 | cold_chain | 0.2409        | 0.2684  |
| A-n32-k5 | grocery    | 0.2409        | 0.2684  |
| B-n31-k5 | atm        | 0.0644        | 0.0843  |
| B-n31-k5 | cargo      | 0.0644        | 0.0843  |
| B-n31-k5 | cold_chain | 0.0644        | 0.0843  |
| B-n31-k5 | grocery    | 0.0644        | 0.0843  |
| E-n13-k4 | atm        | 0.3333        | 0.2462  |
| E-n13-k4 | cargo      | 0.3333        | 0.2462  |
| E-n13-k4 | cold_chain | 0.3333        | 0.2462  |
| E-n13-k4 | grocery    | 0.3333        | 0.2462  |
| P-n19-k2 | atm        | 0.2810        | 0.3403  |
| P-n19-k2 | cargo      | 0.2810        | 0.3403  |
| P-n19-k2 | cold_chain | 0.2810        | 0.3403  |
| P-n19-k2 | grocery    | 0.2810        | 0.3403  |

Pearson korelasyonlari:

| Domain     | n | Pearson r (signed) | p-value (signed) | Pearson r (abs) | p-value (abs) | Mean Abs Stockout Diff |
| ---------- | - | ------------------ | ---------------- | --------------- | ------------- | ---------------------- |
| atm        | 4 | 0.6401             | 0.3599           | 0.7121          | 0.2879        | 0.0194                 |
| cargo      | 4 | 0.7094             | 0.2906           | 0.7094          | 0.2906        | 0.0210                 |
| cold_chain | 4 | 0.5784             | 0.4216           | 0.5784          | 0.4216        | 0.0211                 |
| grocery    | 4 | 0.6699             | 0.3301           | 0.6827          | 0.3173        | 0.0182                 |

Domain hassasiyeti, ortalama mutlak stockout farkina gore. `High divergence`, instance divergence skorunun medyan veya ustunde oldugu durumlar olarak tanimlandi:

| Domain     | avg_abs_stockout_diff | avg_abs_stockout_diff_high_divergence | max_abs_stockout_diff |
| ---------- | --------------------- | ------------------------------------- | --------------------- |
| cargo      | 0.0210                | 0.0419                                | 0.0800                |
| atm        | 0.0194                | 0.0388                                | 0.0737                |
| grocery    | 0.0182                | 0.0364                                | 0.0721                |
| cold_chain | 0.0211                | 0.0328                                | 0.0633                |

En guclu mutlak korelasyon `atm` domain'inde goruldu: r=0.7121, p=0.2879. p-value n=4 nedeniyle guvenilir karar siniri olarak kullanilmamalidir.

High-divergence instance'larda mutlak stockout hassasiyeti sirasi:

```text
cargo > atm > grocery > cold_chain
```

Beklenti cold_chain/grocery > cargo/atm idi. Veri bunu tam dogrulamadi. Bu kosuda en hassas domain'ler `atm` ve `cargo` tarafina kaydi; cold_chain orta seviyede, grocery en dusuk seviyede kaldi. Bunun nedeni, mevcut grocery objective'inin route exposure'i dogrudan kullanmamasi ve cold_chain'in exposure'a duyarli olsa da load-penalty uzerinden farki daha cok maliyete yansitmasi olabilir. Yani route grouping farki stockout'u etkiliyor, ancak etki beklenen domain siralamasini otomatik uretmiyor.

## Doğru Cümle

Route grouping farki ile stockout degisimi arasinda zayif/orta duzeyde bir iliski gozlemlenmistir, ancak n=4 instance ile bu istatistiksel olarak kesin degildir.

## Henüz Doğru Olmayan Cümle

Route-exposure'a bagimli domain'ler motora karsi her zaman daha hassastir.

## Sonraki Adım

Bu hipotezi dogrulamak icin en az 15-20 instance ile ayni analiz tekrarlanmali. Ek olarak, route grouping divergence ile route order/exposure divergence ayrilmali; cunku ayni musteri gruplari korunsa bile ziyaret sirasi degisince cold_chain gibi domain'lerde load-penalty ve stockout davranisi degisebilir.
