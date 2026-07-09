from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_METRICS = [
    "mean_total_cost",
    "mean_domain_loss",
    "stockout_rate",
    "mean_shortfall",
    "cvar90_total_cost",
    "p90_total_cost",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Re-select robust route winners from existing candidate results under "
            "alternative score metrics."
        )
    )
    parser.add_argument("--out-dir", required=True, help="Directory with robust_route_candidate_results.csv.")
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=DEFAULT_METRICS,
        help="Candidate result metric columns to minimize.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    candidate_path = out_dir / "robust_route_candidate_results.csv"
    if not candidate_path.exists():
        raise FileNotFoundError(candidate_path)

    candidate_results = pd.read_csv(candidate_path)
    winners = _select_metric_winners(candidate_results, args.metrics)
    summary = _metric_summary(winners)
    frequency = _metric_frequency(winners)
    instance_diversity = _metric_instance_diversity(winners)

    winners.to_csv(out_dir / "robust_route_score_metric_winners.csv", index=False)
    summary.to_csv(out_dir / "robust_route_score_metric_sensitivity.csv", index=False)
    frequency.to_csv(out_dir / "robust_route_score_metric_frequency.csv", index=False)
    instance_diversity.to_csv(out_dir / "robust_route_score_metric_instance_diversity.csv", index=False)
    _write_report(
        out_dir / "robust_route_score_metric_sensitivity_report.md",
        summary=summary,
        frequency=frequency,
        instance_diversity=instance_diversity,
    )
    print(f"Saved score metric sensitivity analysis to {out_dir}")


def _select_metric_winners(candidate_results: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    if candidate_results.empty:
        return pd.DataFrame()

    feasible = candidate_results[candidate_results["Candidate Feasible"].fillna(False).astype(bool)].copy()
    rows: list[pd.DataFrame] = []
    for metric in metrics:
        if metric not in feasible.columns:
            continue
        scored = feasible.copy()
        scored[metric] = pd.to_numeric(scored[metric], errors="coerce")
        scored = scored[scored[metric].notna()]
        if scored.empty:
            continue
        idx = scored.groupby(["Instance", "Domain"], dropna=False)[metric].idxmin()
        winners = scored.loc[idx].copy()
        winners["Metric"] = metric
        winners["Metric Score Value"] = winners[metric]
        rows.append(winners)
    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True).sort_values(["Metric", "Instance", "Domain"]).reset_index(drop=True)


