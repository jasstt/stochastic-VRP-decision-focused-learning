# Robust Route Score Metric Sensitivity

## Purpose

This diagnostic reuses the same candidate result table and changes only the winner score metric.
It does not rerun routing or LP solves; it asks whether the winner decision is dominated by the chosen objective column.

## Metric Summary

| Metric | Winner Rows | Winner Instances | Unique Winning Route Plans | Unique Winning Candidates | Instances With Domain-Specific Route Choice | Share Domain-Specific Instances | Mean Unique Route Plans Across Domains | Max Unique Route Plans Across Domains | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Top Candidate | Top Candidate Share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cvar90_total_cost | 112 | 28 | 4 | 4 | 1 | 0.0357143 | 1.03571 | 2 | nominal_or_tools | 103 | 0.919643 | ortools:nominal_or_tools | 0.919643 |
| mean_domain_loss | 112 | 28 | 7 | 7 | 7 | 0.25 | 1.39286 | 4 | nominal_or_tools | 60 | 0.535714 | ortools:nominal_or_tools | 0.535714 |
| mean_shortfall | 112 | 28 | 7 | 7 | 5 | 0.178571 | 1.21429 | 3 | nominal_or_tools | 67 | 0.598214 | ortools:nominal_or_tools | 0.598214 |
| mean_total_cost | 112 | 28 | 3 | 3 | 0 | 0 | 1 | 1 | nominal_or_tools | 104 | 0.928571 | ortools:nominal_or_tools | 0.928571 |
| p90_total_cost | 112 | 28 | 3 | 3 | 0 | 0 | 1 | 1 | nominal_or_tools | 104 | 0.928571 | ortools:nominal_or_tools | 0.928571 |
| stockout_rate | 112 | 28 | 6 | 6 | 6 | 0.214286 | 1.21429 | 2 | nominal_or_tools | 69 | 0.616071 | ortools:nominal_or_tools | 0.616071 |

## Route Plan Frequency By Domain

| Metric | Domain | Route Plan | Winner Count | Domain Winner Rows | Winner Share Within Domain |
| --- | --- | --- | --- | --- | --- |
| cvar90_total_cost | atm | nominal_or_tools | 25 | 28 | 0.892857 |
| cvar90_total_cost | atm | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | atm | quantile_p75_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | atm | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | cargo | nominal_or_tools | 26 | 28 | 0.928571 |
| cvar90_total_cost | cargo | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | cargo | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | cold_chain | nominal_or_tools | 26 | 28 | 0.928571 |
| cvar90_total_cost | cold_chain | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | cold_chain | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | grocery | nominal_or_tools | 26 | 28 | 0.928571 |
| cvar90_total_cost | grocery | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| cvar90_total_cost | grocery | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | atm | nominal_or_tools | 14 | 28 | 0.5 |
| mean_domain_loss | atm | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| mean_domain_loss | atm | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_domain_loss | atm | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_domain_loss | atm | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_domain_loss | atm | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | cargo | nominal_or_tools | 14 | 28 | 0.5 |
| mean_domain_loss | cargo | robust_mean_1std_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_domain_loss | cargo | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_domain_loss | cargo | quantile_p75_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_domain_loss | cargo | robust_mean_2std_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_domain_loss | cargo | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | cold_chain | nominal_or_tools | 16 | 28 | 0.571429 |
| mean_domain_loss | cold_chain | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_domain_loss | cold_chain | quantile_p75_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_domain_loss | cold_chain | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_domain_loss | cold_chain | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | cold_chain | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | cold_chain | robust_mean_1std_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_domain_loss | grocery | nominal_or_tools | 16 | 28 | 0.571429 |
| mean_domain_loss | grocery | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_domain_loss | grocery | quantile_p75_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_domain_loss | grocery | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_domain_loss | grocery | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | atm | nominal_or_tools | 17 | 28 | 0.607143 |
| mean_shortfall | atm | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_shortfall | atm | quantile_p75_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_shortfall | atm | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | atm | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | atm | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | cargo | nominal_or_tools | 17 | 28 | 0.607143 |
| mean_shortfall | cargo | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_shortfall | cargo | quantile_p75_scaled_or_tools | 3 | 28 | 0.107143 |
| mean_shortfall | cargo | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | cargo | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | cargo | robust_mean_2std_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | cold_chain | nominal_or_tools | 17 | 28 | 0.607143 |
| mean_shortfall | cold_chain | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_shortfall | cold_chain | quantile_p75_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | cold_chain | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | cold_chain | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | cold_chain | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | cold_chain | robust_mean_1std_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_shortfall | grocery | nominal_or_tools | 16 | 28 | 0.571429 |
| mean_shortfall | grocery | proxy_mean_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_shortfall | grocery | quantile_p75_scaled_or_tools | 4 | 28 | 0.142857 |
| mean_shortfall | grocery | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_shortfall | grocery | robust_mean_2std_scaled_or_tools | 2 | 28 | 0.0714286 |
| mean_total_cost | atm | nominal_or_tools | 26 | 28 | 0.928571 |
| mean_total_cost | atm | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | atm | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | cargo | nominal_or_tools | 26 | 28 | 0.928571 |
| mean_total_cost | cargo | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | cargo | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | cold_chain | nominal_or_tools | 26 | 28 | 0.928571 |
| mean_total_cost | cold_chain | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | cold_chain | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | grocery | nominal_or_tools | 26 | 28 | 0.928571 |
| mean_total_cost | grocery | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| mean_total_cost | grocery | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | atm | nominal_or_tools | 26 | 28 | 0.928571 |
| p90_total_cost | atm | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | atm | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | cargo | nominal_or_tools | 26 | 28 | 0.928571 |
| p90_total_cost | cargo | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | cargo | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | cold_chain | nominal_or_tools | 26 | 28 | 0.928571 |
| p90_total_cost | cold_chain | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | cold_chain | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | grocery | nominal_or_tools | 26 | 28 | 0.928571 |
| p90_total_cost | grocery | proxy_mean_scaled_or_tools | 1 | 28 | 0.0357143 |
| p90_total_cost | grocery | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | atm | nominal_or_tools | 17 | 28 | 0.607143 |
| stockout_rate | atm | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| stockout_rate | atm | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| stockout_rate | atm | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | atm | quantile_p90_scaled_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | atm | robust_mean_1std_scaled_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | cargo | nominal_or_tools | 17 | 28 | 0.607143 |
| stockout_rate | cargo | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| stockout_rate | cargo | proxy_mean_scaled_or_tools | 2 | 28 | 0.0714286 |
| stockout_rate | cargo | quantile_p90_scaled_or_tools | 2 | 28 | 0.0714286 |
| stockout_rate | cargo | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| stockout_rate | cold_chain | nominal_or_tools | 17 | 28 | 0.607143 |
| stockout_rate | cold_chain | quantile_p75_scaled_or_tools | 6 | 28 | 0.214286 |
| stockout_rate | cold_chain | proxy_mean_scaled_or_tools | 2 | 28 | 0.0714286 |
| stockout_rate | cold_chain | robust_mean_1std_scaled_or_tools | 2 | 28 | 0.0714286 |
| stockout_rate | cold_chain | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | grocery | nominal_or_tools | 18 | 28 | 0.642857 |
| stockout_rate | grocery | quantile_p75_scaled_or_tools | 5 | 28 | 0.178571 |
| stockout_rate | grocery | proxy_mean_scaled_or_tools | 3 | 28 | 0.107143 |
| stockout_rate | grocery | proxy_mean_or_tools | 1 | 28 | 0.0357143 |
| stockout_rate | grocery | robust_mean_1std_scaled_or_tools | 1 | 28 | 0.0357143 |

