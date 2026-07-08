# Stockout Mechanism Diagnosis Report

## Test Edilen Hipotezler

1. Capacity utilization farki -> stockout farkini acikliyor mu?
2. Vehicle count / aktif rota sayisi farki -> stockout farkini acikliyor mu?

Bu turda route-level load allocation ve objective interaction test edilmedi; bunlar A.8'in kalan adaylari olarak bir sonraki tura birakildi.

## Veri Seti ve A.5 Kontrolu

Veri seti n=20; ancak mevcut repo icinde X/v3 secimi bulunmadigi icin hazir n=20 set kullanildi. Kategori auditinde %25 sinirini asan gruplar var. Bu nedenle sonuc A.5'in n, x-seviyesi, bootstrap ve leverage disiplinini uygular; fakat stratification maddesi icin sinirli okunmalidir.

| Category Type | Category      | Count | Total | Share  | A.5 <=25% |
| ------------- | ------------- | ----- | ----- | ------ | --------- |
| family        | A             | 4     | 20    | 0.2000 | True      |
| family        | B             | 4     | 20    | 0.2000 | True      |
| family        | E             | 3     | 20    | 0.1500 | True      |
| family        | P             | 9     | 20    | 0.4500 | False     |
| size_bucket   | large_51_99   | 8     | 20    | 0.4000 | False     |
| size_bucket   | medium_20_50  | 10    | 20    | 0.5000 | False     |
| size_bucket   | small_n_lt_20 | 2     | 20    | 0.1000 | True      |

## Capacity Utilization ve Vehicle Count Ciktilari

Capacity utilization rota bazinda `toplam rota talebi / arac kapasitesi` olarak hesaplandi; instance seviyesinde ortalama, varyans ve maksimum raporlandi.

| Instance  | Provider | Mean Util | Util Variance | Max Util | Active Vehicle Count |
| --------- | -------- | --------- | ------------- | -------- | -------------------- |
| A-n32-k5  | OR-Tools | 0.8200    | 0.0457        | 0.9400   | 5                    |
| A-n32-k5  | VROOM    | 0.8200    | 0.0457        | 0.9400   | 5                    |
| A-n33-k5  | OR-Tools | 0.8920    | 0.0072        | 0.9300   | 5                    |
| A-n33-k5  | VROOM    | 0.8920    | 0.0018        | 0.9400   | 5                    |
| A-n45-k6  | OR-Tools | 0.9883    | 0.0001        | 1.0000   | 6                    |
| A-n45-k6  | VROOM    | 0.9883    | 0.0001        | 1.0000   | 6                    |
| A-n60-k9  | OR-Tools | 0.9211    | 0.0112        | 1.0000   | 9                    |
| A-n60-k9  | VROOM    | 0.9211    | 0.0005        | 0.9400   | 9                    |
| B-n31-k5  | OR-Tools | 0.8240    | 0.0228        | 0.9400   | 5                    |
| B-n31-k5  | VROOM    | 0.8240    | 0.0224        | 0.9200   | 5                    |
| B-n34-k5  | OR-Tools | 0.9140    | 0.0017        | 0.9600   | 5                    |
| B-n34-k5  | VROOM    | 0.9140    | 0.0012        | 0.9400   | 5                    |
| B-n38-k6  | OR-Tools | 0.8533    | 0.0025        | 0.9400   | 6                    |
| B-n38-k6  | VROOM    | 0.8533    | 0.0032        | 0.9100   | 6                    |
| B-n78-k10 | OR-Tools | 0.9370    | 0.0003        | 0.9600   | 10                   |
| B-n78-k10 | VROOM    | 0.9370    | 0.0003        | 0.9600   | 10                   |
| E-n23-k3  | OR-Tools | 0.7547    | 0.0229        | 0.9111   | 3                    |
| E-n23-k3  | VROOM    | 0.7547    | 0.0325        | 0.9611   | 3                    |
| E-n51-k5  | OR-Tools | 0.9713    | 0.0014        | 1.0000   | 5                    |
| E-n51-k5  | VROOM    | 0.9713    | 0.0009        | 1.0000   | 5                    |
| E-n76-k7  | OR-Tools | 0.8857    | 0.0035        | 0.9273   | 7                    |
| E-n76-k7  | VROOM    | 0.8857    | 0.0053        | 0.9318   | 7                    |
| P-n16-k8  | OR-Tools | 0.8786    | 0.0016        | 0.9714   | 8                    |
| P-n16-k8  | VROOM    | 0.8786    | 0.0016        | 0.9714   | 8                    |
| P-n19-k2  | OR-Tools | 0.9688    | 0.0003        | 0.9812   | 2                    |
| P-n19-k2  | VROOM    | 0.9688    | 0.0003        | 0.9812   | 2                    |
| P-n20-k2  | OR-Tools | 0.9688    | 0.0013        | 0.9938   | 2                    |
| P-n20-k2  | VROOM    | 0.9688    | 0.0013        | 0.9938   | 2                    |
| P-n21-k2  | OR-Tools | 0.9313    | 0.0000        | 0.9313   | 2                    |
| P-n21-k2  | VROOM    | 0.9313    | 0.0000        | 0.9313   | 2                    |
| P-n50-k8  | OR-Tools | 0.9906    | 0.0003        | 1.0000   | 8                    |
| P-n50-k8  | VROOM    | 0.9906    | 0.0002        | 1.0000   | 8                    |
| P-n55-k7  | OR-Tools | 0.8756    | 0.0052        | 0.9412   | 7                    |
| P-n55-k7  | VROOM    | 0.8756    | 0.0104        | 0.9412   | 7                    |
| P-n60-k10 | OR-Tools | 0.9450    | 0.0039        | 1.0000   | 10                   |
| P-n60-k10 | VROOM    | 0.9450    | 0.0010        | 0.9833   | 10                   |
| P-n65-k10 | OR-Tools | 0.9377    | 0.0033        | 1.0000   | 10                   |
| P-n65-k10 | VROOM    | 0.9377    | 0.0025        | 1.0000   | 10                   |
| P-n76-k4  | OR-Tools | 0.9743    | 0.0006        | 0.9943   | 4                    |
| P-n76-k4  | VROOM    | 0.9743    | 0.0004        | 1.0000   | 4                    |

