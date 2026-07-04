# Routing Dependency Audit

Scope: `benchmark_proxy_vrp/domain_adapters.py`, `benchmark_proxy_vrp/run_domain_engine.py`, and `benchmark_proxy_vrp/stochastic_engine.py`.

This audit was taken before introducing `RoutingSolutionProvider`.

## Direct OR-Tools Output Shape Dependencies

| File | Line | Dependency | OR-Tools-specific assumption |
|---|---:|---|---|
| `benchmark_proxy_vrp/domain_adapters.py` | 10 | `from .ortools_baselines import RouteSolution` | Domain layer imports the concrete OR-Tools wrapper output type instead of a solver-neutral route type. |
| `benchmark_proxy_vrp/domain_adapters.py` | 34 | `anchor_routes: RouteSolution` | `route_features()` is typed against the OR-Tools route wrapper. |
| `benchmark_proxy_vrp/domain_adapters.py` | 42 | `anchor_routes: RouteSolution` | `build_problem()` receives the OR-Tools route wrapper directly. |
| `benchmark_proxy_vrp/domain_adapters.py` | 47 | `anchor_routes.feasible` | Assumes the route object exposes a boolean `feasible` field. |
| `benchmark_proxy_vrp/domain_adapters.py` | 52 | `anchor_routes.method` | Assumes the route object has an OR-Tools baseline method string such as `proxy_mean_or_tools`. |
| `benchmark_proxy_vrp/domain_adapters.py` | 57 | `anchor_routes.route_cost` | Assumes the route object exposes a scalar total route cost named `route_cost`. |
| `benchmark_proxy_vrp/domain_adapters.py` | 147 | `anchor_routes: RouteSolution` | Route feature builder accepts the concrete OR-Tools wrapper type. |
| `benchmark_proxy_vrp/domain_adapters.py` | 158 | `anchor_routes.routes` | Assumes routes are a list of node-index lists, including depot at start/end. |
| `benchmark_proxy_vrp/domain_adapters.py` | 162 | `route[0]` | Assumes every route list is non-empty and starts at the depot node. |
| `benchmark_proxy_vrp/domain_adapters.py` | 164 | `route[1:]` | Assumes route order is the visit order and the final depot can be iterated like a normal node. |
| `benchmark_proxy_vrp/domain_adapters.py` | 201 | `anchor_routes: RouteSolution` | Route group extraction accepts the concrete OR-Tools wrapper type. |
| `benchmark_proxy_vrp/domain_adapters.py` | 205 | `anchor_routes.routes` | Assumes routes are node-index sequences compatible with CVRPLIB customer node ids. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 11 | `solve_cvrp_ortools` import | Domain runner is hard-wired to OR-Tools instead of selecting a routing provider. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 44 | `anchor_solution.feasible` | Assumes the selected route object uses the OR-Tools wrapper field name. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 60 | `anchor_routes=anchor_solution` | Passes the concrete OR-Tools wrapper into domain adapters. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 71 | `anchor_solution.method` | Assumes OR-Tools baseline method naming is available on the route object. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 72 | `anchor_solution.route_cost` | Assumes scalar total route cost field is named `route_cost`. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 74 | `anchor_solution.runtime_sec` | Assumes route object contains solver runtime under `runtime_sec`. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 90 | `solve_cvrp_ortools(...)` | Preferred anchor route is solved by OR-Tools directly. |
| `benchmark_proxy_vrp/run_domain_engine.py` | 98 | `solve_cvrp_ortools(...)` | Fallback anchor route is solved by OR-Tools directly. |

## Stochastic Engine

No OR-Tools-specific output format dependency was found in `benchmark_proxy_vrp/stochastic_engine.py`.

The engine consumes only solver-neutral fields already normalized by the caller:

- `FixedRouteProblem.route_groups`
- `FixedRouteProblem.route_capacity`
- `FixedRouteProblem.route_cost`
- scenario matrices and domain objective vectors

The only route-related assumption is structural, not OR-Tools-specific: `route_groups` must cover each customer exactly once.
