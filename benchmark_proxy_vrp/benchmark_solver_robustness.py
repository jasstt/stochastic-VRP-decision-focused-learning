from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .cvrplib import customer_view, load_instance_json
from .domain_adapters import available_adapters, get_adapter
from .ortools_baselines import build_plans
from .run_domain_engine import _solve_anchor
from .scenario_reduction import scenario_reduction_summary, select_representative_scenarios
from .stochastic_engine import StochasticDecisionEngine, available_lp_backends, evaluate_solution


@dataclass(frozen=True)
class BaselineConfig:
    routing_provider: str
    route_time_limit_sec: int
    lp_backend: str
    lp_time_limit_sec: int
    lp_scenario_limit: int | None

    @property
    def lp_scenario_label(self) -> str:
        return _scenario_limit_label(self.lp_scenario_limit)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark robustness of route providers, LP backends, time limits, "
            "and LP scenario limits against a fixed baseline."
        )
    )
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--out-dir", default="benchmarks/solver_robustness_benchmark")
    parser.add_argument("--domains", nargs="+", default=available_adapters())
    parser.add_argument("--routing-providers", nargs="+", choices=["ortools", "vroom"], default=["ortools", "vroom"])
    parser.add_argument("--lp-backends", nargs="+", default=available_lp_backends())
    parser.add_argument("--route-time-limits", nargs="+", type=int, default=[2, 5])
    parser.add_argument("--lp-time-limits", nargs="+", type=int, default=[10, 30])
    parser.add_argument(
        "--lp-scenario-limits",
        nargs="+",
        default=["full", "60"],
        help="Scenario limits to sweep. Use 'full' or 'none' for the complete planning history.",
    )
    parser.add_argument("--anchor-plan", default="proxy_mean_or_tools")
    parser.add_argument("--fallback-anchor-plan", default="nominal_or_tools")
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-instances", type=int, default=None)
    parser.add_argument("--baseline-routing-provider", choices=["ortools", "vroom"], default="ortools")
    parser.add_argument("--baseline-route-time-limit-sec", type=int, default=None)
    parser.add_argument("--baseline-lp-backend", choices=available_lp_backends(), default="pulp_cbc")
    parser.add_argument("--baseline-lp-time-limit-sec", type=int, default=None)
    parser.add_argument("--baseline-lp-scenario-limit", default="full")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    route_time_limits = sorted(set(args.route_time_limits))
    lp_time_limits = sorted(set(args.lp_time_limits))
    lp_scenario_limits = _parse_scenario_limits(args.lp_scenario_limits)
    baseline = BaselineConfig(
        routing_provider=args.baseline_routing_provider,
        route_time_limit_sec=args.baseline_route_time_limit_sec or max(route_time_limits),
        lp_backend=args.baseline_lp_backend,
        lp_time_limit_sec=args.baseline_lp_time_limit_sec or max(lp_time_limits),
        lp_scenario_limit=_parse_scenario_limit(args.baseline_lp_scenario_limit),
    )

    rows = _run_solver_robustness_benchmark(
        args=args,
        data_dir=data_dir,
        route_time_limits=route_time_limits,
        lp_time_limits=lp_time_limits,
        lp_scenario_limits=lp_scenario_limits,
    )
    results = pd.DataFrame(rows)
    comparisons = _compare_to_baseline(results, baseline)
    summary = _summarize(results, comparisons)
    diagnostics = _diagnose_correlations(comparisons)

    results.to_csv(out_dir / "solver_robustness_results.csv", index=False)
    comparisons.to_csv(out_dir / "solver_robustness_comparisons.csv", index=False)
    summary.to_csv(out_dir / "solver_robustness_summary.csv", index=False)
    diagnostics.to_csv(out_dir / "solver_robustness_diagnostics.csv", index=False)
    _write_report(
        out_dir / "solver_robustness_benchmark_report.md",
        results=results,
        comparisons=comparisons,
        summary=summary,
        diagnostics=diagnostics,
        baseline=baseline,
    )

    print("Solver robustness summary")
    print(summary.to_string(index=False) if not summary.empty else "No rows.")
    print(f"\nSaved {out_dir / 'solver_robustness_benchmark_report.md'}")


