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
| atm | 440 | 114 | 40 | 11 | 4.99263 | ortools:nominal_or_tools | ortools | nominal_or_tools | 14 |
| cargo | 440 | 114 | 40 | 11 | 4.99263 | ortools:nominal_or_tools | ortools | nominal_or_tools | 14 |
| cold_chain | 440 | 114 | 40 | 11 | 4.99263 | ortools:nominal_or_tools | ortools | nominal_or_tools | 16 |
| grocery | 440 | 114 | 40 | 11 | 4.99263 | ortools:nominal_or_tools | ortools | nominal_or_tools | 16 |

## Winners

| Instance | Domain | Candidate | Routing Provider | Route Plan | Score Value | mean_total_cost | stockout_rate | Route Cost | Optimized Load Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 2939.64 | 30121.6 | 0.402381 | 27182 | 8400 |
| X-n106-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 2217.2 | 29399.2 | 0.403429 | 27182 | 8400 |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 2876.71 | 31507.2 | 0.404762 | 27182 | 8255.29 |
| X-n106-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 1963.23 | 29145.2 | 0.404762 | 27182 | 8282.21 |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 364.172 | 16790.2 | 0.41945 | 16426 | 858 |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 274.398 | 16700.4 | 0.424128 | 16426 | 858 |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 341.174 | 16928.7 | 0.417431 | 16426 | 858 |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 234.941 | 16660.9 | 0.416514 | 16426 | 858 |
| X-n115-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 789.043 | 13888 | 0.390789 | 13099 | 1690 |
| X-n115-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 592.23 | 13691.2 | 0.400439 | 13099 | 1690 |
| X-n115-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 786.657 | 14177.4 | 0.383158 | 13099 | 1684.38 |
| X-n115-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 527.675 | 13626.7 | 0.385877 | 13099 | 1690 |
| X-n120-k6 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 50.4405 | 14084.4 | 0.428992 | 14034 | 126 |
| X-n120-k6 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 38.6227 | 14072.6 | 0.429244 | 14034 | 126 |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 47.0182 | 14103 | 0.432017 | 14034 | 123.979 |
| X-n120-k6 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 32.6239 | 14066.6 | 0.432017 | 14034 | 124.387 |
| X-n129-k18 | atm | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 300.341 | 34057.3 | 0.422031 | 33757 | 702 |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 222.984 | 33980 | 0.407656 | 33757 | 702 |
| X-n129-k18 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 285.445 | 34178.9 | 0.414453 | 33757 | 702 |
| X-n129-k18 | grocery | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 194.793 | 33951.8 | 0.42 | 33757 | 702 |
| X-n134-k13 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 3793.67 | 18505.7 | 0.460451 | 14712 | 8359 |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 2783.4 | 17495.4 | 0.448496 | 14712 | 8359 |
| X-n134-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 3406.08 | 18203.3 | 0.457068 | 13345 | 8359 |
| X-n134-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 2368.69 | 15713.7 | 0.458346 | 13345 | 8359 |
| X-n139-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 428.712 | 15254.7 | 0.418913 | 14826 | 1060 |
| X-n139-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 322.826 | 15148.8 | 0.421232 | 14826 | 1060 |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 401.892 | 15424.6 | 0.413116 | 14826 | 1060 |
| X-n139-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 277.498 | 15103.5 | 0.418478 | 14826 | 1060 |
| X-n143-k7 | atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 2511.43 | 21042.4 | 0.314085 | 18531 | 8330 |
| X-n143-k7 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 1860.82 | 20153.8 | 0.308451 | 18293 | 8330 |
| X-n143-k7 | cold_chain | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 2823.61 | 23496.3 | 0.300915 | 19116 | 8330 |
| X-n143-k7 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 1847.75 | 19810.8 | 0.309789 | 17963 | 8330 |
| X-n157-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 75.253 | 17479.3 | 0.485833 | 17404 | 156 |
| X-n157-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 57.1567 | 17461.2 | 0.488013 | 17404 | 156 |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 64.9095 | 17497.7 | 0.484679 | 17404 | 156 |
| X-n157-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 46.0757 | 17450.1 | 0.484936 | 17404 | 156 |
| X-n162-k11 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 4784.5 | 19460.5 | 0.396025 | 14676 | 12914 |
| X-n162-k11 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 3639.1 | 18315.1 | 0.404969 | 14676 | 12914 |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 4693.07 | 21763 | 0.387702 | 14676 | 12914 |
| X-n162-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 3193.44 | 17869.4 | 0.394348 | 14676 | 12914 |
| X-n167-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 520.243 | 23163.2 | 0.417952 | 22643 | 1330 |
| X-n167-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 396.026 | 23039 | 0.415663 | 22643 | 1330 |
| X-n167-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 496.202 | 23377.4 | 0.417892 | 22643 | 1297.47 |
| X-n167-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 340.965 | 22984 | 0.421627 | 22643 | 1302.61 |
| X-n181-k23 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 76.6723 | 26308.7 | 0.438 | 26232 | 184 |
| X-n181-k23 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 58.1962 | 26290.2 | 0.439333 | 26232 | 184 |
| X-n181-k23 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 70.3803 | 26335.6 | 0.435111 | 26232 | 184 |
| X-n181-k23 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 48.9699 | 26281 | 0.435778 | 26232 | 184 |
| X-n186-k15 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 6130.84 | 32112.8 | 0.412432 | 25982 | 14343.8 |
| X-n186-k15 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 4652.29 | 30634.3 | 0.412054 | 25982 | 14389.4 |
| X-n186-k15 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 5729.42 | 34349.4 | 0.411568 | 25982 | 14223.4 |
| X-n186-k15 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 3963.52 | 29945.5 | 0.412865 | 25982 | 14245.5 |
| X-n190-k8 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 487.422 | 18821.4 | 0.422275 | 18334 | 1104 |
| X-n190-k8 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 366.722 | 18700.7 | 0.417619 | 18334 | 1104 |
| X-n190-k8 | cold_chain | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 460.776 | 18978.9 | 0.412063 | 18310 | 1104 |
| X-n190-k8 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 316.873 | 18650.9 | 0.420106 | 18334 | 1104 |
| X-n204-k19 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 6619.74 | 27832.7 | 0.420197 | 21213 | 15884 |
| X-n204-k19 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 5029.81 | 26242.8 | 0.419606 | 21213 | 15884 |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 6187.1 | 30349.8 | 0.415665 | 21213 | 15884 |
| X-n204-k19 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 4267.18 | 25480.2 | 0.419655 | 21213 | 15884 |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 638.48 | 33554.5 | 0.414856 | 32916 | 1616 |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 482.984 | 33399 | 0.413029 | 32916 | 1616 |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 605.836 | 33819.8 | 0.410096 | 32916 | 1616 |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 417.265 | 33333.3 | 0.412596 | 32916 | 1616 |
| X-n214-k11 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 5342.11 | 18425.1 | 0.48169 | 13083 | 10384 |
| X-n214-k11 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 4021.17 | 17744.2 | 0.474742 | 13723 | 10384 |
| X-n214-k11 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 4748.08 | 19824.8 | 0.470329 | 13083 | 10384 |
| X-n214-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 3311.2 | 16170.2 | 0.473521 | 12859 | 10384 |
| X-n219-k73 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 105.157 | 118514 | 0.47656 | 118409 | 219 |
| X-n219-k73 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 79.9599 | 118489 | 0.473853 | 118409 | 219 |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 91.798 | 118541 | 0.473624 | 118409 | 218.954 |
| X-n219-k73 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 64.9144 | 118474 | 0.475872 | 118409 | 219 |
| X-n223-k34 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 605.469 | 48238.5 | 0.454505 | 47633 | 1258 |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 453.222 | 48086.2 | 0.439955 | 47633 | 1258 |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 550.129 | 48425 | 0.44509 | 47633 | 1258 |
| X-n223-k34 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 381.05 | 48014.1 | 0.452523 | 47633 | 1258 |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1931.09 | 35314.1 | 0.474229 | 33383 | 3542 |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1452.31 | 34835.3 | 0.470617 | 33383 | 3542 |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1750.45 | 35703.8 | 0.47163 | 33383 | 3542 |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1208.42 | 34591.4 | 0.469427 | 33383 | 3542 |
| X-n233-k16 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 4800.46 | 28089.5 | 0.454483 | 23289 | 10096 |
| X-n233-k16 | cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 3587.58 | 27090.6 | 0.465819 | 23503 | 10096 |
| X-n233-k16 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 4350.93 | 29382.3 | 0.448405 | 23289 | 10096 |
| X-n233-k16 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 3029.4 | 26318.4 | 0.451293 | 23289 | 10096 |
| X-n237-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 106.921 | 29115.9 | 0.471017 | 29009 | 237.722 |
| X-n237-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 81.1944 | 29090.2 | 0.470932 | 29009 | 237.932 |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 94.3952 | 29146.6 | 0.469958 | 29009 | 236.906 |
| X-n237-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 66.3995 | 29075.4 | 0.469619 | 29009 | 236.856 |
| X-n242-k48 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 687.396 | 92156.4 | 0.473112 | 91469 | 1344 |
| X-n242-k48 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 517.205 | 91986.2 | 0.463444 | 91469 | 1344 |
| X-n242-k48 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 611.725 | 92343.8 | 0.466224 | 91469 | 1344 |
| X-n242-k48 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 426.866 | 91895.9 | 0.470871 | 91469 | 1344 |
| X-n251-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 838.749 | 41303.7 | 0.43748 | 40465 | 1932 |
| X-n251-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 634.767 | 41099.8 | 0.43316 | 40465 | 1932 |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 770.323 | 41585.1 | 0.43368 | 40465 | 1923.68 |
| X-n251-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 534.703 | 40999.7 | 0.43736 | 40465 | 1926.09 |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 6467.14 | 37749.1 | 0.432885 | 31282 | 14053 |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 4841.91 | 36804.9 | 0.432615 | 31963 | 14053 |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 6025.57 | 40101.3 | 0.423038 | 31364 | 14053 |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 4149.22 | 35431.2 | 0.429692 | 31282 | 14053 |
| X-n275-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 108.614 | 22580.6 | 0.417664 | 22472 | 280 |
| X-n275-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 82.7919 | 22554.8 | 0.419781 | 22472 | 280 |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 101.737 | 22624.4 | 0.416934 | 22472 | 279.708 |
| X-n275-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 70.5098 | 22542.5 | 0.416642 | 22472 | 279.971 |
| X-n280-k17 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1805.79 | 40879.8 | 0.461398 | 39074 | 3264 |
| X-n280-k17 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1357.99 | 40432 | 0.446523 | 39074 | 3264 |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 1619.53 | 40419.2 | 0.441577 | 38220 | 3264 |
| X-n280-k17 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1122.05 | 40196.1 | 0.456272 | 39074 | 3264 |
| X-n284-k15 | atm | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 632.189 | 24260.2 | 0.395265 | 23628 | 1635 |
| X-n284-k15 | cargo | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 471.038 | 24099 | 0.390283 | 23628 | 1635 |
| X-n284-k15 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 627.736 | 24566.6 | 0.383781 | 23628 | 1635 |
| X-n284-k15 | grocery | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 423.755 | 24051.8 | 0.3947 | 23628 | 1635 |

