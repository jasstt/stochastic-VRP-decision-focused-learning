from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans, vehicle_count_from_name
from .routing_providers import OrToolsProvider, VroomProvider, instance_to_provider_inputs
from .routing_providers.base import RouteSet
from .stochastic_engine import StochasticDecisionEngine, evaluate_solution


def main() -> None:
    parser = argparse.ArgumentParser(description="Run common stochastic engine across domain adapters.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--routing-provider", choices=["ortools", "vroom"], default="ortools")
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--output", default=None)
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    args = parser.parse_args()

    engine = StochasticDecisionEngine()
    data_dir = Path(args.data_dir)
    rows = []
    for instance_json in sorted(data_dir.glob("*/instance.json")):
        instance = load_instance_json(instance_json)
        nominal, _ = customer_view(instance)
        instance_dir = instance_json.parent
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")

        plans = build_plans(history, nominal)
        anchor_solution = _solve_anchor(
            instance,
            plans,
            args.anchor_plan,
            args.fallback_anchor_plan,
            args.routing_provider,
            args.vroom_url,
            args.time_limit_sec,
        )
        if not anchor_solution.feasible:
            rows.append(
                {
                    "instance": instance.name,
                    "domain": "all",
                    "method": "domain_engine",
                    "feasible": False,
                    "solver_name": anchor_solution.solver_name,
                    "reason": "no_feasible_anchor_route",
                }
            )
            continue

        for domain_name in args.domains:
            adapter = get_adapter(domain_name)
            problem = adapter.build_problem(
                instance=instance,
                anchor_routes=anchor_solution,
                planning_scenarios=history,
                evaluation_scenarios=scenarios,
                node_meta=node_meta,
            )
            solution = engine.solve(problem, time_limit_sec=args.lp_time_limit_sec)
            row = {
                "instance": instance.name,
                "domain": domain_name,
                "method": solution.method,
                "feasible": solution.feasible,
                "solver_name": anchor_solution.solver_name,
                "anchor_method": anchor_solution.raw_metadata.get("method", anchor_solution.solver_name),
                "route_cost": anchor_solution.total_cost,
                "planned_load_total": float(np.sum(solution.loads)) if solution.feasible else np.nan,
                "runtime_sec": float(anchor_solution.raw_metadata.get("runtime_sec", 0.0)) + solution.runtime_sec,
                "reason": solution.reason,
                "objective_value_train": solution.objective_value,
            }
            if solution.feasible:
                row.update(evaluate_solution(problem, solution.loads))
            rows.append(row)

    results = pd.DataFrame(rows)
    out_path = Path(args.output) if args.output else data_dir / "domain_engine_results.csv"
    results.to_csv(out_path, index=False)
    print(results.to_string(index=False))
    print(f"\nSaved {out_path}")


def _solve_anchor(
    instance,
    plans,
    anchor_plan,
    fallback_anchor_plan,
    routing_provider,
    vroom_url,
    time_limit_sec,
) -> RouteSet:
    preferred = _solve_with_provider(
        instance,
        plans[anchor_plan],
        anchor_plan,
        routing_provider,
        vroom_url,
        time_limit_sec,
    )
    if preferred.feasible:
        return preferred
    return _solve_with_provider(
        instance,
        plans[fallback_anchor_plan],
        fallback_anchor_plan,
        routing_provider,
        vroom_url,
        time_limit_sec,
    )


def _solve_with_provider(
    instance,
    planned_customer_loads,
    method,
    routing_provider,
    vroom_url,
    time_limit_sec,
) -> RouteSet:
    provider = _make_provider(routing_provider, method, vroom_url, time_limit_sec)
    nodes, demands, distance_matrix = instance_to_provider_inputs(instance, planned_customer_loads)
    return provider.solve(
        nodes=nodes,
        demands=demands,
        vehicle_capacity=float(instance.capacity),
        num_vehicles=vehicle_count_from_name(instance.name),
        distance_matrix=distance_matrix,
    )


def _make_provider(routing_provider: str, method: str, vroom_url: str, time_limit_sec: int):
    if routing_provider == "ortools":
        return OrToolsProvider(method=method, time_limit_sec=time_limit_sec)
    if routing_provider == "vroom":
        return VroomProvider(vroom_url=vroom_url, method=method, timeout_sec=max(5, time_limit_sec + 5))
    raise ValueError(f"Unknown routing provider: {routing_provider}")


if __name__ == "__main__":
    main()
