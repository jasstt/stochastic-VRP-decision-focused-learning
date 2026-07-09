# Robust Route Metric Comparison

## Scope

This compares first-class X40 robust-route-selection runs. Each run reran route-candidate scoring, LP allocation, and full-scenario winner confirmation under its own `--score-metric`.

## Comparison

| Score Metric | Run Directory | Attempted Instances | Candidate Rows | Candidate Feasible Rows | Winner Instances | Winner Rows | No-Winner Instances | No-Winner List | Domain-Specific Instances | Domain-Specific Share | Confirmed Winner Rows | Confirm Feasible Rows | Metric-Safe Rows | Strict-Safe Rows | Strict-Safe Rate | Fully Certified Instances | Certified Domain-Specific Instances | Certified Domain-Specific Share | Ranking Rows | Ranking Flip Instances | Ranking Flip Rate | Final Full Required Rows | Final Full Required Rate | Top Route Plan | Top Route Plan Count | Top Route Plan Share | Unique Winning Route Plans | Expected Domains |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean_total_cost | benchmarks\robust_route_selection_x40 | 40 | 1760 | 456 | 28 | 112 | 12 | X-n101-k25, X-n125-k30, X-n148-k46, X-n153-k22, X-n172-k51, X-n176-k26, X-n195-k51, X-n200-k36, X-n247-k50, X-n256-k16, X-n266-k58, X-n270-k35 | 0 | 0 | 112 | 112 | 112 | 68 | 0.607143 | 17 | 0 | 0 | 28 | 11 | 0.392857 | 44 | 0.392857 | nominal_or_tools | 104 | 0.928571 | 3 | 4 |
| mean_domain_loss | benchmarks\robust_route_selection_x40_mean_domain_loss | 40 | 1760 | 456 | 28 | 112 | 12 | X-n101-k25, X-n125-k30, X-n148-k46, X-n153-k22, X-n172-k51, X-n176-k26, X-n195-k51, X-n200-k36, X-n247-k50, X-n256-k16, X-n266-k58, X-n270-k35 | 7 | 0.25 | 112 | 112 | 112 | 56 | 0.5 | 14 | 5 | 0.357143 | 28 | 14 | 0.5 | 56 | 0.5 | nominal_or_tools | 60 | 0.535714 | 7 | 4 |
| stockout_rate | benchmarks\robust_route_selection_x40_stockout_rate | 40 | 1760 | 456 | 28 | 112 | 12 | X-n101-k25, X-n125-k30, X-n148-k46, X-n153-k22, X-n172-k51, X-n176-k26, X-n195-k51, X-n200-k36, X-n247-k50, X-n256-k16, X-n266-k58, X-n270-k35 | 6 | 0.214286 | 112 | 112 | 112 | 56 | 0.5 | 14 | 3 | 0.214286 | 28 | 14 | 0.5 | 56 | 0.5 | nominal_or_tools | 69 | 0.616071 | 6 | 4 |

## Certified Instance Diversity

| Score Metric | Instance | Winner Domains | Strict-Safe Domains | Fully Certified Instance | Winner Unique Route Plans | Certified Unique Route Plans | Winner Domain-Specific | Certified Domain-Specific |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean_total_cost | X-n106-k14 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n110-k13 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n115-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n120-k6 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n129-k18 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n134-k13 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n139-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n143-k7 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n157-k13 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n162-k11 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n167-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n181-k23 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n186-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n190-k8 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n204-k19 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n209-k16 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n214-k11 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n219-k73 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n223-k34 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n228-k23 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n233-k16 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n237-k14 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n242-k48 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n251-k28 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n261-k13 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n275-k28 | 4 | 0 | no | 1 | 0 | no | no |
| mean_total_cost | X-n280-k17 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_total_cost | X-n284-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n106-k14 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n110-k13 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n115-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n120-k6 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n129-k18 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n134-k13 | 4 | 4 | yes | 2 | 2 | yes | yes |
| mean_domain_loss | X-n139-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n143-k7 | 4 | 4 | yes | 4 | 4 | yes | yes |
| mean_domain_loss | X-n157-k13 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n162-k11 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n167-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n181-k23 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n186-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n190-k8 | 4 | 4 | yes | 2 | 2 | yes | yes |
| mean_domain_loss | X-n204-k19 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n209-k16 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n214-k11 | 4 | 4 | yes | 3 | 3 | yes | yes |
| mean_domain_loss | X-n219-k73 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n223-k34 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n228-k23 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n233-k16 | 4 | 4 | yes | 2 | 2 | yes | yes |
| mean_domain_loss | X-n237-k14 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n242-k48 | 4 | 4 | yes | 1 | 1 | no | no |
| mean_domain_loss | X-n251-k28 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n261-k13 | 4 | 0 | no | 3 | 0 | yes | no |
| mean_domain_loss | X-n275-k28 | 4 | 0 | no | 1 | 0 | no | no |
| mean_domain_loss | X-n280-k17 | 4 | 0 | no | 2 | 0 | yes | no |
| mean_domain_loss | X-n284-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n106-k14 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n110-k13 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n115-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n120-k6 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n129-k18 | 4 | 0 | no | 2 | 0 | yes | no |
| stockout_rate | X-n134-k13 | 4 | 4 | yes | 2 | 2 | yes | yes |
| stockout_rate | X-n139-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n143-k7 | 4 | 0 | no | 2 | 0 | yes | no |
| stockout_rate | X-n157-k13 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n162-k11 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n167-k10 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n181-k23 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n186-k15 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n190-k8 | 4 | 4 | yes | 2 | 2 | yes | yes |
| stockout_rate | X-n204-k19 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n209-k16 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n214-k11 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n219-k73 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n223-k34 | 4 | 0 | no | 2 | 0 | yes | no |
| stockout_rate | X-n228-k23 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n233-k16 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n237-k14 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n242-k48 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n251-k28 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n261-k13 | 4 | 4 | yes | 2 | 2 | yes | yes |
| stockout_rate | X-n275-k28 | 4 | 0 | no | 1 | 0 | no | no |
| stockout_rate | X-n280-k17 | 4 | 4 | yes | 1 | 1 | no | no |
| stockout_rate | X-n284-k15 | 4 | 4 | yes | 1 | 1 | no | no |