## Full-Scenario Winner Confirmation

| Instance | Domain | Candidate | Fast Stockout | Full Stockout | Stockout Relative Drift | Fast Mean Total Cost | Full Mean Total Cost | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Stable | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | 0.402381 | 0.40419 | 0.00447691 | 30121.6 | 30092 | 0.000984556 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | cargo | ortools:nominal_or_tools | 0.403429 | 0.407714 | 0.0105116 | 29399.2 | 29375.6 | 0.000804798 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | 0.404762 | 0.405048 | 0.000705384 | 31507.2 | 31482.5 | 0.000786546 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | grocery | ortools:nominal_or_tools | 0.404762 | 0.404571 | 0.00047081 | 29145.2 | 29129.8 | 0.00053046 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | 0.41945 | 0.415688 | 0.00904878 | 16790.2 | 16789.3 | 5.32606e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | 0.424128 | 0.416606 | 0.0180577 | 16700.4 | 16699.7 | 3.89006e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.417431 | 0.411651 | 0.0140406 | 16928.7 | 16927 | 9.94206e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | 0.416514 | 0.414495 | 0.00486941 | 16660.9 | 16660.4 | 3.2661e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n115-k10 | atm | ortools:nominal_or_tools | 0.390789 | 0.39307 | 0.00580228 | 13888 | 13880.8 | 0.000520465 | yes | yes | yes | safe |
| X-n115-k10 | cargo | ortools:nominal_or_tools | 0.400439 | 0.397193 | 0.00817138 | 13691.2 | 13685.7 | 0.000407089 | yes | yes | yes | safe |
| X-n115-k10 | cold_chain | ortools:nominal_or_tools | 0.383158 | 0.381579 | 0.00413793 | 14177.4 | 14171.3 | 0.000424269 | yes | yes | yes | safe |
| X-n115-k10 | grocery | ortools:nominal_or_tools | 0.385877 | 0.387368 | 0.00384964 | 13626.7 | 13622.2 | 0.000325952 | yes | yes | yes | safe |
| X-n120-k6 | atm | ortools:nominal_or_tools | 0.428992 | 0.429412 | 0.000978474 | 14084.4 | 14084.1 | 2.30193e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_or_tools | 0.429244 | 0.430252 | 0.00234375 | 14072.6 | 14072.3 | 2.46323e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | 0.432017 | 0.431345 | 0.00155854 | 14103 | 14102.6 | 2.98908e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_or_tools | 0.432017 | 0.431933 | 0.000194553 | 14066.6 | 14066.4 | 1.35661e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | atm | ortools:robust_mean_2std_scaled_or_tools | 0.422031 | 0.419219 | 0.00670891 | 34057.3 | 34055.7 | 4.86233e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.407656 | 0.404609 | 0.00753041 | 33980 | 33978.3 | 4.90639e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | 0.414453 | 0.411328 | 0.00759734 | 34178.9 | 34177.2 | 4.85825e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:robust_mean_2std_scaled_or_tools | 0.42 | 0.419766 | 0.000558347 | 33951.8 | 33951.1 | 2.13329e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n134-k13 | atm | ortools:quantile_p75_scaled_or_tools | 0.460451 | 0.457368 | 0.0067401 | 18505.7 | 18469.6 | 0.0019553 | yes | yes | yes | safe |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | 0.448496 | 0.445338 | 0.007091 | 17495.4 | 17466.8 | 0.00163906 | yes | yes | yes | safe |
| X-n134-k13 | cold_chain | ortools:nominal_or_tools | 0.457068 | 0.454737 | 0.00512566 | 18203.3 | 18176.2 | 0.00149295 | yes | yes | yes | safe |
| X-n134-k13 | grocery | ortools:nominal_or_tools | 0.458346 | 0.456541 | 0.00395257 | 15713.7 | 15693.7 | 0.00127406 | yes | yes | yes | safe |
| X-n139-k10 | atm | ortools:nominal_or_tools | 0.418913 | 0.415725 | 0.00766951 | 15254.7 | 15251.9 | 0.000187403 | yes | yes | yes | safe |
| X-n139-k10 | cargo | ortools:nominal_or_tools | 0.421232 | 0.416522 | 0.0113083 | 15148.8 | 15145.9 | 0.000194443 | yes | yes | yes | safe |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | 0.413116 | 0.412899 | 0.000526501 | 15424.6 | 15421.8 | 0.000181071 | yes | yes | yes | safe |
| X-n139-k10 | grocery | ortools:nominal_or_tools | 0.418478 | 0.41558 | 0.00697472 | 15103.5 | 15101.4 | 0.000139072 | yes | yes | yes | safe |
| X-n143-k7 | atm | ortools:quantile_p90_scaled_or_tools | 0.314085 | 0.312042 | 0.0065448 | 21042.4 | 21018.1 | 0.00115894 | yes | yes | yes | safe |
| X-n143-k7 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.308451 | 0.307042 | 0.00458716 | 20153.8 | 20130 | 0.00118114 | yes | yes | yes | safe |
| X-n143-k7 | cold_chain | ortools:proxy_mean_or_tools | 0.300915 | 0.300634 | 0.000936988 | 23496.3 | 23477.5 | 0.000798247 | yes | yes | yes | safe |
| X-n143-k7 | grocery | ortools:quantile_p75_scaled_or_tools | 0.309789 | 0.309366 | 0.00136581 | 19810.8 | 19796.7 | 0.000710838 | yes | yes | yes | safe |
| X-n157-k13 | atm | ortools:nominal_or_tools | 0.485833 | 0.485769 | 0.000131961 | 17479.3 | 17478.8 | 2.7977e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n157-k13 | cargo | ortools:nominal_or_tools | 0.488013 | 0.484423 | 0.00741035 | 17461.2 | 17460.7 | 2.37057e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | 0.484679 | 0.482821 | 0.00385024 | 17497.7 | 17497.2 | 2.8277e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n157-k13 | grocery | ortools:nominal_or_tools | 0.484936 | 0.483718 | 0.00251789 | 17450.1 | 17449.8 | 1.82655e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n162-k11 | atm | ortools:nominal_or_tools | 0.396025 | 0.395217 | 0.00204306 | 19460.5 | 19418.4 | 0.00217061 | yes | yes | yes | safe |
| X-n162-k11 | cargo | ortools:nominal_or_tools | 0.404969 | 0.402857 | 0.00524206 | 18315.1 | 18268.3 | 0.00256399 | yes | yes | yes | safe |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | 0.387702 | 0.389689 | 0.00510041 | 21763 | 21711.6 | 0.00236985 | yes | yes | yes | safe |
| X-n162-k11 | grocery | ortools:nominal_or_tools | 0.394348 | 0.392671 | 0.0042708 | 17869.4 | 17840.8 | 0.00160499 | yes | yes | yes | safe |
| X-n167-k10 | atm | ortools:nominal_or_tools | 0.417952 | 0.419277 | 0.00316092 | 23163.2 | 23158.8 | 0.000193982 | yes | yes | yes | safe |
| X-n167-k10 | cargo | ortools:nominal_or_tools | 0.415663 | 0.41741 | 0.00418531 | 23039 | 23034.5 | 0.000197099 | yes | yes | yes | safe |
| X-n167-k10 | cold_chain | ortools:nominal_or_tools | 0.417892 | 0.418976 | 0.00258807 | 23377.4 | 23374.2 | 0.000135002 | yes | yes | yes | safe |
| X-n167-k10 | grocery | ortools:nominal_or_tools | 0.421627 | 0.422108 | 0.00114172 | 22984 | 22980.9 | 0.000131893 | yes | yes | yes | safe |
| X-n181-k23 | atm | ortools:nominal_or_tools | 0.438 | 0.437 | 0.00228833 | 26308.7 | 26307.9 | 2.77378e-05 | yes | yes | yes | safe |
| X-n181-k23 | cargo | ortools:nominal_or_tools | 0.439333 | 0.437722 | 0.00368067 | 26290.2 | 26289.7 | 1.83128e-05 | yes | yes | yes | safe |
| X-n181-k23 | cold_chain | ortools:nominal_or_tools | 0.435111 | 0.432389 | 0.00629577 | 26335.6 | 26335 | 2.23793e-05 | yes | yes | yes | safe |
| X-n181-k23 | grocery | ortools:nominal_or_tools | 0.435778 | 0.436111 | 0.000764331 | 26281 | 26280.6 | 1.44611e-05 | yes | yes | yes | safe |
| X-n186-k15 | atm | ortools:nominal_or_tools | 0.412432 | 0.411622 | 0.0019698 | 32112.8 | 32086.5 | 0.00082061 | yes | yes | yes | safe |
| X-n186-k15 | cargo | ortools:nominal_or_tools | 0.412054 | 0.410919 | 0.00276243 | 30634.3 | 30613.4 | 0.000682621 | yes | yes | yes | safe |
| X-n186-k15 | cold_chain | ortools:nominal_or_tools | 0.411568 | 0.409784 | 0.00435299 | 34349.4 | 34321.8 | 0.000804392 | yes | yes | yes | safe |
| X-n186-k15 | grocery | ortools:nominal_or_tools | 0.412865 | 0.412595 | 0.00065505 | 29945.5 | 29928.1 | 0.000583427 | yes | yes | yes | safe |
| X-n190-k8 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.422275 | 0.418254 | 0.00961417 | 18821.4 | 18818.4 | 0.000160685 | yes | yes | yes | safe |
| X-n190-k8 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.417619 | 0.41254 | 0.0123124 | 18700.7 | 18698.5 | 0.000119082 | yes | yes | yes | safe |
| X-n190-k8 | cold_chain | ortools:quantile_p90_scaled_or_tools | 0.412063 | 0.411323 | 0.00180087 | 18978.9 | 18976.2 | 0.000140141 | yes | yes | yes | safe |
| X-n190-k8 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.420106 | 0.416984 | 0.00748636 | 18650.9 | 18648.8 | 0.000111801 | yes | yes | yes | safe |
| X-n204-k19 | atm | ortools:nominal_or_tools | 0.420197 | 0.419803 | 0.000938747 | 27832.7 | 27795.1 | 0.00135523 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_or_tools | 0.419606 | 0.416798 | 0.00673679 | 26242.8 | 26212.3 | 0.00116339 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | 0.415665 | 0.414778 | 0.00213777 | 30349.8 | 30319.1 | 0.00101086 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | 0.419655 | 0.42 | 0.000821018 | 25480.2 | 25455.3 | 0.000977882 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | 0.414856 | 0.411731 | 0.00758991 | 33554.5 | 33549.3 | 0.000154625 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | 0.413029 | 0.409231 | 0.00928102 | 33399 | 33393.9 | 0.000151614 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.410096 | 0.406346 | 0.00922858 | 33819.8 | 33815.4 | 0.000128447 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | 0.412596 | 0.409904 | 0.00656814 | 33333.3 | 33330.5 | 8.2835e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | atm | ortools:quantile_p75_scaled_or_tools | 0.48169 | 0.478404 | 0.00686948 | 18425.1 | 18393.5 | 0.00171724 | yes | yes | yes | safe |
| X-n214-k11 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.474742 | 0.471221 | 0.00747235 | 17744.2 | 17713 | 0.00175848 | yes | yes | yes | safe |
| X-n214-k11 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.470329 | 0.467371 | 0.00632848 | 19824.8 | 19790.2 | 0.00174745 | yes | yes | yes | safe |
| X-n214-k11 | grocery | ortools:nominal_or_tools | 0.473521 | 0.470376 | 0.00668729 | 16170.2 | 16150.8 | 0.00120175 | yes | yes | yes | safe |
| X-n219-k73 | atm | ortools:nominal_or_tools | 0.47656 | 0.474908 | 0.00347725 | 118514 | 118514 | 4.51946e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | 0.473853 | 0.473394 | 0.000968992 | 118489 | 118488 | 3.93247e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | 0.473624 | 0.47344 | 0.000387559 | 118541 | 118540 | 5.18687e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | 0.475872 | 0.474312 | 0.0032882 | 118474 | 118474 | 3.02031e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.454505 | 0.449955 | 0.0101111 | 48238.5 | 48235.4 | 6.3538e-05 | yes | yes | yes | safe |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.439955 | 0.44027 | 0.000716186 | 48086.2 | 48083.9 | 4.78393e-05 | yes | yes | yes | safe |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | 0.44509 | 0.442252 | 0.00641679 | 48425 | 48422.4 | 5.37159e-05 | yes | yes | yes | safe |
| X-n223-k34 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.452523 | 0.448423 | 0.00914114 | 48014.1 | 48012.3 | 3.63243e-05 | yes | yes | yes | safe |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | 0.474229 | 0.461278 | 0.0280775 | 35314.1 | 35300.3 | 0.000389827 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | 0.470617 | 0.452643 | 0.039708 | 34835.3 | 34822.2 | 0.000376284 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.47163 | 0.459207 | 0.027053 | 35703.8 | 35690.4 | 0.000376257 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | 0.469427 | 0.456079 | 0.0292669 | 34591.4 | 34583.9 | 0.000217854 | yes | no | no | final_full_required: domain ranking flip |
| X-n233-k16 | atm | ortools:proxy_mean_scaled_or_tools | 0.454483 | 0.45181 | 0.0059149 | 28089.5 | 28069.3 | 0.000719935 | yes | yes | yes | safe |
| X-n233-k16 | cargo | ortools:quantile_p90_scaled_or_tools | 0.465819 | 0.467112 | 0.00276829 | 27090.6 | 27075.7 | 0.000548333 | yes | yes | yes | safe |
| X-n233-k16 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.448405 | 0.445647 | 0.00619015 | 29382.3 | 29366.4 | 0.000544025 | yes | yes | yes | safe |
| X-n233-k16 | grocery | ortools:proxy_mean_scaled_or_tools | 0.451293 | 0.448707 | 0.00576369 | 26318.4 | 26303.1 | 0.000581875 | yes | yes | yes | safe |
| X-n237-k14 | atm | ortools:nominal_or_tools | 0.471017 | 0.472203 | 0.00251256 | 29115.9 | 29115.1 | 2.89791e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_or_tools | 0.470932 | 0.47161 | 0.00143756 | 29090.2 | 29089.5 | 2.27604e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | 0.469958 | 0.469831 | 0.000270563 | 29146.6 | 29145.8 | 2.52982e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_or_tools | 0.469619 | 0.470805 | 0.00252003 | 29075.4 | 29074.9 | 1.69503e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n242-k48 | atm | ortools:quantile_p75_scaled_or_tools | 0.473112 | 0.467801 | 0.0113536 | 92156.4 | 92152.9 | 3.76682e-05 | yes | yes | yes | safe |
| X-n242-k48 | cargo | ortools:quantile_p75_scaled_or_tools | 0.463444 | 0.458382 | 0.0110437 | 91986.2 | 91983.6 | 2.82034e-05 | yes | yes | yes | safe |
| X-n242-k48 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.466224 | 0.461286 | 0.0107043 | 92343.8 | 92341 | 3.06611e-05 | yes | yes | yes | safe |
| X-n242-k48 | grocery | ortools:quantile_p75_scaled_or_tools | 0.470871 | 0.466556 | 0.00924938 | 91895.9 | 91893.7 | 2.39209e-05 | yes | yes | yes | safe |
| X-n251-k28 | atm | ortools:nominal_or_tools | 0.43748 | 0.4358 | 0.00385498 | 41303.7 | 41299.8 | 9.50027e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | cargo | ortools:nominal_or_tools | 0.43316 | 0.43204 | 0.00259235 | 41099.8 | 41095.9 | 9.33851e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | 0.43368 | 0.43236 | 0.00305301 | 41585.1 | 41581.6 | 8.38037e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | grocery | ortools:nominal_or_tools | 0.43736 | 0.43616 | 0.00275128 | 40999.7 | 40997.7 | 4.91559e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | 0.432885 | 0.428731 | 0.00968871 | 37749.1 | 37675.6 | 0.00195226 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.432615 | 0.429 | 0.00842747 | 36804.9 | 36751.4 | 0.00145695 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | 0.423038 | 0.417962 | 0.0121469 | 40101.3 | 40034.7 | 0.00166421 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_or_tools | 0.429692 | 0.426962 | 0.00639582 | 35431.2 | 35389 | 0.00119254 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | atm | ortools:nominal_or_tools | 0.417664 | 0.417956 | 0.000698568 | 22580.6 | 22579.9 | 3.11968e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cargo | ortools:nominal_or_tools | 0.419781 | 0.418285 | 0.00357735 | 22554.8 | 22554.2 | 2.53688e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | 0.416934 | 0.415985 | 0.0022811 | 22624.4 | 22623.7 | 3.27768e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | grocery | ortools:nominal_or_tools | 0.416642 | 0.417007 | 0.000875197 | 22542.5 | 22542.1 | 1.98041e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | atm | ortools:proxy_mean_scaled_or_tools | 0.461398 | 0.459319 | 0.00452595 | 40879.8 | 40871.3 | 0.000206542 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | cargo | ortools:proxy_mean_scaled_or_tools | 0.446523 | 0.444086 | 0.0054883 | 40432 | 40426 | 0.000147771 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | 0.441577 | 0.445018 | 0.00773196 | 40419.2 | 40410.3 | 0.000221028 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | grocery | ortools:proxy_mean_scaled_or_tools | 0.456272 | 0.455448 | 0.00181003 | 40196.1 | 40191.3 | 0.000117481 | yes | no | no | final_full_required: domain ranking flip |
| X-n284-k15 | atm | ortools:robust_mean_2std_scaled_or_tools | 0.395265 | 0.389117 | 0.0158009 | 24260.2 | 24254.5 | 0.000236419 | yes | yes | yes | safe |
| X-n284-k15 | cargo | ortools:robust_mean_2std_scaled_or_tools | 0.390283 | 0.384735 | 0.0144195 | 24099 | 24094.5 | 0.000186907 | yes | yes | yes | safe |
| X-n284-k15 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | 0.383781 | 0.378763 | 0.0132475 | 24566.6 | 24560.7 | 0.000242306 | yes | yes | yes | safe |
| X-n284-k15 | grocery | ortools:robust_mean_2std_scaled_or_tools | 0.3947 | 0.388516 | 0.0159163 | 24051.8 | 24048.6 | 0.000131823 | yes | yes | yes | safe |

