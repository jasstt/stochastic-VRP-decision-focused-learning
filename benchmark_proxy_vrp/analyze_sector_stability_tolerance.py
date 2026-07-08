from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_SCENARIO_BIAS_RESULTS = "benchmarks/proxy_cvrplib_x_v4/scenario_reduction_bias_results.csv"
DEFAULT_OR_TOOLS_RESULTS = "benchmarks/proxy_cvrplib_n20/domain_engine_results_ortools_provider.csv"
DEFAULT_VROOM_RESULTS = "benchmarks/proxy_cvrplib_n20/domain_engine_results_vroom_provider.csv"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Judge domain adapter stability across fast/full, provider, or perturbation profiles."
    )
    parser.add_argument("--out-dir", default="benchmarks/sector_stability_tolerance_smoke")
    parser.add_argument("--scenario-bias-results", default=DEFAULT_SCENARIO_BIAS_RESULTS)
    parser.add_argument("--ortools-results", default=DEFAULT_OR_TOOLS_RESULTS)
    parser.add_argument("--vroom-results", default=DEFAULT_VROOM_RESULTS)
    parser.add_argument(
        "--comparison",
        action="append",
        default=[],
        metavar="NAME,BASE_LABEL,BASE_CSV,CANDIDATE_LABEL,CANDIDATE_CSV",
        help=(
            "Optional domain_engine-style pair. Use this for perturbation runs, e.g. "
            "perturb_1pct,base,base.csv,jittered,jittered.csv"
        ),
    )
    parser.add_argument("--stockout-rel-threshold", type=float, default=0.05)
    parser.add_argument("--cost-rel-threshold", type=float, default=0.05)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    check_frames: list[pd.DataFrame] = []
    scenario_path = Path(args.scenario_bias_results)
    if scenario_path.exists():
        check_frames.append(_checks_from_scenario_bias(scenario_path))

    ortools_path = Path(args.ortools_results)
    vroom_path = Path(args.vroom_results)
    if ortools_path.exists() and vroom_path.exists():
        check_frames.append(
            _checks_from_domain_engine_pair(
                comparison="provider_switch",
                baseline_label="ortools_provider",
                baseline_path=ortools_path,
                candidate_label="vroom_provider",
                candidate_path=vroom_path,
            )
        )

    for spec in args.comparison:
        check_frames.append(_checks_from_comparison_spec(spec))

    if not check_frames:
        raise SystemExit("No input comparisons found. Provide existing result CSVs or --comparison entries.")

    checks = pd.concat(check_frames, ignore_index=True)
    ranking = _ranking_checks(checks)
    checks = checks.merge(
        ranking[
            [
                "Comparison",
                "Instance",
                "Baseline Ranking",
                "Candidate Ranking",
                "Ranking Flip",
                "Stockout Spearman",
            ]
        ],
        on=["Comparison", "Instance"],
        how="left",
    )
    checks = _apply_tolerance_rules(
        checks,
        stockout_rel_threshold=args.stockout_rel_threshold,
        cost_rel_threshold=args.cost_rel_threshold,
    )
    domain_summary = _domain_summary(checks)
    comparison_summary = _comparison_summary(checks, ranking)

    checks.to_csv(out_dir / "sector_stability_tolerance_checks.csv", index=False)
    ranking.to_csv(out_dir / "sector_stability_ranking_flips.csv", index=False)
    domain_summary.to_csv(out_dir / "sector_stability_domain_summary.csv", index=False)
    comparison_summary.to_csv(out_dir / "sector_stability_comparison_summary.csv", index=False)
    _write_report(
        out_dir / "sector_stability_tolerance_report.md",
        checks=checks,
        ranking=ranking,
        domain_summary=domain_summary,
        comparison_summary=comparison_summary,
        stockout_rel_threshold=args.stockout_rel_threshold,
        cost_rel_threshold=args.cost_rel_threshold,
        scenario_path=scenario_path,
        ortools_path=ortools_path,
        vroom_path=vroom_path,
        custom_specs=args.comparison,
    )

    print("Comparison summary")
    print(comparison_summary.to_string(index=False))
    print("\nDomain summary")
    print(domain_summary.to_string(index=False))
    print(f"\nSaved {out_dir / 'sector_stability_tolerance_report.md'}")


