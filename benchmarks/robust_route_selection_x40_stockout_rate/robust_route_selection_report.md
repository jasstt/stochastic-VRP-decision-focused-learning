# Robust Route Selection Report

## Scope

This diagnostic evaluates multiple routing candidates with the same stochastic decision layer, then selects a domain-level winner by the configured score metric.

- Data dir: `benchmarks/proxy_cvrplib_x_v4`
- Routing providers: `ortools`
- LP backend: `pulp_cbc`
- LP planning scenario limit: `60`
- Score metric: `stockout_rate`
- Full-scenario winner confirmation: `True`

Fast mode is intended for route-candidate screening. Final decision-driving claims should be rerun with full planning history by passing `--lp-planning-scenario-limit 0`.

## Candidate Coverage

| Domain | Candidate_Rows | Feasible_Rows | Instances | Candidates | Median_Total_Runtime_Sec | Top_Winning_Candidate | Top_Winning_Provider | Top_Winning_Route_Plan | Top_Winner_Count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 440 | 114 | 40 | 11 | 4.99221 | ortools:nominal_or_tools | ortools | nominal_or_tools | 17 |
| cargo | 440 | 114 | 40 | 11 | 4.99221 | ortools:nominal_or_tools | ortools | nominal_or_tools | 17 |
| cold_chain | 440 | 114 | 40 | 11 | 4.99221 | ortools:nominal_or_tools | ortools | nominal_or_tools | 17 |
| grocery | 440 | 114 | 40 | 11 | 4.99221 | ortools:nominal_or_tools | ortools | nominal_or_tools | 18 |

## Winners

