# Load Allocation Diagnosis Report

## X Dataset Genişlemesi Durumu

X dataset genişlemesi bu turda gerçekten çalıştırıldı: 24 CVRPLIB X instance indirildi, `vrplib` ile doğrulandı, proxy dataset üretildi ve OR-Tools + VROOM + 4 domain koşuları alındı.

Ortak provider-feasible instance sayısı load-allocation/stockout korelasyonu için 16 oldu:

```text
X-n106-k14, X-n110-k13, X-n115-k10, X-n120-k6, X-n129-k18, X-n134-k13, X-n157-k13, X-n162-k11, X-n167-k10, X-n181-k23, X-n190-k8, X-n223-k34, X-n228-k23, X-n237-k14, X-n242-k48, X-n251-k28
```

Bu n>=15 eşiğini karşılıyor, fakat tüm indirilen 24 instance'ın 8'i OR-Tools tarafında anchor-feasible olmadı. Bu nedenle sonuçlar "X indirilen set" ve "ortak feasible analiz seti" diye ayrı okunmalı.

A.5'in n, en az 3 x-seviyesi, bootstrap CI ve Cook's Distance kontrolleri uygulandı. X24 seçimi 8/8/8 small/medium/large olarak dengeli kuruldu; ancak üç bucket'lı bir tasarımda "her kategori <=%25" kuralı kelimesi kelimesine sağlanamaz. Bu kural literal uygulanacaksa sonraki X turu 4 boyut bucket'ı ve 28 instance ile tasarlanmalı.

## Load Allocation Hipotezi

Her rota için `sum(demands[n] for n in route) / capacity` vektörü çıkarıldı. Sonra provider başına Gini coefficient ve rota yük varyansı hesaplandı.

| Instance   | Provider | Gini Coefficient | Load Variance | Mean Load Util | Max Load Util | Active Vehicle Count | Feasible |
| ---------- | -------- | ---------------- | ------------- | -------------- | ------------- | -------------------- | -------- |
| X-n101-k25 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n101-k25 | VROOM    |                  | 0.0000        |                |               | 0                    | False    |
| X-n106-k14 | OR-Tools | 0.0508           | 0.0153        | 0.9362         | 1.0000        | 14                   | True     |
| X-n106-k14 | VROOM    | 0.0539           | 0.0250        | 0.9362         | 1.0000        | 14                   | True     |
| X-n110-k13 | OR-Tools | 0.0349           | 0.0093        | 0.9510         | 1.0000        | 13                   | True     |
| X-n110-k13 | VROOM    | 0.0420           | 0.0163        | 0.9510         | 1.0000        | 13                   | True     |
| X-n115-k10 | OR-Tools | 0.0560           | 0.0098        | 0.9083         | 1.0000        | 10                   | True     |
| X-n115-k10 | VROOM    | 0.0664           | 0.0186        | 0.9083         | 1.0000        | 10                   | True     |
| X-n120-k6  | OR-Tools | 0.0490           | 0.0185        | 0.9444         | 1.0000        | 6                    | True     |
| X-n120-k6  | VROOM    | 0.0434           | 0.0094        | 0.9444         | 1.0000        | 6                    | True     |
| X-n125-k30 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n125-k30 | VROOM    | 0.0109           | 0.0005        | 0.9816         | 1.0000        | 30                   | True     |
| X-n129-k18 | OR-Tools | 0.0505           | 0.0347        | 0.9473         | 1.0000        | 18                   | True     |
| X-n129-k18 | VROOM    | 0.0510           | 0.0349        | 0.9473         | 1.0000        | 18                   | True     |
| X-n134-k13 | OR-Tools | 0.0078           | 0.0002        | 0.9834         | 1.0000        | 13                   | True     |
| X-n134-k13 | VROOM    | 0.0079           | 0.0002        | 0.9834         | 1.0000        | 13                   | True     |
| X-n153-k22 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n153-k22 | VROOM    | 0.0278           | 0.0062        | 0.9684         | 1.0000        | 22                   | True     |
| X-n157-k13 | OR-Tools | 0.0000           | 0.0000        | 1.0000         | 1.0000        | 13                   | True     |
| X-n157-k13 | VROOM    | 0.0000           | 0.0000        | 1.0000         | 1.0000        | 13                   | True     |
| X-n162-k11 | OR-Tools | 0.0341           | 0.0075        | 0.9442         | 0.9966        | 11                   | True     |
| X-n162-k11 | VROOM    | 0.0430           | 0.0152        | 0.9442         | 1.0000        | 11                   | True     |
| X-n167-k10 | OR-Tools | 0.0586           | 0.0199        | 0.9293         | 1.0000        | 10                   | True     |
| X-n167-k10 | VROOM    | 0.0634           | 0.0350        | 0.9293         | 1.0000        | 10                   | True     |
| X-n172-k51 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n172-k51 | VROOM    | 0.0090           | 0.0003        | 0.9855         | 1.0000        | 51                   | True     |
| X-n176-k26 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n176-k26 | VROOM    | 0.0128           | 0.0014        | 0.9837         | 1.0000        | 26                   | True     |
| X-n181-k23 | OR-Tools | 0.0203           | 0.0052        | 0.9783         | 1.0000        | 23                   | True     |
| X-n181-k23 | VROOM    | 0.0198           | 0.0038        | 0.9783         | 1.0000        | 23                   | True     |
| X-n190-k8  | OR-Tools | 0.0435           | 0.0096        | 0.9447         | 1.0000        | 8                    | True     |
| X-n190-k8  | VROOM    | 0.0473           | 0.0136        | 0.9447         | 1.0000        | 8                    | True     |
| X-n223-k34 | OR-Tools | 0.0159           | 0.0021        | 0.9809         | 1.0000        | 34                   | True     |
| X-n223-k34 | VROOM    | 0.0159           | 0.0017        | 0.9809         | 1.0000        | 34                   | True     |
| X-n228-k23 | OR-Tools | 0.0146           | 0.0013        | 0.9819         | 1.0000        | 23                   | True     |
| X-n228-k23 | VROOM    | 0.0145           | 0.0014        | 0.9819         | 1.0000        | 23                   | True     |
| X-n233-k16 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n233-k16 | VROOM    |                  | 0.0000        |                |               | 0                    | False    |
| X-n237-k14 | OR-Tools | 0.0630           | 0.0564        | 0.9365         | 1.0000        | 14                   | True     |
| X-n237-k14 | VROOM    | 0.0630           | 0.0564        | 0.9365         | 1.0000        | 14                   | True     |
| X-n242-k48 | OR-Tools | 0.0140           | 0.0040        | 0.9851         | 1.0000        | 48                   | True     |
| X-n242-k48 | VROOM    | 0.0145           | 0.0055        | 0.9851         | 1.0000        | 48                   | True     |
| X-n247-k50 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n247-k50 | VROOM    | 0.0573           | 0.0131        | 0.9254         | 1.0000        | 50                   | True     |
| X-n251-k28 | OR-Tools | 0.0218           | 0.0042        | 0.9664         | 1.0000        | 28                   | True     |
| X-n251-k28 | VROOM    | 0.0259           | 0.0041        | 0.9664         | 1.0000        | 28                   | True     |
| X-n256-k16 | OR-Tools |                  | 0.0000        |                |               | 0                    | False    |
| X-n256-k16 | VROOM    |                  | 0.0000        |                |               | 0                    | False    |

