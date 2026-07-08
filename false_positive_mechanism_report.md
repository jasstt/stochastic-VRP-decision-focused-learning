# False Positive Mechanism Report

## Bulgu

n=4 koşusundaki güçlü korelasyonu en çok sürükleyen instance `E-n13-k4`. Bu instance'ın ortalama leverage skoru 0.9602, maksimum Cook's Distance değeri 24.1195. Cook's Distance için pratik eşik `4/n = 1.0`; `E-n13-k4` dört domain'in 4/4'ünde bu eşiğin çok üstünde.

Mekanizma şu: n=4 verisinde iki instance (`A-n32-k5`, `P-n19-k2`) grouping exposure değerinde 0 noktasına oturuyor, `B-n31-k5` küçük bir x değeri veriyor, `E-n13-k4` ise tek yüksek-x nokta olarak aynı anda yüksek pozitif stockout farkı üretiyor. Bu yapı, özellikle n=4 gibi küçük örneklemde regresyon çizgisini tek bir yüksek-x/high-y noktasına bağlayıp sahte güçlü korelasyon yaratıyor.

### n=4 Influence Özeti

| Instance | mean_leverage | max_cooks_distance | mean_cooks_distance | high_cook_domains | mean_grouping_exposure | mean_stockout_diff |
| -------- | ------------- | ------------------ | ------------------- | ----------------- | ---------------------- | ------------------ |
| E-n13-k4 | 0.9602        | 24.1195            | 23.7137             | 4                 | 0.3333                 | 0.0723             |
| B-n31-k5 | 0.2586        | 0.3488             | 0.3430              | 0                 | 0.0772                 | 0.0004             |
| P-n19-k2 | 0.3906        | 0.2660             | 0.1528              | 0                 | 0.0000                 | 0.0032             |
| A-n32-k5 | 0.3906        | 0.1151             | 0.0912              | 0                 | 0.0000                 | 0.0016             |

### Leave-One-Out

`E-n13-k4` çıkarıldığında korelasyon sayısını mekanik olarak okumak doğru değil; kalan tasarımda sadece iki x seviyesi kalıyor ve yüksek-x bölgesi tamamen kayboluyor. Bu yüzden bazı domainlerde r değeri `-1` veya `1` gibi görünse bile bu istatistiksel kanıt değil, üç noktalı dejenere geometri.

| Domain     | Dropped Instance | n remaining | unique x remaining | Pearson r after drop | Pearson p after drop | Full n4 r | Full n4 p | Degenerate Design | Note                                     |
| ---------- | ---------------- | ----------- | ------------------ | -------------------- | -------------------- | --------- | --------- | ----------------- | ---------------------------------------- |
| atm        | E-n13-k4         | 3           | 2                  | -1.0000              | 0.0000               | 0.9609    | 0.0391    | True              | only one non-zero grouping level remains |
| cargo      | E-n13-k4         | 3           | 2                  | 1.0000               | 0.0000               | 0.9826    | 0.0174    | True              | only one non-zero grouping level remains |
| cold_chain | E-n13-k4         | 3           | 2                  | -0.7952              | 0.4148               | 0.9335    | 0.0665    | True              | only one non-zero grouping level remains |
| grocery    | E-n13-k4         | 3           | 2                  | -1.0000              | 0.0000               | 0.9711    | 0.0289    | True              | only one non-zero grouping level remains |

## Instance Büyüklüğü Testi

n=20 setinde stratum sonuçları küçük instance hipotezini tek başına doğrulamıyor. Katı `n<20` küçük stratumunda yalnızca 2 instance var ve grouping exposure x değeri değişmediği için korelasyon hesaplanamıyor. Orta ve büyük stratumlar ise ters yönlü davranıyor: orta stratum çoğunlukla negatif, büyük stratum çoğunlukla pozitif ama p-value'lar genel olarak güçlü değil.

| Domain     | Size Stratum  | Instance Count | Pearson r | p-value | Mean Grouping Exposure Diff | Mean Signed Stockout Diff | Interpretable |
| ---------- | ------------- | -------------- | --------- | ------- | --------------------------- | ------------------------- | ------------- |
| atm        | small_n_lt_20 | 2              |           |         | 0.0000                      | 0.0000                    | False         |
| atm        | medium_20_50  | 10             | -0.4797   | 0.1606  | 0.1872                      | -0.0031                   | True          |
| atm        | large_51_99   | 8              | 0.5814    | 0.1307  | 0.2828                      | -0.0037                   | True          |
| cargo      | small_n_lt_20 | 2              |           |         | 0.0000                      | 0.0000                    | False         |
| cargo      | medium_20_50  | 10             | -0.5055   | 0.1361  | 0.1872                      | -0.0028                   | True          |
| cargo      | large_51_99   | 8              | 0.4763    | 0.2328  | 0.2828                      | -0.0028                   | True          |
| cold_chain | small_n_lt_20 | 2              |           |         | 0.0000                      | 0.0092                    | False         |
| cold_chain | medium_20_50  | 10             | -0.3915   | 0.2632  | 0.1872                      | -0.0010                   | True          |
| cold_chain | large_51_99   | 8              | 0.5703    | 0.1399  | 0.2828                      | -0.0028                   | True          |
| grocery    | small_n_lt_20 | 2              |           |         | 0.0000                      | 0.0000                    | False         |
| grocery    | medium_20_50  | 10             | -0.6822   | 0.0298  | 0.1872                      | -0.0034                   | True          |
| grocery    | large_51_99   | 8              | 0.4909    | 0.2167  | 0.2828                      | -0.0047                   | True          |

