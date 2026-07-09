from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import add_capacity_projected_plans, build_plans, vehicle_count_from_name
from .run_domain_engine import _solve_with_provider
from .scenario_reduction import scenario_reduction_summary, select_representative_scenarios
from .stochastic_engine import StochasticDecisionEngine, available_lp_backends, evaluate_solution


DEFAULT_PLAN_ORDER = [
    "nominal_or_tools",
    "proxy_mean_or_tools",
    "quantile_p75_or_tools",
    "quantile_p90_or_tools",
    "robust_mean_1std_or_tools",
    "robust_mean_2std_or_tools",
]

SCORE_METRICS = [
    "mean_total_cost",
    "cvar90_total_cost",
    "p90_total_cost",
    "stockout_rate",
    "mean_shortfall",
    "mean_domain_loss",
]


@dataclass(frozen=True)
class CandidateRoute:
    instance: str
    plan_name: str
    provider: str
    candidate_name: str
    planned_load_total: float
    planned_load_ratio: float
    feasible: bool
    route_count: int
    route_cost: float
    runtime_sec: float
    reason: str
    route_set: object | None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate multiple route candidates through the common stochastic decision layer."
    )
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--out-dir", default="benchmarks/robust_route_selection")
    parser.add_argument("--instances", nargs="+", default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-instances", type=int, default=None)
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--candidate-plans", nargs="+", default=None)
    parser.add_argument("--routing-providers", nargs="+", choices=["ortools", "vroom"], default=["ortools"])
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    parser.add_argument("--lp-backend", choices=available_lp_backends(), default="pulp_cbc")
    parser.add_argument(
        "--lp-planning-scenario-limit",
        type=int,
        default=60,
        help="Default fast mode. Use 0 or a negative value to keep the full planning history.",
    )
    parser.add_argument("--score-metric", choices=SCORE_METRICS, default="mean_total_cost")
    parser.add_argument(
        "--confirm-winners-full-scenario",
        action="store_true",
        help="Rerun only domain winners with the full planning history and report stability drift.",
    )
    parser.add_argument("--stability-stockout-rel-threshold", type=float, default=0.05)
    parser.add_argument("--stability-cost-rel-threshold", type=float, default=0.05)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidate_results, route_results = _run_selection(args, Path(args.data_dir))
    winners = _select_winners(candidate_results, args.score_metric)
    summary = _summarize(candidate_results, winners)
    full_confirmation = _confirm_winners_full_scenario(args, Path(args.data_dir), winners)
    ranking_stability = _winner_ranking_stability(full_confirmation)
    full_confirmation = _attach_stability_status(full_confirmation, ranking_stability)

    candidate_results.to_csv(out_dir / "robust_route_candidate_results.csv", index=False)
    route_results.to_csv(out_dir / "robust_route_candidates.csv", index=False)
    winners.to_csv(out_dir / "robust_route_winners.csv", index=False)
    summary.to_csv(out_dir / "robust_route_selection_summary.csv", index=False)
    full_confirmation.to_csv(out_dir / "robust_route_winner_full_confirmation.csv", index=False)
    ranking_stability.to_csv(out_dir / "robust_route_winner_ranking_stability.csv", index=False)
    _write_report(
        out_dir / "robust_route_selection_report.md",
        candidate_results=candidate_results,
        route_results=route_results,
        winners=winners,
        summary=summary,
        full_confirmation=full_confirmation,
        ranking_stability=ranking_stability,
        args=args,
    )

    print("Robust route selection summary")
    print(summary.to_string(index=False) if not summary.empty else "No summary rows.")
    print(f"\nSaved {out_dir / 'robust_route_selection_report.md'}")


def _run_selection(args: argparse.Namespace, data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    engine = StochasticDecisionEngine(lp_backend=args.lp_backend)
    candidate_rows: list[dict[str, object]] = []
    route_rows: list[dict[str, object]] = []
    instance_paths = _select_instance_paths(data_dir, args.instances, args.start_index, args.max_instances)

    for position, instance_json in enumerate(instance_paths, start=1):
        instance = load_instance_json(instance_json)
        instance_dir = instance_json.parent
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        lp_history = select_representative_scenarios(history, args.lp_planning_scenario_limit)
        lp_summary = scenario_reduction_summary(history, lp_history)
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")
        fleet_capacity = float(vehicle_count_from_name(instance.name) * instance.capacity)
        plans = add_capacity_projected_plans(build_plans(history, nominal), fleet_capacity=fleet_capacity)
        plan_names = _candidate_plan_names(plans, args.candidate_plans)

        print(
            f"[{position}/{len(instance_paths)}] {instance.name}: "
            f"{len(plan_names)} plans x {len(args.routing_providers)} providers",
            flush=True,
        )
        routes = _solve_candidate_routes(args, instance, plans, plan_names, fleet_capacity)
        route_rows.extend(_route_rows(instance, routes, lp_summary))

        for candidate in routes:
            for domain_name in args.domains:
                base_row = {
                    "Instance": instance.name,
                    "Customers": instance.n_customers,
                    "Domain": domain_name,
                    "Candidate": candidate.candidate_name,
                    "Route Plan": candidate.plan_name,
                    "Routing Provider": candidate.provider,
                    "Route Feasible": candidate.feasible,
                    "LP Feasible": False,
                    "Candidate Feasible": False,
                    "Route Count": candidate.route_count,
                    "Route Cost": candidate.route_cost,
                    "Route Runtime Sec": candidate.runtime_sec,
                    "LP Runtime Sec": np.nan,
                    "Total Runtime Sec": candidate.runtime_sec,
                    "Planned Route Load Total": candidate.planned_load_total,
                    "Planned Route Load Ratio": candidate.planned_load_ratio,
                    "LP Backend": args.lp_backend,
                    "Score Metric": args.score_metric,
                    "Score Value": np.nan,
                    "Reason": candidate.reason,
                    **lp_summary,
                }
                if not candidate.feasible or candidate.route_set is None:
                    candidate_rows.append(base_row)
                    continue

                adapter = get_adapter(domain_name)
                problem = adapter.build_problem(
                    instance=instance,
                    anchor_routes=candidate.route_set,
                    planning_scenarios=lp_history,
                    evaluation_scenarios=scenarios,
                    node_meta=node_meta,
                )
                solution = engine.solve(problem, time_limit_sec=args.lp_time_limit_sec)
                row = {
                    **base_row,
                    "LP Feasible": solution.feasible,
                    "Candidate Feasible": bool(solution.feasible),
                    "LP Runtime Sec": solution.runtime_sec,
                    "Total Runtime Sec": candidate.runtime_sec + solution.runtime_sec,
                    "Objective Value Train": solution.objective_value,
                    "Optimized Load Total": float(np.sum(solution.loads)) if solution.feasible else np.nan,
                    "Reason": solution.reason,
                }
                if solution.feasible:
                    metrics = evaluate_solution(problem, solution.loads)
                    row.update(metrics)
                    row["Score Value"] = metrics[args.score_metric]
                candidate_rows.append(row)
        print(f"[{position}/{len(instance_paths)}] {instance.name}: done", flush=True)

    return pd.DataFrame(candidate_rows), pd.DataFrame(route_rows)


def _select_instance_paths(
    data_dir: Path,
    names: list[str] | None,
    start_index: int,
    max_instances: int | None,
) -> list[Path]:
    if names:
        return [data_dir / name / "instance.json" for name in names]
    paths = sorted(data_dir.glob("*/instance.json"))
    if start_index:
        paths = paths[start_index:]
    if max_instances is not None:
        paths = paths[:max_instances]
    return paths


def _candidate_plan_names(plans: dict[str, np.ndarray], requested: list[str] | None) -> list[str]:
    if requested:
        missing = [name for name in requested if name not in plans]
        if missing:
            raise ValueError(f"Unknown candidate plans: {', '.join(missing)}")
        return requested
    ordered = [name for name in DEFAULT_PLAN_ORDER if name in plans]
    scaled = sorted(name for name in plans if name.endswith("_scaled_or_tools"))
    extras = sorted(name for name in plans if name not in set(ordered + scaled))
    return ordered + scaled + extras


def _solve_candidate_routes(
    args: argparse.Namespace,
    instance,
    plans: dict[str, np.ndarray],
    plan_names: list[str],
    fleet_capacity: float,
) -> list[CandidateRoute]:
    routes = []
    for provider in args.routing_providers:
        for plan_name in plan_names:
            planned_loads = plans[plan_name]
            candidate_name = f"{provider}:{plan_name}"
            planned_total = float(np.sum(planned_loads))
            try:
                route_set = _solve_with_provider(
                    instance=instance,
                    planned_customer_loads=planned_loads,
                    method=candidate_name,
                    routing_provider=provider,
                    vroom_url=args.vroom_url,
                    time_limit_sec=args.time_limit_sec,
                )
                reason = str(route_set.raw_metadata.get("reason", ""))
            except Exception as exc:  # VROOM can be optional in local smoke runs.
                route_set = None
                reason = f"route_solver_error:{type(exc).__name__}:{exc}"
            feasible = bool(route_set is not None and route_set.feasible)
            routes.append(
                CandidateRoute(
                    instance=instance.name,
                    plan_name=plan_name,
                    provider=provider,
                    candidate_name=candidate_name,
                    planned_load_total=planned_total,
                    planned_load_ratio=planned_total / fleet_capacity if fleet_capacity > 0 else np.nan,
                    feasible=feasible,
                    route_count=len(route_set.routes) if feasible and route_set is not None else 0,
                    route_cost=float(route_set.total_cost) if feasible and route_set is not None else np.nan,
                    runtime_sec=float(route_set.raw_metadata.get("runtime_sec", 0.0))
                    if route_set is not None
                    else 0.0,
                    reason=reason,
                    route_set=route_set if feasible else None,
                )
            )
    return routes


def _route_rows(instance, routes: list[CandidateRoute], lp_summary: dict[str, object]) -> list[dict[str, object]]:
    return [
        {
            "Instance": instance.name,
            "Customers": instance.n_customers,
            "Candidate": route.candidate_name,
            "Route Plan": route.plan_name,
            "Routing Provider": route.provider,
            "Route Feasible": route.feasible,
            "Route Count": route.route_count,
            "Route Cost": route.route_cost,
            "Route Runtime Sec": route.runtime_sec,
            "Planned Route Load Total": route.planned_load_total,
            "Planned Route Load Ratio": route.planned_load_ratio,
            "Reason": route.reason,
            **lp_summary,
        }
        for route in routes
    ]


def _select_winners(candidate_results: pd.DataFrame, score_metric: str) -> pd.DataFrame:
    if candidate_results.empty:
        return pd.DataFrame()
    feasible = candidate_results[candidate_results["Candidate Feasible"] == True].copy()
    if feasible.empty:
        return pd.DataFrame()
    winners = feasible.loc[feasible.groupby(["Instance", "Domain"])["Score Value"].idxmin()].copy()
    winners["Winner Rank Metric"] = score_metric
    return winners.sort_values(["Instance", "Domain"]).reset_index(drop=True)


def _summarize(candidate_results: pd.DataFrame, winners: pd.DataFrame) -> pd.DataFrame:
    if candidate_results.empty:
        return pd.DataFrame()
    coverage = (
        candidate_results.groupby(["Domain"], dropna=False)
        .agg(
            Candidate_Rows=("Candidate", "size"),
            Feasible_Rows=("Candidate Feasible", "sum"),
            Instances=("Instance", "nunique"),
            Candidates=("Candidate", "nunique"),
            Median_Total_Runtime_Sec=("Total Runtime Sec", "median"),
        )
        .reset_index()
    )
    if winners.empty:
        coverage["Winner_Rows"] = 0
        return coverage
    win_counts = (
        winners.groupby(["Domain", "Candidate", "Routing Provider", "Route Plan"], dropna=False)
        .size()
        .reset_index(name="Winner_Rows")
    )
    dominant = (
        win_counts.sort_values(["Domain", "Winner_Rows", "Candidate"], ascending=[True, False, True])
        .groupby("Domain", as_index=False)
        .first()
        .rename(
            columns={
                "Candidate": "Top_Winning_Candidate",
                "Routing Provider": "Top_Winning_Provider",
                "Route Plan": "Top_Winning_Route_Plan",
                "Winner_Rows": "Top_Winner_Count",
            }
        )
    )
    return coverage.merge(dominant, on="Domain", how="left")


def _confirm_winners_full_scenario(
    args: argparse.Namespace,
    data_dir: Path,
    winners: pd.DataFrame,
) -> pd.DataFrame:
    if not args.confirm_winners_full_scenario or winners.empty:
        return pd.DataFrame()

    engine = StochasticDecisionEngine(lp_backend=args.lp_backend)
    rows: list[dict[str, object]] = []
    for position, (_, winner) in enumerate(winners.iterrows(), start=1):
        instance_name = str(winner["Instance"])
        domain_name = str(winner["Domain"])
        provider = str(winner["Routing Provider"])
        plan_name = str(winner["Route Plan"])
        print(
            f"[confirm {position}/{len(winners)}] {instance_name} {domain_name}: {provider}:{plan_name}",
            flush=True,
        )

        instance_dir = data_dir / instance_name
        instance = load_instance_json(instance_dir / "instance.json")
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")
        fleet_capacity = float(vehicle_count_from_name(instance.name) * instance.capacity)
        plans = add_capacity_projected_plans(build_plans(history, nominal), fleet_capacity=fleet_capacity)

        base_row = {
            "Instance": instance_name,
            "Customers": instance.n_customers,
            "Domain": domain_name,
            "Candidate": str(winner["Candidate"]),
            "Routing Provider": provider,
            "Route Plan": plan_name,
            "Fast LP Scenario Limit": args.lp_planning_scenario_limit,
            "Full Planning Scenarios": int(len(history)),
            "Fast Score Metric": str(winner["Score Metric"]),
            "Fast Score Value": _as_float(winner.get("Score Value")),
            "Fast Stockout": _as_float(winner.get("stockout_rate")),
            "Fast Mean Total Cost": _as_float(winner.get("mean_total_cost")),
            "Fast Route Cost": _as_float(winner.get("Route Cost")),
            "Confirm Feasible": False,
            "Confirm Runtime Sec": np.nan,
            "Full Objective Value Train": np.nan,
            "Full Stockout": np.nan,
            "Full Mean Total Cost": np.nan,
            "Stockout Relative Drift": np.nan,
            "Mean Total Cost Relative Drift": np.nan,
            "Stockout Drift Safe": False,
            "Mean Total Cost Drift Safe": False,
            "Metric Stability Safe": False,
            "Reason": "",
        }

        if plan_name not in plans:
            rows.append({**base_row, "Reason": f"missing_plan:{plan_name}"})
            continue

        try:
            route_set = _solve_with_provider(
                instance=instance,
                planned_customer_loads=plans[plan_name],
                method=f"{provider}:{plan_name}:full_confirm",
                routing_provider=provider,
                vroom_url=args.vroom_url,
                time_limit_sec=args.time_limit_sec,
            )
        except Exception as exc:
            rows.append({**base_row, "Reason": f"route_solver_error:{type(exc).__name__}:{exc}"})
            continue

        if not route_set.feasible:
            rows.append({**base_row, "Reason": str(route_set.raw_metadata.get("reason", "route_infeasible"))})
            continue

        adapter = get_adapter(domain_name)
        problem = adapter.build_problem(
            instance=instance,
            anchor_routes=route_set,
            planning_scenarios=history,
            evaluation_scenarios=scenarios,
            node_meta=node_meta,
        )
        solution = engine.solve(problem, time_limit_sec=args.lp_time_limit_sec)
        if not solution.feasible:
            rows.append({**base_row, "Confirm Runtime Sec": solution.runtime_sec, "Reason": solution.reason})
            continue

        metrics = evaluate_solution(problem, solution.loads)
        full_stockout = float(metrics["stockout_rate"])
        full_cost = float(metrics["mean_total_cost"])
        stockout_drift = _relative_drift(full_stockout, _as_float(winner.get("stockout_rate")))
        cost_drift = _relative_drift(full_cost, _as_float(winner.get("mean_total_cost")))
        stockout_safe = bool(stockout_drift <= args.stability_stockout_rel_threshold)
        cost_safe = bool(cost_drift <= args.stability_cost_rel_threshold)
        rows.append(
            {
                **base_row,
                "Confirm Feasible": True,
                "Confirm Runtime Sec": solution.runtime_sec,
                "Full Objective Value Train": solution.objective_value,
                "Full Stockout": full_stockout,
                "Full Mean Total Cost": full_cost,
                "Stockout Relative Drift": stockout_drift,
                "Mean Total Cost Relative Drift": cost_drift,
                "Stockout Drift Safe": stockout_safe,
                "Mean Total Cost Drift Safe": cost_safe,
                "Metric Stability Safe": bool(stockout_safe and cost_safe),
            }
        )
    return pd.DataFrame(rows)


def _winner_ranking_stability(full_confirmation: pd.DataFrame) -> pd.DataFrame:
    if full_confirmation.empty:
        return pd.DataFrame()

    rows: list[dict[str, object]] = []
    for instance, group in full_confirmation.groupby("Instance", dropna=False):
        feasible = group[group["Confirm Feasible"] == True].dropna(subset=["Fast Stockout", "Full Stockout"])
        if feasible["Domain"].nunique() < 2:
            rows.append(
                {
                    "Instance": instance,
                    "Domains": int(feasible["Domain"].nunique()),
                    "Fast Ranking": "",
                    "Full Ranking": "",
                    "Ranking Flip": False,
                    "Stockout Spearman": np.nan,
                    "Ranking Note": "insufficient confirmed domains",
                }
            )
            continue
        fast_order = _domain_order(feasible, "Fast Stockout")
        full_order = _domain_order(feasible, "Full Stockout")
        rows.append(
            {
                "Instance": instance,
                "Domains": int(feasible["Domain"].nunique()),
                "Fast Ranking": " > ".join(fast_order),
                "Full Ranking": " > ".join(full_order),
                "Ranking Flip": fast_order != full_order,
                "Stockout Spearman": _spearman_from_orders(fast_order, full_order),
                "Ranking Note": "",
            }
        )
    return pd.DataFrame(rows)


def _attach_stability_status(
    full_confirmation: pd.DataFrame,
    ranking_stability: pd.DataFrame,
) -> pd.DataFrame:
    if full_confirmation.empty:
        return full_confirmation
    out = full_confirmation.copy()
    if not ranking_stability.empty:
        out = out.merge(
            ranking_stability[
                ["Instance", "Fast Ranking", "Full Ranking", "Ranking Flip", "Stockout Spearman", "Ranking Note"]
            ],
            on="Instance",
            how="left",
        )
    else:
        out["Ranking Flip"] = False
    out["Ranking Stable"] = out["Ranking Flip"] == False
    out["Strict Stability Safe"] = (out["Metric Stability Safe"] == True) & (out["Ranking Stable"] == True)
    out["Stability Status"] = out.apply(_stability_status, axis=1)
    return out


def _stability_status(row: pd.Series) -> str:
    if not bool(row.get("Confirm Feasible", False)):
        return "final_full_required: confirmation infeasible"
    if not bool(row.get("Metric Stability Safe", False)):
        return "final_full_required: drift threshold exceeded"
    if not bool(row.get("Ranking Stable", True)):
        return "final_full_required: domain ranking flip"
    return "safe"


def _write_report(
    path: Path,
    candidate_results: pd.DataFrame,
    route_results: pd.DataFrame,
    winners: pd.DataFrame,
    summary: pd.DataFrame,
    full_confirmation: pd.DataFrame,
    ranking_stability: pd.DataFrame,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Robust Route Selection Report",
        "",
        "## Scope",
        "",
        "This diagnostic evaluates multiple routing candidates with the same stochastic decision layer, then selects a domain-level winner by the configured score metric.",
        "",
        f"- Data dir: `{args.data_dir}`",
        f"- Routing providers: `{', '.join(args.routing_providers)}`",
        f"- LP backend: `{args.lp_backend}`",
        f"- LP planning scenario limit: `{args.lp_planning_scenario_limit}`",
        f"- Score metric: `{args.score_metric}`",
        f"- Full-scenario winner confirmation: `{args.confirm_winners_full_scenario}`",
        "",
        "Fast mode is intended for route-candidate screening. Final decision-driving claims should be rerun with full planning history by passing `--lp-planning-scenario-limit 0`.",
        "",
        "## Candidate Coverage",
        "",
        _markdown_table(summary),
        "",
        "## Winners",
        "",
    ]
    if winners.empty:
        lines.append("No feasible domain-level winners were produced.")
    else:
        winner_cols = [
            "Instance",
            "Domain",
            "Candidate",
            "Routing Provider",
            "Route Plan",
            "Score Value",
            "mean_total_cost",
            "stockout_rate",
            "Route Cost",
            "Optimized Load Total",
        ]
        existing = [col for col in winner_cols if col in winners.columns]
        lines.append(_markdown_table(winners[existing]))

    lines.extend(["", "## Full-Scenario Winner Confirmation", ""])
    if full_confirmation.empty:
        lines.append("Full-scenario winner confirmation was not requested or produced no rows.")
    else:
        confirmation_cols = [
            "Instance",
            "Domain",
            "Candidate",
            "Fast Stockout",
            "Full Stockout",
            "Stockout Relative Drift",
            "Fast Mean Total Cost",
            "Full Mean Total Cost",
            "Mean Total Cost Relative Drift",
            "Metric Stability Safe",
            "Ranking Stable",
            "Strict Stability Safe",
            "Stability Status",
        ]
        lines.append(
            _markdown_table(full_confirmation[[col for col in confirmation_cols if col in full_confirmation.columns]])
        )

    lines.extend(["", "## Domain Ranking Stability", ""])
    if ranking_stability.empty:
        lines.append("No ranking stability rows were produced.")
    else:
        lines.append(_markdown_table(ranking_stability))

    lines.extend(
        [
            "",
            "## Route Candidates",
            "",
        ]
    )
    if route_results.empty:
        lines.append("No route candidates were evaluated.")
    else:
        route_cols = [
            "Instance",
            "Candidate",
            "Route Feasible",
            "Route Count",
            "Route Cost",
            "Planned Route Load Ratio",
            "Reason",
        ]
        lines.append(_markdown_table(route_results[[col for col in route_cols if col in route_results.columns]]))

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A domain winner means that route candidate had the lowest selected evaluation metric after the stochastic loading LP.",
            "- This is not a new routing solver; it is a robust selection layer over existing route providers and load plans.",
            "- `Metric Stability Safe` checks only stockout and mean_total_cost drift; `Strict Stability Safe` also requires no domain stockout ranking flip.",
            "- Infeasible high-quantile or robust plans remain visible because capacity pressure is part of the result.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_bool_dtype(display[col]):
            display[col] = display[col].map(lambda value: "yes" if bool(value) else "no")
        elif pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.6g}")
    headers = list(display.columns)
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(rows)


def _relative_drift(reference: float, candidate: float) -> float:
    if pd.isna(reference) or pd.isna(candidate):
        return np.nan
    diff = abs(float(candidate) - float(reference))
    denom = abs(float(reference))
    if denom <= 1e-12:
        return 0.0 if diff <= 1e-12 else float("inf")
    return diff / denom


def _as_float(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def _domain_order(frame: pd.DataFrame, column: str) -> list[str]:
    ordered = frame[["Domain", column]].dropna().copy()
    ordered = ordered.sort_values([column, "Domain"], ascending=[False, True])
    return ordered["Domain"].astype(str).tolist()


def _spearman_from_orders(first_order: list[str], second_order: list[str]) -> float:
    shared = [domain for domain in first_order if domain in set(second_order)]
    n = len(shared)
    if n < 2:
        return np.nan
    first_rank = {domain: rank for rank, domain in enumerate(first_order)}
    second_rank = {domain: rank for rank, domain in enumerate(second_order)}
    diff_sq = sum((first_rank[domain] - second_rank[domain]) ** 2 for domain in shared)
    return float(1.0 - (6.0 * diff_sq) / (n * (n * n - 1)))


if __name__ == "__main__":
    main()
