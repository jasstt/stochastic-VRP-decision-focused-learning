# Robust Route Selection Report

## Scope

This diagnostic evaluates multiple routing candidates with the same stochastic decision layer, then selects a domain-level winner by the configured score metric.

- Data dir: `benchmarks/proxy_cvrplib_x_v4`
- Routing providers: `ortools`
- LP backend: `pulp_cbc`
- LP planning scenario limit: `60`
- Score metric: `mean_domain_loss`
- Full-scenario winner confirmation: `True`

Fast mode is intended for route-candidate screening. Final decision-driving claims should be rerun with full planning history by passing `--lp-planning-scenario-limit 0`.

## Candidate Coverage

| Domain | Candidate_Rows | Feasible_Rows | Instances | Candidates | Median_Total_Runtime_Sec | Top_Winning_Candidate | Top_Winning_Provider | Top_Winning_Route_Plan | Top_Winner_Count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 384 | 175 | 24 | 16 | 5.00517 | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 5 |
| cargo | 384 | 175 | 24 | 16 | 5.00517 | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 4 |
| cold_chain | 384 | 175 | 24 | 16 | 5.00517 | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 4 |
| grocery | 384 | 175 | 24 | 16 | 5.00517 | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 3 |

## Winners

| Instance | Domain | Candidate | Routing Provider | Route Plan | Score Value | mean_total_cost | stockout_rate | Route Cost | Optimized Load Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 2748.29 | 30173.3 | 0.379714 | 27425 | 8400 |
| X-n106-k14 | cargo | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 2059.86 | 29484.9 | 0.377143 | 27425 | 8400 |
| X-n106-k14 | cold_chain | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 2788.62 | 31734.4 | 0.375524 | 27425 | 8350.39 |
| X-n106-k14 | grocery | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 1890.19 | 29315.2 | 0.378381 | 27425 | 8388.95 |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 364.182 | 16803.2 | 0.419358 | 16439 | 858 |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 274.381 | 16713.4 | 0.424128 | 16439 | 858 |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 340.688 | 16941.1 | 0.418073 | 16439 | 858 |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 234.909 | 16673.9 | 0.416606 | 16439 | 858 |
| X-n115-k10 | atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 777.64 | 14070.6 | 0.378333 | 13293 | 1690 |
| X-n115-k10 | cargo | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 582.54 | 13875.5 | 0.385439 | 13293 | 1690 |
| X-n115-k10 | cold_chain | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 776.701 | 14367.1 | 0.359737 | 13293 | 1690 |
| X-n115-k10 | grocery | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 522.253 | 13815.3 | 0.370789 | 13293 | 1690 |
| X-n120-k6 | atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 50.1802 | 14454.2 | 0.430756 | 14404 | 126 |
| X-n120-k6 | cargo | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 38.3938 | 14442.4 | 0.434958 | 14404 | 126 |
| X-n120-k6 | cold_chain | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 46.842 | 14473 | 0.435042 | 14404 | 123.989 |
| X-n120-k6 | grocery | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 32.5595 | 14436.6 | 0.433697 | 14404 | 124.732 |
| X-n129-k18 | atm | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 299.725 | 34098.7 | 0.415078 | 33799 | 702 |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 222.984 | 33980 | 0.407656 | 33757 | 702 |
| X-n129-k18 | cold_chain | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 284.215 | 34212.6 | 0.408281 | 33799 | 702 |
| X-n129-k18 | grocery | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 194.572 | 33993.6 | 0.415625 | 33799 | 702 |
| X-n134-k13 | atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 3793.49 | 16428.5 | 0.461278 | 12635 | 8359 |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 2783.17 | 18184.2 | 0.448647 | 15401 | 8359 |
| X-n134-k13 | cold_chain | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 3398.96 | 16959.8 | 0.456316 | 12210 | 8359 |
| X-n134-k13 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 2369.48 | 16878.5 | 0.462406 | 14509 | 8359 |
| X-n139-k10 | atm | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 427.495 | 16423.5 | 0.418261 | 15996 | 1060 |
| X-n139-k10 | cargo | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 320.999 | 16317 | 0.417391 | 15996 | 1060 |
| X-n139-k10 | cold_chain | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 399.625 | 16593.2 | 0.413841 | 15996 | 1060 |
| X-n139-k10 | grocery | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 276.552 | 16272.6 | 0.416812 | 15996 | 1060 |
| X-n143-k7 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 2511.61 | 20914.6 | 0.312113 | 18403 | 8330 |
| X-n143-k7 | cargo | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 1859.03 | 20309 | 0.307746 | 18450 | 8330 |
| X-n143-k7 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 2819.24 | 22514.4 | 0.302183 | 18166 | 8330 |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 1846.71 | 21882.7 | 0.306901 | 20036 | 8330 |
| X-n162-k11 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 4815.58 | 19614.6 | 0.400373 | 14799 | 12914 |
| X-n162-k11 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 3661.71 | 18460.7 | 0.408509 | 14799 | 12914 |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 4726.17 | 21918.5 | 0.394286 | 14799 | 12914 |
| X-n162-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 3213.92 | 18012.9 | 0.397578 | 14799 | 12914 |
| X-n167-k10 | atm | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 443.572 | 23001.6 | 0.376807 | 22558 | 1330 |
| X-n167-k10 | cargo | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 333.121 | 22891.1 | 0.376084 | 22558 | 1330 |
| X-n167-k10 | cold_chain | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 448.871 | 23249.6 | 0.371747 | 22558 | 1330 |
| X-n167-k10 | grocery | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 303.3 | 22861.3 | 0.37512 | 22558 | 1330 |
| X-n181-k23 | atm | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 75.5894 | 26330.6 | 0.426611 | 26255 | 184 |
| X-n181-k23 | cargo | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 57.4826 | 26312.5 | 0.428722 | 26255 | 184 |
| X-n181-k23 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 69.4089 | 26357.5 | 0.426111 | 26255 | 184 |
| X-n181-k23 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 48.367 | 26303.4 | 0.426389 | 26255 | 184 |
| X-n186-k15 | atm | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 5778.33 | 32244.3 | 0.38573 | 26466 | 14610 |
| X-n186-k15 | cargo | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 4391.59 | 30857.6 | 0.384324 | 26466 | 14610 |
| X-n186-k15 | cold_chain | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 5618.83 | 34772.9 | 0.383189 | 26466 | 14541.9 |
| X-n186-k15 | grocery | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 3839.99 | 30306 | 0.384811 | 26466 | 14581.7 |
| X-n190-k8 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 486.798 | 18833.8 | 0.420265 | 18347 | 1104 |
| X-n190-k8 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 366.357 | 18713.4 | 0.415926 | 18347 | 1104 |
| X-n190-k8 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 461.141 | 19023.4 | 0.411376 | 18347 | 1104 |
| X-n190-k8 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 316.536 | 18663.5 | 0.418519 | 18347 | 1104 |
| X-n204-k19 | atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 6612.44 | 28062.4 | 0.422956 | 21450 | 15884 |
| X-n204-k19 | cargo | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 5015.91 | 26465.9 | 0.421773 | 21450 | 15884 |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 6186.37 | 30455.6 | 0.415665 | 21321 | 15884 |
| X-n204-k19 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 4265.76 | 25586.8 | 0.419212 | 21321 | 15884 |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 637.889 | 33614.9 | 0.414808 | 32977 | 1616 |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 482.512 | 33459.5 | 0.413317 | 32977 | 1616 |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 605.637 | 33880.5 | 0.410529 | 32977 | 1616 |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 417.037 | 33394 | 0.412596 | 32977 | 1616 |
| X-n223-k34 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 605.469 | 48238.5 | 0.454505 | 47633 | 1258 |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 453.222 | 48086.2 | 0.439955 | 47633 | 1258 |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 550.129 | 48425 | 0.44509 | 47633 | 1258 |
| X-n223-k34 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 381.05 | 48014.1 | 0.452523 | 47633 | 1258 |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1931.09 | 35314.1 | 0.474229 | 33383 | 3542 |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1452.31 | 34835.3 | 0.470617 | 33383 | 3542 |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1750.45 | 35703.8 | 0.47163 | 33383 | 3542 |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1208.42 | 34591.4 | 0.469427 | 33383 | 3542 |
| X-n237-k14 | atm | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 106.828 | 29279.8 | 0.470508 | 29173 | 237.722 |
| X-n237-k14 | cargo | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 81.0543 | 28600.1 | 0.472458 | 28519 | 237.932 |
| X-n237-k14 | cold_chain | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 94.183 | 28656.1 | 0.468898 | 28519 | 236.906 |
| X-n237-k14 | grocery | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 66.3804 | 28585.4 | 0.470297 | 28519 | 236.856 |
| X-n242-k48 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 687.223 | 92490.2 | 0.473112 | 91803 | 1344 |
| X-n242-k48 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 517.094 | 92320.1 | 0.463651 | 91803 | 1344 |
| X-n242-k48 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 611.476 | 92675.5 | 0.46722 | 91803 | 1344 |
| X-n242-k48 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 426.811 | 92229.8 | 0.470913 | 91803 | 1344 |
| X-n251-k28 | atm | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 822.157 | 41344.2 | 0.42964 | 40522 | 1932 |
| X-n251-k28 | cargo | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 622.334 | 41144.3 | 0.42608 | 40522 | 1932 |
| X-n251-k28 | cold_chain | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 760.088 | 41638 | 0.42488 | 40522 | 1932 |
| X-n251-k28 | grocery | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 526.223 | 41048.2 | 0.42864 | 40522 | 1932 |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 6467.14 | 37749.1 | 0.432885 | 31282 | 14053 |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 4841.91 | 36804.9 | 0.432615 | 31963 | 14053 |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 6025.57 | 40101.3 | 0.423038 | 31364 | 14053 |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 4147.39 | 35617.4 | 0.430038 | 31470 | 14053 |
| X-n275-k28 | atm | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 107.693 | 22533.7 | 0.412993 | 22426 | 280 |
| X-n275-k28 | cargo | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 82.192 | 22508.2 | 0.414307 | 22426 | 280 |
| X-n275-k28 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 100.907 | 22577.6 | 0.410109 | 22426 | 280 |
| X-n275-k28 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 69.9386 | 22495.9 | 0.411971 | 22426 | 280 |
| X-n280-k17 | atm | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 1803.19 | 40365.2 | 0.460717 | 38562 | 3264 |
| X-n280-k17 | cargo | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 1354.98 | 39917 | 0.46 | 38562 | 3264 |
| X-n280-k17 | cold_chain | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 1617.48 | 40786 | 0.448315 | 38562 | 3264 |
| X-n280-k17 | grocery | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 1121.26 | 39683.3 | 0.452258 | 38562 | 3264 |
| X-n284-k15 | atm | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 632.189 | 24260.2 | 0.395265 | 23628 | 1635 |
| X-n284-k15 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 471.038 | 24099 | 0.390283 | 23628 | 1635 |
| X-n284-k15 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 627.736 | 24566.6 | 0.383781 | 23628 | 1635 |
| X-n284-k15 | grocery | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 423.755 | 24051.8 | 0.3947 | 23628 | 1635 |

