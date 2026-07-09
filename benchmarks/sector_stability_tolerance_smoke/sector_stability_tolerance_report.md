# Sector Stability Tolerance Report

## Scope

This branch defines a tolerance layer for domain-adapter outputs. It judges whether a candidate run can be treated as safe for exploration, or whether the final result must be confirmed with the full scenario/profile.

Inputs used in this smoke run:

- Scenario reduction pair: `benchmarks\proxy_cvrplib_x_v4\scenario_reduction_bias_results.csv`
- OR-Tools provider pair: `benchmarks\proxy_cvrplib_n20\domain_engine_results_ortools_provider.csv`
- VROOM provider pair: `benchmarks\proxy_cvrplib_n20\domain_engine_results_vroom_provider.csv`
- Custom comparison specs: 0

## Tolerance Rules

- Stockout relative drift must be <= 5.0%.
- mean_total_cost relative drift must be <= 5.0%.
- Domain stockout ranking must not flip within the same instance.
- Any feasibility mismatch is automatically final_full_required.

Row status is `safe` only when all four checks pass. Otherwise the row is marked unstable or final_full_required.
`Metric Safe` ignores ranking and only checks feasibility plus stockout/cost drift; `Safe` is stricter and also requires ranking stability.

## Smoke Finding

| Comparison | Instances | Rows | Both_Feasible | Metric_Safe_Rows | Safe_Rows | Max_Stockout_Rel_Drift | Max_Cost_Rel_Drift | Mean_Stockout_Rel_Drift | Mean_Cost_Rel_Drift | Metric Safe Share | Safe Share | Ranking_Flip_Instances |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| provider_switch | 20 | 80 | 80 | 69 | 36 | 0.174224 | 0.0848901 | 0.0226153 | 0.0161086 | 0.8625 | 0.45 | 11 |
| scenario_reduction_limit_60 | 9 | 36 | 36 | 36 | 4 | 0.0187902 | 0.00213767 | 0.00670723 | 0.00060406 | 1 | 0.111111 | 8 |

## Domain Summary

| Comparison | Domain | Rows | Both_Feasible | Metric_Safe_Rows | Safe_Rows | Ranking_Flip_Rows | Mean_Stockout_Rel_Drift | Max_Stockout_Rel_Drift | Mean_Cost_Rel_Drift | Max_Cost_Rel_Drift | Metric Safe Share | Safe Share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| provider_switch | atm | 20 | 20 | 17 | 9 | 11 | 0.0205889 | 0.140187 | 0.0169611 | 0.0848901 | 0.85 | 0.45 |
| provider_switch | cargo | 20 | 20 | 17 | 9 | 11 | 0.0245682 | 0.174224 | 0.0177319 | 0.0786776 | 0.85 | 0.45 |
| provider_switch | cold_chain | 20 | 20 | 18 | 9 | 11 | 0.0266793 | 0.113793 | 0.0131924 | 0.0456958 | 0.9 | 0.45 |
| provider_switch | grocery | 20 | 20 | 17 | 9 | 11 | 0.0186247 | 0.103286 | 0.0165491 | 0.0577477 | 0.85 | 0.45 |
| scenario_reduction_limit_60 | atm | 9 | 9 | 9 | 1 | 8 | 0.0054112 | 0.0170898 | 0.000754372 | 0.00213767 | 1 | 0.111111 |
| scenario_reduction_limit_60 | cargo | 9 | 9 | 9 | 1 | 8 | 0.00822121 | 0.0187902 | 0.000624375 | 0.00162526 | 1 | 0.111111 |
| scenario_reduction_limit_60 | cold_chain | 9 | 9 | 9 | 1 | 8 | 0.00665096 | 0.0163546 | 0.000581783 | 0.00176488 | 1 | 0.111111 |
| scenario_reduction_limit_60 | grocery | 9 | 9 | 9 | 1 | 8 | 0.00654555 | 0.0186075 | 0.000455709 | 0.00121725 | 1 | 0.111111 |

## Ranking Flips

