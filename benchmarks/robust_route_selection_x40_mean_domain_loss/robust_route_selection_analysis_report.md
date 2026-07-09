# Robust Route Selection Analysis

## Scope

- Source directory: `benchmarks\robust_route_selection_x40_mean_domain_loss`
- This report summarizes route-candidate winners after the common stochastic decision layer.
- `Strict Stability Safe` means full-scenario confirmation is feasible, metric drift is within thresholds, and no domain stockout ranking flip was observed.

## Aggregate Summary

| Metric | Value |
| --- | --- |
| instances | 40 |
| domains | 4 |
| candidate_rows | 1760 |
| candidate_feasible_rows | 456 |
| winner_rows | 112 |
| winner_domains | 4 |
| unique_winning_candidates | 7 |
| unique_winning_route_plans | 7 |
| unique_winning_providers | 1 |
| confirmed_winner_rows | 112 |
| confirm_feasible_rate | 1 |
| metric_stability_safe_rate | 1 |
| strict_stability_safe_rate | 0.5 |
| final_full_required_rows | 56 |
| max_stockout_relative_drift | 0.039708 |
| max_mean_total_cost_relative_drift | 0.00256399 |
| ranking_rows | 28 |
| ranking_flip_rate | 0.5 |
| mean_stockout_spearman | 0.885714 |

## Domain-Specific Winner Diversity

| Domain | Winner Rows | Instances | Unique Winning Candidates | Unique Winning Route Plans | Unique Winning Providers | Winner Candidate Entropy | Winner Route Plan Entropy | Normalized Winner Candidate Entropy | Top Candidate | Top Candidate Count | Top Candidate Share | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Confirmed Rows | Strict Stability Safe Rate | Metric Stability Safe Rate | Final Full Required Rows | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 28 | 28 | 6 | 6 | 1 | 2.06048 | 2.06048 | 0.797101 | ortools:nominal_or_tools | 14 | 0.5 | nominal_or_tools | 14 | 0.5 | 28 | 0.5 | 1 | 14 | 0.0280775 | 0.00217061 |
| cargo | 28 | 28 | 6 | 6 | 1 | 2.10851 | 2.10851 | 0.815683 | ortools:nominal_or_tools | 14 | 0.5 | nominal_or_tools | 14 | 0.5 | 28 | 0.5 | 1 | 14 | 0.039708 | 0.00256399 |
| cold_chain | 28 | 28 | 7 | 7 | 1 | 1.99468 | 1.99468 | 0.710519 | ortools:nominal_or_tools | 16 | 0.571429 | nominal_or_tools | 16 | 0.571429 | 28 | 0.5 | 1 | 14 | 0.027053 | 0.00236985 |
| grocery | 28 | 28 | 5 | 5 | 1 | 1.80735 | 1.80735 | 0.778385 | ortools:nominal_or_tools | 16 | 0.571429 | nominal_or_tools | 16 | 0.571429 | 28 | 0.5 | 1 | 14 | 0.0292669 | 0.00160499 |

## Top Candidate Frequencies

| Domain | Candidate | Routing Provider | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- | --- |
| atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 14 | 28 | 0.5 |
| atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| atm | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 14 | 28 | 0.5 |
| cargo | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 4 | 28 | 0.142857 |
| cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 3 | 28 | 0.107143 |

## Instance-Level Route Plan Diversity