def _checks_from_scenario_bias(path: Path) -> pd.DataFrame:
    raw = pd.read_csv(path)
    rows: list[dict[str, object]] = []
    for _, row in raw.iterrows():
        full_feasible = _as_bool(row.get("Full Feasible"))
        limited_feasible = _as_bool(row.get("Limited Feasible"))
        base_stockout = _as_float(row.get("Full Stockout"))
        candidate_stockout = _as_float(row.get("Limited Stockout"))
        base_cost = _as_float(row.get("Full Mean Total Cost"))
        candidate_cost = _as_float(row.get("Limited Mean Total Cost"))
        rows.append(
            _check_row(
                comparison="scenario_reduction_limit_60",
                instance=str(row.get("Instance")),
                customers=_as_float(row.get("Customers")),
                size_bucket=str(row.get("Size Bucket", "")),
                domain=str(row.get("Domain")),
                baseline_label="full_scenario",
                candidate_label="limit_60",
                baseline_feasible=full_feasible,
                candidate_feasible=limited_feasible,
                baseline_stockout=base_stockout,
                candidate_stockout=candidate_stockout,
                baseline_cost=base_cost,
                candidate_cost=candidate_cost,
                reason=str(row.get("Reason", "")),
            )
        )
    return pd.DataFrame(rows)


def _checks_from_comparison_spec(spec: str) -> pd.DataFrame:
    parts = [part.strip() for part in spec.split(",", 4)]
    if len(parts) != 5:
        raise SystemExit(
            "--comparison must be NAME,BASE_LABEL,BASE_CSV,CANDIDATE_LABEL,CANDIDATE_CSV"
        )
    comparison, baseline_label, baseline_csv, candidate_label, candidate_csv = parts
    return _checks_from_domain_engine_pair(
        comparison=comparison,
        baseline_label=baseline_label,
        baseline_path=Path(baseline_csv),
        candidate_label=candidate_label,
        candidate_path=Path(candidate_csv),
    )


def _checks_from_domain_engine_pair(
    comparison: str,
    baseline_label: str,
    baseline_path: Path,
    candidate_label: str,
    candidate_path: Path,
) -> pd.DataFrame:
    baseline = pd.read_csv(baseline_path)
    candidate = pd.read_csv(candidate_path)
    key = ["instance", "domain"]
    merged = baseline.merge(candidate, on=key, suffixes=("_base", "_cand"), how="outer")
    rows: list[dict[str, object]] = []
    for _, row in merged.iterrows():
        instance = str(row.get("instance"))
        baseline_feasible = _as_bool(row.get("feasible_base"))
        candidate_feasible = _as_bool(row.get("feasible_cand"))
        base_stockout = _as_float(row.get("stockout_rate_base"))
        candidate_stockout = _as_float(row.get("stockout_rate_cand"))
        base_cost = _as_float(row.get("mean_total_cost_base"))
        candidate_cost = _as_float(row.get("mean_total_cost_cand"))
        reason = _join_reasons(row.get("reason_base"), row.get("reason_cand"))
        rows.append(
            _check_row(
                comparison=comparison,
                instance=instance,
                customers=_customers_from_name(instance),
                size_bucket=_size_bucket(_customers_from_name(instance)),
                domain=str(row.get("domain")),
                baseline_label=baseline_label,
                candidate_label=candidate_label,
                baseline_feasible=baseline_feasible,
                candidate_feasible=candidate_feasible,
                baseline_stockout=base_stockout,
                candidate_stockout=candidate_stockout,
                baseline_cost=base_cost,
                candidate_cost=candidate_cost,
                reason=reason,
            )
        )
    return pd.DataFrame(rows)


def _check_row(
    *,
    comparison: str,
    instance: str,
    customers: float,
    size_bucket: str,
    domain: str,
    baseline_label: str,
    candidate_label: str,
    baseline_feasible: bool,
    candidate_feasible: bool,
    baseline_stockout: float,
    candidate_stockout: float,
    baseline_cost: float,
    candidate_cost: float,
    reason: str,
) -> dict[str, object]:
    return {
        "Comparison": comparison,
        "Instance": instance,
        "Customers": customers,
        "Size Bucket": size_bucket,
        "Domain": domain,
        "Baseline Profile": baseline_label,
        "Candidate Profile": candidate_label,
        "Baseline Feasible": baseline_feasible,
        "Candidate Feasible": candidate_feasible,
        "Both Feasible": baseline_feasible and candidate_feasible,
        "Baseline Stockout": baseline_stockout,
        "Candidate Stockout": candidate_stockout,
        "Stockout Abs Drift": _abs_drift(baseline_stockout, candidate_stockout),
        "Stockout Relative Drift": _relative_drift(baseline_stockout, candidate_stockout),
        "Baseline Mean Total Cost": baseline_cost,
        "Candidate Mean Total Cost": candidate_cost,
        "Mean Total Cost Abs Drift": _abs_drift(baseline_cost, candidate_cost),
        "Mean Total Cost Relative Drift": _relative_drift(baseline_cost, candidate_cost),
        "Reason": reason,
    }


