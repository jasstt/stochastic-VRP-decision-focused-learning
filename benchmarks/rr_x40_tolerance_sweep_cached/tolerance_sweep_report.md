# Tie-Breaker Tolerance Sweep Report

## Scope

- Run dir: `benchmarks/rr_x40_seeded_merged`
- Score metric: `mean_domain_loss`
- Tolerances: 0.001, 0.005
- Confirmation cache input: `benchmarks/rr_x40_tiebreaker_005/confirmation_cache.csv`
- Missing confirmation allowed: `False`

## Summary

| Tolerance | Near-tied Candidates | Full-LP Calls Required | New Full-LP Calls This Run | Full-Confirmed Rows | Winner Rows | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate | Strict-Safe Rows | Full-LP Call Reduction vs Max Tolerance | Selected Best Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.001 | 265 | 265 | 0 | 265 | 112 | 13 | 7 | 7 / 13 | 13 | 28 | 0.464286 | 56 | 0.450207 | no |
| 0.005 | 482 | 482 | 0 | 482 | 112 | 19 | 14 | 14 / 19 | 8 | 28 | 0.285714 | 78 | 0 | yes |

## Best Trade-Off

Selected tolerance: `0.005`.

Selection rule: keep at least 80% of the maximum certified domain-specific diversity, then minimize full-LP calls, then ranking flip rate.

## Risk Group Split

| Tolerance | Risk Group | Instances | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.001 | anchor_feasible_medium_risk | 24 | 12 | 6 | 6 / 12 | 10 | 24 | 0.416667 |
| 0.001 | high_risk_or_anchor_infeasible | 4 | 1 | 1 | 1 / 1 | 3 | 4 | 0.75 |
| 0.005 | anchor_feasible_medium_risk | 24 | 16 | 11 | 11 / 16 | 7 | 24 | 0.291667 |
| 0.005 | high_risk_or_anchor_infeasible | 4 | 3 | 3 | 3 / 3 | 1 | 4 | 0.25 |

## Interpretation

- `Full-LP Calls Required` is the scientific cost implied by the tolerance.
- `New Full-LP Calls This Run` can be lower when an existing confirmation cache is reused.
- A lower tolerance is only better if it preserves certified diversity and does not increase ranking flips.