def _run_solver_robustness_benchmark(
    args: argparse.Namespace,
    data_dir: Path,
    route_time_limits: list[int],
    lp_time_limits: list[int],
    lp_scenario_limits: list[int | None],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    instance_paths = sorted(data_dir.glob("*/instance.json"))
    if args.start_index:
        instance_paths = instance_paths[args.start_index :]
    if args.max_instances is not None:
        instance_paths = instance_paths[: args.max_instances]

    total_route_jobs = len(instance_paths) * len(args.routing_providers) * len(route_time_limits)
    route_job = 0
    for instance_json in instance_paths:
        instance = load_instance_json(instance_json)
        instance_dir = instance_json.parent
        nominal, _ = customer_view(instance)
        history = pd.read_csv(instance_dir / "proxy_demand_history.csv").drop(columns=["date"]).to_numpy()
        scenarios = np.load(instance_dir / "proxy_saa_scenarios.npy")
        node_meta = pd.read_csv(instance_dir / "proxy_node_meta.csv")
        plans = build_plans(history, nominal)

        for routing_provider in args.routing_providers:
            for route_time_limit in route_time_limits:
                route_job += 1
                print(
                    f"[route {route_job}/{total_route_jobs}] {instance.name}: "
                    f"{routing_provider} t={route_time_limit}s",
                    flush=True,
                )
                try:
                    anchor_solution = _solve_anchor(
                        instance,
                        plans,
                        args.anchor_plan,
                        args.fallback_anchor_plan,
                        routing_provider,
                        args.vroom_url,
                        route_time_limit,
                    )
                    route_error = ""
                except Exception as exc:  # VROOM may be unavailable in local smoke runs.
                    anchor_solution = None
                    route_error = f"route_provider_error:{type(exc).__name__}:{exc}"

                for domain_name in args.domains:
                    for lp_backend in args.lp_backends:
                        for lp_time_limit in lp_time_limits:
                            for lp_scenario_limit in lp_scenario_limits:
                                common = _common_row(
                                    instance_name=instance.name,
                                    customers=instance.n_customers,
                                    domain_name=domain_name,
                                    routing_provider=routing_provider,
                                    route_time_limit=route_time_limit,
                                    lp_backend=lp_backend,
                                    lp_time_limit=lp_time_limit,
                                    lp_scenario_limit=lp_scenario_limit,
                                    history=history,
                                )
                                if anchor_solution is None:
                                    rows.append(
                                        {
                                            **common,
                                            "Route Feasible": False,
                                            "LP Feasible": False,
                                            "Feasible": False,
                                            "Routing Runtime Sec": np.nan,
                                            "LP Runtime Sec": np.nan,
                                            "Total Runtime Sec": np.nan,
                                            "Route Count": np.nan,
                                            "Route Cost": np.nan,
                                            "Objective Value Train": np.nan,
                                            "Reason": route_error,
                                        }
                                    )
                                    continue
                                if not anchor_solution.feasible:
                                    rows.append(
                                        {
                                            **common,
                                            "Route Feasible": False,
                                            "LP Feasible": False,
                                            "Feasible": False,
                                            "Routing Runtime Sec": _route_runtime(anchor_solution),
                                            "LP Runtime Sec": np.nan,
                                            "Total Runtime Sec": _route_runtime(anchor_solution),
                                            "Route Count": 0,
                                            "Route Cost": np.nan,
                                            "Objective Value Train": np.nan,
                                            "Reason": anchor_solution.raw_metadata.get("reason", "no_feasible_anchor_route"),
                                        }
                                    )
                                    continue

                                lp_history = select_representative_scenarios(history, lp_scenario_limit)
                                adapter = get_adapter(domain_name)
                                try:
                                    problem = adapter.build_problem(
                                        instance=instance,
                                        anchor_routes=anchor_solution,
                                        planning_scenarios=lp_history,
                                        evaluation_scenarios=scenarios,
                                        node_meta=node_meta,
                                    )
                                    solution = StochasticDecisionEngine(lp_backend=lp_backend).solve(
                                        problem,
                                        time_limit_sec=lp_time_limit,
                                    )
                                except Exception as exc:
                                    rows.append(
                                        {
                                            **common,
                                            **_scenario_summary(history, lp_history),
                                            "Route Feasible": True,
                                            "LP Feasible": False,
                                            "Feasible": False,
                                            "Routing Runtime Sec": _route_runtime(anchor_solution),
                                            "LP Runtime Sec": np.nan,
                                            "Total Runtime Sec": _route_runtime(anchor_solution),
                                            "Route Count": len(anchor_solution.routes),
                                            "Route Cost": anchor_solution.total_cost,
                                            "Objective Value Train": np.nan,
                                            "Reason": f"lp_error:{type(exc).__name__}:{exc}",
                                        }
                                    )
                                    continue

                                row = {
                                    **common,
                                    **_scenario_summary(history, lp_history),
                                    "Route Feasible": True,
                                    "LP Feasible": bool(solution.feasible),
                                    "Feasible": bool(solution.feasible),
                                    "Routing Runtime Sec": _route_runtime(anchor_solution),
                                    "LP Runtime Sec": solution.runtime_sec,
                                    "Total Runtime Sec": _route_runtime(anchor_solution) + solution.runtime_sec,
                                    "Route Count": len(problem.route_groups),
                                    "Route Cost": problem.route_cost,
                                    "Objective Value Train": solution.objective_value,
                                    "Reason": solution.reason,
                                }
                                if solution.feasible:
                                    row["Planned Load Total"] = float(np.sum(solution.loads))
                                    row.update(evaluate_solution(problem, solution.loads))
                                rows.append(row)
                print(
                    f"[route {route_job}/{total_route_jobs}] {instance.name}: "
                    f"{routing_provider} t={route_time_limit}s done",
                    flush=True,
                )
    return rows


def _common_row(
    instance_name: str,
    customers: int,
    domain_name: str,
    routing_provider: str,
    route_time_limit: int,
    lp_backend: str,
    lp_time_limit: int,
    lp_scenario_limit: int | None,
    history: np.ndarray,
) -> dict[str, object]:
    lp_scenario_count = len(select_representative_scenarios(history, lp_scenario_limit))
    return {
        "Instance": instance_name,
        "Customers": customers,
        "Domain": domain_name,
        "Route Provider": routing_provider,
        "Route Time Limit Sec": route_time_limit,
        "LP Backend": lp_backend,
        "LP Time Limit Sec": lp_time_limit,
        "LP Scenario Limit": _scenario_limit_label(lp_scenario_limit),
        "Planning Scenarios": len(history),
        "LP Planning Scenarios": lp_scenario_count,
        "LP Scenario Fraction": float(lp_scenario_count / len(history)) if len(history) else np.nan,
    }


def _scenario_summary(history: np.ndarray, lp_history: np.ndarray) -> dict[str, object]:
    summary = scenario_reduction_summary(history, lp_history)
    return {
        "LP Scenario Reduced": bool(summary["lp_scenario_reduced"]),
        "LP Original Total Demand Mean": summary["lp_original_total_demand_mean"],
        "LP Reduced Total Demand Mean": summary["lp_reduced_total_demand_mean"],
        "LP Original Total Demand P90": summary["lp_original_total_demand_p90"],
        "LP Reduced Total Demand P90": summary["lp_reduced_total_demand_p90"],
    }


def _route_runtime(anchor_solution) -> float:
    return float(anchor_solution.raw_metadata.get("runtime_sec", 0.0))


def _compare_to_baseline(results: pd.DataFrame, baseline: BaselineConfig) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    feasible = results[results["Feasible"] == True].copy()
    baseline_rows = feasible[
        (feasible["Route Provider"] == baseline.routing_provider)
        & (feasible["Route Time Limit Sec"] == baseline.route_time_limit_sec)
        & (feasible["LP Backend"] == baseline.lp_backend)
        & (feasible["LP Time Limit Sec"] == baseline.lp_time_limit_sec)
        & (feasible["LP Scenario Limit"] == baseline.lp_scenario_label)
    ].copy()
    metric_cols = [
        "stockout_rate",
        "mean_total_cost",
        "Objective Value Train",
        "Route Cost",
        "Total Runtime Sec",
    ]
    available_metrics = [col for col in metric_cols if col in feasible.columns and col in baseline_rows.columns]
    if baseline_rows.empty or not available_metrics:
        return pd.DataFrame()

    baseline_cols = ["Instance", "Domain", *available_metrics]
    baseline_rows = baseline_rows[baseline_cols].rename(columns={col: f"Baseline {col}" for col in available_metrics})
    comparisons = feasible.merge(baseline_rows, on=["Instance", "Domain"], how="inner")
    if comparisons.empty:
        return comparisons

    if "stockout_rate" in comparisons:
        comparisons["Stockout Drift Abs"] = (
            comparisons["stockout_rate"] - comparisons["Baseline stockout_rate"]
        ).abs()
        denom = comparisons["Baseline stockout_rate"].abs().replace(0.0, np.nan)
        comparisons["Stockout Drift Rel"] = comparisons["Stockout Drift Abs"] / denom
    if "mean_total_cost" in comparisons:
        comparisons["Objective Drift Abs"] = (
            comparisons["mean_total_cost"] - comparisons["Baseline mean_total_cost"]
        ).abs()
        denom = comparisons["Baseline mean_total_cost"].abs().replace(0.0, np.nan)
        comparisons["Objective Drift Rel"] = comparisons["Objective Drift Abs"] / denom
    if "Objective Value Train" in comparisons:
        comparisons["Train Objective Drift Abs"] = (
            comparisons["Objective Value Train"] - comparisons["Baseline Objective Value Train"]
        ).abs()
        denom = comparisons["Baseline Objective Value Train"].abs().replace(0.0, np.nan)
        comparisons["Train Objective Drift Rel"] = comparisons["Train Objective Drift Abs"] / denom
    if "Route Cost" in comparisons:
        comparisons["Route Cost Drift Abs"] = (comparisons["Route Cost"] - comparisons["Baseline Route Cost"]).abs()
        denom = comparisons["Baseline Route Cost"].abs().replace(0.0, np.nan)
        comparisons["Route Cost Drift Rel"] = comparisons["Route Cost Drift Abs"] / denom
    if "Total Runtime Sec" in comparisons:
        denom = comparisons["Total Runtime Sec"].replace(0.0, np.nan)
        comparisons["Runtime Speedup vs Baseline"] = comparisons["Baseline Total Runtime Sec"] / denom
    return comparisons.sort_values(
        [
            "Route Provider",
            "Route Time Limit Sec",
            "LP Backend",
            "LP Time Limit Sec",
            "LP Scenario Limit",
            "Instance",
            "Domain",
        ]
    )


def _summarize(results: pd.DataFrame, comparisons: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame()
    group_cols = [
        "Route Provider",
        "Route Time Limit Sec",
        "LP Backend",
        "LP Time Limit Sec",
        "LP Scenario Limit",
    ]
    runtime_summary = (
        results.groupby(group_cols, dropna=False)
        .agg(
            Rows=("Feasible", "size"),
            Feasible_Rows=("Feasible", "sum"),
            Route_Feasible_Rows=("Route Feasible", "sum"),
            LP_Feasible_Rows=("LP Feasible", "sum"),
            Median_Total_Runtime_Sec=("Total Runtime Sec", "median"),
            Mean_Total_Runtime_Sec=("Total Runtime Sec", "mean"),
        )
        .reset_index()
    )
    runtime_summary["Feasibility_Rate"] = runtime_summary["Feasible_Rows"] / runtime_summary["Rows"]
    if comparisons.empty:
        return runtime_summary

    drift_summary = (
        comparisons.groupby(group_cols, dropna=False)
        .agg(
            Compared_Rows=("Feasible", "size"),
            Median_Runtime_Speedup_vs_Baseline=("Runtime Speedup vs Baseline", "median"),
            Mean_Stockout_Drift_Abs=("Stockout Drift Abs", "mean"),
            Max_Stockout_Drift_Abs=("Stockout Drift Abs", "max"),
            Mean_Objective_Drift_Rel=("Objective Drift Rel", "mean"),
            Max_Objective_Drift_Rel=("Objective Drift Rel", "max"),
        )
        .reset_index()
    )
    ci_rows = []
    for keys, group in comparisons.groupby(group_cols, dropna=False):
        key_values = keys if isinstance(keys, tuple) else (keys,)
        stockout_low, stockout_high = _bootstrap_mean_ci(group["Stockout Drift Abs"].dropna().to_numpy())
        objective_low, objective_high = _bootstrap_mean_ci(group["Objective Drift Rel"].dropna().to_numpy())
        ci_rows.append(
            {
                **dict(zip(group_cols, key_values)),
                "Stockout_Drift_Mean_CI_Low": stockout_low,
                "Stockout_Drift_Mean_CI_High": stockout_high,
                "Objective_Drift_Rel_Mean_CI_Low": objective_low,
                "Objective_Drift_Rel_Mean_CI_High": objective_high,
            }
        )
    drift_summary = drift_summary.merge(pd.DataFrame(ci_rows), on=group_cols, how="left")
    return runtime_summary.merge(drift_summary, on=group_cols, how="left")


def _diagnose_correlations(comparisons: pd.DataFrame) -> pd.DataFrame:
    if comparisons.empty:
        return pd.DataFrame()
    rows = []
    x_metrics = ["Route Time Limit Sec", "LP Time Limit Sec", "LP Planning Scenarios"]
    y_metrics = ["Stockout Drift Abs", "Objective Drift Rel"]
    for y_metric in y_metrics:
        if y_metric not in comparisons:
            continue
        for x_metric in x_metrics:
            rows.append(_diagnose_one_correlation(comparisons, x_metric, y_metric))
    return pd.DataFrame(rows)


def _diagnose_one_correlation(df: pd.DataFrame, x_metric: str, y_metric: str) -> dict[str, object]:
    clean = df[[x_metric, y_metric]].replace([np.inf, -np.inf], np.nan).dropna()
    n = len(clean)
    unique_x = clean[x_metric].nunique()
    base = {
        "X Metric": x_metric,
        "Y Metric": y_metric,
        "N": n,
        "Unique X Levels": int(unique_x),
        "Pearson r": np.nan,
        "Permutation p-value": np.nan,
        "Bootstrap CI Low": np.nan,
        "Bootstrap CI High": np.nan,
        "A5 Status": "",
    }
    if n < 3:
        base["A5 Status"] = "insufficient rows"
        return base
    if unique_x < 3:
        base["A5 Status"] = "insufficient x variation; correlation not reported"
        return base

    r_value = _pearson_r(clean[x_metric].to_numpy(dtype=float), clean[y_metric].to_numpy(dtype=float))
    p_value = _permutation_p_value(clean[x_metric].to_numpy(dtype=float), clean[y_metric].to_numpy(dtype=float), r_value)
    ci_low, ci_high = _bootstrap_corr_ci(clean[x_metric].to_numpy(dtype=float), clean[y_metric].to_numpy(dtype=float))
    base.update(
        {
            "Pearson r": r_value,
            "Permutation p-value": p_value,
            "Bootstrap CI Low": ci_low,
            "Bootstrap CI High": ci_high,
            "A5 Status": _a5_status(n, ci_low, ci_high),
        }
    )
    return base


def _a5_status(n: int, ci_low: float, ci_high: float) -> str:
    prefix = "diagnostic signal only; n<15" if n < 15 else "candidate signal"
    if np.isnan(ci_low) or np.isnan(ci_high):
        return f"{prefix}; bootstrap unavailable"
    if ci_low <= 0.0 <= ci_high:
        return f"{prefix}; bootstrap CI includes zero"
    return f"{prefix}; bootstrap CI excludes zero"


def _pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 2 or np.std(x) == 0.0 or np.std(y) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def _permutation_p_value(x: np.ndarray, y: np.ndarray, observed_r: float, n_permutations: int = 1999) -> float:
    if np.isnan(observed_r):
        return float("nan")
    rng = np.random.default_rng(17)
    count = 0
    for _ in range(n_permutations):
        permuted = rng.permutation(y)
        permuted_r = _pearson_r(x, permuted)
        if not np.isnan(permuted_r) and abs(permuted_r) >= abs(observed_r):
            count += 1
    return float((count + 1) / (n_permutations + 1))


def _bootstrap_corr_ci(x: np.ndarray, y: np.ndarray, n_boot: int = 1000) -> tuple[float, float]:
    if len(x) < 3:
        return float("nan"), float("nan")
    rng = np.random.default_rng(23)
    values = []
    n = len(x)
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        r_value = _pearson_r(x[idx], y[idx])
        if not np.isnan(r_value):
            values.append(r_value)
    if not values:
        return float("nan"), float("nan")
    return float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))