def _ranking_checks(checks: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (comparison, instance), group in checks.groupby(["Comparison", "Instance"], dropna=False):
        feasible = group[group["Both Feasible"] == True].dropna(
            subset=["Baseline Stockout", "Candidate Stockout"]
        )
        if feasible["Domain"].nunique() < 2:
            rows.append(
                {
                    "Comparison": comparison,
                    "Instance": instance,
                    "Domains": int(feasible["Domain"].nunique()),
                    "Baseline Ranking": "",
                    "Candidate Ranking": "",
                    "Ranking Flip": False,
                    "Stockout Spearman": np.nan,
                    "Ranking Note": "insufficient domains",
                }
            )
            continue

        baseline_order = _stockout_order(feasible, "Baseline Stockout")
        candidate_order = _stockout_order(feasible, "Candidate Stockout")
        rows.append(
            {
                "Comparison": comparison,
                "Instance": instance,
                "Domains": int(feasible["Domain"].nunique()),
                "Baseline Ranking": " > ".join(baseline_order),
                "Candidate Ranking": " > ".join(candidate_order),
                "Ranking Flip": baseline_order != candidate_order,
                "Stockout Spearman": _spearman_from_orders(baseline_order, candidate_order),
                "Ranking Note": "",
            }
        )
    return pd.DataFrame(rows)


def _apply_tolerance_rules(
    checks: pd.DataFrame,
    *,
    stockout_rel_threshold: float,
    cost_rel_threshold: float,
) -> pd.DataFrame:
    checks = checks.copy()
    checks["Stockout Drift Safe"] = checks["Stockout Relative Drift"] <= stockout_rel_threshold
    checks["Mean Total Cost Drift Safe"] = checks["Mean Total Cost Relative Drift"] <= cost_rel_threshold
    checks["Ranking Stable"] = checks["Ranking Flip"] == False
    checks["Metric Safe"] = (
        (checks["Both Feasible"] == True)
        & (checks["Stockout Drift Safe"] == True)
        & (checks["Mean Total Cost Drift Safe"] == True)
    )
    checks["Safe"] = (
        (checks["Metric Safe"] == True)
        & (checks["Ranking Stable"] == True)
    )
    checks["Stability Status"] = checks.apply(_status_for_row, axis=1)
    return checks


def _status_for_row(row: pd.Series) -> str:
    if not bool(row["Both Feasible"]):
        return "final_full_required: feasibility mismatch"
    if not bool(row["Ranking Stable"]):
        return "unstable: domain ranking flip"
    if not bool(row["Stockout Drift Safe"]):
        return "unstable: stockout drift threshold exceeded"
    if not bool(row["Mean Total Cost Drift Safe"]):
        return "unstable: mean_total_cost drift threshold exceeded"
    return "safe"


def _domain_summary(checks: pd.DataFrame) -> pd.DataFrame:
    if checks.empty:
        return pd.DataFrame()
    grouped = (
        checks.groupby(["Comparison", "Domain"], dropna=False)
        .agg(
            Rows=("Domain", "size"),
            Both_Feasible=("Both Feasible", "sum"),
            Metric_Safe_Rows=("Metric Safe", "sum"),
            Safe_Rows=("Safe", "sum"),
            Ranking_Flip_Rows=("Ranking Flip", "sum"),
            Mean_Stockout_Rel_Drift=("Stockout Relative Drift", "mean"),
            Max_Stockout_Rel_Drift=("Stockout Relative Drift", "max"),
            Mean_Cost_Rel_Drift=("Mean Total Cost Relative Drift", "mean"),
            Max_Cost_Rel_Drift=("Mean Total Cost Relative Drift", "max"),
        )
        .reset_index()
    )
    grouped["Metric Safe Share"] = grouped["Metric_Safe_Rows"] / grouped["Rows"].replace(0, np.nan)
    grouped["Safe Share"] = grouped["Safe_Rows"] / grouped["Rows"].replace(0, np.nan)
    return grouped.sort_values(["Comparison", "Safe Share", "Domain"], ascending=[True, True, True])


def _comparison_summary(checks: pd.DataFrame, ranking: pd.DataFrame) -> pd.DataFrame:
    if checks.empty:
        return pd.DataFrame()
    grouped = (
        checks.groupby("Comparison", dropna=False)
        .agg(
            Instances=("Instance", "nunique"),
            Rows=("Domain", "size"),
            Both_Feasible=("Both Feasible", "sum"),
            Metric_Safe_Rows=("Metric Safe", "sum"),
            Safe_Rows=("Safe", "sum"),
            Max_Stockout_Rel_Drift=("Stockout Relative Drift", "max"),
            Max_Cost_Rel_Drift=("Mean Total Cost Relative Drift", "max"),
            Mean_Stockout_Rel_Drift=("Stockout Relative Drift", "mean"),
            Mean_Cost_Rel_Drift=("Mean Total Cost Relative Drift", "mean"),
        )
        .reset_index()
    )
    grouped["Metric Safe Share"] = grouped["Metric_Safe_Rows"] / grouped["Rows"].replace(0, np.nan)
    grouped["Safe Share"] = grouped["Safe_Rows"] / grouped["Rows"].replace(0, np.nan)
    flip_counts = (
        ranking.groupby("Comparison", dropna=False)
        .agg(Ranking_Flip_Instances=("Ranking Flip", "sum"))
        .reset_index()
    )
    grouped = grouped.merge(flip_counts, on="Comparison", how="left")
    return grouped.sort_values("Comparison")


def _write_report(
    path: Path,
    *,
    checks: pd.DataFrame,
    ranking: pd.DataFrame,
    domain_summary: pd.DataFrame,
    comparison_summary: pd.DataFrame,
    stockout_rel_threshold: float,
    cost_rel_threshold: float,
    scenario_path: Path,
    ortools_path: Path,
    vroom_path: Path,
    custom_specs: list[str],
) -> None:
    unsafe = checks[checks["Safe"] == False].copy()
    unstable_ranking = ranking[ranking["Ranking Flip"] == True].copy()
    full_required = _full_required_rule(unsafe, stockout_rel_threshold, cost_rel_threshold)
    lines = [
        "# Sector Stability Tolerance Report",
        "",
        "## Scope",
        "",
        "This branch defines a tolerance layer for domain-adapter outputs. It judges whether a candidate run can be treated as safe for exploration, or whether the final result must be confirmed with the full scenario/profile.",
        "",
        "Inputs used in this smoke run:",
        "",
        f"- Scenario reduction pair: `{scenario_path}`",
        f"- OR-Tools provider pair: `{ortools_path}`",
        f"- VROOM provider pair: `{vroom_path}`",
        f"- Custom comparison specs: {len(custom_specs)}",
        "",
        "## Tolerance Rules",
        "",
        f"- Stockout relative drift must be <= {stockout_rel_threshold:.1%}.",
        f"- mean_total_cost relative drift must be <= {cost_rel_threshold:.1%}.",
        "- Domain stockout ranking must not flip within the same instance.",
        "- Any feasibility mismatch is automatically final_full_required.",
        "",
        "Row status is `safe` only when all four checks pass. Otherwise the row is marked unstable or final_full_required.",
        "`Metric Safe` ignores ranking and only checks feasibility plus stockout/cost drift; `Safe` is stricter and also requires ranking stability.",
        "",
        "## Smoke Finding",
        "",
        _markdown_table(comparison_summary),
        "",
        "## Domain Summary",
        "",
        _markdown_table(domain_summary),
        "",
        "## Ranking Flips",
        "",
        _markdown_table(
            unstable_ranking[
                [
                    "Comparison",
                    "Instance",
                    "Baseline Ranking",
                    "Candidate Ranking",
                    "Stockout Spearman",
                ]
            ]
            if not unstable_ranking.empty
            else pd.DataFrame()
        ),
        "",
        "## Safe / Unstable Threshold Decision",
        "",
        full_required,
        "",
        "## Perturbation Interface",
        "",
        "Small perturbation runs should be passed through `--comparison NAME,BASE_LABEL,BASE_CSV,CANDIDATE_LABEL,CANDIDATE_CSV`. The CSVs must use the `run_domain_engine` schema: `instance`, `domain`, `feasible`, `stockout_rate`, and `mean_total_cost`.",
        "",
        "This smoke run does not claim perturbation stability unless a perturbation comparison is supplied. It only proves the tolerance judge can score fast/full and provider changes with one common rule set.",
        "",
        "## Correct Sentence",
        "",
        _correct_sentence(comparison_summary, unstable_ranking),
        "",
        "## Not Yet Correct Sentence",
        "",
        "Domain adapters are stable under every solver, scenario, provider, and perturbation choice.",
        "",
        "## Next Step",
        "",
        "Each feature branch should write its own final domain result CSV and feed it into this tolerance judge. Decision-driving README numbers should be backed by a safe row set or by a full-scenario confirmation.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _full_required_rule(unsafe: pd.DataFrame, stockout_threshold: float, cost_threshold: float) -> str:
    if unsafe.empty:
        return (
            "All smoke rows are safe under the current thresholds. Fast mode can be used for exploration in these "
            "profiles, while final reports should still include full-scenario confirmation for decision-driving claims."
        )
    comparisons = ", ".join(sorted(unsafe["Comparison"].dropna().astype(str).unique().tolist()))
    return (
        f"Full confirmation is required for at least one row in: {comparisons}. A row becomes unsafe when stockout "
        f"drift exceeds {stockout_threshold:.1%}, mean_total_cost drift exceeds {cost_threshold:.1%}, ranking flips, "
        "or feasibility changes."
    )


def _correct_sentence(summary: pd.DataFrame, ranking_flips: pd.DataFrame) -> str:
    if summary.empty:
        return "No stability result was produced."
    safe = summary[summary["Safe Share"] >= 1.0]
    unsafe = summary[summary["Safe Share"] < 1.0]
    if unsafe.empty:
        names = ", ".join(summary["Comparison"].astype(str).tolist())
        return f"In this smoke run, {names} stayed inside the tolerance envelope."
    safe_names = ", ".join(safe["Comparison"].astype(str).tolist()) or "none"
    unsafe_names = ", ".join(unsafe["Comparison"].astype(str).tolist())
    flip_note = " Ranking flips were observed." if not ranking_flips.empty else ""
    return (
        f"In this smoke run, safe comparisons: {safe_names}; comparisons requiring full confirmation: "
        f"{unsafe_names}.{flip_note}"
    )


def _stockout_order(frame: pd.DataFrame, column: str) -> list[str]:
    ordered = frame[["Domain", column]].copy()
    ordered["Domain"] = ordered["Domain"].astype(str)
    ordered = ordered.sort_values([column, "Domain"], ascending=[False, True])
    return ordered["Domain"].tolist()


def _spearman_from_orders(baseline_order: list[str], candidate_order: list[str]) -> float:
    common = [domain for domain in baseline_order if domain in set(candidate_order)]
    if len(common) < 2:
        return float("nan")
    baseline_rank = {domain: rank for rank, domain in enumerate(baseline_order, start=1)}
    candidate_rank = {domain: rank for rank, domain in enumerate(candidate_order, start=1)}
    x = np.asarray([baseline_rank[domain] for domain in common], dtype=float)
    y = np.asarray([candidate_rank[domain] for domain in common], dtype=float)
    return _pearsonr(x, y)


def _pearsonr(x: np.ndarray, y: np.ndarray) -> float:
    x_centered = x - x.mean()
    y_centered = y - y.mean()
    denom = math.sqrt(float(np.dot(x_centered, x_centered) * np.dot(y_centered, y_centered)))
    if denom == 0:
        return float("nan")
    return float(np.dot(x_centered, y_centered) / denom)


def _relative_drift(baseline: float, candidate: float) -> float:
    if math.isnan(baseline) or math.isnan(candidate):
        return float("nan")
    if abs(baseline) <= 1e-12:
        return 0.0 if abs(candidate) <= 1e-12 else float("inf")
    return abs(candidate - baseline) / abs(baseline)


def _abs_drift(baseline: float, candidate: float) -> float:
    if math.isnan(baseline) or math.isnan(candidate):
        return float("nan")
    return abs(candidate - baseline)


def _customers_from_name(instance: str) -> float:
    match = re.search(r"-n(\d+)-", instance)
    if not match:
        return float("nan")
    return float(int(match.group(1)) - 1)


def _size_bucket(customers: float) -> str:
    if math.isnan(customers):
        return ""
    if customers <= 150:
        return "small"
    if customers <= 220:
        return "medium"
    return "large"


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if pd.isna(value):
        return False
    return str(value).strip().lower() in {"true", "1", "yes"}


def _as_float(value: object) -> float:
    try:
        if pd.isna(value):
            return float("nan")
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def _join_reasons(left: object, right: object) -> str:
    reasons = []
    for value in [left, right]:
        if pd.isna(value):
            continue
        text = str(value).strip()
        if text:
            reasons.append(text)
    return "; ".join(reasons)


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


if __name__ == "__main__":
    main()
