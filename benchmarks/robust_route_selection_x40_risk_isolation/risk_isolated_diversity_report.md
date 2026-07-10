# Risk-Isolated Diversity Report

## Risk Groups

- `anchor_feasible_medium_risk`: `Prev OR-Tools Anchor Feasible == yes` and `Overall Audit Risk in {medium, low}`.
- `high_risk_or_anchor_infeasible`: all remaining instances.

## Diversity Split

| Score metric | Medium-risk subset certified diversity | High-risk subset certified diversity |
| --- | --- | --- |
| mean_domain_loss | 3 / 12 (X-n134-k13, X-n143-k7, X-n190-k8) | 2 / 2 (X-n214-k11, X-n233-k16) |
| stockout_rate | 3 / 13 (X-n134-k13, X-n190-k8, X-n261-k13) | 0 / 1 |

## Full Summary

| Score Metric | Risk Isolation Group | Instances | Winner Domain-Specific Instances | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity Share | Certified Domain-Specific Instance List |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mean_domain_loss | anchor_feasible_medium_risk | 24 | 5 | 12 | 3 | 0.25 | X-n134-k13, X-n143-k7, X-n190-k8 |
| mean_domain_loss | high_risk_or_anchor_infeasible | 4 | 2 | 2 | 2 | 1 | X-n214-k11, X-n233-k16 |
| mean_total_cost | anchor_feasible_medium_risk | 24 | 0 | 16 | 0 | 0 |  |
| mean_total_cost | high_risk_or_anchor_infeasible | 4 | 0 | 1 | 0 | 0 |  |
| stockout_rate | anchor_feasible_medium_risk | 24 | 6 | 13 | 3 | 0.230769 | X-n134-k13, X-n190-k8, X-n261-k13 |
| stockout_rate | high_risk_or_anchor_infeasible | 4 | 0 | 1 | 0 | 0 |  |

## Certified Domain-Specific Instances

| Score Metric | Instance | Risk Isolation Group | Certified Unique Route Plans | Overall Audit Risk | Prev OR-Tools Anchor Feasible |
| --- | --- | --- | --- | --- | --- |
| mean_domain_loss | X-n134-k13 | anchor_feasible_medium_risk | 2 | medium | yes |
| mean_domain_loss | X-n143-k7 | anchor_feasible_medium_risk | 4 | medium | yes |
| mean_domain_loss | X-n190-k8 | anchor_feasible_medium_risk | 2 | medium | yes |
| mean_domain_loss | X-n214-k11 | high_risk_or_anchor_infeasible | 3 | high | yes |
| mean_domain_loss | X-n233-k16 | high_risk_or_anchor_infeasible | 2 | high | no |
| stockout_rate | X-n134-k13 | anchor_feasible_medium_risk | 2 | medium | yes |
| stockout_rate | X-n190-k8 | anchor_feasible_medium_risk | 2 | medium | yes |
| stockout_rate | X-n261-k13 | anchor_feasible_medium_risk | 2 | medium | yes |
