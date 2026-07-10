# Robust Route Selection Analysis

## Scope

- Source directory: `benchmarks\robust_route_selection_medium_risk_seeded_mean_domain_loss`
- This report summarizes route-candidate winners after the common stochastic decision layer.
- `Strict Stability Safe` means full-scenario confirmation is feasible, metric drift is within thresholds, and no domain stockout ranking flip was observed.

## Aggregate Summary

| Metric | Value |
| --- | --- |
| instances | 24 |
| domains | 4 |
| candidate_rows | 1536 |
| candidate_feasible_rows | 700 |
| winner_rows | 96 |
| winner_domains | 4 |
| unique_winning_candidates | 11 |
| unique_winning_route_plans | 11 |
| unique_winning_providers | 1 |
| confirmed_winner_rows | 96 |
| confirm_feasible_rate | 1 |
| metric_stability_safe_rate | 0.895833 |
| strict_stability_safe_rate | 0.46875 |
| final_full_required_rows | 51 |
| max_stockout_relative_drift | 0.0579452 |
| max_mean_total_cost_relative_drift | 0.0558232 |
| ranking_rows | 24 |
| ranking_flip_rate | 0.5 |
| mean_stockout_spearman | 0.883333 |

## Domain-Specific Winner Diversity

| Domain | Winner Rows | Instances | Unique Winning Candidates | Unique Winning Route Plans | Unique Winning Providers | Winner Candidate Entropy | Winner Route Plan Entropy | Normalized Winner Candidate Entropy | Top Candidate | Top Candidate Count | Top Candidate Share | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Confirmed Rows | Strict Stability Safe Rate | Metric Stability Safe Rate | Final Full Required Rows | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 24 | 24 | 10 | 10 | 1 | 3.17353 | 3.17353 | 0.955329 | ortools:nominal_seed101_or_tools | 5 | 0.208333 | nominal_seed101_or_tools | 5 | 0.208333 | 24 | 0.458333 | 0.916667 | 13 | 0.0545813 | 0.0499346 |
| cargo | 24 | 24 | 10 | 10 | 1 | 3.2406 | 3.2406 | 0.975518 | ortools:nominal_seed101_or_tools | 4 | 0.166667 | nominal_seed101_or_tools | 4 | 0.166667 | 24 | 0.5 | 0.916667 | 12 | 0.0544413 | 0.0536647 |
| cold_chain | 24 | 24 | 10 | 10 | 1 | 3.2406 | 3.2406 | 0.975518 | ortools:nominal_seed103_or_tools | 4 | 0.166667 | nominal_seed103_or_tools | 4 | 0.166667 | 24 | 0.5 | 0.916667 | 12 | 0.055795 | 0.0533638 |
| grocery | 24 | 24 | 11 | 11 | 1 | 3.37581 | 3.37581 | 0.975829 | ortools:nominal_seed101_or_tools | 3 | 0.125 | nominal_seed101_or_tools | 3 | 0.125 | 24 | 0.416667 | 0.833333 | 14 | 0.0579452 | 0.0558232 |

## Top Candidate Frequencies

| Domain | Candidate | Routing Provider | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- | --- |
| atm | ortools:nominal_seed101_or_tools | ortools | nominal_seed101_or_tools | 5 | 24 | 0.208333 |
| atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 3 | 24 | 0.125 |
| atm | ortools:quantile_p75_scaled_seed107_or_tools | ortools | quantile_p75_scaled_seed107_or_tools | 3 | 24 | 0.125 |
| atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 3 | 24 | 0.125 |
| atm | ortools:nominal_seed103_or_tools | ortools | nominal_seed103_or_tools | 2 | 24 | 0.0833333 |
| atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 2 | 24 | 0.0833333 |
| atm | ortools:proxy_mean_scaled_seed109_or_tools | ortools | proxy_mean_scaled_seed109_or_tools | 2 | 24 | 0.0833333 |
| atm | ortools:robust_mean_1std_scaled_seed113_or_tools | ortools | robust_mean_1std_scaled_seed113_or_tools | 2 | 24 | 0.0833333 |
| atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 1 | 24 | 0.0416667 |
| atm | ortools:robust_mean_2std_scaled_or_tools | ortools | robust_mean_2std_scaled_or_tools | 1 | 24 | 0.0416667 |

## Instance-Level Route Plan Diversity