OR-Tools - VROOM farkları:

| Instance   | Common Route Feasible | Gini Diff | Load Variance Diff | Mean Load Util Diff | Active Vehicle Count Diff |
| ---------- | --------------------- | --------- | ------------------ | ------------------- | ------------------------- |
| X-n101-k25 | False                 |           |                    |                     | 0                         |
| X-n106-k14 | True                  | -0.0031   | -0.0097            | 0.0000              | 0                         |
| X-n110-k13 | True                  | -0.0072   | -0.0070            | 0.0000              | 0                         |
| X-n115-k10 | True                  | -0.0104   | -0.0087            | 0.0000              | 0                         |
| X-n120-k6  | True                  | 0.0056    | 0.0091             | 0.0000              | 0                         |
| X-n125-k30 | False                 |           |                    |                     | -30                       |
| X-n129-k18 | True                  | -0.0005   | -0.0002            | 0.0000              | 0                         |
| X-n134-k13 | True                  | -0.0001   | -0.0000            | 0.0000              | 0                         |
| X-n153-k22 | False                 |           |                    |                     | -22                       |
| X-n157-k13 | True                  | 0.0000    | 0.0000             | 0.0000              | 0                         |
| X-n162-k11 | True                  | -0.0089   | -0.0077            | 0.0000              | 0                         |
| X-n167-k10 | True                  | -0.0049   | -0.0150            | 0.0000              | 0                         |
| X-n172-k51 | False                 |           |                    |                     | -51                       |
| X-n176-k26 | False                 |           |                    |                     | -26                       |
| X-n181-k23 | True                  | 0.0005    | 0.0014             | 0.0000              | 0                         |
| X-n190-k8  | True                  | -0.0038   | -0.0040            | 0.0000              | 0                         |
| X-n223-k34 | True                  | 0.0000    | 0.0004             | 0.0000              | 0                         |
| X-n228-k23 | True                  | 0.0001    | -0.0001            | 0.0000              | 0                         |
| X-n233-k16 | False                 |           |                    |                     | 0                         |
| X-n237-k14 | True                  | 0.0000    | 0.0000             | 0.0000              | 0                         |
| X-n242-k48 | True                  | -0.0004   | -0.0015            | 0.0000              | 0                         |
| X-n247-k50 | False                 |           |                    |                     | -50                       |
| X-n251-k28 | True                  | -0.0041   | 0.0001             | 0.0000              | 0                         |
| X-n256-k16 | False                 |           |                    |                     | 0                         |