## n=4 ile n20 Geri Kalanı Karşılaştırması

n=20 geri kalanında max grouping exposure yüksek kalmasına rağmen signed stockout farkı aynı yönde büyümüyor. Bu, n=4 sinyalinin genel bir exposure mekanizması değil, orijinal küçük setteki nokta yerleşiminden kaynaklanan bir regresyon yanılsaması olduğunu destekliyor.

| Set                       | Domain     | Instances | Pearson r | p-value | Mean x | Mean y  | Max x  | Max y  |
| ------------------------- | ---------- | --------- | --------- | ------- | ------ | ------- | ------ | ------ |
| n20_overlap_with_original | atm        | 3         | -1.0000   | 0.0000  | 0.0257 | -0.0013 | 0.0772 | 0.0000 |
| n20_remainder             | atm        | 17        | -0.0662   | 0.8007  | 0.2386 | -0.0034 | 0.4286 | 0.0071 |
| original_n4               | atm        | 4         | 0.9609    | 0.0391  | 0.1026 | 0.0175  | 0.3333 | 0.0737 |
| n20_overlap_with_original | cargo      | 3         | 1.0000    | 0.0000  | 0.0257 | 0.0013  | 0.0772 | 0.0038 |
| n20_remainder             | cargo      | 17        | -0.0632   | 0.8095  | 0.2386 | -0.0032 | 0.4286 | 0.0128 |
| original_n4               | cargo      | 4         | 0.9826    | 0.0174  | 0.1026 | 0.0210  | 0.3333 | 0.0800 |
| n20_overlap_with_original | cold_chain | 3         | -0.7952   | 0.4148  | 0.0257 | 0.0071  | 0.0772 | 0.0128 |
| n20_remainder             | cold_chain | 17        | -0.0944   | 0.7185  | 0.2386 | -0.0021 | 0.4286 | 0.0125 |
| original_n4               | cold_chain | 4         | 0.9335    | 0.0665  | 0.1026 | 0.0211  | 0.3333 | 0.0633 |
| n20_overlap_with_original | grocery    | 3         | -1.0000   | 0.0000  | 0.0257 | -0.0002 | 0.0772 | 0.0000 |
| n20_remainder             | grocery    | 17        | -0.1581   | 0.5444  | 0.2386 | -0.0041 | 0.4286 | 0.0063 |
| original_n4               | grocery    | 4         | 0.9711    | 0.0289  | 0.1026 | 0.0179  | 0.3333 | 0.0721 |

## Metodolojik Ders

n=4 gibi çok küçük örneklemlerde tek bir instance istatistiksel sonucu domine edebilir. Bu sadece bu VRP benchmarkı için değil, projenin diğer iddiaları için de geçerli: quantum/klasik kıyas, stochastic loading, OSRM etkisi veya domain adapter etkisi fark etmez; örneklem küçükse bir problem ailesi, bir kapasite baskısı seviyesi veya tek bir uç instance tüm sonucu taşıyabilir. Bu yüzden küçük örneklem sonuçları "kanıt" değil, en fazla hipotez üretici tanı sinyali olarak yazılmalı.

## Doğru Cümle

n=4 koşusundaki güçlü `grouping exposure -> stockout` korelasyonu, esas olarak `E-n13-k4` instance'ının yüksek leverage/Cook's Distance etkisi ve kalan üç noktanın zayıf x çeşitliliği tarafından üretilmiş bir küçük örneklem yanılsamasıdır.

## Sonraki Adım

Instance seçimi yaparken minimum örneklem büyüklüğü kuralı uygulanmalı: tek bir kategoriden, örneğin çok küçük/çok büyük instance'lardan gelen örnek sayısı toplam örneklemin %25'ini geçmemeli. Ayrıca her stratumda en az 5 instance ve en az 3 farklı grouping exposure seviyesi yoksa domain bazlı Pearson korelasyonu iddia olarak sunulmamalı.