| Instance | Customers | Domains | Winner Rows | Unique Winning Candidates Across Domains | Unique Winning Route Plans Across Domains | Route Plan Entropy Across Domains | Normalized Route Plan Entropy Across Domains | Candidate Entropy Across Domains | All Domains Same Candidate | All Domains Same Route Plan | Confirmed Winner Rows | Strict Stability Safe Rows | Final Full Required Rows | Ranking Flip | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 105 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.055795 | 0.00608732 |
| X-n110-k13 | 109 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0180577 | 0.000834837 |
| X-n115-k10 | 114 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 2 | 2 | no | 0.0579452 | 0.00455841 |
| X-n120-k6 | 119 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00213592 | 0.00580762 |
| X-n129-k18 | 128 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 0 | 4 | yes | 0.00829635 | 0.0121433 |
| X-n134-k13 | 133 | 4 | 4 | 4 | 4 | 2 | 1 | 2 | no | no | 4 | 3 | 1 | no | 0.0105159 | 0.0558232 |
| X-n139-k10 | 138 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0117688 | 0.0541776 |
| X-n143-k7 | 142 | 4 | 4 | 4 | 4 | 2 | 1 | 2 | no | no | 4 | 0 | 4 | yes | 0.00841866 | 0.0435835 |
| X-n162-k11 | 161 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0140302 | 0.0105344 |
| X-n167-k10 | 166 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00276243 | 0.000153741 |
| X-n181-k23 | 180 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00402075 | 2.66658e-05 |
| X-n186-k15 | 185 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00510421 | 0.00184014 |
| X-n190-k8 | 189 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00820829 | 0.000869516 |
| X-n204-k19 | 203 | 4 | 4 | 2 | 2 | 1 | 1 | 1 | no | no | 4 | 0 | 4 | yes | 0.00538642 | 0.00575457 |
| X-n209-k16 | 208 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0102934 | 0.00196416 |
| X-n223-k34 | 222 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0101111 | 6.3538e-05 |
| X-n228-k23 | 227 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.039708 | 0.000389827 |
| X-n237-k14 | 236 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 0 | 4 | yes | 0.00483958 | 0.000213274 |
| X-n242-k48 | 241 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0128632 | 0.0036602 |
| X-n251-k28 | 250 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00131976 | 0.000128238 |
| X-n261-k13 | 260 | 4 | 4 | 4 | 4 | 2 | 1 | 2 | no | no | 4 | 0 | 4 | yes | 0.0121469 | 0.00195226 |
| X-n275-k28 | 274 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00248557 | 3.09769e-05 |
| X-n280-k17 | 279 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.011361 | 0.000246385 |
| X-n284-k15 | 283 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0159163 | 0.000242306 |

## Certified Winner Rate

| Scope | Winner Rows | Confirmed Rows | Confirm Feasible Rows | Metric Stability Safe Rows | Strict Stability Safe Rows | Strict Stability Safe Rate | Final Full Required Rows | Ranking Flip Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 96 | 96 | 96 | 86 | 45 | 0.46875 | 51 | 12 |
| domain:atm | 24 | 24 | 24 | 22 | 11 | 0.458333 | 13 | 12 |
| domain:cargo | 24 | 24 | 24 | 22 | 12 | 0.5 | 12 | 12 |
| domain:cold_chain | 24 | 24 | 24 | 22 | 12 | 0.5 | 12 | 12 |
| domain:grocery | 24 | 24 | 24 | 20 | 10 | 0.416667 | 14 | 12 |

## Final Full Required Rows