Domain bazlı korelasyonlar:

| Domain     | Predictor          | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label      |
| ---------- | ------------------ | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------- |
| atm        | Gini Diff          | 16 | 15              | 0.8845    | 0.0000  | 0.7210           | 0.9663            | False            | candidate_mechanism |
| atm        | Load Variance Diff | 16 | 15              | 0.9114    | 0.0000  | 0.8473           | 0.9918            | False            | candidate_mechanism |
| cargo      | Gini Diff          | 16 | 15              | 0.8213    | 0.0001  | 0.5121           | 0.9413            | False            | candidate_mechanism |
| cargo      | Load Variance Diff | 16 | 15              | 0.8555    | 0.0000  | 0.7118           | 0.9595            | False            | candidate_mechanism |
| cold_chain | Gini Diff          | 16 | 15              | 0.8992    | 0.0000  | 0.7118           | 0.9792            | False            | candidate_mechanism |
| cold_chain | Load Variance Diff | 16 | 15              | 0.9121    | 0.0000  | 0.8503           | 0.9885            | False            | candidate_mechanism |
| grocery    | Gini Diff          | 16 | 15              | 0.9023    | 0.0000  | 0.7384           | 0.9766            | False            | candidate_mechanism |
| grocery    | Load Variance Diff | 16 | 15              | 0.9048    | 0.0000  | 0.8375           | 0.9926            | False            | candidate_mechanism |

Load allocation icin aday mekanizma sinyali bulundu. Bu satirlar once baska X secimleri ve route time-limit duyarliligi ile dogrulanmali.

## Leverage Kontrolü

Cook's Distance kontrolunde 3x(4/n) esigini asan instance'lar var; leave-one-out sonucu asagida.

