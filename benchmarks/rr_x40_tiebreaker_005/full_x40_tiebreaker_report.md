# Full X40 Tie-Breaker Report

## Selected Tolerance Result

| Tolerance | Near-tied Candidates | Full-LP Calls Required | New Full-LP Calls This Run | Full-Confirmed Rows | Winner Rows | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate | Strict-Safe Rows | Full-LP Call Reduction vs Max Tolerance | Selected Best Tradeoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.005 | 482 | 482 | 161 | 482 | 112 | 19 | 14 | 14 / 19 | 8 | 28 | 0.285714 | 78 | 0 | yes |

## Risk Group Result

| Tolerance | Risk Group | Instances | Fully Certified Instances | Certified Domain-Specific Instances | Certified Diversity | Ranking Flips | Ranking Rows | Flip Rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.005 | anchor_feasible_medium_risk | 24 | 16 | 11 | 11 / 16 | 7 | 24 | 0.291667 |
| 0.005 | high_risk_or_anchor_infeasible | 4 | 3 | 3 | 3 / 3 | 1 | 4 | 0.25 |

## Cost Context

| Tolerance | Near-tied Candidates |
| --- | ---: |
| 0.1% | 265 |
| 0.5% | 482 |
| 1.0% | 607 |

The selected 0.5% tolerance reduces the implied full-LP confirmation set by 20.6% versus 1.0% tolerance (482 vs 607 rows). This run needed only 161 new full-LP calls because the 321 medium-risk rows were served from the existing confirmation cache.

## Decision

The full X40 result supports upgrading the branch to `NEAR_PASS/CONFIRMATION_HEAVY`: certified diversity increased and ranking flips dropped, but the fast drift proxy failed and full-LP confirmation remains mandatory.
