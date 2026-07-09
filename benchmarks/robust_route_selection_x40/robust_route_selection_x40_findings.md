# Robust Route Selection X40 Findings

## Scope

Bu kosu, `feature/robust-route-selection` branch'inde X40 dataset uzerinde OR-Tools-only route candidate pool'u test eder.

- Dataset: `benchmarks/proxy_cvrplib_x_v4`
- Instances attempted: 40
- Domains: atm, cargo, cold_chain, grocery
- Routing provider: OR-Tools only
- Candidate plans per instance: 11
- Fast screening: `--lp-planning-scenario-limit 60`
- Confirmation gate: winners rerun with full planning scenario history
- Default winner metric: `mean_total_cost`

## Task Breakdown

1. Main run: X40 OR-Tools-only robust route selection was run with fast LP screening and full-scenario confirmation for selected winners.
2. Metrics agent: aggregate summaries, winner diversity, certification rows, and final-full-required rows were generated.
3. Methodology agent: report-language guardrails were prepared so weak or negative signals are not overstated.
4. Feasibility agent: X40 capacity pressure and candidate feasibility risks were audited before interpreting winner diversity.
5. Score sensitivity: existing candidate results were re-ranked under alternative score metrics without rerunning LP solves.

## Main Result

The default `mean_total_cost` result is stable but not domain-diverse.

| Metric | Value |
| --- | ---: |
| Candidate rows | 1760 |
| Candidate feasible rows | 456 |
| Winner rows | 112 |
| Winner-producing instances | 28 / 40 |
| Full-confirmed winner rows | 112 / 112 |
| Metric-stability safe rows | 112 / 112 |
| Strict-stability safe rows | 68 / 112 |
| Final-full-required rows | 44 / 112 |
| Ranking flip rate | 39.3% |
| Max stockout relative drift | 2.04% |
| Max mean-total-cost relative drift | 1.20% |

Interpretation: fast screening was metric-stable for the selected winners, but 44 winner rows still require full-run caution because stockout ranking flipped. The strict certified rate is therefore 60.7%, not 100%.

## Domain Winner Diversity

Under the default `mean_total_cost` score, all four domains selected the same route plan in every winner-producing instance.

| Metric | Value |
| --- | ---: |
| Winner-producing instances | 28 |
| Instances with domain-specific route choice | 0 |
| Top route plan | `nominal_or_tools` |
| Top route plan share | 26 / 28 per domain |

This is a negative result for the strongest version of the claim. X40 does not show that the default objective produces sector-specific route switching.

## Score Metric Sensitivity

Changing only the winner score metric changes the picture:

| Score metric | Domain-specific instances | Share | Max route plans in one instance |
| --- | ---: | ---: | ---: |
| `mean_total_cost` | 0 / 28 | 0.0% | 1 |
| `p90_total_cost` | 0 / 28 | 0.0% | 1 |
| `cvar90_total_cost` | 1 / 28 | 3.6% | 2 |
| `mean_shortfall` | 5 / 28 | 17.9% | 3 |
| `stockout_rate` | 6 / 28 | 21.4% | 2 |
| `mean_domain_loss` | 7 / 28 | 25.0% | 4 |

Interpretation: route cost dominates the default objective. Domain-specific switching appears only when the selection metric is closer to domain loss or service-risk metrics. This is a useful signal, but it is post-hoc and not full-confirmed under those alternative metrics yet.

## Feasibility Notes

Twelve instances produced no winner rows:

`X-n101-k25`, `X-n125-k30`, `X-n148-k46`, `X-n153-k22`, `X-n172-k51`, `X-n176-k26`, `X-n195-k51`, `X-n200-k36`, `X-n247-k50`, `X-n256-k16`, `X-n266-k58`, `X-n270-k35`.

The feasibility audit shows high capacity pressure is expected in this X40 slice. Unscaled proxy/quantile/robust plans frequently fail deterministic capacity prechecks; this is not a domain-objective failure by itself. The scaled rescue plans matter: `X-n233-k16` and `X-n214-k11` produce winners through scaled plans even though nominal or high-pressure candidates are fragile.

## Correct Sentence

X40 OR-Tools-only results show that the robust-route-selection layer can certify stable winners after full-scenario confirmation, but under the default `mean_total_cost` score it does not produce domain-specific route switching; domain-aware switching appears only as a post-hoc signal when using domain-loss or stockout-focused metrics.

## Not Yet Correct Sentence

"The sector-specific stochastic model beats one-size-fits-all routing under the default X40 objective."

This is not supported. The default score selected the same route plan across all domains in every winner-producing instance.

## Next Step

Run a first-class alternative-objective experiment, not just post-hoc re-ranking:

1. Re-run X40 with `--score-metric mean_domain_loss --confirm-winners-full-scenario`.
2. Re-run X40 with `--score-metric stockout_rate --confirm-winners-full-scenario`.
3. Compare certified domain-specific diversity only on `Strict Stability Safe` rows.
4. If diversity survives certification, expand the candidate route pool with randomized OR-Tools seeds or VROOM as a separate provider-sensitivity branch.