def _metric_summary(winners: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()

    rows = []
    for metric, group in winners.groupby("Metric", sort=False, dropna=False):
        instance_diversity = _instance_route_diversity(group)
        route_counts = group["Route Plan"].value_counts(dropna=False)
        candidate_counts = group["Candidate"].value_counts(dropna=False)
        top_route_plan = str(route_counts.index[0]) if not route_counts.empty else ""
        rows.append(
            {
                "Metric": metric,
                "Winner Rows": len(group),
                "Winner Instances": group["Instance"].nunique(),
                "Unique Winning Route Plans": group["Route Plan"].nunique(),
                "Unique Winning Candidates": group["Candidate"].nunique(),
                "Instances With Domain-Specific Route Choice": int(
                    (instance_diversity["Unique Route Plans Across Domains"] > 1).sum()
                ),
                "Share Domain-Specific Instances": _safe_ratio(
                    int((instance_diversity["Unique Route Plans Across Domains"] > 1).sum()),
                    len(instance_diversity),
                ),
                "Mean Unique Route Plans Across Domains": _safe_mean(
                    instance_diversity["Unique Route Plans Across Domains"]
                ),
                "Max Unique Route Plans Across Domains": _safe_max(
                    instance_diversity["Unique Route Plans Across Domains"]
                ),
                "Top Route Plan": top_route_plan,
                "Top Route Plan Count": int(route_counts.iloc[0]) if not route_counts.empty else 0,
                "Top Route Plan Share": _safe_ratio(int(route_counts.iloc[0]), len(group))
                if not route_counts.empty
                else np.nan,
                "Top Candidate": str(candidate_counts.index[0]) if not candidate_counts.empty else "",
                "Top Candidate Share": _safe_ratio(int(candidate_counts.iloc[0]), len(group))
                if not candidate_counts.empty
                else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _metric_frequency(winners: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()
    keys = ["Metric", "Domain", "Route Plan"]
    counts = winners.groupby(keys, dropna=False).size().reset_index(name="Winner Count")
    totals = winners.groupby(["Metric", "Domain"], dropna=False).size().reset_index(name="Domain Winner Rows")
    counts = counts.merge(totals, on=["Metric", "Domain"], how="left")
    counts["Winner Share Within Domain"] = counts["Winner Count"] / counts["Domain Winner Rows"]
    return counts.sort_values(["Metric", "Domain", "Winner Count"], ascending=[True, True, False]).reset_index(
        drop=True
    )


def _metric_instance_diversity(winners: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()

    rows = []
    for metric, metric_group in winners.groupby("Metric", sort=False, dropna=False):
        rows.extend(_instance_route_diversity(metric_group, metric=metric).to_dict("records"))
    return pd.DataFrame(rows).sort_values(["Metric", "Instance"]).reset_index(drop=True)


def _instance_route_diversity(winners: pd.DataFrame, metric: str | None = None) -> pd.DataFrame:
    rows = []
    for instance, group in winners.groupby("Instance", dropna=False):
        row = {
            "Instance": instance,
            "Domains": group["Domain"].nunique(),
            "Unique Route Plans Across Domains": group["Route Plan"].nunique(),
            "Unique Candidates Across Domains": group["Candidate"].nunique(),
            "All Domains Same Route Plan": bool(group["Route Plan"].nunique() <= 1),
            "Route Plans": " | ".join(
                f"{domain}:{plan}"
                for domain, plan in group.sort_values("Domain")[["Domain", "Route Plan"]].itertuples(
                    index=False, name=None
                )
            ),
        }
        if metric is not None:
            row = {"Metric": metric, **row}
        rows.append(row)
    return pd.DataFrame(rows)


def _write_report(
    path: Path,
    summary: pd.DataFrame,
    frequency: pd.DataFrame,
    instance_diversity: pd.DataFrame,
) -> None:
    lines = [
        "# Robust Route Score Metric Sensitivity",
        "",
        "## Purpose",
        "",
        "This diagnostic reuses the same candidate result table and changes only the winner score metric.",
        "It does not rerun routing or LP solves; it asks whether the winner decision is dominated by the chosen objective column.",
        "",
        "## Metric Summary",
        "",
        _markdown_table(summary),
        "",
        "## Route Plan Frequency By Domain",
        "",
        _markdown_table(frequency),
        "",
        "## Instance Diversity",
        "",
        _markdown_table(instance_diversity),
        "",
        "## Interpretation Rule",
        "",
        "- If `mean_total_cost` has low diversity but domain-loss metrics have higher diversity, route cost is dominating the default winner objective.",
        "- Domain-specific route switching should be claimed only for the metric under which it is measured.",
        "- This is a post-hoc diagnostic from feasible candidate rows, not a full-scenario certification by itself.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_bool_dtype(display[col]):
            display[col] = display[col].map(lambda value: "yes" if bool(value) else "no")
        elif pd.api.types.is_numeric_dtype(display[col]):
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.6g}")
        else:
            display[col] = display[col].fillna("")
    rows = [
        "| " + " | ".join(str(col) for col in display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(rows)


def _safe_ratio(numerator: int, denominator: int) -> float:
    return float(numerator / denominator) if denominator else np.nan


def _safe_mean(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce")
    return float(values.mean()) if values.notna().any() else np.nan


def _safe_max(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce")
    return float(values.max()) if values.notna().any() else np.nan


if __name__ == "__main__":
    main()