Aktif arac sayisi farki:

| Instance  | OR-Tools | VROOM | Diff |
| --------- | -------- | ----- | ---- |
| A-n32-k5  | 5        | 5     | 0    |
| A-n33-k5  | 5        | 5     | 0    |
| A-n45-k6  | 6        | 6     | 0    |
| A-n60-k9  | 9        | 9     | 0    |
| B-n31-k5  | 5        | 5     | 0    |
| B-n34-k5  | 5        | 5     | 0    |
| B-n38-k6  | 6        | 6     | 0    |
| B-n78-k10 | 10       | 10    | 0    |
| E-n23-k3  | 3        | 3     | 0    |
| E-n51-k5  | 5        | 5     | 0    |
| E-n76-k7  | 7        | 7     | 0    |
| P-n16-k8  | 8        | 8     | 0    |
| P-n19-k2  | 2        | 2     | 0    |
| P-n20-k2  | 2        | 2     | 0    |
| P-n21-k2  | 2        | 2     | 0    |
| P-n50-k8  | 8        | 8     | 0    |
| P-n55-k7  | 7        | 7     | 0    |
| P-n60-k10 | 10       | 10    | 0    |
| P-n65-k10 | 10       | 10    | 0    |
| P-n76-k4  | 4        | 4     | 0    |

## Bulgular

A.5 kurallari uygulandi: n<15 ise tani sinyali, x degiskeninde en az 3 farkli seviye yoksa korelasyon raporlanmadi, bootstrap CI sifiri kapsiyorsa "korelasyon yok" olarak isaretlendi.

| Domain     | Predictor          | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label           |
| ---------- | ------------------ | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------------ |
| atm        | Capacity Util Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| atm        | Vehicle Count Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| cargo      | Capacity Util Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| cargo      | Vehicle Count Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| cold_chain | Capacity Util Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| cold_chain | Vehicle Count Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| grocery    | Capacity Util Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |
| grocery    | Vehicle Count Diff | 20 | 1               |           |         |                  |                   | False            | insufficient_x_variation |

Bu kosuda 0 aday mekanizma satiri bulundu. 0 satirda bootstrap CI sifiri kapsadigi icin korelasyon yok dendi; 8 satirda x varyasyonu yetersiz oldugu icin korelasyon raporlanmadi.

Onemli teknik ayrim: mean utilization farkinin sifira dusmesi beklenebilir. Iki motor ayni toplam talebi ayni aktif arac sayisina boldugunde instance-level ortalama doluluk matematiksel olarak ayni kalir. Buna ragmen `Util Variance` ve `Max Util` satirlarinda farklar goruluyor; bu farklar bu turun mean-utilization hipotezinden cok route-level load allocation adayina aittir ve bir sonraki tani calismasinda ayrica test edilmelidir.

## Leverage Kontrolu

Cook's Distance kontrolunde 3x(4/n) esigini asan domine edici instance gorulmedi.

| Domain     | Predictor          | Instance  | Cook's Distance | Cook Threshold 4/n | Severe Threshold 3x | Severe Cook Flag |
| ---------- | ------------------ | --------- | --------------- | ------------------ | ------------------- | ---------------- |
| atm        | Capacity Util Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Capacity Util Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| atm        | Vehicle Count Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Capacity Util Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| cargo      | Vehicle Count Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Capacity Util Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| cold_chain | Vehicle Count Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Capacity Util Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | A-n32-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | A-n33-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | A-n45-k6  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | A-n60-k9  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | B-n31-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | B-n34-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | B-n38-k6  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | B-n78-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | E-n23-k3  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | E-n51-k5  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | E-n76-k7  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n16-k8  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n19-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n20-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n21-k2  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n50-k8  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n55-k7  |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n60-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n65-k10 |                 | 0.2000             | 0.6000              | False            |
| grocery    | Vehicle Count Diff | P-n76-k4  |                 | 0.2000             | 0.6000              | False            |

## A.8'in Guncellenmis Hali

Capacity utilization ve vehicle count farki da stockout siralamasini aciklamiyor. Kalan adaylar (load allocation, objective interaction) icin ayri calisma gerekir. A.8 acik kalmaya devam ediyor.

## Dogru Cumle

Bu n=20 tani kosusunda capacity utilization farki ve aktif arac sayisi farki, stockout siralamasinin motora gore neden degistigini A.5 standartlarinda aciklamadi.

## Henuz Dogru Olmayan Cumle

"Stockout siralamasinin motora gore degismesi capacity utilization farkindan veya aktif arac sayisi farkindan kaynaklanir."

## Sonraki Adim

Route-level load allocation farkini test eden bir sonraki tani calismasini kur: rota basina yuk payi, route-level shortfall contribution ve domain objective bilesenlerini OR-Tools/VROOM farki olarak olc.