| Instance | Domain | Candidate | Routing Provider | Route Plan | Score Value | mean_total_cost | stockout_rate | Route Cost | Optimized Load Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.402381 | 30121.6 | 0.402381 | 27182 | 8400 |
| X-n106-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.403429 | 29399.2 | 0.403429 | 27182 | 8400 |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.404762 | 31507.2 | 0.404762 | 27182 | 8255.29 |
| X-n106-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.404762 | 29145.2 | 0.404762 | 27182 | 8282.21 |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.41945 | 16790.2 | 0.41945 | 16426 | 858 |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.424128 | 16700.4 | 0.424128 | 16426 | 858 |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.417431 | 16928.7 | 0.417431 | 16426 | 858 |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.416514 | 16660.9 | 0.416514 | 16426 | 858 |
| X-n115-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.390789 | 13888 | 0.390789 | 13099 | 1690 |
| X-n115-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.400439 | 13691.2 | 0.400439 | 13099 | 1690 |
| X-n115-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.383158 | 14177.4 | 0.383158 | 13099 | 1684.38 |
| X-n115-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.385877 | 13626.7 | 0.385877 | 13099 | 1690 |
| X-n120-k6 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.428992 | 14084.4 | 0.428992 | 14034 | 126 |
| X-n120-k6 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.429244 | 14072.6 | 0.429244 | 14034 | 126 |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.432017 | 14103 | 0.432017 | 14034 | 123.979 |
| X-n120-k6 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.432017 | 14066.6 | 0.432017 | 14034 | 124.387 |
| X-n129-k18 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.416094 | 31756.3 | 0.416094 | 31451 | 702 |
| X-n129-k18 | cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 0.405938 | 33262.5 | 0.405938 | 33039 | 702 |
| X-n129-k18 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.406562 | 31871.2 | 0.406562 | 31451 | 702 |
| X-n129-k18 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.416328 | 31648.5 | 0.416328 | 31451 | 702 |
| X-n134-k13 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.460451 | 18505.7 | 0.460451 | 14712 | 8359 |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.448496 | 17495.4 | 0.448496 | 14712 | 8359 |
| X-n134-k13 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.454361 | 19605.1 | 0.454361 | 14712 | 8359 |
| X-n134-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.458346 | 15713.7 | 0.458346 | 13345 | 8359 |
| X-n139-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.418913 | 15254.7 | 0.418913 | 14826 | 1060 |
| X-n139-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.421232 | 15148.8 | 0.421232 | 14826 | 1060 |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.413116 | 15424.6 | 0.413116 | 14826 | 1060 |
| X-n139-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.418478 | 15103.5 | 0.418478 | 14826 | 1060 |
| X-n143-k7 | atm | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 0.309296 | 21625.5 | 0.309296 | 19114 | 8330 |
| X-n143-k7 | cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 0.308099 | 20394.5 | 0.308099 | 18531 | 8330 |
| X-n143-k7 | cold_chain | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 0.300634 | 23535.5 | 0.300634 | 19114 | 8330 |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 0.306549 | 20962.3 | 0.306549 | 19114 | 8330 |
| X-n157-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.485833 | 17479.3 | 0.485833 | 17404 | 156 |
| X-n157-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.488013 | 17461.2 | 0.488013 | 17404 | 156 |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.484679 | 17497.7 | 0.484679 | 17404 | 156 |
| X-n157-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.484936 | 17450.1 | 0.484936 | 17404 | 156 |
| X-n162-k11 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.396025 | 19460.5 | 0.396025 | 14676 | 12914 |
| X-n162-k11 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.404969 | 18315.1 | 0.404969 | 14676 | 12914 |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.387702 | 21763 | 0.387702 | 14676 | 12914 |
| X-n162-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.394348 | 17869.4 | 0.394348 | 14676 | 12914 |
| X-n167-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.417952 | 23163.2 | 0.417952 | 22643 | 1330 |
| X-n167-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.415663 | 23039 | 0.415663 | 22643 | 1330 |
| X-n167-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.417892 | 23377.4 | 0.417892 | 22643 | 1297.47 |
| X-n167-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.421627 | 22984 | 0.421627 | 22643 | 1302.61 |
| X-n181-k23 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.438 | 26308.7 | 0.438 | 26232 | 184 |
| X-n181-k23 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.439333 | 26290.2 | 0.439333 | 26232 | 184 |
| X-n181-k23 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.435111 | 26335.6 | 0.435111 | 26232 | 184 |
| X-n181-k23 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.435778 | 26281 | 0.435778 | 26232 | 184 |
| X-n186-k15 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.412432 | 32112.8 | 0.412432 | 25982 | 14343.8 |
| X-n186-k15 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.412054 | 30634.3 | 0.412054 | 25982 | 14389.4 |
| X-n186-k15 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.411568 | 34349.4 | 0.411568 | 25982 | 14223.4 |
| X-n186-k15 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.412865 | 29945.5 | 0.412865 | 25982 | 14245.5 |
| X-n190-k8 | atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 0.420529 | 18797.9 | 0.420529 | 18310 | 1104 |
| X-n190-k8 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.414921 | 18665.2 | 0.414921 | 18293 | 1104 |
| X-n190-k8 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.408836 | 18972.8 | 0.408836 | 18293 | 1104 |
| X-n190-k8 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.418624 | 18611.3 | 0.418624 | 18293 | 1104 |
| X-n204-k19 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.420197 | 27832.7 | 0.420197 | 21213 | 15884 |
| X-n204-k19 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.419606 | 26242.8 | 0.419606 | 21213 | 15884 |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.415665 | 30349.8 | 0.415665 | 21213 | 15884 |
| X-n204-k19 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.419655 | 25480.2 | 0.419655 | 21213 | 15884 |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.414856 | 33554.5 | 0.414856 | 32916 | 1616 |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.413029 | 33399 | 0.413029 | 32916 | 1616 |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.410096 | 33819.8 | 0.410096 | 32916 | 1616 |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.412596 | 33333.3 | 0.412596 | 32916 | 1616 |
| X-n214-k11 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.478075 | 18201.2 | 0.478075 | 12859 | 10384 |
| X-n214-k11 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.473521 | 16893.2 | 0.473521 | 12859 | 10384 |
| X-n214-k11 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.468685 | 19654.6 | 0.468685 | 12859 | 10384 |
| X-n214-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.473521 | 16170.2 | 0.473521 | 12859 | 10384 |
| X-n219-k73 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.47656 | 118514 | 0.47656 | 118409 | 219 |
| X-n219-k73 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.473853 | 118489 | 0.473853 | 118409 | 219 |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.473624 | 118541 | 0.473624 | 118409 | 218.954 |
| X-n219-k73 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.475872 | 118474 | 0.475872 | 118409 | 219 |
| X-n223-k34 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.454144 | 46797.4 | 0.454144 | 46188 | 1258 |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.439955 | 48086.2 | 0.439955 | 47633 | 1258 |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.44509 | 48425 | 0.44509 | 47633 | 1258 |
| X-n223-k34 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.451937 | 46571.3 | 0.451937 | 46188 | 1258 |
| X-n228-k23 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.464361 | 32281.5 | 0.464361 | 30349 | 3542 |
| X-n228-k23 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.452203 | 31801.5 | 0.452203 | 30349 | 3542 |
| X-n228-k23 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.453172 | 32740.6 | 0.453172 | 30349 | 3542 |
| X-n228-k23 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.457357 | 31558.5 | 0.457357 | 30349 | 3542 |
| X-n233-k16 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.454483 | 28089.5 | 0.454483 | 23289 | 10096 |
| X-n233-k16 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.459655 | 26886.9 | 0.459655 | 23289 | 10096 |
| X-n233-k16 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.448405 | 29382.3 | 0.448405 | 23289 | 10096 |
| X-n233-k16 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.451293 | 26318.4 | 0.451293 | 23289 | 10096 |
| X-n237-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.471017 | 29115.9 | 0.471017 | 29009 | 237.722 |
| X-n237-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.470932 | 29090.2 | 0.470932 | 29009 | 237.932 |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.469958 | 29146.6 | 0.469958 | 29009 | 236.906 |
| X-n237-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.469619 | 29075.4 | 0.469619 | 29009 | 236.856 |
| X-n242-k48 | atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.473112 | 92156.4 | 0.473112 | 91469 | 1344 |
| X-n242-k48 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.463444 | 91986.2 | 0.463444 | 91469 | 1344 |
| X-n242-k48 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.466224 | 92343.8 | 0.466224 | 91469 | 1344 |
| X-n242-k48 | grocery | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.470871 | 91895.9 | 0.470871 | 91469 | 1344 |
| X-n251-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.43748 | 41303.7 | 0.43748 | 40465 | 1932 |
| X-n251-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.43316 | 41099.8 | 0.43316 | 40465 | 1932 |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.43368 | 41585.1 | 0.43368 | 40465 | 1923.68 |
| X-n251-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.43736 | 40999.7 | 0.43736 | 40465 | 1926.09 |
| X-n261-k13 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.430885 | 37840.9 | 0.430885 | 31364 | 14053 |
| X-n261-k13 | cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.426077 | 36129.1 | 0.426077 | 31282 | 14053 |
| X-n261-k13 | cold_chain | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 0.421923 | 40067.2 | 0.421923 | 31282 | 14053 |
| X-n261-k13 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 0.428269 | 35515.1 | 0.428269 | 31364 | 14053 |
| X-n275-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.417664 | 22580.6 | 0.417664 | 22472 | 280 |
| X-n275-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.419781 | 22554.8 | 0.419781 | 22472 | 280 |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.416934 | 22624.4 | 0.416934 | 22472 | 279.708 |
| X-n275-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.416642 | 22542.5 | 0.416642 | 22472 | 279.971 |
| X-n280-k17 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.452832 | 40027.9 | 0.452832 | 38220 | 3264 |
| X-n280-k17 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.438387 | 39580.1 | 0.438387 | 38220 | 3264 |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.441577 | 40419.2 | 0.441577 | 38220 | 3264 |
| X-n280-k17 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 0.450215 | 39344.3 | 0.450215 | 38220 | 3264 |
| X-n284-k15 | atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.392721 | 23784.2 | 0.392721 | 23151 | 1635 |
| X-n284-k15 | cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.388092 | 23623.8 | 0.388092 | 23151 | 1635 |
| X-n284-k15 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.380707 | 24088.2 | 0.380707 | 23151 | 1635 |
| X-n284-k15 | grocery | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 0.39106 | 23575.3 | 0.39106 | 23151 | 1635 |

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
| X-n129-k18 | atm | ortools:quantile_p75_scaled_or_tools | 0.416094 | 0.416016 | 0.000187793 | 31756.3 | 31753.8 | 7.94798e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:quantile_p90_scaled_or_tools | 0.405938 | 0.408984 | 0.00744986 | 33262.5 | 33260.1 | 7.21386e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.406562 | 0.408125 | 0.00382848 | 31871.2 | 31868.8 | 7.50673e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:quantile_p75_scaled_or_tools | 0.416328 | 0.414062 | 0.0054717 | 31648.5 | 31647.1 | 4.37567e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n134-k13 | atm | ortools:quantile_p75_scaled_or_tools | 0.460451 | 0.457368 | 0.0067401 | 18505.7 | 18469.6 | 0.0019553 | yes | yes | yes | safe |
| X-n134-k13 | cargo | ortools:quantile_p75_scaled_or_tools | 0.448496 | 0.445338 | 0.007091 | 17495.4 | 17466.8 | 0.00163906 | yes | yes | yes | safe |
| X-n134-k13 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.454361 | 0.452707 | 0.00365388 | 19605.1 | 19570.5 | 0.00176944 | yes | yes | yes | safe |
| X-n134-k13 | grocery | ortools:nominal_or_tools | 0.458346 | 0.456541 | 0.00395257 | 15713.7 | 15693.7 | 0.00127406 | yes | yes | yes | safe |
| X-n139-k10 | atm | ortools:nominal_or_tools | 0.418913 | 0.415725 | 0.00766951 | 15254.7 | 15251.9 | 0.000187403 | yes | yes | yes | safe |
| X-n139-k10 | cargo | ortools:nominal_or_tools | 0.421232 | 0.416522 | 0.0113083 | 15148.8 | 15145.9 | 0.000194443 | yes | yes | yes | safe |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | 0.413116 | 0.412899 | 0.000526501 | 15424.6 | 15421.8 | 0.000181071 | yes | yes | yes | safe |
| X-n139-k10 | grocery | ortools:nominal_or_tools | 0.418478 | 0.41558 | 0.00697472 | 15103.5 | 15101.4 | 0.000139072 | yes | yes | yes | safe |
| X-n143-k7 | atm | ortools:proxy_mean_or_tools | 0.309296 | 0.309366 | 0.000227635 | 21625.5 | 21602.1 | 0.00108536 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | cargo | ortools:quantile_p90_scaled_or_tools | 0.308099 | 0.306972 | 0.00367057 | 20394.5 | 20365.4 | 0.0014289 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | cold_chain | ortools:proxy_mean_or_tools | 0.300634 | 0.298521 | 0.00707714 | 23535.5 | 23511.3 | 0.00103113 | yes | no | no | final_full_required: domain ranking flip |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | 0.306549 | 0.309225 | 0.00865407 | 20962.3 | 20946.9 | 0.000736558 | yes | no | no | final_full_required: domain ranking flip |
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
| X-n190-k8 | atm | ortools:quantile_p90_scaled_or_tools | 0.420529 | 0.417566 | 0.00709579 | 18797.9 | 18794.5 | 0.000180964 | yes | yes | yes | safe |
| X-n190-k8 | cargo | ortools:quantile_p75_scaled_or_tools | 0.414921 | 0.411852 | 0.00745118 | 18665.2 | 18662.6 | 0.000138382 | yes | yes | yes | safe |
| X-n190-k8 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.408836 | 0.404709 | 0.0101974 | 18972.8 | 18969.8 | 0.000157206 | yes | yes | yes | safe |
| X-n190-k8 | grocery | ortools:quantile_p75_scaled_or_tools | 0.418624 | 0.413915 | 0.0113767 | 18611.3 | 18609.5 | 9.91307e-05 | yes | yes | yes | safe |
| X-n204-k19 | atm | ortools:nominal_or_tools | 0.420197 | 0.419803 | 0.000938747 | 27832.7 | 27795.1 | 0.00135523 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_or_tools | 0.419606 | 0.416798 | 0.00673679 | 26242.8 | 26212.3 | 0.00116339 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | 0.415665 | 0.414778 | 0.00213777 | 30349.8 | 30319.1 | 0.00101086 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | 0.419655 | 0.42 | 0.000821018 | 25480.2 | 25455.3 | 0.000977882 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | 0.414856 | 0.411731 | 0.00758991 | 33554.5 | 33549.3 | 0.000154625 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | 0.413029 | 0.409231 | 0.00928102 | 33399 | 33393.9 | 0.000151614 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.410096 | 0.406346 | 0.00922858 | 33819.8 | 33815.4 | 0.000128447 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | 0.412596 | 0.409904 | 0.00656814 | 33333.3 | 33330.5 | 8.2835e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | atm | ortools:nominal_or_tools | 0.478075 | 0.474695 | 0.00712096 | 18201.2 | 18168 | 0.00182475 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | cargo | ortools:nominal_or_tools | 0.473521 | 0.470047 | 0.00739113 | 16893.2 | 16868.8 | 0.00144799 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | cold_chain | ortools:nominal_or_tools | 0.468685 | 0.463286 | 0.0116538 | 19654.6 | 19625.3 | 0.00149428 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | grocery | ortools:nominal_or_tools | 0.473521 | 0.470376 | 0.00668729 | 16170.2 | 16150.8 | 0.00120175 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | atm | ortools:nominal_or_tools | 0.47656 | 0.474908 | 0.00347725 | 118514 | 118514 | 4.51946e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | 0.473853 | 0.473394 | 0.000968992 | 118489 | 118488 | 3.93247e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | 0.473624 | 0.47344 | 0.000387559 | 118541 | 118540 | 5.18687e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | 0.475872 | 0.474312 | 0.0032882 | 118474 | 118474 | 3.02031e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | atm | ortools:quantile_p75_scaled_or_tools | 0.454144 | 0.451306 | 0.00628805 | 46797.4 | 46793.4 | 8.7049e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.439955 | 0.44027 | 0.000716186 | 48086.2 | 48083.9 | 4.78393e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | 0.44509 | 0.442252 | 0.00641679 | 48425 | 48422.4 | 5.37159e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | grocery | ortools:quantile_p75_scaled_or_tools | 0.451937 | 0.451396 | 0.00119749 | 46571.3 | 46569 | 4.96824e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n228-k23 | atm | ortools:nominal_or_tools | 0.464361 | 0.457885 | 0.0141428 | 32281.5 | 32270.9 | 0.000327558 | yes | yes | yes | safe |
| X-n228-k23 | cargo | ortools:nominal_or_tools | 0.452203 | 0.446432 | 0.0129268 | 31801.5 | 31791.1 | 0.000328467 | yes | yes | yes | safe |
| X-n228-k23 | cold_chain | ortools:nominal_or_tools | 0.453172 | 0.448943 | 0.00942008 | 32740.6 | 32729.8 | 0.000330877 | yes | yes | yes | safe |
| X-n228-k23 | grocery | ortools:nominal_or_tools | 0.457357 | 0.454317 | 0.00669058 | 31558.5 | 31552.7 | 0.000182576 | yes | yes | yes | safe |
| X-n233-k16 | atm | ortools:proxy_mean_scaled_or_tools | 0.454483 | 0.45181 | 0.0059149 | 28089.5 | 28069.3 | 0.000719935 | yes | yes | yes | safe |
| X-n233-k16 | cargo | ortools:proxy_mean_scaled_or_tools | 0.459655 | 0.453233 | 0.0141702 | 26886.9 | 26871.3 | 0.00057803 | yes | yes | yes | safe |
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
| X-n261-k13 | atm | ortools:proxy_mean_scaled_or_tools | 0.430885 | 0.428231 | 0.00619723 | 37840.9 | 37764.4 | 0.00202485 | yes | yes | yes | safe |
| X-n261-k13 | cargo | ortools:quantile_p75_scaled_or_tools | 0.426077 | 0.421115 | 0.0117819 | 36129.1 | 36075.1 | 0.00149691 | yes | yes | yes | safe |
| X-n261-k13 | cold_chain | ortools:quantile_p75_scaled_or_tools | 0.421923 | 0.418423 | 0.00836474 | 40067.2 | 40001.1 | 0.00165242 | yes | yes | yes | safe |
| X-n261-k13 | grocery | ortools:proxy_mean_scaled_or_tools | 0.428269 | 0.426192 | 0.00487321 | 35515.1 | 35473 | 0.00118869 | yes | yes | yes | safe |
| X-n275-k28 | atm | ortools:nominal_or_tools | 0.417664 | 0.417956 | 0.000698568 | 22580.6 | 22579.9 | 3.11968e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cargo | ortools:nominal_or_tools | 0.419781 | 0.418285 | 0.00357735 | 22554.8 | 22554.2 | 2.53688e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | 0.416934 | 0.415985 | 0.0022811 | 22624.4 | 22623.7 | 3.27768e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | grocery | ortools:nominal_or_tools | 0.416642 | 0.417007 | 0.000875197 | 22542.5 | 22542.1 | 1.98041e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | atm | ortools:nominal_or_tools | 0.452832 | 0.458172 | 0.0116561 | 40027.9 | 40017.4 | 0.000263029 | yes | yes | yes | safe |
| X-n280-k17 | cargo | ortools:nominal_or_tools | 0.438387 | 0.441792 | 0.00770729 | 39580.1 | 39572.4 | 0.000194203 | yes | yes | yes | safe |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | 0.441577 | 0.445018 | 0.00773196 | 40419.2 | 40410.3 | 0.000221028 | yes | yes | yes | safe |
| X-n280-k17 | grocery | ortools:nominal_or_tools | 0.450215 | 0.454194 | 0.00875947 | 39344.3 | 39336.9 | 0.000187554 | yes | yes | yes | safe |
| X-n284-k15 | atm | ortools:robust_mean_1std_scaled_or_tools | 0.392721 | 0.388693 | 0.0103636 | 23784.2 | 23778.4 | 0.000242916 | yes | yes | yes | safe |
| X-n284-k15 | cargo | ortools:robust_mean_1std_scaled_or_tools | 0.388092 | 0.38311 | 0.013005 | 23623.8 | 23619.5 | 0.000180718 | yes | yes | yes | safe |
| X-n284-k15 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | 0.380707 | 0.379541 | 0.00307234 | 24088.2 | 24082.5 | 0.000235147 | yes | yes | yes | safe |
| X-n284-k15 | grocery | ortools:robust_mean_1std_scaled_or_tools | 0.39106 | 0.386678 | 0.0113314 | 23575.3 | 23571.5 | 0.000159654 | yes | yes | yes | safe |