| Instance | Customers | Domains | Winner Rows | Unique Winning Candidates Across Domains | Unique Winning Route Plans Across Domains | Route Plan Entropy Across Domains | Normalized Route Plan Entropy Across Domains | Candidate Entropy Across Domains | All Domains Same Candidate | All Domains Same Route Plan | Confirmed Winner Rows | Strict Stability Safe Rows | Final Full Required Rows | Ranking Flip | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 105 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0105116 | 0.000984556 |
| X-n110-k13 | 109 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0180577 | 9.94206e-05 |
| X-n115-k10 | 114 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00817138 | 0.000520465 |
| X-n120-k6 | 119 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00234375 | 2.98908e-05 |
| X-n129-k18 | 128 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00759734 | 4.90639e-05 |
| X-n134-k13 | 133 | 4 | 4 | 2 | 2 | 1 | 1 | 1 | no | no | 4 | 4 | 0 | no | 0.007091 | 0.0019553 |
| X-n139-k10 | 138 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0113083 | 0.000194443 |
| X-n143-k7 | 142 | 4 | 4 | 4 | 4 | 2 | 1 | 2 | no | no | 4 | 4 | 0 | no | 0.0065448 | 0.00118114 |
| X-n157-k13 | 156 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00741035 | 2.8277e-05 |
| X-n162-k11 | 161 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00524206 | 0.00256399 |
| X-n167-k10 | 166 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00418531 | 0.000197099 |
| X-n181-k23 | 180 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00629577 | 2.77378e-05 |
| X-n186-k15 | 185 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00435299 | 0.00082061 |
| X-n190-k8 | 189 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 4 | 0 | no | 0.0123124 | 0.000160685 |
| X-n204-k19 | 203 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00673679 | 0.00135523 |
| X-n209-k16 | 208 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00928102 | 0.000154625 |
| X-n214-k11 | 213 | 4 | 4 | 3 | 3 | 1.5 | 0.946395 | 1.5 | no | no | 4 | 4 | 0 | no | 0.00747235 | 0.00175848 |
| X-n219-k73 | 218 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00347725 | 5.18687e-06 |
| X-n223-k34 | 222 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0101111 | 6.3538e-05 |
| X-n228-k23 | 227 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.039708 | 0.000389827 |
| X-n233-k16 | 232 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 4 | 0 | no | 0.00619015 | 0.000719935 |
| X-n237-k14 | 236 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00252003 | 2.89791e-05 |
| X-n242-k48 | 241 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0113536 | 3.76682e-05 |
| X-n251-k28 | 250 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00385498 | 9.50027e-05 |
| X-n261-k13 | 260 | 4 | 4 | 3 | 3 | 1.5 | 0.946395 | 1.5 | no | no | 4 | 0 | 4 | yes | 0.0121469 | 0.00195226 |
| X-n275-k28 | 274 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00357735 | 3.27768e-05 |
| X-n280-k17 | 279 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 0 | 4 | yes | 0.00773196 | 0.000221028 |
| X-n284-k15 | 283 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0159163 | 0.000242306 |

## Certified Winner Rate

| Scope | Winner Rows | Confirmed Rows | Confirm Feasible Rows | Metric Stability Safe Rows | Strict Stability Safe Rows | Strict Stability Safe Rate | Final Full Required Rows | Ranking Flip Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 112 | 112 | 112 | 112 | 56 | 0.5 | 56 | 14 |
| domain:atm | 28 | 28 | 28 | 28 | 14 | 0.5 | 14 | 14 |
| domain:cargo | 28 | 28 | 28 | 28 | 14 | 0.5 | 14 | 14 |
| domain:cold_chain | 28 | 28 | 28 | 28 | 14 | 0.5 | 14 | 14 |
| domain:grocery | 28 | 28 | 28 | 28 | 14 | 0.5 | 14 | 14 |

## Final Full Required Rows

| Instance | Domain | Candidate | Route Plan | Routing Provider | Confirm Feasible | Stockout Relative Drift | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Flip | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00447691 | 0.000984556 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0105116 | 0.000804798 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000705384 | 0.000786546 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00047081 | 0.00053046 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00904878 | 5.32606e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0180577 | 3.89006e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0140406 | 9.94206e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00486941 | 3.2661e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000978474 | 2.30193e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00234375 | 2.46323e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00155854 | 2.98908e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000194553 | 1.35661e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | atm | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00670891 | 4.86233e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00753041 | 4.90639e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00759734 | 4.85825e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.000558347 | 2.13329e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000131961 | 2.7977e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00741035 | 2.37057e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00385024 | 2.8277e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00251789 | 1.82655e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000938747 | 0.00135523 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00673679 | 0.00116339 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00213777 | 0.00101086 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000821018 | 0.000977882 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00758991 | 0.000154625 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00928102 | 0.000151614 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00922858 | 0.000128447 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00656814 | 8.2835e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00347725 | 4.51946e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000968992 | 3.93247e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000387559 | 5.18687e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0032882 | 3.02031e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0280775 | 0.000389827 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.039708 | 0.000376284 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.027053 | 0.000376257 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0292669 | 0.000217854 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00251256 | 2.89791e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00143756 | 2.27604e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000270563 | 2.52982e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00252003 | 1.69503e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00385498 | 9.50027e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00259235 | 9.33851e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00305301 | 8.38037e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00275128 | 4.91559e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00968871 | 0.00195226 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00842747 | 0.00145695 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0121469 | 0.00166421 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00639582 | 0.00119254 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000698568 | 3.11968e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00357735 | 2.53688e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0022811 | 3.27768e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000875197 | 1.98041e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n280-k17 | atm | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00452595 | 0.000206542 | yes | yes | no | final_full_required: domain ranking flip |
| X-n280-k17 | cargo | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0054883 | 0.000147771 | yes | yes | no | final_full_required: domain ranking flip |
| X-n280-k17 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00773196 | 0.000221028 | yes | yes | no | final_full_required: domain ranking flip |
| X-n280-k17 | grocery | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00181003 | 0.000117481 | yes | yes | no | final_full_required: domain ranking flip |

## Ranking Stability

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

## Suggested Interpretation

- Winner diversity is the main signal for whether sector objectives change route choice.
- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.
- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.
- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.
