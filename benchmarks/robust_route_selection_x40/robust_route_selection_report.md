# Robust Route Selection Report

## Scope

This diagnostic evaluates multiple routing candidates with the same stochastic decision layer, then selects a domain-level winner by the configured score metric.

- Data dir: `benchmarks/proxy_cvrplib_x_v4`
- Routing providers: `ortools`
- LP backend: `pulp_cbc`
- LP planning scenario limit: `60`
- Score metric: `mean_total_cost`
- Full-scenario winner confirmation: `True`

Fast mode is intended for route-candidate screening. Final decision-driving claims should be rerun with full planning history by passing `--lp-planning-scenario-limit 0`.

## Candidate Coverage

| Domain | Candidate_Rows | Feasible_Rows | Instances | Candidates | Median_Total_Runtime_Sec | Top_Winning_Candidate | Top_Winning_Provider | Top_Winning_Route_Plan | Top_Winner_Count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 440 | 114 | 40 | 11 | 4.99843 | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 |
| cargo | 440 | 114 | 40 | 11 | 4.99843 | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 |
| cold_chain | 440 | 114 | 40 | 11 | 4.99843 | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 |
| grocery | 440 | 114 | 40 | 11 | 4.99843 | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 |

## Winners

| Instance | Domain | Candidate | Routing Provider | Route Plan | Score Value | mean_total_cost | stockout_rate | Route Cost | Optimized Load Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 30121.6 | 30121.6 | 0.402381 | 27182 | 8400 |
| X-n106-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 29399.2 | 29399.2 | 0.403429 | 27182 | 8400 |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 31507.2 | 31507.2 | 0.404762 | 27182 | 8255.29 |
| X-n106-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 29145.2 | 29145.2 | 0.404762 | 27182 | 8282.21 |
| X-n110-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 15771 | 15771 | 0.433119 | 15387 | 858 |
| X-n110-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 15675.7 | 15675.7 | 0.43945 | 15387 | 858 |
| X-n110-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 15893.2 | 15893.2 | 0.432844 | 15387 | 851.148 |
| X-n110-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 15632 | 15632 | 0.433028 | 15387 | 852.04 |
| X-n115-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 13888 | 13888 | 0.390789 | 13099 | 1690 |
| X-n115-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 13691.2 | 13691.2 | 0.400439 | 13099 | 1690 |
| X-n115-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 14177.4 | 14177.4 | 0.383158 | 13099 | 1684.38 |
| X-n115-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 13626.7 | 13626.7 | 0.385877 | 13099 | 1690 |
| X-n120-k6 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 14084.4 | 14084.4 | 0.428992 | 14034 | 126 |
| X-n120-k6 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 14072.6 | 14072.6 | 0.429244 | 14034 | 126 |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 14103 | 14103 | 0.432017 | 14034 | 123.979 |
| X-n120-k6 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 14066.6 | 14066.6 | 0.432017 | 14034 | 124.387 |
| X-n129-k18 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 31021.9 | 31021.9 | 0.471172 | 30677 | 679.052 |
| X-n129-k18 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 30936.3 | 30936.3 | 0.469687 | 30677 | 684.614 |
| X-n129-k18 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 31106.3 | 31106.3 | 0.462578 | 30677 | 674.271 |
| X-n129-k18 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 30890 | 30890 | 0.469922 | 30677 | 674.728 |
| X-n134-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 17142 | 17142 | 0.46188 | 13345 | 8359 |
| X-n134-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 16133.9 | 16133.9 | 0.455263 | 13345 | 8359 |
| X-n134-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 18203.3 | 18203.3 | 0.457068 | 13345 | 8359 |
| X-n134-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 15713.7 | 15713.7 | 0.458346 | 13345 | 8359 |
| X-n139-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 15254.7 | 15254.7 | 0.418913 | 14826 | 1060 |
| X-n139-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 15148.8 | 15148.8 | 0.421232 | 14826 | 1060 |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 15424.6 | 15424.6 | 0.413116 | 14826 | 1060 |
| X-n139-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 15103.5 | 15103.5 | 0.418478 | 14826 | 1060 |
| X-n143-k7 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 19948.3 | 19948.3 | 0.413803 | 16647 | 7970.16 |
| X-n143-k7 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 19135.1 | 19135.1 | 0.42162 | 16647 | 8036.47 |
| X-n143-k7 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 21304.6 | 21304.6 | 0.407394 | 16647 | 7770.39 |
| X-n143-k7 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 18806.7 | 18806.7 | 0.413521 | 16647 | 7801.35 |
| X-n157-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 17479.3 | 17479.3 | 0.485833 | 17404 | 156 |
| X-n157-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 17461.2 | 17461.2 | 0.488013 | 17404 | 156 |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 17497.7 | 17497.7 | 0.484679 | 17404 | 156 |
| X-n157-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 17450.1 | 17450.1 | 0.484936 | 17404 | 156 |
| X-n162-k11 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 19460.5 | 19460.5 | 0.396025 | 14676 | 12914 |
| X-n162-k11 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 18315.1 | 18315.1 | 0.404969 | 14676 | 12914 |
| X-n162-k11 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 21763 | 21763 | 0.387702 | 14676 | 12914 |
| X-n162-k11 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 17869.4 | 17869.4 | 0.394348 | 14676 | 12914 |
| X-n167-k10 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 23163.2 | 23163.2 | 0.417952 | 22643 | 1330 |
| X-n167-k10 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 23039 | 23039 | 0.415663 | 22643 | 1330 |
| X-n167-k10 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 23377.4 | 23377.4 | 0.417892 | 22643 | 1297.47 |
| X-n167-k10 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 22984 | 22984 | 0.421627 | 22643 | 1302.61 |
| X-n181-k23 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 26308.7 | 26308.7 | 0.438 | 26232 | 184 |
| X-n181-k23 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 26290.2 | 26290.2 | 0.439333 | 26232 | 184 |
| X-n181-k23 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 26335.6 | 26335.6 | 0.435111 | 26232 | 184 |
| X-n181-k23 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 26281 | 26281 | 0.435778 | 26232 | 184 |
| X-n186-k15 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 32112.8 | 32112.8 | 0.412432 | 25982 | 14343.8 |
| X-n186-k15 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 30634.3 | 30634.3 | 0.412054 | 25982 | 14389.4 |
| X-n186-k15 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 34349.4 | 34349.4 | 0.411568 | 25982 | 14223.4 |
| X-n186-k15 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 29945.5 | 29945.5 | 0.412865 | 25982 | 14245.5 |
| X-n190-k8 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 18646.9 | 18646.9 | 0.437354 | 18122 | 1104 |
| X-n190-k8 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 18522 | 18522 | 0.437302 | 18122 | 1104 |
| X-n190-k8 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 18821.1 | 18821.1 | 0.428677 | 18122 | 1104 |
| X-n190-k8 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 18459.5 | 18459.5 | 0.433228 | 18122 | 1104 |
| X-n204-k19 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 27832.7 | 27832.7 | 0.420197 | 21213 | 15884 |
| X-n204-k19 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 26242.8 | 26242.8 | 0.419606 | 21213 | 15884 |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 30349.8 | 30349.8 | 0.415665 | 21213 | 15884 |
| X-n204-k19 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 25480.2 | 25480.2 | 0.419655 | 21213 | 15884 |
| X-n209-k16 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 33125.1 | 33125.1 | 0.418125 | 32468 | 1616 |
| X-n209-k16 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 32967.9 | 32967.9 | 0.417115 | 32468 | 1616 |
| X-n209-k16 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 33383.7 | 33383.7 | 0.411923 | 32468 | 1616 |
| X-n209-k16 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 32895.3 | 32895.3 | 0.415769 | 32468 | 1616 |
| X-n214-k11 | atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 17836.3 | 17836.3 | 0.482629 | 12479 | 10384 |
| X-n214-k11 | cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 16504 | 16504 | 0.482723 | 12479 | 10384 |
| X-n214-k11 | cold_chain | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 19206.7 | 19206.7 | 0.477606 | 12479 | 10384 |
| X-n214-k11 | grocery | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 15804 | 15804 | 0.479437 | 12479 | 10384 |
| X-n219-k73 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 118514 | 118514 | 0.47656 | 118409 | 219 |
| X-n219-k73 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 118489 | 118489 | 0.473853 | 118409 | 219 |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 118541 | 118541 | 0.473624 | 118409 | 218.954 |
| X-n219-k73 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 118474 | 118474 | 0.475872 | 118409 | 219 |
| X-n223-k34 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 44732.1 | 44732.1 | 0.461486 | 44118 | 1258 |
| X-n223-k34 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 44579.9 | 44579.9 | 0.451937 | 44118 | 1258 |
| X-n223-k34 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 44908.6 | 44908.6 | 0.454324 | 44118 | 1258 |
| X-n223-k34 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 44503.7 | 44503.7 | 0.458243 | 44118 | 1258 |
| X-n228-k23 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 32281.5 | 32281.5 | 0.464361 | 30349 | 3542 |
| X-n228-k23 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 31801.5 | 31801.5 | 0.452203 | 30349 | 3542 |
| X-n228-k23 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 32740.6 | 32740.6 | 0.453172 | 30349 | 3542 |
| X-n228-k23 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 31558.5 | 31558.5 | 0.457357 | 30349 | 3542 |
| X-n233-k16 | atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 28089.5 | 28089.5 | 0.454483 | 23289 | 10096 |
| X-n233-k16 | cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 26886.9 | 26886.9 | 0.459655 | 23289 | 10096 |
| X-n233-k16 | cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 29382.3 | 29382.3 | 0.448405 | 23289 | 10096 |
| X-n233-k16 | grocery | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 26318.4 | 26318.4 | 0.451293 | 23289 | 10096 |
| X-n237-k14 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 29115.9 | 29115.9 | 0.471017 | 29009 | 237.722 |
| X-n237-k14 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 29090.2 | 29090.2 | 0.470932 | 29009 | 237.932 |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 29146.6 | 29146.6 | 0.469958 | 29009 | 236.906 |
| X-n237-k14 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 29075.4 | 29075.4 | 0.469619 | 29009 | 236.856 |
| X-n242-k48 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 87275 | 87275 | 0.48029 | 86573 | 1344 |
| X-n242-k48 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 87102.7 | 87102.7 | 0.476598 | 86573 | 1344 |
| X-n242-k48 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 87444 | 87444 | 0.476556 | 86573 | 1338.02 |
| X-n242-k48 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 87007 | 87007 | 0.478008 | 86573 | 1338.85 |
| X-n251-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 41303.7 | 41303.7 | 0.43748 | 40465 | 1932 |
| X-n251-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 41099.8 | 41099.8 | 0.43316 | 40465 | 1932 |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 41585.1 | 41585.1 | 0.43368 | 40465 | 1923.68 |
| X-n251-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 40999.7 | 40999.7 | 0.43736 | 40465 | 1926.09 |
| X-n261-k13 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 36539.4 | 36539.4 | 0.471692 | 29400 | 14002.2 |
| X-n261-k13 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 34795.1 | 34795.1 | 0.471962 | 29400 | 14044.5 |
| X-n261-k13 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 38482.4 | 38482.4 | 0.461692 | 29400 | 13719.1 |
| X-n261-k13 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 33860.1 | 33860.1 | 0.469 | 29400 | 13743.4 |
| X-n275-k28 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 22580.6 | 22580.6 | 0.417664 | 22472 | 280 |
| X-n275-k28 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 22554.8 | 22554.8 | 0.419781 | 22472 | 280 |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 22624.4 | 22624.4 | 0.416934 | 22472 | 279.708 |
| X-n275-k28 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 22542.5 | 22542.5 | 0.416642 | 22472 | 279.971 |
| X-n280-k17 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 40027.9 | 40027.9 | 0.452832 | 38220 | 3264 |
| X-n280-k17 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 39580.1 | 39580.1 | 0.438387 | 38220 | 3264 |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 40419.2 | 40419.2 | 0.441577 | 38220 | 3264 |
| X-n280-k17 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 39344.3 | 39344.3 | 0.450215 | 38220 | 3264 |
| X-n284-k15 | atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 23200.9 | 23200.9 | 0.414382 | 22522 | 1635 |
| X-n284-k15 | cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 23034.9 | 23034.9 | 0.413039 | 22522 | 1635 |
| X-n284-k15 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 23478.3 | 23478.3 | 0.406855 | 22522 | 1627.03 |
| X-n284-k15 | grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 22971.5 | 22971.5 | 0.41371 | 22522 | 1633.32 |

