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

Build the same proxy datasets with OSRM road-time costs instead of CVRPLIB
Euclidean/explicit edge costs:

```bash
python -m benchmark_proxy_vrp.build_benchmark_dataset \
  --out-dir benchmarks/proxy_cvrplib_osrm \
  --distance-source osrm \
  --osrm-cost-unit duration_minutes \
  --osrm-coordinate-mode scale-to-bbox \
  --days 365 \
  --scenarios 200 \
  --seed 42
```

For real geocoded data, use `--osrm-coordinate-mode lonlat`. For CVRPLIB
instances, `scale-to-bbox` maps benchmark x/y coordinates into a real bounding
box before querying OSRM. The default bbox is a dense Berlin road-network area;
override `--osrm-bbox min_lon,min_lat,max_lon,max_lat` for another city. This
preserves the benchmark layout but should be treated as a road-network proxy,
not real customer geography. Instances without coordinates cannot be queried in
OSRM; by default they fall back to the original CVRPLIB matrix and are marked
with `distance_matrix_source=cvrplib:no_coordinates`.

By default, proxy demand features are generated from the original CVRPLIB matrix
(`--proxy-feature-source cvrplib`). That keeps demand history fixed when testing
multiple OSRM bounding boxes, so city/bbox sensitivity measures the road matrix
effect instead of mixing route-cost and demand-generation effects. Use
`--proxy-feature-source active-distance` only when you intentionally want the
proxy demand model to use the currently selected distance matrix.

Run OR-Tools baselines:

```bash
python -m benchmark_proxy_vrp.run_baselines --time-limit-sec 5 --lp-time-limit-sec 30
python -m benchmark_proxy_vrp.summarize_results
```

Run the same baselines on the OSRM road-time dataset:

```bash
python -m benchmark_proxy_vrp.run_baselines \
  --data-dir benchmarks/proxy_cvrplib_osrm \
  --time-limit-sec 5 \
  --lp-time-limit-sec 30
python -m benchmark_proxy_vrp.summarize_results \
  --results benchmarks/proxy_cvrplib_osrm/baseline_results.csv
```

Run the common stochastic engine with domain adapters:

```bash
python -m benchmark_proxy_vrp.run_domain_engine --routing-provider ortools --time-limit-sec 2 --lp-time-limit-sec 30
python -m benchmark_proxy_vrp.summarize_domain_results
```

For fast diagnostic loops, keep routing unchanged but reduce only the LP
planning scenarios with a deterministic total-demand-stratified subset:

```bash
python -m benchmark_proxy_vrp.run_domain_engine \
  --routing-provider ortools \
  --time-limit-sec 2 \
  --lp-time-limit-sec 30 \
  --lp-planning-scenario-limit 60
```

The full planning history should still be used for final report runs unless a
scenario-reduction accuracy check is reported alongside the result.

Current X40 bias check:

- 9 OR-Tools-anchor-feasible X instances, balanced across small/medium/large.
- 36 domain rows comparing full X40 planning history against `limit=60`.
- Worst instance-level domain-max relative stockout drift: 1.88%.
- Instances exceeding the 5% drift threshold: 0/9.

Rule: `--lp-planning-scenario-limit 60` is acceptable for exploration, debug,
and hypothesis-screening runs. Final README/report numbers and decision-driving
comparisons should be confirmed with full planning history.

Benchmark LP backends and scenario reduction:

```bash
python -m benchmark_proxy_vrp.benchmark_lp_backends \
  --data-dir benchmarks/proxy_cvrplib \
  --max-instances 1 \
  --domains atm cold_chain \
  --lp-planning-scenario-limit 60
```

Run a solver robustness sweep across route providers, LP backends, time limits,
and scenario limits:

```bash
python -m benchmark_proxy_vrp.benchmark_solver_robustness \
  --data-dir benchmarks/proxy_cvrplib \
  --out-dir benchmarks/solver_robustness_benchmark_smoke \
  --max-instances 2 \
  --domains atm cold_chain \
  --routing-providers ortools vroom \
  --route-time-limits 2 \
  --lp-backends pulp_cbc ortools_glop ortools_pdlp \
  --lp-time-limits 10 \
  --lp-scenario-limits full 60
```

The configured baseline is OR-Tools + CBC + full planning history at the
largest supplied route/LP time limits. VROOM rows are reported as provider
failures if the local VROOM service is not reachable.

Run the same engine through VROOM in custom-matrix mode:

```bash
python -m benchmark_proxy_vrp.run_domain_engine \
  --routing-provider vroom \
  --vroom-url http://localhost:3000 \
  --time-limit-sec 5 \
  --lp-time-limit-sec 30 \
  --output benchmarks/proxy_cvrplib/domain_engine_results_vroom_provider.csv
```

Run the common stochastic engine on the OSRM road-time dataset:

```bash
python -m benchmark_proxy_vrp.run_domain_engine \
  --data-dir benchmarks/proxy_cvrplib_osrm \
  --time-limit-sec 5 \
  --lp-time-limit-sec 30
python -m benchmark_proxy_vrp.summarize_domain_results \
  --results benchmarks/proxy_cvrplib_osrm/domain_engine_results.csv
```