| Domain     | Predictor          | Instance   | Cook's Distance | Cook Threshold 4/n | Severe Threshold 3x | Severe Cook Flag |
| ---------- | ------------------ | ---------- | --------------- | ------------------ | ------------------- | ---------------- |
| atm        | Gini Diff          | X-n115-k10 | 0.4907          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n167-k10 | 0.2766          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n110-k13 | 0.1491          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n162-k11 | 0.1489          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n251-k28 | 0.1387          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n106-k14 | 0.0317          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n120-k6  | 0.0272          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n181-k23 | 0.0208          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n242-k48 | 0.0171          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n129-k18 | 0.0118          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n190-k8  | 0.0068          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n237-k14 | 0.0020          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n134-k13 | 0.0015          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n228-k23 | 0.0001          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n223-k34 | 0.0001          | 0.2500             | 0.7500              | False            |
| atm        | Gini Diff          | X-n157-k13 | 0.0000          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n115-k10 | 0.9363          | 0.2500             | 0.7500              | True             |
| atm        | Load Variance Diff | X-n167-k10 | 0.2520          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n120-k6  | 0.1836          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n106-k14 | 0.1615          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n181-k23 | 0.0197          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n162-k11 | 0.0166          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n129-k18 | 0.0154          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n110-k13 | 0.0132          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n134-k13 | 0.0056          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n228-k23 | 0.0017          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n242-k48 | 0.0015          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n157-k13 | 0.0014          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n190-k8  | 0.0013          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n223-k34 | 0.0005          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n251-k28 | 0.0001          | 0.2500             | 0.7500              | False            |
| atm        | Load Variance Diff | X-n237-k14 | 0.0001          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n115-k10 | 0.4189          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n110-k13 | 0.2206          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n167-k10 | 0.1308          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n228-k23 | 0.1172          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n251-k28 | 0.0911          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n181-k23 | 0.0680          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n162-k11 | 0.0462          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n120-k6  | 0.0389          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n242-k48 | 0.0345          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n190-k8  | 0.0273          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n129-k18 | 0.0193          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n106-k14 | 0.0184          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n134-k13 | 0.0047          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n223-k34 | 0.0022          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n157-k13 | 0.0001          | 0.2500             | 0.7500              | False            |
| cargo      | Gini Diff          | X-n237-k14 | 0.0000          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n115-k10 | 0.5975          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n167-k10 | 0.2702          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n228-k23 | 0.0988          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n106-k14 | 0.0916          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n181-k23 | 0.0729          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n110-k13 | 0.0547          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n129-k18 | 0.0230          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n162-k11 | 0.0204          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n190-k8  | 0.0185          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n242-k48 | 0.0135          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n134-k13 | 0.0024          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n120-k6  | 0.0024          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n223-k34 | 0.0019          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n157-k13 | 0.0014          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n251-k28 | 0.0008          | 0.2500             | 0.7500              | False            |
| cargo      | Load Variance Diff | X-n237-k14 | 0.0004          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n115-k10 | 0.3269          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n167-k10 | 0.2755          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n110-k13 | 0.2022          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n251-k28 | 0.1750          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n162-k11 | 0.0574          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n106-k14 | 0.0302          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n228-k23 | 0.0174          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n157-k13 | 0.0132          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n129-k18 | 0.0120          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n237-k14 | 0.0036          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n120-k6  | 0.0020          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n190-k8  | 0.0009          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n242-k48 | 0.0008          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n223-k34 | 0.0005          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n134-k13 | 0.0001          | 0.2500             | 0.7500              | False            |
| cold_chain | Gini Diff          | X-n181-k23 | 0.0001          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n115-k10 | 0.8051          | 0.2500             | 0.7500              | True             |
| cold_chain | Load Variance Diff | X-n167-k10 | 0.3677          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n106-k14 | 0.1867          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n162-k11 | 0.0647          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n120-k6  | 0.0562          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n228-k23 | 0.0358          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n110-k13 | 0.0185          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n129-k18 | 0.0146          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n157-k13 | 0.0055          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n242-k48 | 0.0052          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n223-k34 | 0.0016          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n181-k23 | 0.0011          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n251-k28 | 0.0010          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n134-k13 | 0.0006          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n190-k8  | 0.0006          | 0.2500             | 0.7500              | False            |
| cold_chain | Load Variance Diff | X-n237-k14 | 0.0003          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n115-k10 | 0.5479          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n167-k10 | 0.2240          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n110-k13 | 0.1855          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n251-k28 | 0.1726          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n162-k11 | 0.1189          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n106-k14 | 0.0351          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n129-k18 | 0.0108          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n242-k48 | 0.0099          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n181-k23 | 0.0081          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n228-k23 | 0.0063          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n190-k8  | 0.0057          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n237-k14 | 0.0049          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n157-k13 | 0.0046          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n134-k13 | 0.0031          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n120-k6  | 0.0014          | 0.2500             | 0.7500              | False            |
| grocery    | Gini Diff          | X-n223-k34 | 0.0000          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n115-k10 | 0.9121          | 0.2500             | 0.7500              | True             |
| grocery    | Load Variance Diff | X-n167-k10 | 0.5402          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n106-k14 | 0.1511          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n162-k11 | 0.0360          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n120-k6  | 0.0358          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n228-k23 | 0.0178          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n129-k18 | 0.0124          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n110-k13 | 0.0113          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n181-k23 | 0.0059          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n237-k14 | 0.0006          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n223-k34 | 0.0006          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n157-k13 | 0.0005          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n251-k28 | 0.0005          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n190-k8  | 0.0004          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n134-k13 | 0.0002          | 0.2500             | 0.7500              | False            |
| grocery    | Load Variance Diff | X-n242-k48 | 0.0000          | 0.2500             | 0.7500              | False            |

| Domain     | Predictor          | Dropped Instance | n  | Unique x Levels | Pearson r | p-value | Bootstrap CI Low | Bootstrap CI High | CI Contains Zero | Evidence Label      |
| ---------- | ------------------ | ---------------- | -- | --------------- | --------- | ------- | ---------------- | ----------------- | ---------------- | ------------------- |
| atm        | Load Variance Diff | X-n115-k10       | 15 | 14              | 0.9784    | 0.0000  | 0.9485           | 0.9941            | False            | candidate_mechanism |
| cold_chain | Load Variance Diff | X-n115-k10       | 15 | 14              | 0.9640    | 0.0000  | 0.9108           | 0.9931            | False            | candidate_mechanism |
| grocery    | Load Variance Diff | X-n115-k10       | 15 | 14              | 0.9733    | 0.0000  | 0.9359           | 0.9949            | False            | candidate_mechanism |

## A.8'in Şu Anki Durumu

Üç aday test edildi:

- Capacity utilization: açıklamadı; mean utilization farkı aynı toplam talep ve aynı araç sayısı nedeniyle tek seviyeye sıkıştı.
- Vehicle count: açıklamadı; önceki n20 koşusunda tüm ortak instance'larda araç sayısı aynıydı.
- Load allocation: aday mekanizma sinyali verdi.

A.8 kismen daraldi: load allocation en az bir domain/predictor kombinasyonunda aday mekanizma verdi, fakat objective interaction ayrica test edilmeden nihai neden denemez.

## Sonraki Adım

Aday load-allocation predictor'unu farkli route time-limitleri ve OSRM matrisiyle tekrar calistir; sonra objective interaction'i kontrol degiskeni olarak ekle.
