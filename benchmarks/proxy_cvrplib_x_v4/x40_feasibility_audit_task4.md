# X40 Feasibility Audit - Task 4

Bu denetim ana robust-route-selection runner çıktısına dokunmadan, X40 manifest ve önceki causal-test audit kayıtları üzerinden çalıştırıldı.

## Bulgu

- Instance sayısı: 40
- Önceki OR-Tools anchor-feasible olmayan instance: 13
- En az bir generated route candidate deterministik capacity precheck ile elenecek instance: 40
- Risk dağılımı: high=16, medium=24, low=0
- Önemli ayrım: proxy/quantile/robust unscaled planların kapasiteyi aşması beklenen bir davranış; runner bunları görünür bırakıp ayrıca scaled rescue plan ekliyor. Bu yüzden tek başına unscaled candidate infeasibility, domain etkisi değildir.

## High Risk Instance List

| Instance | Customers | Vehicles | Nominal Load Ratio | Generated Candidates | Deterministic Candidate Failures | Nontrivial Candidates After Precheck | Prev OR-Tools Anchor Feasible | Capacity Pressure Risk | Route Solver Risk | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n270-k35 | 269 | 35 | 0.9973 | 11 | 5 | 6 | False | high | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995; large instance >=250 customers |
| X-n256-k16 | 255 | 16 | 0.9956 | 11 | 5 | 6 | False | high | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995; large instance >=250 customers |
| X-n233-k16 | 232 | 16 | 0.9997 | 11 | 5 | 6 | False | high | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995 |
| X-n195-k51 | 194 | 51 | 0.9975 | 11 | 5 | 6 | False | high | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995; very high vehicle count |
| X-n101-k25 | 100 | 25 | 0.9994 | 11 | 5 | 6 | False | high | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995 |
| X-n266-k58 | 265 | 58 | 0.9926 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98; very high vehicle count; large instance >=250 customers |
| X-n247-k50 | 246 | 50 | 0.9254 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; very high vehicle count |
| X-n200-k36 | 199 | 36 | 0.9856 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n176-k26 | 175 | 26 | 0.9837 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n172-k51 | 171 | 51 | 0.9855 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98; very high vehicle count |
| X-n153-k22 | 152 | 22 | 0.9684 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n148-k46 | 147 | 46 | 0.9867 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n125-k30 | 124 | 30 | 0.9816 | 11 | 5 | 6 | False | medium | high | previous OR-Tools anchor infeasible; 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n219-k73 | 218 | 73 | 0.9954 | 11 | 5 | 6 | True | high | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995; very high vehicle count |
| X-n214-k11 | 213 | 11 | 0.9973 | 11 | 5 | 6 | True | high | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995 |
| X-n157-k13 | 156 | 13 | 1.0000 | 11 | 5 | 6 | True | high | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.995 |

## Medium Risk Instance List

| Instance | Customers | Vehicles | Nominal Load Ratio | Generated Candidates | Deterministic Candidate Failures | Nontrivial Candidates After Precheck | Prev OR-Tools Anchor Feasible | Capacity Pressure Risk | Route Solver Risk | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n284-k15 | 283 | 15 | 0.9339 | 11 | 5 | 6 | True | medium | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; large instance >=250 customers |
| X-n280-k17 | 279 | 17 | 0.9905 | 11 | 5 | 6 | True | medium | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98; large instance >=250 customers |
| X-n275-k28 | 274 | 28 | 0.9786 | 11 | 5 | 6 | True | medium | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; large instance >=250 customers |
| X-n261-k13 | 260 | 13 | 0.9522 | 11 | 5 | 6 | True | medium | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; large instance >=250 customers |
| X-n251-k28 | 250 | 28 | 0.9664 | 11 | 5 | 6 | True | medium | medium | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; large instance >=250 customers |
| X-n242-k48 | 241 | 48 | 0.9851 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n237-k14 | 236 | 14 | 0.9365 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n228-k23 | 227 | 23 | 0.9819 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n223-k34 | 222 | 34 | 0.9809 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n209-k16 | 208 | 16 | 0.9573 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n204-k19 | 203 | 19 | 0.9528 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n190-k8 | 189 | 8 | 0.9447 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n186-k15 | 185 | 15 | 0.9482 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n181-k23 | 180 | 23 | 0.9783 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n167-k10 | 166 | 10 | 0.9293 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n162-k11 | 161 | 11 | 0.9442 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n143-k7 | 142 | 7 | 0.8974 | 11 | 4 | 7 | True | medium | low | 4/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n139-k10 | 138 | 10 | 0.9802 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n134-k13 | 133 | 13 | 0.9834 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated; nominal fleet load ratio >=0.98 |
| X-n129-k18 | 128 | 18 | 0.9473 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n120-k6 | 119 | 6 | 0.9444 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n115-k10 | 114 | 10 | 0.9083 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n110-k13 | 109 | 13 | 0.9510 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |
| X-n106-k14 | 105 | 14 | 0.9362 | 11 | 5 | 6 | True | medium | low | 5/11 generated route candidates fail deterministic capacity precheck; 5 scaled rescue plans generated |

## OR-Tools-only Confound Değerlendirmesi

VROOM kullanılmaması doğru izolasyon: provider farkı, route grouping/order/provider heuristic confoundu ve lokal VROOM servis erişimi devreden çıkıyor. Bu koşudan çıkacak bulgular solver-agnostic değil; doğru cümle OR-Tools route candidate pool üzerinde domain-aware selection bulgusudur.

## X40 Koşusu Sonrası Sanity Checks

1. `robust_route_candidates.csv` içinde deterministic capacity precheck ile elenen unscaled planları beklenen elenme olarak ayır; bunları domain objective başarısızlığı gibi yorumlama.
2. High-risk listedeki önceki OR-Tools anchor-infeasible instance’larda scaled rescue planların route üretip üretmediğini ayrıca kontrol et.
3. `robust_route_candidate_results.csv` içinde route-feasible fakat LP-infeasible satırları ayır; bunlar kapasite precheck değil stochastic LP/domain objective kaynaklıdır.
4. `robust_route_winners.csv` high-risk instance içeriyorsa, winner planının unscaled overloaded plan olmadığını doğrula; öyleyse audit veya runner bug olabilir.
5. `robust_route_winner_full_confirmation.csv` içinde high-risk ve medium-risk winner’lar için `Metric Stability Safe` ve `Strict Stability Safe` oranlarını ayrı raporla.
6. Domain winner diversity hesabını all-set ve anchor-feasible subset olarak iki kez ver; aksi halde route infeasibility domain diversity sinyalini şişirebilir.
