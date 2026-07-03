# Benchmark Proxy VRP Track

This branch adds a separate benchmark-driven VRP track. It does not reuse the
original synthetic ATM generator.

## Data

Raw benchmark seed set:

- `benchmarks/cvrplib/raw/A-n32-k5.vrp`
- `benchmarks/cvrplib/raw/B-n31-k5.vrp`
- `benchmarks/cvrplib/raw/E-n13-k4.vrp`
- `benchmarks/cvrplib/raw/P-n19-k2.vrp`

Source and IDs are documented in `benchmarks/cvrplib/README.md`.

Generated proxy data:

- `benchmarks/proxy_cvrplib/<instance>/instance.json`
- `benchmarks/proxy_cvrplib/<instance>/proxy_demand_history.csv`
- `benchmarks/proxy_cvrplib/<instance>/proxy_saa_scenarios.npy`
- `benchmarks/proxy_cvrplib/<instance>/proxy_node_meta.csv`

The proxy generator uses only pre-optimization information:

- nominal CVRPLIB customer demand
- distance from depot
- common day-level shocks
- node-level lognormal demand noise

It is intentionally not tuned against SPO+, OR-Tools, or any baseline result.

## Reproduce

Build proxy datasets:

```bash
python -m benchmark_proxy_vrp.build_benchmark_dataset --days 365 --scenarios 200 --seed 42
```

Run OR-Tools baselines:

```bash
python -m benchmark_proxy_vrp.run_baselines --time-limit-sec 5 --lp-time-limit-sec 30
python -m benchmark_proxy_vrp.summarize_results
```

Output:

- `benchmarks/proxy_cvrplib/manifest.csv`
- `benchmarks/proxy_cvrplib/baseline_results.csv`
- `benchmarks/proxy_cvrplib/best_by_instance.csv`
- `benchmarks/proxy_cvrplib/method_summary.csv`

## Baselines

Current baseline plans:

- `nominal_or_tools`: route with original CVRPLIB nominal demand
- `proxy_mean_or_tools`: route with mean proxy demand
- `quantile_p75_or_tools`, `quantile_p90_or_tools`: route with proxy quantile demand
- `robust_mean_1std_or_tools`, `robust_mean_2std_or_tools`: route with mean plus uncertainty buffer
- `*_scaled_or_tools`: same target profile projected down to fleet capacity when raw target exceeds fleet capacity
- `stoch_lp_on_nominal_routes`: adapted stochastic loading LP on nominal OR-Tools routes
- `stoch_lp_on_proxy_mean_routes`: adapted stochastic loading LP on proxy-mean OR-Tools routes

Infeasible rows are kept in the result table. They are part of the result, not a
failure to hide: tight CVRPLIB capacities often cannot support high quantile or
robust buffers with the original fleet size.

## Metrics

Each feasible plan is tested on the same SAA scenarios:

- mean total cost
- p90 total cost
- mean shortfall
- p90 shortfall
- stockout rate
- mean overfill

Cost uses route cost plus proxy recourse terms:

```text
total = route_cost + 3.0 * shortfall + 0.15 * overfill
```

These are benchmark units, not real currency.

The stochastic loading LP is trained on `proxy_demand_history.csv` and evaluated
on `proxy_saa_scenarios.npy`, so the optimized load plan does not directly see
the evaluation scenarios.
