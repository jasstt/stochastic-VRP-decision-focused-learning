# Robust Route Selection Analysis

## Scope

- Source directory: `benchmarks\robust_route_selection_x40_stockout_rate`
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
| unique_winning_candidates | 6 |
| unique_winning_route_plans | 6 |
| unique_winning_providers | 1 |
| confirmed_winner_rows | 112 |
| confirm_feasible_rate | 1 |
| metric_stability_safe_rate | 1 |
| strict_stability_safe_rate | 0.5 |
| final_full_required_rows | 56 |
| max_stockout_relative_drift | 0.0180577 |
| max_mean_total_cost_relative_drift | 0.00256399 |
| ranking_rows | 28 |
| ranking_flip_rate | 0.5 |
| mean_stockout_spearman | 0.878571 |

## Domain-Specific Winner Diversity

| Domain | Winner Rows | Instances | Unique Winning Candidates | Unique Winning Route Plans | Unique Winning Providers | Winner Candidate Entropy | Winner Route Plan Entropy | Normalized Winner Candidate Entropy | Top Candidate | Top Candidate Count | Top Candidate Share | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Confirmed Rows | Strict Stability Safe Rate | Metric Stability Safe Rate | Final Full Required Rows | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 28 | 28 | 6 | 6 | 1 | 1.74123 | 1.74123 | 0.673601 | ortools:nominal_or_tools | 17 | 0.607143 | nominal_or_tools | 17 | 0.607143 | 28 | 0.5 | 1 | 14 | 0.0141428 | 0.00217061 |
| cargo | 28 | 28 | 5 | 5 | 1 | 1.69677 | 1.69677 | 0.730757 | ortools:nominal_or_tools | 17 | 0.607143 | nominal_or_tools | 17 | 0.607143 | 28 | 0.5 | 1 | 14 | 0.0180577 | 0.00256399 |
| cold_chain | 28 | 28 | 5 | 5 | 1 | 1.6289 | 1.6289 | 0.70153 | ortools:nominal_or_tools | 17 | 0.607143 | nominal_or_tools | 17 | 0.607143 | 28 | 0.5 | 1 | 14 | 0.0140406 | 0.00236985 |
| grocery | 28 | 28 | 5 | 5 | 1 | 1.54224 | 1.54224 | 0.664207 | ortools:nominal_or_tools | 18 | 0.642857 | nominal_or_tools | 18 | 0.642857 | 28 | 0.5 | 1 | 14 | 0.0113767 | 0.00160499 |

## Top Candidate Frequencies

| Domain | Candidate | Routing Provider | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- | --- |
| atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 17 | 28 | 0.607143 |
| atm | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| atm | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| atm | ortools:robust_mean_1std_scaled_or_tools | ortools | robust_mean_1std_scaled_or_tools | 1 | 28 | 0.0357143 |
| cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 17 | 28 | 0.607143 |
| cargo | ortools:quantile_p75_scaled_or_tools | ortools | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 2 | 28 | 0.0714286 |
| cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 2 | 28 | 0.0714286 |

## Instance-Level Route Plan Diversity