## Full-Scenario Winner Confirmation

| Instance | Domain | Candidate | Fast Stockout | Full Stockout | Stockout Relative Drift | Fast Mean Total Cost | Full Mean Total Cost | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Stable | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_seed101_or_tools | 0.379714 | 0.400095 | 0.0509403 | 30173.3 | 30115.9 | 0.00190482 | no | no | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | cargo | ortools:nominal_seed101_or_tools | 0.377143 | 0.398857 | 0.0544413 | 29484.9 | 29405.8 | 0.00268803 | no | no | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | cold_chain | ortools:nominal_seed101_or_tools | 0.375524 | 0.397714 | 0.055795 | 31734.4 | 31542.4 | 0.00608732 | no | no | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | grocery | ortools:nominal_seed101_or_tools | 0.378381 | 0.400476 | 0.0551724 | 29315.2 | 29146.6 | 0.00578436 | no | no | no | final_full_required: drift threshold exceeded |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | 0.419358 | 0.415688 | 0.00882807 | 16803.2 | 16789.3 | 0.000828162 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | 0.424128 | 0.416606 | 0.0180577 | 16713.4 | 16699.7 | 0.000816307 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.418073 | 0.411651 | 0.0156006 | 16941.1 | 16927 | 0.000834837 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | 0.416606 | 0.414495 | 0.00509075 | 16673.9 | 16660.4 | 0.000811047 | yes | no | no | final_full_required: domain ranking flip |
| X-n115-k10 | atm | ortools:nominal_seed101_or_tools | 0.378333 | 0.400175 | 0.0545813 | 14070.6 | 14007.9 | 0.00447936 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n115-k10 | cargo | ortools:nominal_seed101_or_tools | 0.385439 | 0.404123 | 0.046234 | 13875.5 | 13812.6 | 0.00455841 | yes | yes | yes | safe |
| X-n115-k10 | cold_chain | ortools:nominal_seed101_or_tools | 0.359737 | 0.376667 | 0.0449464 | 14367.1 | 14324.5 | 0.00297575 | yes | yes | yes | safe |
| X-n115-k10 | grocery | ortools:nominal_seed101_or_tools | 0.370789 | 0.393596 | 0.0579452 | 13815.3 | 13752.8 | 0.00453775 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n120-k6 | atm | ortools:nominal_seed101_or_tools | 0.430756 | 0.43 | 0.00175884 | 14454.2 | 14370.7 | 0.00580674 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_seed101_or_tools | 0.434958 | 0.435462 | 0.00115785 | 14442.4 | 14359 | 0.00580762 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_seed101_or_tools | 0.435042 | 0.434706 | 0.000773246 | 14473 | 14389.6 | 0.00579754 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_seed101_or_tools | 0.433697 | 0.432773 | 0.00213592 | 14436.6 | 14353.3 | 0.00580036 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | atm | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.415078 | 0.415156 | 0.000188182 | 34098.7 | 33690.4 | 0.0121197 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.407656 | 0.404609 | 0.00753041 | 33980 | 33978.3 | 4.90639e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.408281 | 0.404922 | 0.00829635 | 34212.6 | 33810.1 | 0.0119062 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.415625 | 0.414141 | 0.00358423 | 33993.6 | 33585.7 | 0.0121433 | yes | no | no | final_full_required: domain ranking flip |
| X-n134-k13 | atm | ortools:nominal_seed101_or_tools | 0.461278 | 0.457444 | 0.00838264 | 16428.5 | 16384 | 0.00271669 | yes | yes | yes | safe |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | 0.448647 | 0.445338 | 0.00742867 | 18184.2 | 17466.8 | 0.041072 | yes | yes | yes | safe |
| X-n134-k13 | cold_chain | ortools:nominal_seed103_or_tools | 0.456316 | 0.451729 | 0.0101531 | 16959.8 | 16894.2 | 0.00388325 | yes | yes | yes | safe |
| X-n134-k13 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.462406 | 0.457594 | 0.0105159 | 16878.5 | 15986.1 | 0.0558232 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | atm | ortools:proxy_mean_scaled_seed109_or_tools | 0.418261 | 0.414565 | 0.00891453 | 16423.5 | 15642.4 | 0.0499346 | yes | no | no | final_full_required: domain ranking flip |
| X-n139-k10 | cargo | ortools:proxy_mean_scaled_seed109_or_tools | 0.417391 | 0.412536 | 0.0117688 | 16317 | 15486 | 0.0536647 | no | no | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | cold_chain | ortools:proxy_mean_scaled_seed109_or_tools | 0.413841 | 0.411232 | 0.00634361 | 16593.2 | 15752.6 | 0.0533638 | no | no | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | grocery | ortools:proxy_mean_scaled_seed109_or_tools | 0.416812 | 0.414058 | 0.00665033 | 16272.6 | 15436.3 | 0.0541776 | no | no | no | final_full_required: drift threshold exceeded |
| X-n143-k7 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.312113 | 0.311127 | 0.00316885 | 20914.6 | 20781.8 | 0.00638891 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | cargo | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.307746 | 0.305986 | 0.00575374 | 20309 | 20240.1 | 0.00340589 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | 0.302183 | 0.30331 | 0.00371488 | 22514.4 | 22498.8 | 0.000694279 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | 0.306901 | 0.309507 | 0.00841866 | 21882.7 | 20968.8 | 0.0435835 | yes | no | no | final_full_required: domain ranking flip |
| X-n162-k11 | atm | ortools:nominal_or_tools | 0.400373 | 0.395217 | 0.0130442 | 19614.6 | 19418.4 | 0.0101052 | yes | yes | yes | safe |
| X-n162-k11 | cargo | ortools:nominal_or_tools | 0.408509 | 0.402857 | 0.0140302 | 18460.7 | 18268.3 | 0.0105344 | yes | yes | yes | safe |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | 0.394286 | 0.389689 | 0.0117947 | 21918.5 | 21711.6 | 0.00953165 | yes | yes | yes | safe |
| X-n162-k11 | grocery | ortools:nominal_or_tools | 0.397578 | 0.392671 | 0.012496 | 18012.9 | 17840.8 | 0.00964729 | yes | yes | yes | safe |
| X-n167-k10 | atm | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.376807 | 0.377048 | 0.00063908 | 23001.6 | 22998 | 0.000153741 | yes | yes | yes | safe |
| X-n167-k10 | cargo | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.376084 | 0.375301 | 0.00208668 | 22891.1 | 22887.8 | 0.000144435 | yes | yes | yes | safe |
| X-n167-k10 | cold_chain | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.371747 | 0.370723 | 0.00276243 | 23249.6 | 23247.1 | 0.000105623 | yes | yes | yes | safe |
| X-n167-k10 | grocery | ortools:robust_mean_1std_scaled_seed113_or_tools | 0.37512 | 0.374819 | 0.0008036 | 22861.3 | 22859.5 | 7.89791e-05 | yes | yes | yes | safe |
| X-n181-k23 | atm | ortools:quantile_p75_scaled_seed107_or_tools | 0.426611 | 0.428333 | 0.00402075 | 26330.6 | 26329.9 | 2.66658e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n181-k23 | cargo | ortools:quantile_p75_scaled_seed107_or_tools | 0.428722 | 0.427556 | 0.00272869 | 26312.5 | 26311.9 | 2.36717e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n181-k23 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | 0.426111 | 0.425 | 0.00261438 | 26357.5 | 26356.8 | 2.5708e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n181-k23 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | 0.426389 | 0.428 | 0.00376428 | 26303.4 | 26303 | 1.58369e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n186-k15 | atm | ortools:nominal_seed103_or_tools | 0.38573 | 0.384595 | 0.00295151 | 32244.3 | 32188.5 | 0.00173416 | yes | yes | yes | safe |
| X-n186-k15 | cargo | ortools:nominal_seed103_or_tools | 0.384324 | 0.383514 | 0.00211416 | 30857.6 | 30811.4 | 0.00149923 | yes | yes | yes | safe |
| X-n186-k15 | cold_chain | ortools:nominal_seed103_or_tools | 0.383189 | 0.381243 | 0.00510421 | 34772.9 | 34709 | 0.00184014 | yes | yes | yes | safe |
| X-n186-k15 | grocery | ortools:nominal_seed103_or_tools | 0.384811 | 0.383946 | 0.00225257 | 30306 | 30264 | 0.00138643 | yes | yes | yes | safe |
| X-n190-k8 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.420265 | 0.418254 | 0.00480708 | 18833.8 | 18818.4 | 0.000818329 | yes | yes | yes | safe |
| X-n190-k8 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.415926 | 0.41254 | 0.00820829 | 18713.4 | 18698.5 | 0.000794828 | yes | yes | yes | safe |
| X-n190-k8 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | 0.411376 | 0.409894 | 0.0036143 | 19023.4 | 19006.9 | 0.000869516 | yes | yes | yes | safe |
| X-n190-k8 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.418519 | 0.416984 | 0.00367974 | 18663.5 | 18648.8 | 0.000790799 | yes | yes | yes | safe |
| X-n204-k19 | atm | ortools:nominal_seed101_or_tools | 0.422956 | 0.42069 | 0.00538642 | 28062.4 | 27919.3 | 0.00512727 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_seed101_or_tools | 0.421773 | 0.419951 | 0.00434018 | 26465.9 | 26314.5 | 0.00575457 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | 0.415665 | 0.414778 | 0.00213777 | 30455.6 | 30319.1 | 0.00450027 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | 0.419212 | 0.42 | 0.00187661 | 25586.8 | 25455.3 | 0.0051647 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | 0.414808 | 0.411731 | 0.00747314 | 33614.9 | 33549.3 | 0.00195525 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | 0.413317 | 0.409231 | 0.0099859 | 33459.5 | 33393.9 | 0.00196416 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.410529 | 0.406346 | 0.0102934 | 33880.5 | 33815.4 | 0.00192367 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | 0.412596 | 0.409904 | 0.00656814 | 33394 | 33330.5 | 0.00190614 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.454505 | 0.449955 | 0.0101111 | 48238.5 | 48235.4 | 6.3538e-05 | yes | yes | yes | safe |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.439955 | 0.44027 | 0.000716186 | 48086.2 | 48083.9 | 4.78393e-05 | yes | yes | yes | safe |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | 0.44509 | 0.442252 | 0.00641679 | 48425 | 48422.4 | 5.37159e-05 | yes | yes | yes | safe |
| X-n223-k34 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.452523 | 0.448423 | 0.00914114 | 48014.1 | 48012.3 | 3.63243e-05 | yes | yes | yes | safe |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | 0.474229 | 0.461278 | 0.0280775 | 35314.1 | 35300.3 | 0.000389827 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | 0.470617 | 0.452643 | 0.039708 | 34835.3 | 34822.2 | 0.000376284 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.47163 | 0.459207 | 0.027053 | 35703.8 | 35690.4 | 0.000376257 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | 0.469427 | 0.456079 | 0.0292669 | 34591.4 | 34583.9 | 0.000217854 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | atm | ortools:quantile_p75_scaled_seed107_or_tools | 0.470508 | 0.472797 | 0.00483958 | 29279.8 | 29286.1 | 0.000213274 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_seed103_or_tools | 0.472458 | 0.472585 | 0.000268986 | 28600.1 | 28599.5 | 1.91181e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_seed103_or_tools | 0.468898 | 0.46928 | 0.000812641 | 28656.1 | 28655.5 | 2.37827e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_seed103_or_tools | 0.470297 | 0.470339 | 9.00901e-05 | 28585.4 | 28584.9 | 1.70244e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n242-k48 | atm | ortools:quantile_p75_scaled_or_tools | 0.473112 | 0.467801 | 0.0113536 | 92490.2 | 92152.9 | 0.0036602 | yes | yes | yes | safe |
| X-n242-k48 | cargo | ortools:quantile_p75_scaled_or_tools | 0.463651 | 0.458382 | 0.0114963 | 92320.1 | 91983.6 | 0.00365808 | yes | yes | yes | safe |
| X-n242-k48 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.46722 | 0.461286 | 0.0128632 | 92675.5 | 92341 | 0.00362285 | yes | yes | yes | safe |
| X-n242-k48 | grocery | ortools:quantile_p75_scaled_or_tools | 0.470913 | 0.466556 | 0.00933831 | 92229.8 | 91893.7 | 0.00365796 | yes | yes | yes | safe |
| X-n251-k28 | atm | ortools:nominal_seed103_or_tools | 0.42964 | 0.42964 | 0 | 41344.2 | 41339 | 0.000125051 | yes | yes | yes | safe |
| X-n251-k28 | cargo | ortools:nominal_seed103_or_tools | 0.42608 | 0.4256 | 0.00112782 | 41144.3 | 41139.1 | 0.000128238 | yes | yes | yes | safe |
| X-n251-k28 | cold_chain | ortools:nominal_seed103_or_tools | 0.42488 | 0.42432 | 0.00131976 | 41638 | 41632.8 | 0.000125191 | yes | yes | yes | safe |
| X-n251-k28 | grocery | ortools:nominal_seed103_or_tools | 0.42864 | 0.4284 | 0.000560224 | 41048.2 | 41045.3 | 7.05344e-05 | yes | yes | yes | safe |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | 0.432885 | 0.428731 | 0.00968871 | 37749.1 | 37675.6 | 0.00195226 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.432615 | 0.429 | 0.00842747 | 36804.9 | 36751.4 | 0.00145695 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.423038 | 0.417962 | 0.0121469 | 40101.3 | 40034.7 | 0.00166421 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | 0.430038 | 0.428385 | 0.00386066 | 35617.4 | 35575.9 | 0.0011654 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | atm | ortools:quantile_p75_scaled_seed107_or_tools | 0.412993 | 0.41365 | 0.00158814 | 22533.7 | 22533 | 3.09769e-05 | yes | yes | yes | safe |
| X-n275-k28 | cargo | ortools:quantile_p75_scaled_seed107_or_tools | 0.414307 | 0.413832 | 0.00114649 | 22508.2 | 22507.6 | 2.74275e-05 | yes | yes | yes | safe |
| X-n275-k28 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | 0.410109 | 0.411131 | 0.00248557 | 22577.6 | 22577 | 2.75564e-05 | yes | yes | yes | safe |
| X-n275-k28 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | 0.411971 | 0.412555 | 0.00141543 | 22495.9 | 22495.5 | 1.92932e-05 | yes | yes | yes | safe |
| X-n280-k17 | atm | ortools:proxy_mean_scaled_seed109_or_tools | 0.460717 | 0.463835 | 0.00672282 | 40365.2 | 40355.2 | 0.000246385 | yes | yes | yes | safe |
| X-n280-k17 | cargo | ortools:proxy_mean_scaled_seed109_or_tools | 0.46 | 0.459928 | 0.00015586 | 39917 | 39910 | 0.000174937 | yes | yes | yes | safe |
| X-n280-k17 | cold_chain | ortools:proxy_mean_scaled_seed109_or_tools | 0.448315 | 0.450609 | 0.00509068 | 40786 | 40776.5 | 0.000232693 | yes | yes | yes | safe |
| X-n280-k17 | grocery | ortools:proxy_mean_scaled_seed109_or_tools | 0.452258 | 0.457455 | 0.011361 | 39683.3 | 39677.2 | 0.000153849 | yes | yes | yes | safe |
| X-n284-k15 | atm | ortools:robust_mean_2std_scaled_or_tools | 0.395265 | 0.389117 | 0.0158009 | 24260.2 | 24254.5 | 0.000236419 | yes | yes | yes | safe |
| X-n284-k15 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.390283 | 0.384735 | 0.0144195 | 24099 | 24094.5 | 0.000186907 | yes | yes | yes | safe |
| X-n284-k15 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | 0.383781 | 0.378763 | 0.0132475 | 24566.6 | 24560.7 | 0.000242306 | yes | yes | yes | safe |
| X-n284-k15 | grocery | ortools:robust_mean_2std_scaled_or_tools | 0.3947 | 0.388516 | 0.0159163 | 24051.8 | 24048.6 | 0.000131823 | yes | yes | yes | safe |