def _bootstrap_mean_ci(values: np.ndarray, n_boot: int = 1000) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(31)
    means = [float(np.mean(values[rng.integers(0, len(values), size=len(values))])) for _ in range(n_boot)]
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def _write_report(
    path: Path,
    results: pd.DataFrame,
    comparisons: pd.DataFrame,
    summary: pd.DataFrame,
    diagnostics: pd.DataFrame,
    baseline: BaselineConfig,
) -> None:
    n_instances = int(results["Instance"].nunique()) if "Instance" in results else 0
    n_domains = int(results["Domain"].nunique()) if "Domain" in results else 0
    feasible_rows = int(results["Feasible"].sum()) if "Feasible" in results else 0
    total_rows = int(len(results))
    evidence_label = "diagnostic signal only" if n_instances < 15 else "candidate benchmark evidence"

    lines = [
        "# Solver Robustness Benchmark Report",
        "",
        "## Scope",
        "",
        "This benchmark sweeps routing provider, route time limit, LP backend, LP time limit, and LP scenario limit.",
        "CBC through PuLP remains the default reference backend. OR-Tools GLOP/PDLP are reported as cross-checks.",
        "GAMS is intentionally excluded from this branch.",
        "",
        "## Baseline",
        "",
        (
            f"Baseline = route provider `{baseline.routing_provider}`, route time limit "
            f"`{baseline.route_time_limit_sec}s`, LP backend `{baseline.lp_backend}`, "
            f"LP time limit `{baseline.lp_time_limit_sec}s`, LP scenario limit `{baseline.lp_scenario_label}`."
        ),
        "",
        "## A.5 Evidence Status",
        "",
        (
            f"Rows: {total_rows}; feasible rows: {feasible_rows}; instances: {n_instances}; "
            f"domains: {n_domains}. This run is classified as **{evidence_label}**."
        ),
        "",
        "## Summary",
        "",
        _markdown_table(summary) if not summary.empty else "No summary rows were produced.",
        "",
        "## Drift Against Baseline",
        "",
    ]
    if comparisons.empty:
        lines.append("No feasible rows could be compared to the configured baseline.")
    else:
        cols = [
            "Instance",
            "Domain",
            "Route Provider",
            "Route Time Limit Sec",
            "LP Backend",
            "LP Time Limit Sec",
            "LP Scenario Limit",
            "Runtime Speedup vs Baseline",
            "Stockout Drift Abs",
            "Objective Drift Rel",
        ]
        available = [col for col in cols if col in comparisons.columns]
        lines.append(_markdown_table(comparisons[available].head(40)))
        if len(comparisons) > 40:
            lines.append("")
            lines.append(f"_Showing first 40 of {len(comparisons)} comparison rows; see CSV for full output._")

    lines.extend(
        [
            "",
            "## Correlation Diagnostics",
            "",
        ]
    )
    if diagnostics.empty:
        lines.append("No correlation diagnostics were produced.")
    else:
        lines.append(_markdown_table(diagnostics))
    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            "- Treat n<15 runs as smoke diagnostics, not proof.",
            "- Do not report a correlation when the x variable has fewer than 3 distinct levels.",
            "- If a bootstrap confidence interval includes zero, treat the relationship as unstable.",
            "- A solver variant is a safe default candidate only if feasibility stays high and stockout/objective drift remain near zero.",
            "- Final README/report claims should use full planning scenarios even when `limit=60` is acceptable for exploration.",
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


def _parse_scenario_limits(values: Iterable[str]) -> list[int | None]:
    parsed = [_parse_scenario_limit(value) for value in values]
    deduped: list[int | None] = []
    for value in parsed:
        if value not in deduped:
            deduped.append(value)
    return deduped


def _parse_scenario_limit(value: str | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    key = value.strip().lower()
    if key in {"full", "none", "null", "all", "0"}:
        return None
    parsed = int(key)
    if parsed <= 0:
        return None
    return parsed


def _scenario_limit_label(value: int | None) -> str:
    return "full" if value is None else str(int(value))


if __name__ == "__main__":
    main()