## Full-Scenario Winner Confirmation

| Instance | Domain | Candidate | Fast Stockout | Full Stockout | Stockout Relative Drift | Fast Mean Total Cost | Full Mean Total Cost | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Stable | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | 0.402381 | 0.40419 | 0.00447691 | 30121.6 | 30092 | 0.000984556 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | cargo | ortools:nominal_or_tools | 0.403429 | 0.407714 | 0.0105116 | 29399.2 | 29375.6 | 0.000804798 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | 0.404762 | 0.405048 | 0.000705384 | 31507.2 | 31482.5 | 0.000786546 | yes | no | no | final_full_required: domain ranking flip |
| X-n106-k14 | grocery | ortools:nominal_or_tools | 0.404762 | 0.404571 | 0.00047081 | 29145.2 | 29129.8 | 0.00053046 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | atm | ortools:nominal_or_tools | 0.433119 | 0.432294 | 0.00191002 | 15771 | 15769.9 | 6.87416e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:nominal_or_tools | 0.43945 | 0.438073 | 0.00314136 | 15675.7 | 15675.4 | 1.58408e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:nominal_or_tools | 0.432844 | 0.432752 | 0.000211999 | 15893.2 | 15891.9 | 8.44157e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:nominal_or_tools | 0.433028 | 0.432844 | 0.000423908 | 15632 | 15631.5 | 3.03947e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n115-k10 | atm | ortools:nominal_or_tools | 0.390789 | 0.39307 | 0.00580228 | 13888 | 13880.8 | 0.000520465 | yes | yes | yes | safe |
| X-n115-k10 | cargo | ortools:nominal_or_tools | 0.400439 | 0.397193 | 0.00817138 | 13691.2 | 13685.7 | 0.000407089 | yes | yes | yes | safe |
| X-n115-k10 | cold_chain | ortools:nominal_or_tools | 0.383158 | 0.381579 | 0.00413793 | 14177.4 | 14171.3 | 0.000424269 | yes | yes | yes | safe |
| X-n115-k10 | grocery | ortools:nominal_or_tools | 0.385877 | 0.387368 | 0.00384964 | 13626.7 | 13622.2 | 0.000325952 | yes | yes | yes | safe |
| X-n120-k6 | atm | ortools:nominal_or_tools | 0.428992 | 0.429412 | 0.000978474 | 14084.4 | 14084.1 | 2.30193e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_or_tools | 0.429244 | 0.430252 | 0.00234375 | 14072.6 | 14072.3 | 2.46323e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | 0.432017 | 0.431345 | 0.00155854 | 14103 | 14102.6 | 2.98908e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_or_tools | 0.432017 | 0.431933 | 0.000194553 | 14066.6 | 14066.4 | 1.35661e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n129-k18 | atm | ortools:nominal_or_tools | 0.471172 | 0.476016 | 0.0101756 | 31021.9 | 31019.8 | 6.53865e-05 | yes | yes | yes | safe |
| X-n129-k18 | cargo | ortools:nominal_or_tools | 0.469687 | 0.471875 | 0.00463576 | 30936.3 | 30933.9 | 7.78408e-05 | yes | yes | yes | safe |
| X-n129-k18 | cold_chain | ortools:nominal_or_tools | 0.462578 | 0.465 | 0.00520833 | 31106.3 | 31104.5 | 5.99801e-05 | yes | yes | yes | safe |
| X-n129-k18 | grocery | ortools:nominal_or_tools | 0.469922 | 0.473281 | 0.00709805 | 30890 | 30889 | 3.27687e-05 | yes | yes | yes | safe |
| X-n134-k13 | atm | ortools:nominal_or_tools | 0.46188 | 0.45797 | 0.00853719 | 17142 | 17112.3 | 0.00173909 | yes | yes | yes | safe |
| X-n134-k13 | cargo | ortools:nominal_or_tools | 0.455263 | 0.45203 | 0.00715236 | 16133.9 | 16113.7 | 0.00125414 | yes | yes | yes | safe |
| X-n134-k13 | cold_chain | ortools:nominal_or_tools | 0.457068 | 0.454737 | 0.00512566 | 18203.3 | 18176.2 | 0.00149295 | yes | yes | yes | safe |
| X-n134-k13 | grocery | ortools:nominal_or_tools | 0.458346 | 0.456541 | 0.00395257 | 15713.7 | 15693.7 | 0.00127406 | yes | yes | yes | safe |
| X-n139-k10 | atm | ortools:nominal_or_tools | 0.418913 | 0.415725 | 0.00766951 | 15254.7 | 15251.9 | 0.000187403 | yes | yes | yes | safe |
| X-n139-k10 | cargo | ortools:nominal_or_tools | 0.421232 | 0.416522 | 0.0113083 | 15148.8 | 15145.9 | 0.000194443 | yes | yes | yes | safe |
| X-n139-k10 | cold_chain | ortools:nominal_or_tools | 0.413116 | 0.412899 | 0.000526501 | 15424.6 | 15421.8 | 0.000181071 | yes | yes | yes | safe |
| X-n139-k10 | grocery | ortools:nominal_or_tools | 0.418478 | 0.41558 | 0.00697472 | 15103.5 | 15101.4 | 0.000139072 | yes | yes | yes | safe |
| X-n143-k7 | atm | ortools:nominal_or_tools | 0.413803 | 0.411972 | 0.00444444 | 19948.3 | 19934.8 | 0.000675467 | yes | yes | yes | safe |
| X-n143-k7 | cargo | ortools:nominal_or_tools | 0.42162 | 0.414296 | 0.0176781 | 19135.1 | 19111.3 | 0.00124597 | yes | yes | yes | safe |
| X-n143-k7 | cold_chain | ortools:nominal_or_tools | 0.407394 | 0.405775 | 0.00399167 | 21304.6 | 21280.1 | 0.00115256 | yes | yes | yes | safe |
| X-n143-k7 | grocery | ortools:nominal_or_tools | 0.413521 | 0.410915 | 0.00634105 | 18806.7 | 18792.8 | 0.000743348 | yes | yes | yes | safe |
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
| X-n190-k8 | atm | ortools:nominal_or_tools | 0.437354 | 0.430847 | 0.015105 | 18646.9 | 18426.3 | 0.011975 | yes | yes | yes | safe |
| X-n190-k8 | cargo | ortools:nominal_or_tools | 0.437302 | 0.428677 | 0.0201185 | 18522 | 18302.7 | 0.0119843 | yes | yes | yes | safe |
| X-n190-k8 | cold_chain | ortools:nominal_or_tools | 0.428677 | 0.423651 | 0.0118646 | 18821.1 | 18602 | 0.011775 | yes | yes | yes | safe |
| X-n190-k8 | grocery | ortools:nominal_or_tools | 0.433228 | 0.426667 | 0.015377 | 18459.5 | 18240.3 | 0.0120186 | yes | yes | yes | safe |
| X-n204-k19 | atm | ortools:nominal_or_tools | 0.420197 | 0.419803 | 0.000938747 | 27832.7 | 27795.1 | 0.00135523 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_or_tools | 0.419606 | 0.416798 | 0.00673679 | 26242.8 | 26212.3 | 0.00116339 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | 0.415665 | 0.414778 | 0.00213777 | 30349.8 | 30319.1 | 0.00101086 | yes | no | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | 0.419655 | 0.42 | 0.000821018 | 25480.2 | 25455.3 | 0.000977882 | yes | no | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:nominal_or_tools | 0.418125 | 0.413221 | 0.0118674 | 33125.1 | 33119.8 | 0.000160604 | yes | yes | yes | safe |
| X-n209-k16 | cargo | ortools:nominal_or_tools | 0.417115 | 0.41149 | 0.0136698 | 32967.9 | 32963.3 | 0.000139774 | yes | yes | yes | safe |
| X-n209-k16 | cold_chain | ortools:nominal_or_tools | 0.411923 | 0.410048 | 0.00457263 | 33383.7 | 33379 | 0.000140195 | yes | yes | yes | safe |
| X-n209-k16 | grocery | ortools:nominal_or_tools | 0.415769 | 0.411394 | 0.0106346 | 32895.3 | 32892.4 | 8.79758e-05 | yes | yes | yes | safe |
| X-n214-k11 | atm | ortools:quantile_p90_scaled_or_tools | 0.482629 | 0.480329 | 0.00478937 | 17836.3 | 17799.5 | 0.00206653 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | cargo | ortools:quantile_p90_scaled_or_tools | 0.482723 | 0.473052 | 0.0204446 | 16504 | 16470.7 | 0.00202049 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | cold_chain | ortools:quantile_p90_scaled_or_tools | 0.477606 | 0.470845 | 0.0143584 | 19206.7 | 19169.4 | 0.00194799 | yes | no | no | final_full_required: domain ranking flip |
| X-n214-k11 | grocery | ortools:quantile_p90_scaled_or_tools | 0.479437 | 0.475962 | 0.00729927 | 15804 | 15784.8 | 0.00122045 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | atm | ortools:nominal_or_tools | 0.47656 | 0.474908 | 0.00347725 | 118514 | 118514 | 4.51946e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | 0.473853 | 0.473394 | 0.000968992 | 118489 | 118488 | 3.93247e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | 0.473624 | 0.47344 | 0.000387559 | 118541 | 118540 | 5.18687e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | 0.475872 | 0.474312 | 0.0032882 | 118474 | 118474 | 3.02031e-06 | yes | no | no | final_full_required: domain ranking flip |
| X-n223-k34 | atm | ortools:nominal_or_tools | 0.461486 | 0.458468 | 0.00658283 | 44732.1 | 44728.8 | 7.43087e-05 | yes | yes | yes | safe |
| X-n223-k34 | cargo | ortools:nominal_or_tools | 0.451937 | 0.446982 | 0.0110854 | 44579.9 | 44577.3 | 5.69173e-05 | yes | yes | yes | safe |
| X-n223-k34 | cold_chain | ortools:nominal_or_tools | 0.454324 | 0.44991 | 0.00981177 | 44908.6 | 44905.6 | 6.72791e-05 | yes | yes | yes | safe |
| X-n223-k34 | grocery | ortools:nominal_or_tools | 0.458243 | 0.456982 | 0.00275998 | 44503.7 | 44501.8 | 4.1294e-05 | yes | yes | yes | safe |
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
| X-n242-k48 | atm | ortools:nominal_or_tools | 0.48029 | 0.47527 | 0.010564 | 87275 | 87271.6 | 3.97464e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n242-k48 | cargo | ortools:nominal_or_tools | 0.476598 | 0.467884 | 0.0186236 | 87102.7 | 87100 | 3.13938e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n242-k48 | cold_chain | ortools:nominal_or_tools | 0.476556 | 0.470207 | 0.0135016 | 87444 | 87440.1 | 4.55383e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n242-k48 | grocery | ortools:nominal_or_tools | 0.478008 | 0.4739 | 0.00866824 | 87007 | 87004.8 | 2.50252e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | atm | ortools:nominal_or_tools | 0.43748 | 0.4358 | 0.00385498 | 41303.7 | 41299.8 | 9.50027e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | cargo | ortools:nominal_or_tools | 0.43316 | 0.43204 | 0.00259235 | 41099.8 | 41095.9 | 9.33851e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | 0.43368 | 0.43236 | 0.00305301 | 41585.1 | 41581.6 | 8.38037e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n251-k28 | grocery | ortools:nominal_or_tools | 0.43736 | 0.43616 | 0.00275128 | 40999.7 | 40997.7 | 4.91559e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n261-k13 | atm | ortools:nominal_or_tools | 0.471692 | 0.468192 | 0.00747556 | 36539.4 | 36470.5 | 0.00188859 | yes | yes | yes | safe |
| X-n261-k13 | cargo | ortools:nominal_or_tools | 0.471962 | 0.468577 | 0.00722318 | 34795.1 | 34744.2 | 0.00146468 | yes | yes | yes | safe |
| X-n261-k13 | cold_chain | ortools:nominal_or_tools | 0.461692 | 0.458385 | 0.00721598 | 38482.4 | 38417.3 | 0.00169443 | yes | yes | yes | safe |
| X-n261-k13 | grocery | ortools:nominal_or_tools | 0.469 | 0.465962 | 0.00652084 | 33860.1 | 33819.4 | 0.00120343 | yes | yes | yes | safe |
| X-n275-k28 | atm | ortools:nominal_or_tools | 0.417664 | 0.417956 | 0.000698568 | 22580.6 | 22579.9 | 3.11968e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cargo | ortools:nominal_or_tools | 0.419781 | 0.418285 | 0.00357735 | 22554.8 | 22554.2 | 2.53688e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | 0.416934 | 0.415985 | 0.0022811 | 22624.4 | 22623.7 | 3.27768e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n275-k28 | grocery | ortools:nominal_or_tools | 0.416642 | 0.417007 | 0.000875197 | 22542.5 | 22542.1 | 1.98041e-05 | yes | no | no | final_full_required: domain ranking flip |
| X-n280-k17 | atm | ortools:nominal_or_tools | 0.452832 | 0.458172 | 0.0116561 | 40027.9 | 40017.4 | 0.000263029 | yes | yes | yes | safe |
| X-n280-k17 | cargo | ortools:nominal_or_tools | 0.438387 | 0.441792 | 0.00770729 | 39580.1 | 39572.4 | 0.000194203 | yes | yes | yes | safe |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | 0.441577 | 0.445018 | 0.00773196 | 40419.2 | 40410.3 | 0.000221028 | yes | yes | yes | safe |
| X-n280-k17 | grocery | ortools:nominal_or_tools | 0.450215 | 0.454194 | 0.00875947 | 39344.3 | 39336.9 | 0.000187554 | yes | yes | yes | safe |
| X-n284-k15 | atm | ortools:nominal_or_tools | 0.414382 | 0.409717 | 0.0113842 | 23200.9 | 23195.6 | 0.000229822 | yes | yes | yes | safe |
| X-n284-k15 | cargo | ortools:nominal_or_tools | 0.413039 | 0.408127 | 0.0120346 | 23034.9 | 23029.8 | 0.000219473 | yes | yes | yes | safe |
| X-n284-k15 | cold_chain | ortools:nominal_or_tools | 0.406855 | 0.402862 | 0.00991141 | 23478.3 | 23472.8 | 0.000234842 | yes | yes | yes | safe |
| X-n284-k15 | grocery | ortools:nominal_or_tools | 0.41371 | 0.408198 | 0.0135042 | 22971.5 | 22968 | 0.000151553 | yes | yes | yes | safe |