## Feasibility / Audit-Risk Coverage

| Score Metric | Risk Dimension | Risk Level | Candidate Rows | Candidate Feasible Rows | Winner Rows | Winner Instances | Domain-Specific Instances | Full Confirmation Rows | Strict-Safe Rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean_total_cost | Overall Audit Risk | high | 704 | 96 | 16 | 4 | 0 | 16 | 4 |
| mean_total_cost | Overall Audit Risk | medium | 1056 | 360 | 96 | 24 | 0 | 96 | 64 |
| mean_total_cost | Capacity Pressure Risk | high | 352 | 96 | 16 | 4 | 0 | 16 | 4 |
| mean_total_cost | Capacity Pressure Risk | medium | 1408 | 360 | 96 | 24 | 0 | 96 | 64 |
| mean_total_cost | Prev OR-Tools Anchor Feasible | False | 572 | 12 | 4 | 1 | 0 | 4 | 4 |
| mean_total_cost | Prev OR-Tools Anchor Feasible | True | 1188 | 444 | 108 | 27 | 0 | 108 | 64 |
| mean_domain_loss | Overall Audit Risk | high | 704 | 96 | 16 | 4 | 2 | 16 | 8 |
| mean_domain_loss | Overall Audit Risk | medium | 1056 | 360 | 96 | 24 | 5 | 96 | 48 |
| mean_domain_loss | Capacity Pressure Risk | high | 352 | 96 | 16 | 4 | 2 | 16 | 8 |
| mean_domain_loss | Capacity Pressure Risk | medium | 1408 | 360 | 96 | 24 | 5 | 96 | 48 |
| mean_domain_loss | Prev OR-Tools Anchor Feasible | False | 572 | 12 | 4 | 1 | 1 | 4 | 4 |
| mean_domain_loss | Prev OR-Tools Anchor Feasible | True | 1188 | 444 | 108 | 27 | 6 | 108 | 52 |
| stockout_rate | Overall Audit Risk | high | 704 | 96 | 16 | 4 | 0 | 16 | 4 |
| stockout_rate | Overall Audit Risk | medium | 1056 | 360 | 96 | 24 | 6 | 96 | 52 |
| stockout_rate | Capacity Pressure Risk | high | 352 | 96 | 16 | 4 | 0 | 16 | 4 |
| stockout_rate | Capacity Pressure Risk | medium | 1408 | 360 | 96 | 24 | 6 | 96 | 52 |
| stockout_rate | Prev OR-Tools Anchor Feasible | False | 572 | 12 | 4 | 1 | 0 | 4 | 4 |
| stockout_rate | Prev OR-Tools Anchor Feasible | True | 1188 | 444 | 108 | 27 | 6 | 108 | 52 |

## Interpretation Rule

- `Domain-Specific Instances` counts full-confirmed winner-producing instances where domains selected more than one route plan.
- `Certified Domain-Specific Instances` is stricter: all expected domains in that instance must be `Strict Stability Safe`, and the certified route plans must still differ.
- `Metric-Safe Rows` alone are not decision-ready if stockout ranking flips; use `Strict-Safe Rows` for final claims.
- These runs are OR-Tools-only and proxy-demand benchmark runs; they do not establish solver-agnostic or real-sector demand claims.
