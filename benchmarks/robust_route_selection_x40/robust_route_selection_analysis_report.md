# Robust Route Selection Analysis

## Scope

- Source directory: `benchmarks\robust_route_selection_x40`
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
| unique_winning_candidates | 3 |
| unique_winning_route_plans | 3 |
| unique_winning_providers | 1 |
| confirmed_winner_rows | 112 |
| confirm_feasible_rate | 1 |
| metric_stability_safe_rate | 1 |
| strict_stability_safe_rate | 0.607143 |
| final_full_required_rows | 44 |
| max_stockout_relative_drift | 0.0204446 |
| max_mean_total_cost_relative_drift | 0.0120186 |
| ranking_rows | 28 |
| ranking_flip_rate | 0.392857 |
| mean_stockout_spearman | 0.878571 |

## Domain-Specific Winner Diversity

| Domain | Winner Rows | Instances | Unique Winning Candidates | Unique Winning Route Plans | Unique Winning Providers | Winner Candidate Entropy | Winner Route Plan Entropy | Normalized Winner Candidate Entropy | Top Candidate | Top Candidate Count | Top Candidate Share | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Confirmed Rows | Strict Stability Safe Rate | Metric Stability Safe Rate | Final Full Required Rows | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 28 | 28 | 3 | 3 | 1 | 0.442661 | 0.442661 | 0.279288 | ortools:nominal_or_tools | 26 | 0.928571 | nominal_or_tools | 26 | 0.928571 | 28 | 0.607143 | 1 | 11 | 0.015105 | 0.011975 |
| cargo | 28 | 28 | 3 | 3 | 1 | 0.442661 | 0.442661 | 0.279288 | ortools:nominal_or_tools | 26 | 0.928571 | nominal_or_tools | 26 | 0.928571 | 28 | 0.607143 | 1 | 11 | 0.0204446 | 0.0119843 |
| cold_chain | 28 | 28 | 3 | 3 | 1 | 0.442661 | 0.442661 | 0.279288 | ortools:nominal_or_tools | 26 | 0.928571 | nominal_or_tools | 26 | 0.928571 | 28 | 0.607143 | 1 | 11 | 0.0143584 | 0.011775 |
| grocery | 28 | 28 | 3 | 3 | 1 | 0.442661 | 0.442661 | 0.279288 | ortools:nominal_or_tools | 26 | 0.928571 | nominal_or_tools | 26 | 0.928571 | 28 | 0.607143 | 1 | 11 | 0.015377 | 0.0120186 |

## Top Candidate Frequencies

| Domain | Candidate | Routing Provider | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- | --- |
| atm | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 | 28 | 0.928571 |
| atm | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| atm | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cargo | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 | 28 | 0.928571 |
| cargo | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cargo | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 | 28 | 0.928571 |
| cold_chain | ortools:proxy_mean_scaled_or_tools | ortools | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cold_chain | ortools:quantile_p90_scaled_or_tools | ortools | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| grocery | ortools:nominal_or_tools | ortools | nominal_or_tools | 26 | 28 | 0.928571 |

## Instance-Level Route Plan Diversity

