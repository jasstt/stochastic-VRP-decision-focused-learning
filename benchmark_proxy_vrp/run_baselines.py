from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .ortools_baselines import (
    add_capacity_projected_plans,
    build_plans,
    evaluate_fixed_load_plan,
    solve_cvrp_ortools,
    vehicle_count_from_name,
)
from .stochastic_loading import solve_stochastic_loading_lp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run benchmark proxy baselines.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--stockout-penalty", type=float, default=3.0)
    parser.add_argument("--overfill-cost", type=float, default=0.15)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    rows = []
    for instance_json in sorted(data_dir.glob("*/instance.json")):
        instance = load_instance_json(instance_json)
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_json.parent / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        scenarios = np.load(instance_json.parent / "proxy_saa_scenarios.npy")
        fleet_capacity = instance.capacity * vehicle_count_from_name(instance.name)

        plans = add_capacity_projected_plans(build_plans(history, nominal), fleet_capacity)
        route_solutions = {}
        for method, planned in plans.items():
            solution = solve_cvrp_ortools(
                instance,
                planned,
                method=method,
                time_limit_sec=args.time_limit_sec,
            )
            route_solutions[method] = solution
            base = {
                "instance": instance.name,
                "method": method,
                "feasible": solution.feasible,
                "route_cost": solution.route_cost,
                "routes_used": len(solution.routes),
                "runtime_sec": solution.runtime_sec,
                "reason": solution.reason,
                "planned_load_total": float(np.sum(planned)),
                "fleet_capacity": float(fleet_capacity),
            }
            if solution.feasible:
                metrics = evaluate_fixed_load_plan(
                    planned,
                    scenarios,
                    solution.route_cost,
                    stockout_penalty=args.stockout_penalty,
                    overfill_cost=args.overfill_cost,
                )
                base.update(metrics)
            rows.append(base)

        for anchor_name in ("nominal_or_tools", "proxy_mean_or_tools"):
            anchor = route_solutions.get(anchor_name)
            if anchor is None:
                continue
            method = f"stoch_lp_on_{anchor_name.replace('_or_tools', '')}_routes"
            loading = solve_stochastic_loading_lp(
                instance,
                anchor,
                history,
                method=method,
                stockout_penalty=args.stockout_penalty,
                overfill_cost=args.overfill_cost,
                time_limit_sec=args.lp_time_limit_sec,
            )
            base = {
                "instance": instance.name,
                "method": method,
                "feasible": loading.feasible,
                "route_cost": anchor.route_cost if anchor and anchor.feasible else np.nan,
                "routes_used": len(anchor.routes) if anchor and anchor.feasible else 0,
                "runtime_sec": (anchor.runtime_sec if anchor else 0.0) + loading.runtime_sec,
                "reason": loading.reason,
                "planned_load_total": float(np.sum(loading.loads)) if loading.feasible else np.nan,
                "fleet_capacity": float(fleet_capacity),
            }
            if loading.feasible:
                metrics = evaluate_fixed_load_plan(
                    loading.loads,
                    scenarios,
                    anchor.route_cost,
                    stockout_penalty=args.stockout_penalty,
                    overfill_cost=args.overfill_cost,
                )
                base.update(metrics)
                base["lp_objective_train"] = loading.objective_value
            rows.append(base)

    results = pd.DataFrame(rows)
    out_path = data_dir / "baseline_results.csv"
    results.to_csv(out_path, index=False)
    print(results.to_string(index=False))
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
