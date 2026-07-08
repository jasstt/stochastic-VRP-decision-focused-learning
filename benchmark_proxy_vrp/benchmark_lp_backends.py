from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans
from .run_domain_engine import _solve_anchor
from .scenario_reduction import scenario_reduction_summary, select_representative_scenarios
from .stochastic_engine import StochasticDecisionEngine, available_lp_backends, evaluate_solution


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark stochastic LP backends on fixed route-domain problems.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--out-dir", default="benchmarks/lp_backend_benchmark")
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--backends", nargs="+", default=available_lp_backends())
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--routing-provider", choices=["ortools", "vroom"], default="ortools")
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    parser.add_argument(
        "--lp-planning-scenario-limit",
        type=int,
        default=None,
        help="Use a deterministic total-demand-stratified subset for faster LP diagnostics.",
    )
    parser.add_argument("--start-index", type=int, default=0, help="Zero-based instance start index after sorting.")
    parser.add_argument("--max-instances", type=int, default=None)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = _run_backend_benchmark(args, data_dir)
    results = pd.DataFrame(rows)
    comparisons = _compare_to_cbc(results)
    summary = _summarize(results, comparisons)

    results.to_csv(out_dir / "lp_backend_benchmark_results.csv", index=False)
    comparisons.to_csv(out_dir / "lp_backend_benchmark_comparisons.csv", index=False)
    summary.to_csv(out_dir / "lp_backend_benchmark_summary.csv", index=False)
    _write_report(out_dir / "lp_backend_benchmark_report.md", results, comparisons, summary)

    print("LP backend summary")
    print(summary.to_string(index=False))
    print(f"\nSaved {out_dir / 'lp_backend_benchmark_report.md'}")


def _run_backend_benchmark(args: argparse.Namespace, data_dir: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    instance_paths = sorted(data_dir.glob("*/instance.json"))
    if args.start_index:
        instance_paths = instance_paths[args.start_index :]
    if args.max_instances is not None:
        instance_paths = instance_paths[: args.max_instances]

    for position, instance_json in enumerate(instance_paths, start=1):
        instance = load_instance_json(instance_json)
        print(f"[{position}/{len(instance_paths)}] {instance.name}: solving anchor", flush=True)
        instance_dir = instance_json.parent
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        lp_history = select_representative_scenarios(history, args.lp_planning_scenario_limit)
        lp_scenario_summary = scenario_reduction_summary(history, lp_history)
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
                    "Instance": instance.name,
                    "Customers": instance.n_customers,
                    "Planning Scenarios": len(history),
                    "LP Planning Scenarios": len(lp_history),
                    "Domain": "all",
                    "Backend": "all",
                    "Feasible": False,
                    "Runtime Sec": np.nan,
                    "Objective Value": np.nan,
                    "Reason": "no_feasible_anchor_route",
                    **lp_scenario_summary,
                }
            )
            continue

        for domain_name in args.domains:
            adapter = get_adapter(domain_name)
            problem = adapter.build_problem(
                instance=instance,
                anchor_routes=anchor_solution,
                planning_scenarios=lp_history,
                evaluation_scenarios=scenarios,
                node_meta=node_meta,
            )
            for backend in args.backends:
                engine = StochasticDecisionEngine(lp_backend=backend)
                solution = engine.solve(problem, time_limit_sec=args.lp_time_limit_sec)
                row = {
                    "Instance": instance.name,
                    "Customers": instance.n_customers,
                    "Planning Scenarios": len(history),
                    "LP Planning Scenarios": len(lp_history),
                    "Domain": domain_name,
                    "Backend": backend,
                    "Feasible": solution.feasible,
                    "Runtime Sec": solution.runtime_sec,
                    "Objective Value": solution.objective_value,
                    "Reason": solution.reason,
                    "Planned Load Total": float(np.sum(solution.loads)) if solution.feasible else np.nan,
                    "Route Count": len(problem.route_groups),
                    "Route Cost": problem.route_cost,
                    **lp_scenario_summary,
                }
                if solution.feasible:
                    row.update(evaluate_solution(problem, solution.loads))
                rows.append(row)
        print(f"[{position}/{len(instance_paths)}] {instance.name}: done", flush=True)
    return rows


