# VROOM Comparison Report

Status: completed with a caveat.

## VROOM Setup

The requested Docker Hub image did not exist:

```text
docker pull vroomvrp/vroom-docker
=> not found
```

The official GHCR image was used instead:

```text
docker pull ghcr.io/vroom-project/vroom-docker:v1.15.0
docker run -d --name benchmark-vroom -p 3000:3000 ghcr.io/vroom-project/vroom-docker:v1.15.0
```

Container status:

```text
Up / healthy on localhost:3000
```

The coordinate-only smoke test from the prompt failed:

```json
{"code":3,"error":"Failed to connect to 0.0.0.0:5000"}
```

Interpretation: the VROOM HTTP server is running, but coordinate requests need a routing backend. For this project we pass explicit CVRPLIB/OSRM cost matrices, so the custom-matrix VROOM test was used and passed:

```json
{"code":0,"summary":{"cost":20,"routes":1,"unassigned":0}}
```

No mock or fake VROOM output was used.

## Experiment

Dataset: `benchmarks/proxy_cvrplib`

Conditions:

- 4 CVRPLIB instances
- 4 domains: `atm`, `grocery`, `cargo`, `cold_chain`
- 2 routing providers: `ortools`, `vroom`
- Total: 32 domain-engine runs

Outputs:

- `benchmarks/proxy_cvrplib/domain_engine_results_ortools_provider.csv`
- `benchmarks/proxy_cvrplib/domain_engine_results_vroom_provider.csv`

## Domain Summary

| Domain | Provider | Feasible | Total Cost | Route Cost | Stockout | Load Penalty |
|---|---|---:|---:|---:|---:|---:|
| atm | OR-Tools | 4/4 | 1779.62 | 493.00 | 0.3060 | 0.00 |
| atm | VROOM | 4/4 | 1487.99 | 491.50 | 0.2886 | 0.00 |
| cargo | OR-Tools | 4/4 | 1445.07 | 493.00 | 0.3077 | 0.00 |
| cargo | VROOM | 4/4 | 1206.52 | 491.50 | 0.2868 | 0.00 |
| cold_chain | OR-Tools | 4/4 | 3177.75 | 493.00 | 0.3182 | 1000.67 |
| cold_chain | VROOM | 4/4 | 3279.49 | 491.50 | 0.2971 | 1131.99 |
| grocery | OR-Tools | 4/4 | 1595.08 | 493.00 | 0.3157 | 0.00 |
| grocery | VROOM | 4/4 | 1538.87 | 491.50 | 0.2978 | 0.00 |

## Feasibility Comparison

OR-Tools and VROOM were feasible on the same 16 instance-domain conditions.

No feasibility mismatch was observed.

## Cost Comparison

Route costs differ on `B-n31-k5` and route groupings differ on `E-n13-k4`, even when total route cost is the same. This is normal: OR-Tools and VROOM use different heuristics and can produce different feasible route decompositions.

The goal of this milestone is not to declare one routing engine better. The goal is to check whether the stochastic decision layer runs through the same interface over both engines.

## Critical Test: Stochastic Layer Motor Independence

What passed:

- The same `DomainAdapter` code ran on both providers.
- The same `StochasticDecisionEngine` code ran on both providers.
- All 32 runs completed without fallback or mocked output.
- `cold_chain` remained the only domain with nonzero load-penalty cost under both providers.
- `cold_chain` remained the most expensive domain under both providers.
- `cargo` remained the lowest average total-cost domain under both providers.

What did not fully pass:

- Domain stockout ranking was not identical.
- OR-Tools stockout order, high to low: `cold_chain > grocery > cargo > atm`.
- VROOM stockout order, high to low: `grocery > cold_chain > atm > cargo`.

Interpretation: the solver-agnostic interface is proven, and the stochastic layer is operational over both routing engines. Full behavior invariance is not proven, because route grouping changes can alter route-level capacity allocation and route-exposure features.

## Known Limitations

- VROOM coordinate mode failed because no routing backend was available at `0.0.0.0:5000`; this comparison used VROOM custom matrices.
- OR-Tools and VROOM may optimize different internal objectives and heuristics.
- Route-cost comparison is not a claim that one engine is better.
- Only 4 instances were tested; this is a presence/integration test, not statistical evidence.
- Time windows are still not modeled in route optimization.

## Conclusion

Correct claim:

> The stochastic decision layer can run through a formal provider interface on OR-Tools and VROOM, with identical feasibility coverage on the four-instance smoke set.

Not yet correct:

> The stochastic decision layer is behaviorally invariant to routing engine choice.
