# Solver-Agnostic Milestone Report

## What Was Proven

- `RoutingSolutionProvider` and `RouteSet` were added as a formal routing-engine interface.
- `OrToolsProvider` wraps the existing OR-Tools logic without changing the direct solver's route cost on the 4 smoke instances.
- OR-Tools regression test: PASS.
- `VroomProvider` integrates with a real VROOM server in custom-matrix mode.
- The domain engine now supports `--routing-provider ortools` and `--routing-provider vroom`.
- 4 domains x 2 providers x 4 instances were executed: 32 runs.
- Feasibility matched across providers on all 16 instance-domain pairs.

## What Was Not Fully Proven

- VROOM coordinate mode did not pass because the Docker container had no routing backend at `0.0.0.0:5000`; the working integration uses custom matrices.
- Behavioral invariance is not fully proven: stockout ranking changed between OR-Tools and VROOM.
- Only 2 routing engines were tested.
- Instance count is still 4; there is no statistical power.
- Time windows are still not included in route optimization.

## Key Result

| Provider | Feasible domain runs | Avg route cost | Lowest avg total-cost domain | Highest avg total-cost domain |
|---|---:|---:|---|---|
| OR-Tools | 16/16 | 493.00 | cargo | cold_chain |
| VROOM | 16/16 | 491.50 | cargo | cold_chain |

The stochastic layer is operational over both engines, but route grouping differences affect downstream domain metrics.

## Correct Sentence

> Stochastic decision layer, iki farklı açık kaynak routing motoru (OR-Tools, VROOM) üzerinde formal bir arayüz aracılığıyla test edilmiş ve feasibility/çalışabilirlik açısından tutarlı davranış göstermiştir.

## Sentence That Is Not Yet Correct

> Bu, tamamen solver-agnostik, üretime hazır ve routing motorundan davranışsal olarak bağımsız bir altyapıdır.

## Next Step

Add a `RoutingSolutionProvider` regression suite that compares route coverage, route cost, and domain-metric ranking across at least 15-20 instances. Then add a third provider or a VROOM setup with a real routing backend for coordinate-mode validation.
