# Robust Route Selection Analysis

## Scope

- Source directory: `benchmarks\robust_route_selection_stability_smoke`
- This report summarizes route-candidate winners after the common stochastic decision layer.
- `Strict Stability Safe` means full-scenario confirmation is feasible, metric drift is within thresholds, and no domain stockout ranking flip was observed.

## Aggregate Summary

| Metric | Value |
| --- | --- |
| instances | 1 |
| domains | 2 |
| candidate_rows | 20 |
| candidate_feasible_rows | 8 |
| winner_rows | 2 |
| winner_domains | 2 |
| unique_winning_candidates | 2 |
| unique_winning_route_plans | 2 |
| unique_winning_providers | 1 |
| confirmed_winner_rows | 2 |
| confirm_feasible_rate | 1 |
| metric_stability_safe_rate | 1 |
| strict_stability_safe_rate | 1 |
| final_full_required_rows | 0 |
| max_stockout_relative_drift | 0.0115632 |
| max_mean_total_cost_relative_drift | 0.00635293 |
| ranking_rows | 1 |
| ranking_flip_rate | 0 |
| mean_stockout_spearman | 1 |

## Domain-Specific Winner Diversity

| Domain | Winner Rows | Instances | Unique Winning Candidates | Unique Winning Route Plans | Unique Winning Providers | Winner Candidate Entropy | Winner Route Plan Entropy | Normalized Winner Candidate Entropy | Top Candidate | Top Candidate Count | Top Candidate Share | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Confirmed Rows | Strict Stability Safe Rate | Metric Stability Safe Rate | Final Full Required Rows | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | ortools:proxy_mean_or_tools | 1 | 1 | proxy_mean_or_tools | 1 | 1 | 1 | 1 | 1 | 0 | 0.0043021 | 0.00411617 |
| cold_chain | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | ortools:nominal_or_tools | 1 | 1 | nominal_or_tools | 1 | 1 | 1 | 1 | 1 | 0 | 0.0115632 | 0.00635293 |

## Top Candidate Frequencies

| Domain | Candidate | Routing Provider | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- | --- |
| atm | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 1 | 1 | 1 |
| cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 1 | 1 | 1 |

## Instance-Level Route Plan Diversity

| Instance | Customers | Domains | Winner Rows | Unique Winning Candidates Across Domains | Unique Winning Route Plans Across Domains | Route Plan Entropy Across Domains | Normalized Route Plan Entropy Across Domains | Candidate Entropy Across Domains | All Domains Same Candidate | All Domains Same Route Plan | Confirmed Winner Rows | Strict Stability Safe Rows | Final Full Required Rows | Ranking Flip | Max Stockout Relative Drift | Max Mean Total Cost Relative Drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | 31 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | no | no | 2 | 2 | 0 | no | 0.0115632 | 0.00635293 |

## Certified Winner Rate

| Scope | Winner Rows | Confirmed Rows | Confirm Feasible Rows | Metric Stability Safe Rows | Strict Stability Safe Rows | Strict Stability Safe Rate | Final Full Required Rows | Ranking Flip Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all | 2 | 2 | 2 | 2 | 2 | 1 | 0 | 0 |
| domain:atm | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| domain:cold_chain | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |

## Final Full Required Rows

No non-safe full-confirmed winner rows were found.

## Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | 2 | cold_chain > atm | cold_chain > atm | no | 1 |  |

## Suggested Interpretation

- Winner diversity is the main signal for whether sector objectives change route choice.
- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.
- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.
- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.