| Instance | Customers | Domains | Winner Rows | Unique Winning Candidates Across Domains | Unique Winning Route Plans Across Domains | Route Plan Entropy Across Domains | Normalized Route Plan Entropy Across Domains | Candidate Entropy Across Domains | All Domains Same Candidate | All Domains Same Route Plan | Confirmed Winner Rows | Strict Stability Safe Rows | Final Full Required Rows | Ranking Flip | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | 105 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0105116 | 0.000984556 |
| X-n110-k13 | 109 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00314136 | 8.44157e-05 |
| X-n115-k10 | 114 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00817138 | 0.000520465 |
| X-n120-k6 | 119 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00234375 | 2.98908e-05 |
| X-n129-k18 | 128 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0101756 | 7.78408e-05 |
| X-n134-k13 | 133 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00853719 | 0.00173909 |
| X-n139-k10 | 138 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0113083 | 0.000194443 |
| X-n143-k7 | 142 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0176781 | 0.00124597 |
| X-n157-k13 | 156 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00741035 | 2.8277e-05 |
| X-n162-k11 | 161 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00524206 | 0.00256399 |
| X-n167-k10 | 166 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00418531 | 0.000197099 |
| X-n181-k23 | 180 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00629577 | 2.77378e-05 |
| X-n186-k15 | 185 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00435299 | 0.00082061 |
| X-n190-k8 | 189 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0201185 | 0.0120186 |
| X-n204-k19 | 203 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00673679 | 0.00135523 |
| X-n209-k16 | 208 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0136698 | 0.000160604 |
| X-n214-k11 | 213 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0204446 | 0.00206653 |
| X-n219-k73 | 218 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00347725 | 5.18687e-06 |
| X-n223-k34 | 222 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0110854 | 7.43087e-05 |
| X-n228-k23 | 227 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0141428 | 0.000330877 |
| X-n233-k16 | 232 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0141702 | 0.000719935 |
| X-n237-k14 | 236 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00252003 | 2.89791e-05 |
| X-n242-k48 | 241 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.0186236 | 4.55383e-05 |
| X-n251-k28 | 250 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00385498 | 9.50027e-05 |
| X-n261-k13 | 260 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.00747556 | 0.00188859 |
| X-n275-k28 | 274 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 0 | 4 | yes | 0.00357735 | 3.27768e-05 |
| X-n280-k17 | 279 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0116561 | 0.000263029 |
| X-n284-k15 | 283 | 4 | 4 | 1 | 1 | 0 | 0 | 0 | yes | yes | 4 | 4 | 0 | no | 0.0135042 | 0.000234842 |

## Certified Winner Rate

| Scope | Winner Rows | Confirmed Rows | Confirm Feasible Rows | Metric Stability Safe Rows | Strict Stability Safe Rows | Strict Stability Safe Rate | Final Full Required Rows | Ranking Flip Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 112 | 112 | 112 | 112 | 68 | 0.607143 | 44 | 11 |
| domain:atm | 28 | 28 | 28 | 28 | 17 | 0.607143 | 11 | 11 |
| domain:cargo | 28 | 28 | 28 | 28 | 17 | 0.607143 | 11 | 11 |
| domain:cold_chain | 28 | 28 | 28 | 28 | 17 | 0.607143 | 11 | 11 |
| domain:grocery | 28 | 28 | 28 | 28 | 17 | 0.607143 | 11 | 11 |

## Final Full Required Rows

| Instance | Domain | Candidate | Route Plan | Routing Provider | Confirm Feasible | Stockout Relative Drift | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Flip | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-n106-k14 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00447691 | 0.000984556 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0105116 | 0.000804798 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000705384 | 0.000786546 | yes | yes | no | final_full_required: domain ranking flip |
| X-n106-k14 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00047081 | 0.00053046 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00191002 | 6.87416e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00314136 | 1.58408e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000211999 | 8.44157e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n110-k13 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000423908 | 3.03947e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000978474 | 2.30193e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00234375 | 2.46323e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00155854 | 2.98908e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n120-k6 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000194553 | 1.35661e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000131961 | 2.7977e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00741035 | 2.37057e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00385024 | 2.8277e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n157-k13 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00251789 | 1.82655e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000938747 | 0.00135523 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00673679 | 0.00116339 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00213777 | 0.00101086 | yes | yes | no | final_full_required: domain ranking flip |
| X-n204-k19 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000821018 | 0.000977882 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | atm | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.00478937 | 0.00206653 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | cargo | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.0204446 | 0.00202049 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | cold_chain | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.0143584 | 0.00194799 | yes | yes | no | final_full_required: domain ranking flip |
| X-n214-k11 | grocery | ortools:quantile_p90_scaled_or_tools | quantile_p90_scaled_or_tools | ortools | yes | 0.00729927 | 0.00122045 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00347725 | 4.51946e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000968992 | 3.93247e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000387559 | 5.18687e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n219-k73 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0032882 | 3.02031e-06 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00251256 | 2.89791e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00143756 | 2.27604e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.000270563 | 2.52982e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n237-k14 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00252003 | 1.69503e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n242-k48 | atm | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.010564 | 3.97464e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n242-k48 | cargo | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0186236 | 3.13938e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n242-k48 | cold_chain | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.0135016 | 4.55383e-05 | yes | yes | no | final_full_required: domain ranking flip |
| X-n242-k48 | grocery | ortools:nominal_or_tools | nominal_or_tools | ortools | yes | 0.00866824 | 2.50252e-05 | yes | yes | no | final_full_required: domain ranking flip |
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

## Suggested Interpretation

- Winner diversity is the main signal for whether sector objectives change route choice.
- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.
- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.
- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.
