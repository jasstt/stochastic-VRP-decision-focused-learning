# Tie-Breaker Tolerance Sweep Report

## Scope

- Run dir: `benchmarks/robust_route_selection_medium_risk_seeded_mean_domain_loss`
- Score metric: `mean_domain_loss`
- Tolerances: 0.001, 0.005, 0.01
- Confirmation cache input: `benchmarks/robust_route_selection_medium_risk_seeded_tiebreaker/near_tied_candidate_full_confirmation.csv`
- Missing confirmation allowed: `False`

## Summary

| Tolerance | Near-tied Candidates | Full-LP Calls Required | New Full-LP Calls This Run | Full-Confirmed Rows | Winner Rows | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate | Strict-Safe Rows | Full-LP Call Reduction vs Max Tolerance | Selected Best Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.001 | 164 | 164 | 0 | 164 | 96 | 12 | 6 | 6 / 12 | 10 | 24 | 0.416667 | 52 | 0.627273 | no |
| 0.005 | 321 | 321 | 0 | 321 | 96 | 16 | 11 | 11 / 16 | 7 | 24 | 0.291667 | 66 | 0.270455 | yes |
| 0.01 | 440 | 440 | 0 | 440 | 96 | 13 | 10 | 10 / 13 | 11 | 24 | 0.458333 | 52 | 0 | no |

## Best Trade-Off

Selected tolerance: `0.005`.

Selection rule: keep at least 80% of the maximum certified domain-specific diversity, then minimize full-LP calls, then ranking flip rate.

## Risk Group Split

| Tolerance | Risk Group | Instances | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.001 | anchor_feasible_medium_risk | 24 | 12 | 6 | 6 / 12 | 10 | 24 | 0.416667 |
| 0.001 | high_risk_or_anchor_infeasible | 0 | 0 | 0 | 0 / 0 | 0 | 0 |  |
| 0.005 | anchor_feasible_medium_risk | 24 | 16 | 11 | 11 / 16 | 7 | 24 | 0.291667 |
| 0.005 | high_risk_or_anchor_infeasible | 0 | 0 | 0 | 0 / 0 | 0 | 0 |  |
| 0.01 | anchor_feasible_medium_risk | 24 | 13 | 10 | 10 / 13 | 11 | 24 | 0.458333 |
| 0.01 | high_risk_or_anchor_infeasible | 0 | 0 | 0 | 0 / 0 | 0 | 0 |  |

## Interpretation

- `Full-LP Calls Required` is the scientific cost implied by the tolerance.
- `New Full-LP Calls This Run` can be lower when an existing confirmation cache is reused.
- A lower tolerance is only better if it preserves certified diversity and does not increase ranking flips.