## Domain Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | cold_chain > grocery > cargo > atm | cargo > cold_chain > grocery > atm | yes | 0.4 |  |
| X-n110-k13 | 4 | cargo > atm > cold_chain > grocery | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n115-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n120-k6 | 4 | cold_chain > grocery > cargo > atm | grocery > cold_chain > cargo > atm | yes | 0.8 |  |
| X-n129-k18 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n134-k13 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n139-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n143-k7 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n157-k13 | 4 | cargo > atm > grocery > cold_chain | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n162-k11 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n167-k10 | 4 | grocery > atm > cold_chain > cargo | grocery > atm > cold_chain > cargo | no | 1 |  |
| X-n181-k23 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n186-k15 | 4 | grocery > atm > cargo > cold_chain | grocery > atm > cargo > cold_chain | no | 1 |  |
| X-n190-k8 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n204-k19 | 4 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | yes | 0.8 |  |
| X-n209-k16 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n214-k11 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n219-k73 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n223-k34 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n228-k23 | 4 | atm > cold_chain > cargo > grocery | atm > cold_chain > grocery > cargo | yes | 0.8 |  |
| X-n233-k16 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n237-k14 | 4 | atm > cargo > cold_chain > grocery | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n242-k48 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n251-k28 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n261-k13 | 4 | atm > cargo > grocery > cold_chain | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n275-k28 | 4 | cargo > atm > cold_chain > grocery | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n280-k17 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n284-k15 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |

