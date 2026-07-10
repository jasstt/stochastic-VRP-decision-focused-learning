# Medium-Risk Candidate Pool and Tie-Breaker Report

## Scope

This test ran only on the `anchor_feasible_medium_risk` subset from X40:

- Instances: 24
- Provider: OR-Tools only
- Primary score metric: `mean_domain_loss`
- Base candidate plans: 11
- Added route variants: 5
- Added variant specs: `nominal_or_tools:101`, `nominal_or_tools:103`, `quantile_p75_scaled_or_tools:107`, `proxy_mean_scaled_or_tools:109`, `robust_mean_1std_scaled_or_tools:113`
- Variant mechanism: seeded search-cost perturbation. The installed OR-Tools build does not expose a native `random_seed` field, so this is a reproducible route-topology perturbation; reported route costs are still computed on the original distance matrix.

## Result Summary

| Test | Candidate rows | Candidate feasible rows | Winner domain-specific instances | Fully certified instances | Certified domain-specific instances | Ranking flip rate | Strict-safe rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Medium-risk baseline `mean_domain_loss` | 1056 | 360 | 5 / 24 | 12 | 3 | n/a here | n/a here |
| Seeded candidate pool, normal winner selection | 1536 | 700 | 6 / 24 | 10 | 0 | 12 / 24 | 45 / 96 |
| Seeded candidate pool + stockout-drift tie-breaker | 1536 | 700 | 20 / 24 | 13 | 10 | 11 / 24 | 52 / 96 |

## Interpretation

Candidate pool expansion alone did not solve stability. It increased route-plan variety and feasible candidates, but the normally selected seeded winners had zero certified domain-specific instances because the fully certified instances collapsed to common winners.

The stockout-drift tie-breaker changed the picture: it selected from 440 near-tied candidates after full confirmation and produced 10 certified domain-specific instances. This is the strongest signal so far that domain-specific route selection can survive outside fragile/high-risk instances.

The caution is still real: ranking flips remained in 11 / 24 instances. The tie-breaker improved strict-safe rows from 45 / 96 to 52 / 96, but it did not eliminate stability risk.

## Certified Domain-Specific Instances

| Instance | Certified unique route plans |
| --- | ---: |
| `X-n120-k6` | 4 |
| `X-n129-k18` | 3 |
| `X-n134-k13` | 3 |
| `X-n143-k7` | 4 |
| `X-n167-k10` | 2 |
| `X-n190-k8` | 3 |
| `X-n237-k14` | 3 |
| `X-n261-k13` | 3 |
| `X-n275-k28` | 3 |
| `X-n284-k15` | 3 |

## Decision

Risk isolation passed, and the medium-risk tie-breaker diagnostic is positive. The branch moves from `KISMEN/POSITIVE_DIAGNOSTIC` to `KISMEN/STRONG_DIAGNOSTIC`: not PASS yet, because ranking stability is still imperfect and the tie-breaker currently requires full-confirming many near-tied candidates.

## Next Step

Turn the tie-breaker into a cheaper production-style gate:

1. Reduce the near-tie confirmation set, for example tolerance sweep `0.1%`, `0.5%`, `1.0%`.
2. Add a fast proxy for drift before full confirmation, so not all near-tied rows require full LP.
3. Re-run the best tolerance on all X40, still reporting high-risk and medium-risk separately.