## Instance Diversity

| Metric | Instance | Domains | Unique Route Plans Across Domains | Unique Candidates Across Domains | All Domains Same Route Plan | Route Plans |
| --- | --- | --- | --- | --- | --- | --- |
| cvar90_total_cost | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n110-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n129-k18 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n134-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n143-k7 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n190-k8 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n209-k16 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n214-k11 | 4 | 1 | 1 | yes | atm:quantile_p90_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:quantile_p90_scaled_or_tools | grocery:quantile_p90_scaled_or_tools |
| cvar90_total_cost | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n223-k34 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n228-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n233-k16 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| cvar90_total_cost | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n242-k48 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n261-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n280-k17 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| cvar90_total_cost | X-n284-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n110-k13 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_domain_loss | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n129-k18 | 4 | 1 | 1 | yes | atm:robust_mean_2std_scaled_or_tools | cargo:robust_mean_2std_scaled_or_tools | cold_chain:robust_mean_2std_scaled_or_tools | grocery:robust_mean_2std_scaled_or_tools |
| mean_domain_loss | X-n134-k13 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n143-k7 | 4 | 4 | 4 | no | atm:quantile_p90_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:proxy_mean_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_domain_loss | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n190-k8 | 4 | 2 | 2 | no | atm:robust_mean_1std_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:quantile_p90_scaled_or_tools | grocery:robust_mean_1std_scaled_or_tools |
| mean_domain_loss | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n209-k16 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_domain_loss | X-n214-k11 | 4 | 3 | 3 | no | atm:quantile_p75_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n223-k34 | 4 | 1 | 1 | yes | atm:robust_mean_1std_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:robust_mean_1std_scaled_or_tools | grocery:robust_mean_1std_scaled_or_tools |
| mean_domain_loss | X-n228-k23 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_domain_loss | X-n233-k16 | 4 | 2 | 2 | no | atm:proxy_mean_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_domain_loss | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n242-k48 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_domain_loss | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n261-k13 | 4 | 3 | 3 | no | atm:quantile_p75_scaled_or_tools | cargo:robust_mean_2std_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_domain_loss | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_domain_loss | X-n280-k17 | 4 | 2 | 2 | no | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:nominal_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_domain_loss | X-n284-k15 | 4 | 1 | 1 | yes | atm:robust_mean_2std_scaled_or_tools | cargo:robust_mean_2std_scaled_or_tools | cold_chain:robust_mean_2std_scaled_or_tools | grocery:robust_mean_2std_scaled_or_tools |
| mean_shortfall | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n110-k13 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_shortfall | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n129-k18 | 4 | 1 | 1 | yes | atm:robust_mean_2std_scaled_or_tools | cargo:robust_mean_2std_scaled_or_tools | cold_chain:robust_mean_2std_scaled_or_tools | grocery:robust_mean_2std_scaled_or_tools |
| mean_shortfall | X-n134-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n143-k7 | 4 | 3 | 3 | no | atm:proxy_mean_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_shortfall | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n190-k8 | 4 | 2 | 2 | no | atm:robust_mean_1std_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:quantile_p90_scaled_or_tools | grocery:robust_mean_1std_scaled_or_tools |
| mean_shortfall | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n209-k16 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_shortfall | X-n214-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n223-k34 | 4 | 1 | 1 | yes | atm:robust_mean_1std_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:robust_mean_1std_scaled_or_tools | grocery:robust_mean_1std_scaled_or_tools |
| mean_shortfall | X-n228-k23 | 4 | 2 | 2 | no | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_shortfall | X-n233-k16 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_shortfall | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n242-k48 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_shortfall | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n261-k13 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| mean_shortfall | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_shortfall | X-n280-k17 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_shortfall | X-n284-k15 | 4 | 2 | 2 | no | atm:robust_mean_2std_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:robust_mean_2std_scaled_or_tools | grocery:robust_mean_2std_scaled_or_tools |
| mean_total_cost | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n110-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n129-k18 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n134-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n143-k7 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n190-k8 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n209-k16 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n214-k11 | 4 | 1 | 1 | yes | atm:quantile_p90_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:quantile_p90_scaled_or_tools | grocery:quantile_p90_scaled_or_tools |
| mean_total_cost | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n223-k34 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n228-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n233-k16 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| mean_total_cost | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n242-k48 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n261-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n280-k17 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| mean_total_cost | X-n284-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n110-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n129-k18 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n134-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n143-k7 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n190-k8 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n209-k16 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n214-k11 | 4 | 1 | 1 | yes | atm:quantile_p90_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:quantile_p90_scaled_or_tools | grocery:quantile_p90_scaled_or_tools |
| p90_total_cost | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n223-k34 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n228-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n233-k16 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| p90_total_cost | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n242-k48 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n261-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n280-k17 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| p90_total_cost | X-n284-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n106-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n110-k13 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| stockout_rate | X-n115-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n120-k6 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n129-k18 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| stockout_rate | X-n134-k13 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n139-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n143-k7 | 4 | 2 | 2 | no | atm:proxy_mean_or_tools | cargo:quantile_p90_scaled_or_tools | cold_chain:proxy_mean_or_tools | grocery:proxy_mean_or_tools |
| stockout_rate | X-n157-k13 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n162-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n167-k10 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n181-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n186-k15 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n190-k8 | 4 | 2 | 2 | no | atm:quantile_p90_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| stockout_rate | X-n204-k19 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n209-k16 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| stockout_rate | X-n214-k11 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n219-k73 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n223-k34 | 4 | 2 | 2 | no | atm:quantile_p75_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:robust_mean_1std_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| stockout_rate | X-n228-k23 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n233-k16 | 4 | 1 | 1 | yes | atm:proxy_mean_scaled_or_tools | cargo:proxy_mean_scaled_or_tools | cold_chain:proxy_mean_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| stockout_rate | X-n237-k14 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n242-k48 | 4 | 1 | 1 | yes | atm:quantile_p75_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:quantile_p75_scaled_or_tools |
| stockout_rate | X-n251-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n261-k13 | 4 | 2 | 2 | no | atm:proxy_mean_scaled_or_tools | cargo:quantile_p75_scaled_or_tools | cold_chain:quantile_p75_scaled_or_tools | grocery:proxy_mean_scaled_or_tools |
| stockout_rate | X-n275-k28 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n280-k17 | 4 | 1 | 1 | yes | atm:nominal_or_tools | cargo:nominal_or_tools | cold_chain:nominal_or_tools | grocery:nominal_or_tools |
| stockout_rate | X-n284-k15 | 4 | 1 | 1 | yes | atm:robust_mean_1std_scaled_or_tools | cargo:robust_mean_1std_scaled_or_tools | cold_chain:robust_mean_1std_scaled_or_tools | grocery:robust_mean_1std_scaled_or_tools |

## Interpretation Rule

- If `mean_total_cost` has low diversity but domain-loss metrics have higher diversity, route cost is dominating the default winner objective.
- Domain-specific route switching should be claimed only for the metric under which it is measured.
- This is a post-hoc diagnostic from feasible candidate rows, not a full-scenario certification by itself.