## Domain Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | cold_chain > grocery > cargo > atm | cargo > cold_chain > grocery > atm | yes | 0.4 |  |
| X-n110-k13 | 4 | cargo > atm > cold_chain > grocery | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n115-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n120-k6 | 4 | cold_chain > grocery > cargo > atm | grocery > cold_chain > cargo > atm | yes | 0.8 |  |
| X-n129-k18 | 4 | grocery > atm > cold_chain > cargo | atm > grocery > cargo > cold_chain | yes | 0.6 |  |
| X-n134-k13 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n139-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n143-k7 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n157-k13 | 4 | cargo > atm > grocery > cold_chain | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n162-k11 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n167-k10 | 4 | grocery > atm > cold_chain > cargo | grocery > atm > cold_chain > cargo | no | 1 |  |
| X-n181-k23 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n186-k15 | 4 | grocery > atm > cargo > cold_chain | grocery > atm > cargo > cold_chain | no | 1 |  |
| X-n190-k8 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n204-k19 | 4 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | yes | 0.8 |  |
| X-n209-k16 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n214-k11 | 4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.8 |  |
| X-n219-k73 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n223-k34 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n228-k23 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n233-k16 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n237-k14 | 4 | atm > cargo > cold_chain > grocery | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n242-k48 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n251-k28 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n261-k13 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n275-k28 | 4 | cargo > atm > cold_chain > grocery | cargo > atm > grocery > cold_chain | yes | 0.8 |  |
| X-n280-k17 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
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
| X-n134-k13 | ortools:robust_mean_1std_scaled_or_tools | yes | 13 | 13469 | 0.995 |  |
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
| X-n143-k7 | ortools:proxy_mean_or_tools | yes | 7 | 19114 | 0.9959 |  |
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
| X-n190-k8 | ortools:nominal_or_tools | yes | 8 | 17905 | 0.944746 |  |
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
| X-n214-k11 | ortools:robust_mean_1std_scaled_or_tools | yes | 11 | 13721 | 0.995 |  |
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