## Domain Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 4 | cold_chain > grocery > cargo > atm | cargo > cold_chain > grocery > atm | yes | 0.4 |  |
| X-n110-k13 | 4 | cargo > atm > grocery > cold_chain | cargo > grocery > cold_chain > atm | yes | 0.4 |  |
| X-n115-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n120-k6 | 4 | cold_chain > grocery > cargo > atm | grocery > cold_chain > cargo > atm | yes | 0.8 |  |
| X-n129-k18 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cargo > cold_chain | no | 1 |  |
| X-n134-k13 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n139-k10 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n143-k7 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n157-k13 | 4 | cargo > atm > grocery > cold_chain | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n162-k11 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n167-k10 | 4 | grocery > atm > cold_chain > cargo | grocery > atm > cold_chain > cargo | no | 1 |  |
| X-n181-k23 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n186-k15 | 4 | grocery > atm > cargo > cold_chain | grocery > atm > cargo > cold_chain | no | 1 |  |
| X-n190-k8 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n204-k19 | 4 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | yes | 0.8 |  |
| X-n209-k16 | 4 | atm > cargo > grocery > cold_chain | atm > cargo > grocery > cold_chain | no | 1 |  |
| X-n214-k11 | 4 | cargo > atm > grocery > cold_chain | atm > grocery > cargo > cold_chain | yes | 0.4 |  |
| X-n219-k73 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n223-k34 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n228-k23 | 4 | atm > grocery > cold_chain > cargo | atm > grocery > cold_chain > cargo | no | 1 |  |
| X-n233-k16 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
| X-n237-k14 | 4 | atm > cargo > cold_chain > grocery | atm > cargo > grocery > cold_chain | yes | 0.8 |  |
| X-n242-k48 | 4 | atm > grocery > cargo > cold_chain | atm > grocery > cold_chain > cargo | yes | 0.8 |  |
| X-n251-k28 | 4 | atm > grocery > cold_chain > cargo | grocery > atm > cold_chain > cargo | yes | 0.8 |  |
| X-n261-k13 | 4 | cargo > atm > grocery > cold_chain | cargo > atm > grocery > cold_chain | no | 1 |  |
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