| Instance | Domain | Candidate | Route Plan | Routing Provider | Confirm Feasible | Stockout Relative Drift | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Flip | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.0509403 | 0.00190482 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | cargo | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.0544413 | 0.00268803 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | cold_chain | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.055795 | 0.00608732 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n106-k14 | grocery | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.0551724 | 0.00578436 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n110-k13 | atm | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00882807 | 0.000828162 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0180577 | 0.000816307 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0156006 | 0.000834837 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.00509075 | 0.000811047 | yes | yes | no | final_full_required: domain ranking flip |
| X-n115-k10 | atm | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.0545813 | 0.00447936 | no | no | no | final_full_required: drift threshold exceeded |
| X-n115-k10 | grocery | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.0579452 | 0.00453775 | no | no | no | final_full_required: drift threshold exceeded |
| X-n120-k6 | atm | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.00175884 | 0.00580674 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.00115785 | 0.00580762 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.000773246 | 0.00579754 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.00213592 | 0.00580036 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | atm | ortools:robust_mean_1std_scaled_seed113_or_tools | robust_mean_1std_scaled_seed113_or_tools | ortools | yes | 0.000188182 | 0.0121197 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00753041 | 4.90639e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:robust_mean_1std_scaled_seed113_or_tools | robust_mean_1std_scaled_seed113_or_tools | ortools | yes | 0.00829635 | 0.0119062 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:robust_mean_1std_scaled_seed113_or_tools | robust_mean_1std_scaled_seed113_or_tools | ortools | yes | 0.00358423 | 0.0121433 | yes | yes | no | final_full_required: domain ranking flip |
| X-n134-k13 | grocery | ortools:robust_mean_1std_scaled_or_tools | robust_mean_1std_scaled_or_tools | ortools | yes | 0.0105159 | 0.0558232 | no | no | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | atm | ortools:proxy_mean_scaled_seed109_or_tools | proxy_mean_scaled_seed109_or_tools | ortools | yes | 0.00891453 | 0.0499346 | yes | yes | no | final_full_required: domain ranking flip |
| X-n139-k10 | cargo | ortools:proxy_mean_scaled_seed109_or_tools | proxy_mean_scaled_seed109_or_tools | ortools | yes | 0.0117688 | 0.0536647 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | cold_chain | ortools:proxy_mean_scaled_seed109_or_tools | proxy_mean_scaled_seed109_or_tools | ortools | yes | 0.00634361 | 0.0533638 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n139-k10 | grocery | ortools:proxy_mean_scaled_seed109_or_tools | proxy_mean_scaled_seed109_or_tools | ortools | yes | 0.00665033 | 0.0541776 | no | yes | no | final_full_required: drift threshold exceeded |
| X-n143-k7 | atm | ortools:robust_mean_1std_scaled_or_tools | robust_mean_1std_scaled_or_tools | ortools | yes | 0.00316885 | 0.00638891 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | cargo | ortools:robust_mean_1std_scaled_seed113_or_tools | robust_mean_1std_scaled_seed113_or_tools | ortools | yes | 0.00575374 | 0.00340589 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00371488 | 0.000694279 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | proxy_mean_or_tools | ortools | yes | 0.00841866 | 0.0435835 | yes | yes | no | final_full_required: domain ranking flip |
| X-n181-k23 | atm | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00402075 | 2.66658e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n181-k23 | cargo | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00272869 | 2.36717e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n181-k23 | cold_chain | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00261438 | 2.5708e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n181-k23 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00376428 | 1.58369e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | atm | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.00538642 | 0.00512727 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_seed101_or_tools | nominal_seed101_or_tools | ortools | yes | 0.00434018 | 0.00575457 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00213777 | 0.00450027 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00187661 | 0.0051647 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00747314 | 0.00195525 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | cargo | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.0099859 | 0.00196416 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | cold_chain | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.0102934 | 0.00192367 | yes | yes | no | final_full_required: domain ranking flip |
| X-n209-k16 | grocery | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00656814 | 0.00190614 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | atm | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0280775 | 0.000389827 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | cargo | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.039708 | 0.000376284 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.027053 | 0.000376257 | yes | yes | no | final_full_required: domain ranking flip |
| X-n228-k23 | grocery | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0292669 | 0.000217854 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | atm | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00483958 | 0.000213274 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_seed103_or_tools | nominal_seed103_or_tools | ortools | yes | 0.000268986 | 1.91181e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_seed103_or_tools | nominal_seed103_or_tools | ortools | yes | 0.000812641 | 2.37827e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_seed103_or_tools | nominal_seed103_or_tools | ortools | yes | 9.00901e-05 | 1.70244e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00968871 | 0.00195226 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | cargo | ortools:robust_mean_2std_scaled_or_tools | robust_mean_2std_scaled_or_tools | ortools | yes | 0.00842747 | 0.00145695 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | cold_chain | ortools:proxy_mean_scaled_or_tools | proxy_mean_scaled_or_tools | ortools | yes | 0.0121469 | 0.00166421 | yes | yes | no | final_full_required: domain ranking flip |
| X-n261-k13 | grocery | ortools:quantile_p75_scaled_seed107_or_tools | quantile_p75_scaled_seed107_or_tools | ortools | yes | 0.00386066 | 0.0011654 | yes | yes | no | final_full_required: domain ranking flip |

## Ranking Stability

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

## Suggested Interpretation

- Winner diversity is the main signal for whether sector objectives change route choice.
- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.
- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.
- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.
