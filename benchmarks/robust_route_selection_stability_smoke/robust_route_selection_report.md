# Robust Route Selection Report

## Scope

This diagnostic evaluates multiple routing candidates with the same stochastic decision layer, then selects a domain-level winner by the configured score metric.

- Data dir: `benchmarks/proxy_cvrplib`
- Routing providers: `ortools`
- LP backend: `pulp_cbc`
- LP planning scenario limit: `60`
- Score metric: `mean_total_cost`
- Full-scenario winner confirmation: `True`

Fast mode is intended for route-candidate screening. Final decision-driving claims should be rerun with full planning history by passing `--lp-planning-scenario-limit 0`.

## Candidate Coverage

| Domain | Candidate_Rows | Feasible_Rows | Instances | Candidates | Median_Total_Runtime_Sec | Top_Winning_Candidate | Top_Winning_Provider | Top_Winning_Route_Plan | Top_Winner_Count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atm | 10 | 4 | 1 | 10 | 2.00291 | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 1 |
| cold_chain | 10 | 4 | 1 | 10 | 2.00291 | ortools:nominal_or_tools | ortools | nominal_or_tools | 1 |

## Winners

| Instance | Domain | Candidate | Routing Provider | Route Plan | Score Value | mean_total_cost | stockout_rate | Route Cost | Optimized Load Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | atm | ortools:proxy_mean_or_tools | ortools | proxy_mean_or_tools | 942.388 | 942.388 | 0.338871 | 796 | 483.626 |
| A-n32-k5 | cold_chain | ortools:nominal_or_tools | ortools | nominal_or_tools | 1035.07 | 1035.07 | 0.380968 | 784 | 456.822 |

## Full-Scenario Winner Confirmation

| Instance | Domain | Candidate | Fast Stockout | Full Stockout | Stockout Relative Drift | Fast Mean Total Cost | Full Mean Total Cost | Mean Total Cost Relative Drift | Metric Stability Safe | Ranking Stable | Strict Stability Safe | Stability Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | atm | ortools:proxy_mean_or_tools | 0.338871 | 0.337419 | 0.0043021 | 942.388 | 938.525 | 0.00411617 | yes | yes | yes | safe |
| A-n32-k5 | cold_chain | ortools:nominal_or_tools | 0.380968 | 0.376613 | 0.0115632 | 1035.07 | 1028.54 | 0.00635293 | yes | yes | yes | safe |

## Domain Ranking Stability

| Instance | Domains | Fast Ranking | Full Ranking | Ranking Flip | Stockout Spearman | Ranking Note |
| --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | 2 | cold_chain > atm | cold_chain > atm | no | 1 |  |

## Route Candidates

| Instance | Candidate | Route Feasible | Route Count | Route Cost | Planned Route Load Ratio | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| A-n32-k5 | ortools:nominal_or_tools | yes | 5 | 784 | 0.82 |  |
| A-n32-k5 | ortools:proxy_mean_or_tools | yes | 5 | 796 | 0.872444 |  |
| A-n32-k5 | ortools:quantile_p75_or_tools | no | 0 |  | 1.02232 | total_load_exceeds_fleet_capacity |
| A-n32-k5 | ortools:quantile_p90_or_tools | no | 0 |  | 1.24259 | total_load_exceeds_fleet_capacity |
| A-n32-k5 | ortools:robust_mean_1std_or_tools | no | 0 |  | 1.15581 | total_load_exceeds_fleet_capacity |
| A-n32-k5 | ortools:robust_mean_2std_or_tools | no | 0 |  | 1.43918 | total_load_exceeds_fleet_capacity |
| A-n32-k5 | ortools:quantile_p75_scaled_or_tools | yes | 5 | 1011 | 0.995 |  |
| A-n32-k5 | ortools:quantile_p90_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |
| A-n32-k5 | ortools:robust_mean_1std_scaled_or_tools | yes | 5 | 995 | 0.995 |  |
| A-n32-k5 | ortools:robust_mean_2std_scaled_or_tools | no | 0 |  | 0.995 | ortools_no_solution |

## Interpretation

- A domain winner means that route candidate had the lowest selected evaluation metric after the stochastic loading LP.
- This is not a new routing solver; it is a robust selection layer over existing route providers and load plans.
- `Metric Stability Safe` checks only stockout and mean_total_cost drift; `Strict Stability Safe` also requires no domain stockout ranking flip.
- Infeasible high-quantile or robust plans remain visible because capacity pressure is part of the result.