| Comparison | Instance | Baseline Ranking | Candidate Ranking | Stockout Spearman |
| --- | --- | --- | --- | --- |
| provider_switch | A-n33-k5 | cold_chain > grocery > atm > cargo | grocery > atm > cargo > cold_chain | -0.2 |
| provider_switch | A-n45-k6 | cargo > atm > grocery > cold_chain | atm > cargo > grocery > cold_chain | 0.8 |
| provider_switch | A-n60-k9 | cargo > atm > grocery > cold_chain | atm > grocery > cargo > cold_chain | 0.4 |
| provider_switch | B-n78-k10 | grocery > atm > cargo > cold_chain | atm > grocery > cargo > cold_chain | 0.8 |
| provider_switch | E-n23-k3 | cold_chain > grocery > atm > cargo | cold_chain > grocery > cargo > atm | 0.8 |
| provider_switch | E-n51-k5 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | 0.8 |
| provider_switch | E-n76-k7 | atm > grocery > cargo > cold_chain | grocery > atm > cargo > cold_chain | 0.8 |
| provider_switch | P-n19-k2 | cold_chain > atm > grocery > cargo | atm > grocery > cargo > cold_chain | -0.2 |
| provider_switch | P-n55-k7 | grocery > atm > cold_chain > cargo | grocery > cold_chain > cargo > atm | 0.4 |
| provider_switch | P-n60-k10 | atm > grocery > cargo > cold_chain | grocery > cargo > atm > cold_chain | 0.4 |
| provider_switch | P-n76-k4 | atm > cargo > grocery > cold_chain | atm > grocery > cargo > cold_chain | 0.8 |
| scenario_reduction_limit_60 | X-n106-k14 | grocery > cold_chain > atm > cargo | grocery > atm > cold_chain > cargo | 0.8 |
| scenario_reduction_limit_60 | X-n120-k6 | cold_chain > cargo > grocery > atm | cold_chain > grocery > cargo > atm | 0.8 |
| scenario_reduction_limit_60 | X-n143-k7 | atm > grocery > cargo > cold_chain | atm > cargo > grocery > cold_chain | 0.8 |
| scenario_reduction_limit_60 | X-n157-k13 | atm > grocery > cargo > cold_chain | cargo > atm > cold_chain > grocery | 0 |
| scenario_reduction_limit_60 | X-n214-k11 | atm > grocery > cargo > cold_chain | atm > cargo > grocery > cold_chain | 0.8 |
| scenario_reduction_limit_60 | X-n237-k14 | cargo > atm > grocery > cold_chain | cargo > cold_chain > atm > grocery | 0.4 |
| scenario_reduction_limit_60 | X-n261-k13 | atm > cargo > grocery > cold_chain | cargo > atm > grocery > cold_chain | 0.8 |
| scenario_reduction_limit_60 | X-n284-k15 | atm > cargo > grocery > cold_chain | cargo > atm > grocery > cold_chain | 0.8 |

## Safe / Unstable Threshold Decision

Full confirmation is required for at least one row in: provider_switch, scenario_reduction_limit_60. A row becomes unsafe when stockout drift exceeds 5.0%, mean_total_cost drift exceeds 5.0%, ranking flips, or feasibility changes.

## Perturbation Interface

Small perturbation runs should be passed through `--comparison NAME,BASE_LABEL,BASE_CSV,CANDIDATE_LABEL,CANDIDATE_CSV`. The CSVs must use the `run_domain_engine` schema: `instance`, `domain`, `feasible`, `stockout_rate`, and `mean_total_cost`.

This smoke run does not claim perturbation stability unless a perturbation comparison is supplied. It only proves the tolerance judge can score fast/full and provider changes with one common rule set.

## Correct Sentence

In this smoke run, safe comparisons: none; comparisons requiring full confirmation: provider_switch, scenario_reduction_limit_60. Ranking flips were observed.

## Not Yet Correct Sentence

Domain adapters are stable under every solver, scenario, provider, and perturbation choice.

## Next Step

Each feature branch should write its own final domain result CSV and feed it into this tolerance judge. Decision-driving README numbers should be backed by a safe row set or by a full-scenario confirmation.
