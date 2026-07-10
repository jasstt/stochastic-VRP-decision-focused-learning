# Robust Route Metric Comparison

## Scope

This compares first-class X40 robust-route-selection runs. Each run reran route-candidate scoring, LP allocation, and full-scenario winner confirmation under its own `--score-metric`.

## Comparison

| Score Metric | Run Directory | Attempted Instances | Candidate Rows | Candidate Feasible Rows | Winner Instances | Winner Rows | No-Winner Instances | No-Winner List | Domain-Specific Instances | Domain-Specific Share | Confirmed Winner Rows | Confirm Feasible Rows | Metric-Safe Rows | Strict-Safe Rows | Strict-Safe Rate | Fully Certified Instances | Certified Domain-Specific Instances | Certified Domain-Specific Share | Ranking Rows | Ranking Flip Instances | Ranking Flip Rate | Final Full Required Rows | Final Full Required Rate | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Unique Winning Route Plans | Expected Domains |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seeded_mean_domain_loss | benchmarks\robust_route_selection_medium_risk_seeded_mean_domain_loss | 24 | 1536 | 700 | 24 | 96 | 0 |  | 6 | 0.25 | 96 | 96 | 86 | 45 | 0.46875 | 10 | 0 | 0 | 24 | 12 | 0.5 | 51 | 0.53125 | nominal_seed101_or_tools | 15 | 0.15625 | 11 | 4 |

## Certified Instance Diversity

| Score Metric | Instance | Winner Domains | Strict-Safe Domains | Fully Certified Instance | Winner Unique Route Plans | Certified Unique Route Plans | Winner Domain-Specific | Certified Domain-Specific |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seeded_mean_domain_loss | X-n106-k14 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n110-k13 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n115-k10 | 4 | 2 | no | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n120-k6 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n129-k18 | 4 | 0 | no | 2 | 0 | yes | no |
| seeded_mean_domain_loss | X-n134-k13 | 4 | 3 | no | 4 | 3 | yes | no |
| seeded_mean_domain_loss | X-n139-k10 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n143-k7 | 4 | 0 | no | 4 | 0 | yes | no |
| seeded_mean_domain_loss | X-n162-k11 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n167-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n181-k23 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n186-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n190-k8 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n204-k19 | 4 | 0 | no | 2 | 0 | yes | no |
| seeded_mean_domain_loss | X-n209-k16 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n223-k34 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n228-k23 | 4 | 0 | no | 1 | 0 | no | no |
| seeded_mean_domain_loss | X-n237-k14 | 4 | 0 | no | 2 | 0 | yes | no |
| seeded_mean_domain_loss | X-n242-k48 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n251-k28 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n261-k13 | 4 | 0 | no | 4 | 0 | yes | no |
| seeded_mean_domain_loss | X-n275-k28 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n280-k17 | 4 | 4 | yes | 1 | 1 | no | no |
| seeded_mean_domain_loss | X-n284-k15 | 4 | 4 | yes | 1 | 1 | no | no |

## Feasibility / Audit-Risk Coverage

| Score Metric | Risk Dimension | Risk Level | Candidate Rows | Candidate Feasible Rows | Winner Rows | Winner Instances | Domain-Specific Instances | Full Confirmation Rows | Strict-Safe Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seeded_mean_domain_loss | Overall Audit Risk | medium | 1536 | 700 | 96 | 24 | 6 | 96 | 45 |
| seeded_mean_domain_loss | Capacity Pressure Risk | medium | 1536 | 700 | 96 | 24 | 6 | 96 | 45 |
| seeded_mean_domain_loss | Prev OR-Tools Anchor Feasible | True | 1536 | 700 | 96 | 24 | 6 | 96 | 45 |

## Interpretation Rule

- `Domain-Specific Instances` counts full-confirmed winner-producing instances where domains selected more than one route plan.
- `Certified Domain-Specific Instances` is stricter: all expected domains in that instance must be `Strict Stability Safe`, and the certified route plans must still differ.
- `Metric-Safe Rows` alone are not decision-ready if stockout ranking flips; use `Strict-Safe Rows` for final claims.
- These runs are OR-Tools-only and proxy-demand benchmark runs; they do not establish solver-agnostic or real-sector demand claims.