| Instance | Customers | Domains | Winner Rows | Unique Winning Candidates Across Domains | Unique Winning Route Plans Across Domains | Route Plan Entropy Across Domains | Normalized Route Plan Entropy Across Domains | Candidate Entropy Across Domains | All Domains Same Candidate | All Domains Same Route Plan | Confirmed Winner Rows | Strict Stability Safe Rows | Final Full Required Rows | Ranking Flip | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 105 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0105116 | 0.000984556 |
| X-n110-k13 | 109 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0180577 | 9.94206e-05 |
| X-n115-k10 | 114 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00817138 | 0.000520465 |
| X-n120-k6 | 119 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00234375 | 2.98908e-05 |
| X-n129-k18 | 128 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 0 | 4 | yes | 0.00744986 | 7.94798e-05 |
| X-n134-k13 | 133 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 4 | 0 | no | 0.007091 | 0.0019553 |
| X-n139-k10 | 138 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0113083 | 0.000194443 |
| X-n143-k7 | 142 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 0 | 4 | yes | 0.00865407 | 0.0014289 |
| X-n157-k13 | 156 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00741035 | 2.8277e-05 |
| X-n162-k11 | 161 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00524206 | 0.00256399 |
| X-n167-k10 | 166 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00418531 | 0.000197099 |
| X-n181-k23 | 180 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00629577 | 2.77378e-05 |
| X-n186-k15 | 185 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00435299 | 0.00082061 |
| X-n190-k8 | 189 | 4 | 4 | 2 | 2 | 0.811278 | 0.811278 | 0.811278 | no | no | 4 | 4 | 0 | no | 0.0113767 | 0.000180964 |
| X-n204-k19 | 203 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00673679 | 0.00135523 |
| X-n209-k16 | 208 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00928102 | 0.000154625 |
| X-n214-k11 | 213 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0116538 | 0.00182475 |
| X-n219-k73 | 218 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00347725 | 5.18687e-06 |
| X-n223-k34 | 222 | 4 | 4 | 2 | 2 | 1 | 1 | 1 | no | no | 4 | 0 | 4 | yes | 0.00641679 | 8.7049e-05 |
| X-n228-k23 | 227 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0141428 | 0.000330877 |
| X-n233-k16 | 232 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0141702 | 0.000719935 |
| X-n237-k14 | 236 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00252003 | 2.89791e-05 |
| X-n242-k48 | 241 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0113536 | 3.76682e-05 |
| X-n251-k28 | 250 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00385498 | 9.50027e-05 |
| X-n261-k13 | 260 | 4 | 4 | 2 | 2 | 1 | 1 | 1 | no | no | 4 | 4 | 0 | no | 0.0117819 | 0.00202485 |
| X-n275-k28 | 274 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00357735 | 3.27768e-05 |
| X-n280-k17 | 279 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0116561 | 0.000263029 |
| X-n284-k15 | 283 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.013005 | 0.000242916 |

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
| X-n129-k18 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.000187793 | 7.94798e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cargo | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.00744986 | 7.21386e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | cold_chain | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00382848 | 7.50673e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n129-k18 | grocery | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.0054717 | 4.37567e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | atm | ortools:proxy_mean_or_tools | proxy_mean_or_tools | ortools | yes | 0.000227635 | 0.00108536 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | cargo | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.00367057 | 0.0014289 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | cold_chain | ortools:proxy_mean_or_tools | proxy_mean_or_tools | ortools | yes | 0.00707714 | 0.00103113 | yes | yes | no | final_full_required: domain ranking flip |
| X-n143-k7 | grocery | ortools:proxy_mean_or_tools | proxy_mean_or_tools | ortools | yes | 0.00865407 | 0.000736558 | yes | yes | no | final_full_required: domain ranking flip |
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
| X-n214-k11 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00712096 | 0.00182475 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00739113 | 0.00144799 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0116538 | 0.00149428 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00668729 | 0.00120175 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00347725 | 4.51946e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000968992 | 3.93247e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000387559 | 5.18687e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0032882 | 3.02031e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n223-k34 | atm | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00628805 | 8.7049e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n223-k34 | cargo | ortools:robust_mean_1std_scaled_or_tools | robust_mean_1std_scaled_or_tools | ortools | yes | 0.000716186 | 4.78393e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n223-k34 | cold_chain | ortools:robust_mean_1std_scaled_or_tools | robust_mean_1std_scaled_or_tools | ortools | yes | 0.00641679 | 5.37159e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n223-k34 | grocery | ortools:quantile_p75_scaled_or_tools | quantile_p75_scaled_or_tools | ortools | yes | 0.00119749 | 4.96824e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00251256 | 2.89791e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00143756 | 2.27604e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000270563 | 2.52982e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00252003 | 1.69503e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00385498 | 9.50027e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00259235 | 9.33851e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00305301 | 8.38037e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n251-k28 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00275128 | 4.91559e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000698568 | 3.11968e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00357735 | 2.53688e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0022811 | 3.27768e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n275-k28 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000875197 | 1.98041e-05 | yes | yes | no | final_full_required: domain ranking flip |

## Ranking Stability

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

## Suggested Interpretation

- Winner diversity is the main signal for whether sector objectives change route choice.
- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.
- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.
- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.