Output:

- `benchmarks/proxy_cvrplib/manifest.csv`
- `benchmarks/proxy_cvrplib/baseline_results.csv`
- `benchmarks/proxy_cvrplib/best_by_instance.csv`
- `benchmarks/proxy_cvrplib/method_summary.csv`
- `benchmarks/proxy_cvrplib/domain_engine_results.csv`
- `benchmarks/proxy_cvrplib/domain_summary.csv`
- `benchmarks/proxy_cvrplib/domain_best_by_instance.csv`
- `benchmarks/proxy_cvrplib_osrm/*` when the OSRM road-time track is built

## Baselines

Current baseline plans:

- `nominal_or_tools`: route with original CVRPLIB nominal demand
- `proxy_mean_or_tools`: route with mean proxy demand
- `quantile_p75_or_tools`, `quantile_p90_or_tools`: route with proxy quantile demand
- `robust_mean_1std_or_tools`, `robust_mean_2std_or_tools`: route with mean plus uncertainty buffer
- `*_scaled_or_tools`: same target profile projected down to fleet capacity when raw target exceeds fleet capacity
- `stoch_lp_on_nominal_routes`: adapted stochastic loading LP on nominal OR-Tools routes
- `stoch_lp_on_proxy_mean_routes`: adapted stochastic loading LP on proxy-mean OR-Tools routes

Domain adapters on the common engine:

- `atm`: high stockout penalty, low surplus cost, mild CVaR tail-risk term
- `grocery`: moderate missed-demand penalty, higher waste/overfill cost
- `cargo`: failed first-attempt/overflow penalty with stronger tail-risk focus
- `cold_chain`: perishable delivery with shortage, waste, and route-exposure load penalties

Infeasible rows are kept in the result table. They are part of the result, not a
failure to hide: tight CVRPLIB capacities often cannot support high quantile or
robust buffers with the original fleet size.

## Domain Adapter Contract

The extension point is `benchmark_proxy_vrp.domain_adapters.DomainAdapter`.
A new sector adapter should subclass it and implement:

```python
def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
    ...
```

The returned `DomainObjective` must provide customer-aligned vectors:

- `shortage_penalty`: cost of unmet demand by customer
- `surplus_penalty`: cost of over-supply/waste by customer
- `load_penalty`: optional deterministic cost for planned load, used when the
  sector has route-exposure or handling risk beyond demand uncertainty
- `risk_weight` and `cvar_alpha`: optional tail-risk aversion

The default `build_problem()` converts any feasible route solution into fixed
route groups and passes route-derived customer features into the adapter:

- `route_id`
- `route_position_rank`
- `route_size`
- `arrival_cost`
- `arrival_exposure_rank`

Most sectors only need to implement `objective()`. Override `route_features()`
or `build_problem()` only when a sector changes the structure of the problem.

Example:

```python
class ColdChainAdapter(DomainAdapter):
    def objective(self, node_meta, route_features):
        exposure = route_features["arrival_exposure_rank"].to_numpy(float)
        return DomainObjective(
            name="cold_chain",
            shortage_penalty=...,
            surplus_penalty=...,
            load_penalty=0.04 + 0.28 * exposure,
        )
```

This keeps the stochastic engine reusable while letting sectors define their
own penalty calibration and structural recourse terms.

## Adding a New Routing Provider

The extension point is `benchmark_proxy_vrp.routing_providers.RoutingSolutionProvider`.
A new routing engine must return the standard `RouteSet` object:

```python
@dataclass
class RouteSet:
    routes: list[list[int]]
    route_costs: list[float]
    total_cost: float
    vehicle_assignments: dict[int, int]
    feasible: bool
    solver_name: str
    raw_metadata: dict
```

Steps:

1. Inherit from `RoutingSolutionProvider`.
2. Implement `solve(nodes, demands, vehicle_capacity, num_vehicles, distance_matrix=None)`.
3. Return a `RouteSet`; do not leak solver-specific response shapes into domain adapters.
4. Implement `solver_name()`.
5. Add a `--routing-provider` option in `run_domain_engine.py`.
6. Run the OR-Tools-style regression check: direct solver vs provider wrapper must match feasibility and route cost for the smoke instances.

Examples:

- `benchmark_proxy_vrp/routing_providers/ortools_provider.py`
- `benchmark_proxy_vrp/routing_providers/vroom_provider.py`

## Metrics

Each feasible plan is tested on the same SAA scenarios:

- mean total cost
- p90 total cost
- mean shortfall
- p90 shortfall
- stockout rate
- mean overfill
- mean load-penalty loss, when a domain uses route-exposure load costs

Cost uses route cost plus proxy recourse terms:

```text
total = route_cost + 3.0 * shortfall + 0.15 * overfill
```

These are benchmark units, not real currency.

When `--distance-source osrm` is used, `route_cost` is the selected OSRM cost
unit, defaulting to road travel minutes. The instance JSON also stores raw OSRM
duration seconds and road-distance meters matrices.

The stochastic loading LP is trained on `proxy_demand_history.csv` and evaluated
on `proxy_saa_scenarios.npy`, so the optimized load plan does not directly see
the evaluation scenarios.