def _compare_to_cbc(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty or "Backend" not in results:
        return pd.DataFrame()
    feasible = results[results["Feasible"] == True].copy()
    required = {"Instance", "Domain", "Runtime Sec", "Objective Value", "stockout_rate", "mean_total_cost"}
    if feasible.empty or not required.issubset(feasible.columns):
        return pd.DataFrame()
    baseline = feasible[feasible["Backend"] == "pulp_cbc"][
        ["Instance", "Domain", "Runtime Sec", "Objective Value", "stockout_rate", "mean_total_cost"]
    ].rename(
        columns={
            "Runtime Sec": "CBC Runtime Sec",
            "Objective Value": "CBC Objective Value",
            "stockout_rate": "CBC Stockout Rate",
            "mean_total_cost": "CBC Mean Total Cost",
        }
    )
    others = feasible[feasible["Backend"] != "pulp_cbc"].merge(baseline, on=["Instance", "Domain"], how="inner")
    if others.empty:
        return others
    others["Runtime Speedup vs CBC"] = others["CBC Runtime Sec"] / others["Runtime Sec"].replace(0.0, np.nan)
    others["Objective Abs Diff vs CBC"] = (others["Objective Value"] - others["CBC Objective Value"]).abs()
    denom = others["CBC Objective Value"].abs().replace(0.0, np.nan)
    others["Objective Rel Diff vs CBC"] = others["Objective Abs Diff vs CBC"] / denom
    others["Stockout Abs Diff vs CBC"] = (others["stockout_rate"] - others["CBC Stockout Rate"]).abs()
    others["Mean Total Cost Abs Diff vs CBC"] = (others["mean_total_cost"] - others["CBC Mean Total Cost"]).abs()
    return others.sort_values(["Backend", "Instance", "Domain"])


def _summarize(results: pd.DataFrame, comparisons: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    runtime_summary = (
        results.groupby("Backend", dropna=False)
        .agg(
            Runs=("Backend", "size"),
            Feasible=("Feasible", "sum"),
            Median_Runtime_Sec=("Runtime Sec", "median"),
            Mean_Runtime_Sec=("Runtime Sec", "mean"),
        )
        .reset_index()
    )
    if comparisons.empty:
        return runtime_summary
    comparison_summary = (
        comparisons.groupby("Backend", dropna=False)
        .agg(
            Median_Speedup_vs_CBC=("Runtime Speedup vs CBC", "median"),
            Mean_Speedup_vs_CBC=("Runtime Speedup vs CBC", "mean"),
            Max_Objective_Rel_Diff_vs_CBC=("Objective Rel Diff vs CBC", "max"),
            Max_Stockout_Abs_Diff_vs_CBC=("Stockout Abs Diff vs CBC", "max"),
        )
        .reset_index()
    )
    return runtime_summary.merge(comparison_summary, on="Backend", how="left")


def _write_report(path: Path, results: pd.DataFrame, comparisons: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines = [
        "# LP Backend Benchmark Report",
        "",
        "## Scope",
        "",
        "This benchmark keeps the routing anchor fixed and changes only the stochastic LP backend.",
        "CBC through PuLP remains the reference backend; OR-Tools GLOP/PDLP are speed candidates.",
        "",
        "## Summary",
        "",
    ]
    if summary.empty:
        lines.append("No benchmark rows were produced.")
    else:
        lines.append(_markdown_table(summary))
    lines.extend(["", "## CBC Comparison", ""])
    if comparisons.empty:
        lines.append("No non-CBC feasible rows could be compared against CBC.")
    else:
        cols = [
            "Instance",
            "Domain",
            "Backend",
            "Runtime Speedup vs CBC",
            "Objective Rel Diff vs CBC",
            "Stockout Abs Diff vs CBC",
        ]
        lines.append(_markdown_table(comparisons[cols]))
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- A backend is a safe drop-in candidate only if it is faster and keeps objective/stockout deltas near zero.",
            "- PDLP is a first-order LP solver, so speed gains must be checked against numerical drift before using it for final reports.",
            "- If generic LP backends do not give enough speedup, the next step is a route-level structured allocator that exploits the separable recourse form directly.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.6g}")
    headers = list(display.columns)
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
    return "\n".join(rows)


if __name__ == "__main__":
    main()