## Domain Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | yes | 0.8 |  |
| X-n110-k13 | 4 | cargo > atm > cold_chain > grocery | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n115-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n120-k6 | 4 | cold_chain > cargo > grocery > atm | cargo > cold_chain > grocery > atm | yes | 0.8 |  |
| X-n129-k18 | 4 | grocery > atm > cold_chain > cargo | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n134-k13 | 4 | grocery > atm > cold_chain > cargo | grocery > atm > cold_chain > cargo | no | 1 |  |
| X-n139-k10 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n143-k7 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n162-k11 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n167-k10 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n181-k23 | 4 | cargo > atm > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.4 |  |
| X-n186-k15 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n190-k8 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n204-k19 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n209-k16 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n223-k34 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n228-k23 | 4 | atm > cold_chain > cargo > grocery | atm > cold_chain > grocery > cargo | yes | 0.8 |  |
| X-n237-k14 | 4 | cargo > atm > grocery > cold_chain | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n242-k48 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n251-k28 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n261-k13 | 4 | atm > cargo > grocery > cold_chain | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n275-k28 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n280-k17 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n284-k15 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |

## Route Candidates

| Instance | Candidate | Route Feasible | Route Count | Route Cost | Planned Route Load Ratio | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | ortools:nominal_or_tools | yes | 14 | 27182 | 0.93619 |  |
| X-n106-k14 | ortools:proxy_mean_or_tools | no | 0 |  | 1.03315 | total_load_exceeds_fleet_capacity |
| X-n106-k14 | ortools:quantile_p75_or_tools | no | 0 |  | 1.20215 | total_load_exceeds_fleet_capacity |
| X-n106-k14 | ortools:quantile_p90_or_tools | no | 0 |  | 1.42665 | total_load_exceeds_fleet_capacity |
| X-n106-k14 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.34178 | total_load_exceeds_fleet_capacity |
| X-n106-k14 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.65041 | total_load_exceeds_fleet_capacity |
| X-n106-k14 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:nominal_seed101_or_tools | yes | 14 | 27425 | 0.93619 |  |
| X-n106-k14 | ortools:nominal_seed103_or_tools | yes | 14 | 27116 | 0.93619 |  |
| X-n106-k14 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n106-k14 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:nominal_or_tools | yes | 13 | 15588 | 0.951049 |  |
| X-n110-k13 | ortools:proxy_mean_or_tools | no | 0 |  | 1.07472 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:quantile_p75_or_tools | no | 0 |  | 1.24557 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.49375 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39846 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.72219 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:proxy_mean_scaled_or_tools | yes | 13 | 16439 | 0.995 |  |
| X-n110-k13 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:nominal_seed101_or_tools | yes | 13 | 16029 | 0.951049 |  |
| X-n110-k13 | ortools:nominal_seed103_or_tools | yes | 13 | 15898 | 0.951049 |  |
| X-n110-k13 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 13 | 16162 | 0.995 |  |
| X-n110-k13 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:nominal_or_tools | yes | 10 | 13298 | 0.908284 |  |
| X-n115-k10 | ortools:proxy_mean_or_tools | no | 0 |  | 1.00385 | total_load_exceeds_fleet_capacity |
| X-n115-k10 | ortools:quantile_p75_or_tools | no | 0 |  | 1.18706 | total_load_exceeds_fleet_capacity |
| X-n115-k10 | ortools:quantile_p90_or_tools | no | 0 |  | 1.44084 | total_load_exceeds_fleet_capacity |
| X-n115-k10 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.35429 | total_load_exceeds_fleet_capacity |
| X-n115-k10 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.70473 | single_node_exceeds_capacity |
| X-n115-k10 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:nominal_seed101_or_tools | yes | 10 | 13293 | 0.908284 |  |
| X-n115-k10 | ortools:nominal_seed103_or_tools | yes | 10 | 14930 | 0.908284 |  |
| X-n115-k10 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n115-k10 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n120-k6 | ortools:nominal_or_tools | yes | 6 | 14219 | 0.944444 |  |
| X-n120-k6 | ortools:proxy_mean_or_tools | yes | 6 | 14219 | 1.05969 |  |
| X-n120-k6 | ortools:quantile_p75_or_tools | yes | 6 | 14219 | 1.22264 |  |
| X-n120-k6 | ortools:quantile_p90_or_tools | no | 0 |  | 1.4497 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.36156 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.66342 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:proxy_mean_scaled_or_tools | yes | 6 | 14219 | 0.995 |  |
| X-n120-k6 | ortools:quantile_p75_scaled_or_tools | yes | 6 | 14219 | 0.995 |  |
| X-n120-k6 | ortools:quantile_p90_scaled_or_tools | yes | 6 | 14219 | 0.995 |  |
| X-n120-k6 | ortools:robust_mean_1std_scaled_or_tools | yes | 6 | 14052 | 0.995 |  |
| X-n120-k6 | ortools:robust_mean_2std_scaled_or_tools | yes | 6 | 14052 | 0.995 |  |
| X-n120-k6 | ortools:nominal_seed101_or_tools | yes | 6 | 14404 | 0.944444 |  |
| X-n120-k6 | ortools:nominal_seed103_or_tools | yes | 6 | 14579 | 0.944444 |  |
| X-n120-k6 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 6 | 14703 | 0.995 |  |
| X-n120-k6 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 6 | 14111 | 0.995 |  |
| X-n120-k6 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 6 | 14278 | 0.995 |  |
| X-n129-k18 | ortools:nominal_or_tools | yes | 18 | 30985 | 0.947293 |  |
| X-n129-k18 | ortools:proxy_mean_or_tools | no | 0 |  | 1.03581 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:quantile_p75_or_tools | no | 0 |  | 1.20693 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:quantile_p90_or_tools | no | 0 |  | 1.46375 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.36925 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.7027 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:proxy_mean_scaled_or_tools | yes | 18 | 31829 | 0.995 |  |
| X-n129-k18 | ortools:quantile_p75_scaled_or_tools | yes | 18 | 31544 | 0.995 |  |
| X-n129-k18 | ortools:quantile_p90_scaled_or_tools | yes | 18 | 33579 | 0.995 |  |
| X-n129-k18 | ortools:robust_mean_1std_scaled_or_tools | yes | 18 | 33008 | 0.995 |  |
| X-n129-k18 | ortools:robust_mean_2std_scaled_or_tools | yes | 18 | 33757 | 0.995 |  |
| X-n129-k18 | ortools:nominal_seed101_or_tools | yes | 18 | 31270 | 0.947293 |  |
| X-n129-k18 | ortools:nominal_seed103_or_tools | yes | 18 | 32270 | 0.947293 |  |
| X-n129-k18 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 18 | 31458 | 0.995 |  |
| X-n129-k18 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 18 | 32863 | 0.995 |  |
| X-n129-k18 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 18 | 33799 | 0.995 |  |
| X-n134-k13 | ortools:nominal_or_tools | yes | 13 | 13630 | 0.983371 |  |
| X-n134-k13 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09862 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:quantile_p75_or_tools | no | 0 |  | 1.2792 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53346 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.43845 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.77828 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n134-k13 | ortools:quantile_p75_scaled_or_tools | yes | 13 | 15401 | 0.995 |  |
| X-n134-k13 | ortools:quantile_p90_scaled_or_tools | yes | 13 | 15608 | 0.995 |  |
| X-n134-k13 | ortools:robust_mean_1std_scaled_or_tools | yes | 13 | 14509 | 0.995 |  |
| X-n134-k13 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n134-k13 | ortools:nominal_seed101_or_tools | yes | 13 | 12635 | 0.983371 |  |
| X-n134-k13 | ortools:nominal_seed103_or_tools | yes | 13 | 12210 | 0.983371 |  |
| X-n134-k13 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n134-k13 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n134-k13 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 13 | 14602 | 0.995 |  |
| X-n139-k10 | ortools:nominal_or_tools | yes | 10 | 14877 | 0.980189 |  |
| X-n139-k10 | ortools:proxy_mean_or_tools | no | 0 |  | 1.08142 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:quantile_p75_or_tools | no | 0 |  | 1.25423 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:quantile_p90_or_tools | no | 0 |  | 1.48754 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39682 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71222 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n139-k10 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n139-k10 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n139-k10 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n139-k10 | ortools:nominal_seed101_or_tools | yes | 10 | 14943 | 0.980189 |  |
| X-n139-k10 | ortools:nominal_seed103_or_tools | yes | 10 | 15332 | 0.980189 |  |
| X-n139-k10 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 10 | 15996 | 0.995 |  |
| X-n139-k10 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n139-k10 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:nominal_or_tools | yes | 7 | 16662 | 0.897359 |  |
| X-n143-k7 | ortools:proxy_mean_or_tools | yes | 7 | 20036 | 0.9959 |  |
| X-n143-k7 | ortools:quantile_p75_or_tools | no | 0 |  | 1.1607 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:quantile_p90_or_tools | no | 0 |  | 1.40025 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.30625 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.6166 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:proxy_mean_scaled_or_tools | yes | 7 | 18747 | 0.995 |  |
| X-n143-k7 | ortools:quantile_p75_scaled_or_tools | yes | 7 | 18056 | 0.995 |  |
| X-n143-k7 | ortools:quantile_p90_scaled_or_tools | yes | 7 | 18642 | 0.995 |  |
| X-n143-k7 | ortools:robust_mean_1std_scaled_or_tools | yes | 7 | 18403 | 0.995 |  |
| X-n143-k7 | ortools:robust_mean_2std_scaled_or_tools | yes | 7 | 18906 | 0.995 |  |
| X-n143-k7 | ortools:nominal_seed101_or_tools | yes | 7 | 17828 | 0.897359 |  |
| X-n143-k7 | ortools:nominal_seed103_or_tools | yes | 7 | 16802 | 0.897359 |  |
| X-n143-k7 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 7 | 18802 | 0.995 |  |
| X-n143-k7 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 7 | 18166 | 0.995 |  |
| X-n143-k7 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 7 | 18450 | 0.995 |  |
| X-n162-k11 | ortools:nominal_or_tools | yes | 11 | 14799 | 0.944247 |  |
| X-n162-k11 | ortools:proxy_mean_or_tools | no | 0 |  | 1.08732 | total_load_exceeds_fleet_capacity |
| X-n162-k11 | ortools:quantile_p75_or_tools | no | 0 |  | 1.26411 | total_load_exceeds_fleet_capacity |
| X-n162-k11 | ortools:quantile_p90_or_tools | no | 0 |  | 1.52037 | total_load_exceeds_fleet_capacity |
| X-n162-k11 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.41925 | total_load_exceeds_fleet_capacity |
| X-n162-k11 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.75118 | total_load_exceeds_fleet_capacity |
| X-n162-k11 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:nominal_seed101_or_tools | yes | 11 | 14878 | 0.944247 |  |
| X-n162-k11 | ortools:nominal_seed103_or_tools | yes | 11 | 14821 | 0.944247 |  |
| X-n162-k11 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n162-k11 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:nominal_or_tools | yes | 10 | 22643 | 0.929323 |  |
| X-n167-k10 | ortools:proxy_mean_or_tools | no | 0 |  | 1.00635 | total_load_exceeds_fleet_capacity |
| X-n167-k10 | ortools:quantile_p75_or_tools | no | 0 |  | 1.16513 | total_load_exceeds_fleet_capacity |
| X-n167-k10 | ortools:quantile_p90_or_tools | no | 0 |  | 1.39022 | total_load_exceeds_fleet_capacity |
| X-n167-k10 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.30116 | total_load_exceeds_fleet_capacity |
| X-n167-k10 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.59598 | total_load_exceeds_fleet_capacity |
| X-n167-k10 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:nominal_seed101_or_tools | yes | 10 | 22530 | 0.929323 |  |
| X-n167-k10 | ortools:nominal_seed103_or_tools | yes | 10 | 22324 | 0.929323 |  |
| X-n167-k10 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 10 | 22790 | 0.995 |  |
| X-n167-k10 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n167-k10 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 10 | 22558 | 0.995 |  |
| X-n181-k23 | ortools:nominal_or_tools | yes | 23 | 26513 | 0.978261 |  |
| X-n181-k23 | ortools:proxy_mean_or_tools | yes | 23 | 26513 | 1.07587 |  |
| X-n181-k23 | ortools:quantile_p75_or_tools | yes | 23 | 26513 | 1.24209 |  |
| X-n181-k23 | ortools:quantile_p90_or_tools | no | 0 |  | 1.47136 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.38655 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.69723 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:proxy_mean_scaled_or_tools | yes | 23 | 26513 | 0.995 |  |
| X-n181-k23 | ortools:quantile_p75_scaled_or_tools | yes | 23 | 26513 | 0.995 |  |
| X-n181-k23 | ortools:quantile_p90_scaled_or_tools | yes | 23 | 26513 | 0.995 |  |
| X-n181-k23 | ortools:robust_mean_1std_scaled_or_tools | yes | 23 | 26513 | 0.995 |  |
| X-n181-k23 | ortools:robust_mean_2std_scaled_or_tools | yes | 23 | 26513 | 0.995 |  |
| X-n181-k23 | ortools:nominal_seed101_or_tools | yes | 23 | 26327 | 0.978261 |  |
| X-n181-k23 | ortools:nominal_seed103_or_tools | yes | 23 | 26217 | 0.978261 |  |
| X-n181-k23 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 23 | 26275 | 0.995 |  |
| X-n181-k23 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 23 | 26255 | 0.995 |  |
| X-n181-k23 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 23 | 26185 | 0.995 |  |
| X-n186-k15 | ortools:nominal_or_tools | yes | 15 | 26050 | 0.948186 |  |
| X-n186-k15 | ortools:proxy_mean_or_tools | no | 0 |  | 1.04791 | total_load_exceeds_fleet_capacity |
| X-n186-k15 | ortools:quantile_p75_or_tools | no | 0 |  | 1.21474 | total_load_exceeds_fleet_capacity |
| X-n186-k15 | ortools:quantile_p90_or_tools | no | 0 |  | 1.45142 | total_load_exceeds_fleet_capacity |
| X-n186-k15 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.35858 | total_load_exceeds_fleet_capacity |
| X-n186-k15 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.66926 | total_load_exceeds_fleet_capacity |
| X-n186-k15 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:nominal_seed101_or_tools | yes | 15 | 26666 | 0.948186 |  |
| X-n186-k15 | ortools:nominal_seed103_or_tools | yes | 15 | 26466 | 0.948186 |  |
| X-n186-k15 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n186-k15 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n190-k8 | ortools:nominal_or_tools | yes | 8 | 18180 | 0.944746 |  |
| X-n190-k8 | ortools:proxy_mean_or_tools | no | 0 |  | 1.05354 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:quantile_p75_or_tools | no | 0 |  | 1.22919 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:quantile_p90_or_tools | no | 0 |  | 1.48526 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.38498 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71643 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:proxy_mean_scaled_or_tools | yes | 8 | 18297 | 0.995 |  |
| X-n190-k8 | ortools:quantile_p75_scaled_or_tools | yes | 8 | 18293 | 0.995 |  |
| X-n190-k8 | ortools:quantile_p90_scaled_or_tools | yes | 8 | 18321 | 0.995 |  |
| X-n190-k8 | ortools:robust_mean_1std_scaled_or_tools | yes | 8 | 18347 | 0.995 |  |
| X-n190-k8 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:nominal_seed101_or_tools | yes | 8 | 17873 | 0.944746 |  |
| X-n190-k8 | ortools:nominal_seed103_or_tools | yes | 8 | 18118 | 0.944746 |  |
| X-n190-k8 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 8 | 18290 | 0.995 |  |
| X-n190-k8 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 8 | 18230 | 0.995 |  |
| X-n190-k8 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 8 | 18359 | 0.995 |  |
| X-n204-k19 | ortools:nominal_or_tools | yes | 19 | 21321 | 0.952846 |  |
| X-n204-k19 | ortools:proxy_mean_or_tools | no | 0 |  | 1.04867 | total_load_exceeds_fleet_capacity |
| X-n204-k19 | ortools:quantile_p75_or_tools | no | 0 |  | 1.21616 | total_load_exceeds_fleet_capacity |
| X-n204-k19 | ortools:quantile_p90_or_tools | no | 0 |  | 1.44503 | total_load_exceeds_fleet_capacity |
| X-n204-k19 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.34953 | total_load_exceeds_fleet_capacity |
| X-n204-k19 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.65039 | total_load_exceeds_fleet_capacity |
| X-n204-k19 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:nominal_seed101_or_tools | yes | 19 | 21450 | 0.952846 |  |
| X-n204-k19 | ortools:nominal_seed103_or_tools | yes | 19 | 21635 | 0.952846 |  |
| X-n204-k19 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:nominal_or_tools | yes | 16 | 32468 | 0.957302 |  |
| X-n209-k16 | ortools:proxy_mean_or_tools | no | 0 |  | 1.06964 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:quantile_p75_or_tools | no | 0 |  | 1.23784 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:quantile_p90_or_tools | no | 0 |  | 1.4837 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39098 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71232 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:proxy_mean_scaled_or_tools | yes | 16 | 32551 | 0.995 |  |
| X-n209-k16 | ortools:quantile_p75_scaled_or_tools | yes | 16 | 32977 | 0.995 |  |
| X-n209-k16 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:nominal_seed101_or_tools | yes | 16 | 33133 | 0.957302 |  |
| X-n209-k16 | ortools:nominal_seed103_or_tools | yes | 16 | 33343 | 0.957302 |  |
| X-n209-k16 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 16 | 33286 | 0.995 |  |
| X-n209-k16 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n223-k34 | ortools:nominal_or_tools | yes | 34 | 44118 | 0.980922 |  |
| X-n223-k34 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09559 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:quantile_p75_or_tools | no | 0 |  | 1.27514 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53309 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.43998 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.78437 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:proxy_mean_scaled_or_tools | yes | 34 | 46581 | 0.995 |  |
| X-n223-k34 | ortools:quantile_p75_scaled_or_tools | yes | 34 | 46188 | 0.995 |  |
| X-n223-k34 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:robust_mean_1std_scaled_or_tools | yes | 34 | 47633 | 0.995 |  |
| X-n223-k34 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n223-k34 | ortools:nominal_seed101_or_tools | yes | 34 | 44090 | 0.980922 |  |
| X-n223-k34 | ortools:nominal_seed103_or_tools | yes | 34 | 43892 | 0.980922 |  |
| X-n223-k34 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 34 | 44102 | 0.995 |  |
| X-n223-k34 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 34 | 44117 | 0.995 |  |
| X-n223-k34 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:nominal_or_tools | yes | 23 | 30349 | 0.981931 |  |
| X-n228-k23 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09294 | total_load_exceeds_fleet_capacity |
| X-n228-k23 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28635 | total_load_exceeds_fleet_capacity |
| X-n228-k23 | ortools:quantile_p90_or_tools | no | 0 |  | 1.57669 | single_node_exceeds_capacity |
| X-n228-k23 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.46876 | single_node_exceeds_capacity |
| X-n228-k23 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.84457 | single_node_exceeds_capacity |
| X-n228-k23 | ortools:proxy_mean_scaled_or_tools | yes | 23 | 33383 | 0.995 |  |
| X-n228-k23 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n228-k23 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:nominal_seed101_or_tools | yes | 23 | 31166 | 0.981931 |  |
| X-n228-k23 | ortools:nominal_seed103_or_tools | no | 0 |  | 0.981931 | ortools_no_solution |
| X-n228-k23 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n228-k23 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n237-k14 | ortools:nominal_or_tools | yes | 14 | 29009 | 0.936508 |  |
| X-n237-k14 | ortools:proxy_mean_or_tools | yes | 14 | 29009 | 1.04689 |  |
| X-n237-k14 | ortools:quantile_p75_or_tools | yes | 14 | 29009 | 1.20898 |  |
| X-n237-k14 | ortools:quantile_p90_or_tools | no | 0 |  | 1.44719 | total_load_exceeds_fleet_capacity |
| X-n237-k14 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.3586 | total_load_exceeds_fleet_capacity |
| X-n237-k14 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.6703 | total_load_exceeds_fleet_capacity |
| X-n237-k14 | ortools:proxy_mean_scaled_or_tools | yes | 14 | 29009 | 0.995 |  |
| X-n237-k14 | ortools:quantile_p75_scaled_or_tools | yes | 14 | 29009 | 0.995 |  |
| X-n237-k14 | ortools:quantile_p90_scaled_or_tools | yes | 14 | 29009 | 0.995 |  |
| X-n237-k14 | ortools:robust_mean_1std_scaled_or_tools | yes | 14 | 29009 | 0.995 |  |
| X-n237-k14 | ortools:robust_mean_2std_scaled_or_tools | yes | 14 | 29009 | 0.995 |  |
| X-n237-k14 | ortools:nominal_seed101_or_tools | yes | 14 | 28862 | 0.936508 |  |
| X-n237-k14 | ortools:nominal_seed103_or_tools | yes | 14 | 28519 | 0.936508 |  |
| X-n237-k14 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 14 | 28600 | 0.995 |  |
| X-n237-k14 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 14 | 29173 | 0.995 |  |
| X-n237-k14 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 14 | 28893 | 0.995 |  |
| X-n242-k48 | ortools:nominal_or_tools | yes | 48 | 86573 | 0.985119 |  |
| X-n242-k48 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09819 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28009 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53482 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.43482 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.77144 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:proxy_mean_scaled_or_tools | yes | 48 | 88091 | 0.995 |  |
| X-n242-k48 | ortools:quantile_p75_scaled_or_tools | yes | 48 | 91803 | 0.995 |  |
| X-n242-k48 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:nominal_seed101_or_tools | yes | 48 | 87329 | 0.985119 |  |
| X-n242-k48 | ortools:nominal_seed103_or_tools | yes | 48 | 86092 | 0.985119 |  |
| X-n242-k48 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 48 | 87732 | 0.995 |  |
| X-n242-k48 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 48 | 89764 | 0.995 |  |
| X-n242-k48 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:nominal_or_tools | yes | 28 | 40465 | 0.966356 |  |
| X-n251-k28 | ortools:proxy_mean_or_tools | no | 0 |  | 1.07837 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:quantile_p75_or_tools | no | 0 |  | 1.24953 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:quantile_p90_or_tools | no | 0 |  | 1.49285 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39742 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71646 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n251-k28 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n251-k28 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n251-k28 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n251-k28 | ortools:nominal_seed101_or_tools | yes | 28 | 40789 | 0.966356 |  |
| X-n251-k28 | ortools:nominal_seed103_or_tools | yes | 28 | 40522 | 0.966356 |  |
| X-n251-k28 | ortools:proxy_mean_scaled_seed109_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n251-k28 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n251-k28 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n261-k13 | ortools:nominal_or_tools | yes | 13 | 29400 | 0.952181 |  |
| X-n261-k13 | ortools:proxy_mean_or_tools | no | 0 |  | 1.06615 | total_load_exceeds_fleet_capacity |
| X-n261-k13 | ortools:quantile_p75_or_tools | no | 0 |  | 1.24357 | total_load_exceeds_fleet_capacity |
| X-n261-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.51369 | total_load_exceeds_fleet_capacity |
| X-n261-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.40757 | total_load_exceeds_fleet_capacity |
| X-n261-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.74898 | total_load_exceeds_fleet_capacity |
| X-n261-k13 | ortools:proxy_mean_scaled_or_tools | yes | 13 | 31364 | 0.995 |  |
| X-n261-k13 | ortools:quantile_p75_scaled_or_tools | yes | 13 | 31282 | 0.995 |  |
| X-n261-k13 | ortools:quantile_p90_scaled_or_tools | yes | 13 | 31580 | 0.995 |  |
| X-n261-k13 | ortools:robust_mean_1std_scaled_or_tools | yes | 13 | 31915 | 0.995 |  |
| X-n261-k13 | ortools:robust_mean_2std_scaled_or_tools | yes | 13 | 31963 | 0.995 |  |
| X-n261-k13 | ortools:nominal_seed101_or_tools | yes | 13 | 29488 | 0.952181 |  |
| X-n261-k13 | ortools:nominal_seed103_or_tools | yes | 13 | 30943 | 0.952181 |  |
| X-n261-k13 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 13 | 30438 | 0.995 |  |
| X-n261-k13 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 13 | 31470 | 0.995 |  |
| X-n261-k13 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 13 | 32161 | 0.995 |  |
| X-n275-k28 | ortools:nominal_or_tools | yes | 28 | 22472 | 0.978571 |  |
| X-n275-k28 | ortools:proxy_mean_or_tools | yes | 28 | 22472 | 1.09607 |  |
| X-n275-k28 | ortools:quantile_p75_or_tools | yes | 28 | 22472 | 1.26514 |  |
| X-n275-k28 | ortools:quantile_p90_or_tools | no | 0 |  | 1.50245 | total_load_exceeds_fleet_capacity |
| X-n275-k28 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.40938 | total_load_exceeds_fleet_capacity |
| X-n275-k28 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.7227 | total_load_exceeds_fleet_capacity |
| X-n275-k28 | ortools:proxy_mean_scaled_or_tools | yes | 28 | 22472 | 0.995 |  |
| X-n275-k28 | ortools:quantile_p75_scaled_or_tools | yes | 28 | 22472 | 0.995 |  |
| X-n275-k28 | ortools:quantile_p90_scaled_or_tools | yes | 28 | 22472 | 0.995 |  |
| X-n275-k28 | ortools:robust_mean_1std_scaled_or_tools | yes | 28 | 22472 | 0.995 |  |
| X-n275-k28 | ortools:robust_mean_2std_scaled_or_tools | yes | 28 | 22472 | 0.995 |  |
| X-n275-k28 | ortools:nominal_seed101_or_tools | yes | 28 | 22674 | 0.978571 |  |
| X-n275-k28 | ortools:nominal_seed103_or_tools | yes | 28 | 22466 | 0.978571 |  |
| X-n275-k28 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 28 | 22488 | 0.995 |  |
| X-n275-k28 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 28 | 22426 | 0.995 |  |
| X-n275-k28 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 28 | 22542 | 0.995 |  |
| X-n280-k17 | ortools:nominal_or_tools | yes | 17 | 38220 | 0.990502 |  |
| X-n280-k17 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09361 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28626 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:quantile_p90_or_tools | no | 0 |  | 1.57057 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.45732 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.82103 | single_node_exceeds_capacity |
| X-n280-k17 | ortools:proxy_mean_scaled_or_tools | yes | 17 | 39074 | 0.995 |  |
| X-n280-k17 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n280-k17 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n280-k17 | ortools:nominal_seed101_or_tools | yes | 17 | 39975 | 0.990502 |  |
| X-n280-k17 | ortools:nominal_seed103_or_tools | yes | 17 | 38196 | 0.990502 |  |
| X-n280-k17 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 17 | 38562 | 0.995 |  |
| X-n280-k17 | ortools:quantile_p75_scaled_seed107_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n280-k17 | ortools:robust_mean_1std_scaled_seed113_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:nominal_or_tools | yes | 15 | 22522 | 0.933945 |  |
| X-n284-k15 | ortools:proxy_mean_or_tools | no | 0 |  | 1.0341 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:quantile_p75_or_tools | no | 0 |  | 1.20737 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:quantile_p90_or_tools | no | 0 |  | 1.44221 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.35125 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.6684 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:proxy_mean_scaled_or_tools | yes | 15 | 22663 | 0.995 |  |
| X-n284-k15 | ortools:quantile_p75_scaled_or_tools | yes | 15 | 23026 | 0.995 |  |
| X-n284-k15 | ortools:quantile_p90_scaled_or_tools | yes | 15 | 22676 | 0.995 |  |
| X-n284-k15 | ortools:robust_mean_1std_scaled_or_tools | yes | 15 | 23151 | 0.995 |  |
| X-n284-k15 | ortools:robust_mean_2std_scaled_or_tools | yes | 15 | 23628 | 0.995 |  |
| X-n284-k15 | ortools:nominal_seed101_or_tools | yes | 15 | 22020 | 0.933945 |  |
| X-n284-k15 | ortools:nominal_seed103_or_tools | yes | 15 | 22228 | 0.933945 |  |
| X-n284-k15 | ortools:proxy_mean_scaled_seed109_or_tools | yes | 15 | 22726 | 0.995 |  |
| X-n284-k15 | ortools:quantile_p75_scaled_seed107_or_tools | yes | 15 | 22386 | 0.995 |  |
| X-n284-k15 | ortools:robust_mean_1std_scaled_seed113_or_tools | yes | 15 | 23033 | 0.995 |  |

## Interpretation

- A domain winner means that route candidate had the lowest selected evaluation metric after the stochastic loading LP.
- This is not a new routing solver; it is a robust selection layer over existing route providers and load plans.
- `Metric Stability Safe` checks only stockout and mean_total_cost drift; `Strict Stability Safe` also requires no domain stockout ranking flip.
- Infeasible high-quantile or robust plans remain visible because capacity pressure is part of the result.