## Route Candidates

| Instance | Candidate | Route Feasible | Route Count | Route Cost | Planned Route Load Ratio | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| X-n101-k25 | ortools:nominal_or_tools | no | 0 |  | 0.999417 | ortools_no_solution |
| X-n101-k25 | ortools:proxy_mean_or_tools | no | 0 |  | 1.12029 | total_load_exceeds_fleet_capacity |
| X-n101-k25 | ortools:quantile_p75_or_tools | no | 0 |  | 1.31075 | total_load_exceeds_fleet_capacity |
| X-n101-k25 | ortools:quantile_p90_or_tools | no | 0 |  | 1.57519 | total_load_exceeds_fleet_capacity |
| X-n101-k25 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.47146 | total_load_exceeds_fleet_capacity |
| X-n101-k25 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.82262 | single_node_exceeds_capacity |
| X-n101-k25 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n101-k25 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n101-k25 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n101-k25 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n101-k25 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
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
| X-n110-k13 | ortools:nominal_or_tools | yes | 13 | 15387 | 0.951049 |  |
| X-n110-k13 | ortools:proxy_mean_or_tools | no | 0 |  | 1.07472 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:quantile_p75_or_tools | no | 0 |  | 1.24557 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.49375 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39846 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.72219 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:proxy_mean_scaled_or_tools | yes | 13 | 16426 | 0.995 |  |
| X-n110-k13 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n110-k13 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n110-k13 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n115-k10 | ortools:nominal_or_tools | yes | 10 | 13099 | 0.908284 |  |
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
| X-n120-k6 | ortools:nominal_or_tools | yes | 6 | 14034 | 0.944444 |  |
| X-n120-k6 | ortools:proxy_mean_or_tools | yes | 6 | 14034 | 1.05969 |  |
| X-n120-k6 | ortools:quantile_p75_or_tools | yes | 6 | 14034 | 1.22264 |  |
| X-n120-k6 | ortools:quantile_p90_or_tools | no | 0 |  | 1.4497 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.36156 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.66342 | total_load_exceeds_fleet_capacity |
| X-n120-k6 | ortools:proxy_mean_scaled_or_tools | yes | 6 | 14034 | 0.995 |  |
| X-n120-k6 | ortools:quantile_p75_scaled_or_tools | yes | 6 | 14034 | 0.995 |  |
| X-n120-k6 | ortools:quantile_p90_scaled_or_tools | yes | 6 | 14034 | 0.995 |  |
| X-n120-k6 | ortools:robust_mean_1std_scaled_or_tools | yes | 6 | 14034 | 0.995 |  |
| X-n120-k6 | ortools:robust_mean_2std_scaled_or_tools | yes | 6 | 14034 | 0.995 |  |
| X-n125-k30 | ortools:nominal_or_tools | no | 0 |  | 0.98156 | ortools_no_solution |
| X-n125-k30 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09612 | total_load_exceeds_fleet_capacity |
| X-n125-k30 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28196 | total_load_exceeds_fleet_capacity |
| X-n125-k30 | ortools:quantile_p90_or_tools | no | 0 |  | 1.55071 | total_load_exceeds_fleet_capacity |
| X-n125-k30 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.45711 | total_load_exceeds_fleet_capacity |
| X-n125-k30 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.8181 | single_node_exceeds_capacity |
| X-n125-k30 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n125-k30 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n125-k30 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n125-k30 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n125-k30 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n129-k18 | ortools:nominal_or_tools | yes | 18 | 30677 | 0.947293 |  |
| X-n129-k18 | ortools:proxy_mean_or_tools | no | 0 |  | 1.03581 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:quantile_p75_or_tools | no | 0 |  | 1.20693 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:quantile_p90_or_tools | no | 0 |  | 1.46375 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.36925 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.7027 | total_load_exceeds_fleet_capacity |
| X-n129-k18 | ortools:proxy_mean_scaled_or_tools | yes | 18 | 31770 | 0.995 |  |
| X-n129-k18 | ortools:quantile_p75_scaled_or_tools | yes | 18 | 31451 | 0.995 |  |
| X-n129-k18 | ortools:quantile_p90_scaled_or_tools | yes | 18 | 33039 | 0.995 |  |
| X-n129-k18 | ortools:robust_mean_1std_scaled_or_tools | yes | 18 | 32958 | 0.995 |  |
| X-n129-k18 | ortools:robust_mean_2std_scaled_or_tools | yes | 18 | 33757 | 0.995 |  |
| X-n134-k13 | ortools:nominal_or_tools | yes | 13 | 13345 | 0.983371 |  |
| X-n134-k13 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09862 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:quantile_p75_or_tools | no | 0 |  | 1.2792 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53346 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.43845 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.77828 | total_load_exceeds_fleet_capacity |
| X-n134-k13 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n134-k13 | ortools:quantile_p75_scaled_or_tools | yes | 13 | 14712 | 0.995 |  |
| X-n134-k13 | ortools:quantile_p90_scaled_or_tools | yes | 13 | 14999 | 0.995 |  |
| X-n134-k13 | ortools:robust_mean_1std_scaled_or_tools | yes | 13 | 13638 | 0.995 |  |
| X-n134-k13 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n139-k10 | ortools:nominal_or_tools | yes | 10 | 14826 | 0.980189 |  |
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
| X-n143-k7 | ortools:nominal_or_tools | yes | 7 | 16647 | 0.897359 |  |
| X-n143-k7 | ortools:proxy_mean_or_tools | yes | 7 | 19116 | 0.9959 |  |
| X-n143-k7 | ortools:quantile_p75_or_tools | no | 0 |  | 1.1607 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:quantile_p90_or_tools | no | 0 |  | 1.40025 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.30625 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.6166 | total_load_exceeds_fleet_capacity |
| X-n143-k7 | ortools:proxy_mean_scaled_or_tools | yes | 7 | 18707 | 0.995 |  |
| X-n143-k7 | ortools:quantile_p75_scaled_or_tools | yes | 7 | 17963 | 0.995 |  |
| X-n143-k7 | ortools:quantile_p90_scaled_or_tools | yes | 7 | 18531 | 0.995 |  |
| X-n143-k7 | ortools:robust_mean_1std_scaled_or_tools | yes | 7 | 18293 | 0.995 |  |
| X-n143-k7 | ortools:robust_mean_2std_scaled_or_tools | yes | 7 | 18682 | 0.995 |  |
| X-n148-k46 | ortools:nominal_or_tools | no | 0 |  | 0.986715 | ortools_no_solution |
| X-n148-k46 | ortools:proxy_mean_or_tools | no | 0 |  | 1.10696 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:quantile_p75_or_tools | no | 0 |  | 1.29172 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:quantile_p90_or_tools | no | 0 |  | 1.56278 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.4554 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.80384 | single_node_exceeds_capacity |
| X-n148-k46 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n148-k46 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n148-k46 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n148-k46 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n153-k22 | ortools:nominal_or_tools | no | 0 |  | 0.968434 | ortools_no_solution |
| X-n153-k22 | ortools:proxy_mean_or_tools | no | 0 |  | 1.08356 | total_load_exceeds_fleet_capacity |
| X-n153-k22 | ortools:quantile_p75_or_tools | no | 0 |  | 1.27571 | total_load_exceeds_fleet_capacity |
| X-n153-k22 | ortools:quantile_p90_or_tools | no | 0 |  | 1.56029 | single_node_exceeds_capacity |
| X-n153-k22 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.44686 | single_node_exceeds_capacity |
| X-n153-k22 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.81016 | single_node_exceeds_capacity |
| X-n153-k22 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n153-k22 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n153-k22 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n153-k22 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n153-k22 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n157-k13 | ortools:nominal_or_tools | yes | 13 | 17404 | 1 |  |
| X-n157-k13 | ortools:proxy_mean_or_tools | yes | 13 | 17404 | 1.10253 |  |
| X-n157-k13 | ortools:quantile_p75_or_tools | yes | 13 | 17404 | 1.27393 |  |
| X-n157-k13 | ortools:quantile_p90_or_tools | no | 0 |  | 1.50781 | total_load_exceeds_fleet_capacity |
| X-n157-k13 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.41547 | total_load_exceeds_fleet_capacity |
| X-n157-k13 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.72842 | total_load_exceeds_fleet_capacity |
| X-n157-k13 | ortools:proxy_mean_scaled_or_tools | yes | 13 | 17404 | 0.995 |  |
| X-n157-k13 | ortools:quantile_p75_scaled_or_tools | yes | 13 | 17404 | 0.995 |  |
| X-n157-k13 | ortools:quantile_p90_scaled_or_tools | yes | 13 | 17404 | 0.995 |  |
| X-n157-k13 | ortools:robust_mean_1std_scaled_or_tools | yes | 13 | 17404 | 0.995 |  |
| X-n157-k13 | ortools:robust_mean_2std_scaled_or_tools | yes | 13 | 17404 | 0.995 |  |
| X-n162-k11 | ortools:nominal_or_tools | yes | 11 | 14676 | 0.944247 |  |
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
| X-n172-k51 | ortools:nominal_or_tools | no | 0 |  | 0.985507 | ortools_no_solution |
| X-n172-k51 | ortools:proxy_mean_or_tools | no | 0 |  | 1.08888 | total_load_exceeds_fleet_capacity |
| X-n172-k51 | ortools:quantile_p75_or_tools | no | 0 |  | 1.27118 | total_load_exceeds_fleet_capacity |
| X-n172-k51 | ortools:quantile_p90_or_tools | no | 0 |  | 1.52711 | single_node_exceeds_capacity |
| X-n172-k51 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.42457 | total_load_exceeds_fleet_capacity |
| X-n172-k51 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.76026 | single_node_exceeds_capacity |
| X-n172-k51 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n172-k51 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n172-k51 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n172-k51 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n172-k51 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n176-k26 | ortools:nominal_or_tools | no | 0 |  | 0.983749 | ortools_no_solution |
| X-n176-k26 | ortools:proxy_mean_or_tools | no | 0 |  | 1.07706 | total_load_exceeds_fleet_capacity |
| X-n176-k26 | ortools:quantile_p75_or_tools | no | 0 |  | 1.2635 | total_load_exceeds_fleet_capacity |
| X-n176-k26 | ortools:quantile_p90_or_tools | no | 0 |  | 1.54349 | single_node_exceeds_capacity |
| X-n176-k26 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.44081 | single_node_exceeds_capacity |
| X-n176-k26 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.80455 | single_node_exceeds_capacity |
| X-n176-k26 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n176-k26 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n176-k26 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n176-k26 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n176-k26 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n181-k23 | ortools:nominal_or_tools | yes | 23 | 26232 | 0.978261 |  |
| X-n181-k23 | ortools:proxy_mean_or_tools | yes | 23 | 26232 | 1.07587 |  |
| X-n181-k23 | ortools:quantile_p75_or_tools | yes | 23 | 26232 | 1.24209 |  |
| X-n181-k23 | ortools:quantile_p90_or_tools | no | 0 |  | 1.47136 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.38655 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.69723 | total_load_exceeds_fleet_capacity |
| X-n181-k23 | ortools:proxy_mean_scaled_or_tools | yes | 23 | 26232 | 0.995 |  |
| X-n181-k23 | ortools:quantile_p75_scaled_or_tools | yes | 23 | 26232 | 0.995 |  |
| X-n181-k23 | ortools:quantile_p90_scaled_or_tools | yes | 23 | 26232 | 0.995 |  |
| X-n181-k23 | ortools:robust_mean_1std_scaled_or_tools | yes | 23 | 26232 | 0.995 |  |
| X-n181-k23 | ortools:robust_mean_2std_scaled_or_tools | yes | 23 | 26232 | 0.995 |  |
| X-n186-k15 | ortools:nominal_or_tools | yes | 15 | 25982 | 0.948186 |  |
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
| X-n190-k8 | ortools:nominal_or_tools | yes | 8 | 18122 | 0.944746 |  |
| X-n190-k8 | ortools:proxy_mean_or_tools | no | 0 |  | 1.05354 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:quantile_p75_or_tools | no | 0 |  | 1.22919 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:quantile_p90_or_tools | no | 0 |  | 1.48526 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.38498 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71643 | total_load_exceeds_fleet_capacity |
| X-n190-k8 | ortools:proxy_mean_scaled_or_tools | yes | 8 | 18282 | 0.995 |  |
| X-n190-k8 | ortools:quantile_p75_scaled_or_tools | yes | 8 | 18293 | 0.995 |  |
| X-n190-k8 | ortools:quantile_p90_scaled_or_tools | yes | 8 | 18310 | 0.995 |  |
| X-n190-k8 | ortools:robust_mean_1std_scaled_or_tools | yes | 8 | 18334 | 0.995 |  |
| X-n190-k8 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n195-k51 | ortools:nominal_or_tools | no | 0 |  | 0.997508 | ortools_no_solution |
| X-n195-k51 | ortools:proxy_mean_or_tools | no | 0 |  | 1.10918 | total_load_exceeds_fleet_capacity |
| X-n195-k51 | ortools:quantile_p75_or_tools | no | 0 |  | 1.2944 | total_load_exceeds_fleet_capacity |
| X-n195-k51 | ortools:quantile_p90_or_tools | no | 0 |  | 1.56338 | total_load_exceeds_fleet_capacity |
| X-n195-k51 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.46036 | total_load_exceeds_fleet_capacity |
| X-n195-k51 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.81153 | single_node_exceeds_capacity |
| X-n195-k51 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n195-k51 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n195-k51 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n195-k51 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n195-k51 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n200-k36 | ortools:nominal_or_tools | no | 0 |  | 0.985558 | ortools_no_solution |
| X-n200-k36 | ortools:proxy_mean_or_tools | no | 0 |  | 1.0951 | total_load_exceeds_fleet_capacity |
| X-n200-k36 | ortools:quantile_p75_or_tools | no | 0 |  | 1.26728 | total_load_exceeds_fleet_capacity |
| X-n200-k36 | ortools:quantile_p90_or_tools | no | 0 |  | 1.51648 | total_load_exceeds_fleet_capacity |
| X-n200-k36 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.42125 | total_load_exceeds_fleet_capacity |
| X-n200-k36 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.74741 | total_load_exceeds_fleet_capacity |
| X-n200-k36 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n200-k36 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n200-k36 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n200-k36 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n200-k36 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n204-k19 | ortools:nominal_or_tools | yes | 19 | 21213 | 0.952846 |  |
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
| X-n209-k16 | ortools:nominal_or_tools | yes | 16 | 32468 | 0.957302 |  |
| X-n209-k16 | ortools:proxy_mean_or_tools | no | 0 |  | 1.06964 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:quantile_p75_or_tools | no | 0 |  | 1.23784 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:quantile_p90_or_tools | no | 0 |  | 1.4837 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.39098 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.71232 | total_load_exceeds_fleet_capacity |
| X-n209-k16 | ortools:proxy_mean_scaled_or_tools | yes | 16 | 32551 | 0.995 |  |
| X-n209-k16 | ortools:quantile_p75_scaled_or_tools | yes | 16 | 32916 | 0.995 |  |
| X-n209-k16 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n209-k16 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:nominal_or_tools | yes | 11 | 12859 | 0.997304 |  |
| X-n214-k11 | ortools:proxy_mean_or_tools | no | 0 |  | 1.10989 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:quantile_p75_or_tools | no | 0 |  | 1.29515 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:quantile_p90_or_tools | no | 0 |  | 1.55797 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.4535 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.79711 | total_load_exceeds_fleet_capacity |
| X-n214-k11 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n214-k11 | ortools:quantile_p75_scaled_or_tools | yes | 11 | 13083 | 0.995 |  |
| X-n214-k11 | ortools:quantile_p90_scaled_or_tools | yes | 11 | 12479 | 0.995 |  |
| X-n214-k11 | ortools:robust_mean_1std_scaled_or_tools | yes | 11 | 13723 | 0.995 |  |
| X-n214-k11 | ortools:robust_mean_2std_scaled_or_tools | yes | 11 | 13222 | 0.995 |  |
| X-n219-k73 | ortools:nominal_or_tools | yes | 73 | 118409 | 0.995434 |  |
| X-n219-k73 | ortools:proxy_mean_or_tools | yes | 73 | 118409 | 1.10674 |  |
| X-n219-k73 | ortools:quantile_p75_or_tools | yes | 73 | 118409 | 1.2765 |  |
| X-n219-k73 | ortools:quantile_p90_or_tools | no | 0 |  | 1.51625 | total_load_exceeds_fleet_capacity |
| X-n219-k73 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.42242 | total_load_exceeds_fleet_capacity |
| X-n219-k73 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.7381 | total_load_exceeds_fleet_capacity |
| X-n219-k73 | ortools:proxy_mean_scaled_or_tools | yes | 73 | 118409 | 0.995 |  |
| X-n219-k73 | ortools:quantile_p75_scaled_or_tools | yes | 73 | 118409 | 0.995 |  |
| X-n219-k73 | ortools:quantile_p90_scaled_or_tools | yes | 73 | 118409 | 0.995 |  |
| X-n219-k73 | ortools:robust_mean_1std_scaled_or_tools | yes | 73 | 118409 | 0.995 |  |
| X-n219-k73 | ortools:robust_mean_2std_scaled_or_tools | yes | 73 | 118409 | 0.995 |  |
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
| X-n233-k16 | ortools:nominal_or_tools | no | 0 |  | 0.999703 | ortools_no_solution |
| X-n233-k16 | ortools:proxy_mean_or_tools | no | 0 |  | 1.12266 | total_load_exceeds_fleet_capacity |
| X-n233-k16 | ortools:quantile_p75_or_tools | no | 0 |  | 1.31538 | total_load_exceeds_fleet_capacity |
| X-n233-k16 | ortools:quantile_p90_or_tools | no | 0 |  | 1.58537 | total_load_exceeds_fleet_capacity |
| X-n233-k16 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.47908 | total_load_exceeds_fleet_capacity |
| X-n233-k16 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.83549 | total_load_exceeds_fleet_capacity |
| X-n233-k16 | ortools:proxy_mean_scaled_or_tools | yes | 16 | 23289 | 0.995 |  |
| X-n233-k16 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n233-k16 | ortools:quantile_p90_scaled_or_tools | yes | 16 | 23503 | 0.995 |  |
| X-n233-k16 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n233-k16 | ortools:robust_mean_2std_scaled_or_tools | yes | 16 | 23942 | 0.995 |  |
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
| X-n242-k48 | ortools:nominal_or_tools | yes | 48 | 86573 | 0.985119 |  |
| X-n242-k48 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09819 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28009 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53482 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.43482 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.77144 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:proxy_mean_scaled_or_tools | yes | 48 | 88091 | 0.995 |  |
| X-n242-k48 | ortools:quantile_p75_scaled_or_tools | yes | 48 | 91469 | 0.995 |  |
| X-n242-k48 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n242-k48 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n247-k50 | ortools:nominal_or_tools | no | 0 |  | 0.925373 | ortools_no_solution |
| X-n247-k50 | ortools:proxy_mean_or_tools | no | 0 |  | 1.01348 | total_load_exceeds_fleet_capacity |
| X-n247-k50 | ortools:quantile_p75_or_tools | no | 0 |  | 1.18962 | total_load_exceeds_fleet_capacity |
| X-n247-k50 | ortools:quantile_p90_or_tools | no | 0 |  | 1.45589 | single_node_exceeds_capacity |
| X-n247-k50 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.3509 | single_node_exceeds_capacity |
| X-n247-k50 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.68833 | single_node_exceeds_capacity |
| X-n247-k50 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n247-k50 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n247-k50 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n247-k50 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n247-k50 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
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
| X-n256-k16 | ortools:nominal_or_tools | no | 0 |  | 0.995612 | ortools_no_solution |
| X-n256-k16 | ortools:proxy_mean_or_tools | no | 0 |  | 1.1165 | total_load_exceeds_fleet_capacity |
| X-n256-k16 | ortools:quantile_p75_or_tools | no | 0 |  | 1.28747 | total_load_exceeds_fleet_capacity |
| X-n256-k16 | ortools:quantile_p90_or_tools | no | 0 |  | 1.53745 | total_load_exceeds_fleet_capacity |
| X-n256-k16 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.44223 | total_load_exceeds_fleet_capacity |
| X-n256-k16 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.76796 | total_load_exceeds_fleet_capacity |
| X-n256-k16 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n256-k16 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n256-k16 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n256-k16 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n256-k16 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
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
| X-n266-k58 | ortools:nominal_or_tools | no | 0 |  | 0.992611 | ortools_no_solution |
| X-n266-k58 | ortools:proxy_mean_or_tools | no | 0 |  | 1.09575 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:quantile_p75_or_tools | no | 0 |  | 1.27063 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:quantile_p90_or_tools | no | 0 |  | 1.51069 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.4151 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.73445 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n266-k58 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | total_load_exceeds_fleet_capacity |
| X-n266-k58 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n270-k35 | ortools:nominal_or_tools | no | 0 |  | 0.997265 | ortools_no_solution |
| X-n270-k35 | ortools:proxy_mean_or_tools | no | 0 |  | 1.12529 | total_load_exceeds_fleet_capacity |
| X-n270-k35 | ortools:quantile_p75_or_tools | no | 0 |  | 1.3047 | total_load_exceeds_fleet_capacity |
| X-n270-k35 | ortools:quantile_p90_or_tools | no | 0 |  | 1.56342 | total_load_exceeds_fleet_capacity |
| X-n270-k35 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.46493 | total_load_exceeds_fleet_capacity |
| X-n270-k35 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.80457 | total_load_exceeds_fleet_capacity |
| X-n270-k35 | ortools:proxy_mean_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n270-k35 | ortools:quantile_p75_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n270-k35 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n270-k35 | ortools:robust_mean_1std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| X-n270-k35 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
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
| X-n284-k15 | ortools:nominal_or_tools | yes | 15 | 22522 | 0.933945 |  |
| X-n284-k15 | ortools:proxy_mean_or_tools | no | 0 |  | 1.0341 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:quantile_p75_or_tools | no | 0 |  | 1.20737 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:quantile_p90_or_tools | no | 0 |  | 1.44221 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.35125 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.6684 | total_load_exceeds_fleet_capacity |
| X-n284-k15 | ortools:proxy_mean_scaled_or_tools | yes | 15 | 22663 | 0.995 |  |
| X-n284-k15 | ortools:quantile_p75_scaled_or_tools | yes | 15 | 23026 | 0.995 |  |
| X-n284-k15 | ortools:quantile_p90_scaled_or_tools | yes | 15 | 22673 | 0.995 |  |
| X-n284-k15 | ortools:robust_mean_1std_scaled_or_tools | yes | 15 | 23151 | 0.995 |  |
| X-n284-k15 | ortools:robust_mean_2std_scaled_or_tools | yes | 15 | 23628 | 0.995 |  |

## Interpretation

- A domain winner means that route candidate had the lowest selected evaluation metric after the stochastic loading LP.
- This is not a new routing solver; it is a robust selection layer over existing route providers and load plans.
- `Metric Stability Safe` checks only stockout and mean_total_cost drift; `Strict Stability Safe` also requires no domain stockout ranking flip.
- Infeasible high-quantile or robust plans remain visible because capacity pressure is part of the result.
