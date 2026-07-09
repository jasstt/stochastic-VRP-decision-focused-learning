from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare full-confirmed robust route selection runs across score metrics."
    )
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        help="Run spec in the form score_metric=path/to/output_dir. Pass once per run.",
    )
    parser.add_argument("--out-dir", required=True, help="Directory for comparison CSV/MD outputs.")
    parser.add_argument(
        "--audit-file",
        default=None,
        help="Optional X40 feasibility audit CSV for risk-stratified coverage summaries.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    audit = pd.read_csv(args.audit_file) if args.audit_file else pd.DataFrame()

    run_summaries = []
    certified_instances = []
    risk_rows = []
    for metric, run_dir in [_parse_run_spec(spec) for spec in args.run]:
        data = _read_run(run_dir)
        summary = _summarize_run(metric, run_dir, data)
        run_summaries.append(summary)
        certified_instances.append(_certified_instance_rows(metric, data))
        if not audit.empty:
            risk_rows.append(_risk_summary(metric, data, audit))

    comparison = pd.DataFrame(run_summaries)
    certified = pd.concat(certified_instances, ignore_index=True) if certified_instances else pd.DataFrame()
    risk_summary = pd.concat(risk_rows, ignore_index=True) if risk_rows else pd.DataFrame()

    comparison.to_csv(out_dir / "robust_route_metric_comparison.csv", index=False)
    certified.to_csv(out_dir / "robust_route_certified_instance_diversity.csv", index=False)
    risk_summary.to_csv(out_dir / "robust_route_metric_comparison_by_audit_risk.csv", index=False)
    _write_report(out_dir / "robust_route_metric_comparison_report.md", comparison, certified, risk_summary)

    print(f"Saved robust route metric comparison to {out_dir}")


def _parse_run_spec(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise ValueError(f"Run spec must be score_metric=path, got {spec!r}")
    metric, path = spec.split("=", 1)
    return metric.strip(), Path(path.strip())


def _read_run(run_dir: Path) -> dict[str, pd.DataFrame]:
    files = {
        "candidate_results": "robust_route_candidate_results.csv",
        "winners": "robust_route_winners.csv",
        "full_confirmation": "robust_route_winner_full_confirmation.csv",
        "ranking_stability": "robust_route_winner_ranking_stability.csv",
    }
    out = {}
    missing = []
    for key, filename in files.items():
        path = run_dir / filename
        if not path.exists():
            missing.append(str(path))
        else:
            out[key] = pd.read_csv(path)
    if missing:
        raise FileNotFoundError("Missing run outputs: " + ", ".join(missing))
    return out


def _summarize_run(metric: str, run_dir: Path, data: dict[str, pd.DataFrame]) -> dict[str, object]:
    candidates = data["candidate_results"]
    winners = data["winners"]
    full = data["full_confirmation"]
    ranking = data["ranking_stability"]

    attempted_instances = set(candidates["Instance"].dropna().astype(str))
    winner_instances = set(winners["Instance"].dropna().astype(str))
    no_winner = sorted(attempted_instances - winner_instances)
    domains_expected = int(winners["Domain"].nunique()) if not winners.empty else 0

    instance_diversity = _instance_diversity(winners)
    domain_specific = instance_diversity[instance_diversity["Unique Route Plans"] > 1]
    certified_instances = _certified_instance_rows(metric, data)
    fully_certified = certified_instances[certified_instances["Fully Certified Instance"]]
    certified_diverse = fully_certified[fully_certified["Certified Unique Route Plans"] > 1]

    route_counts = winners["Route Plan"].value_counts(dropna=False)
    strict_safe = _bool_series(full, "Strict Stability Safe")
    metric_safe = _bool_series(full, "Metric Stability Safe")
    confirm_feasible = _bool_series(full, "Confirm Feasible")
    ranking_flip = _bool_series(ranking, "Ranking Flip")
    final_full_required = full["Stability Status"].fillna("") != "safe" if "Stability Status" in full else pd.Series(dtype=bool)

    return {
        "Score Metric": metric,
        "Run Directory": str(run_dir),
        "Attempted Instances": len(attempted_instances),
        "Candidate Rows": len(candidates),
        "Candidate Feasible Rows": int(_bool_series(candidates, "Candidate Feasible").sum()),
        "Winner Instances": len(winner_instances),
        "Winner Rows": len(winners),
        "No-Winner Instances": len(no_winner),
        "No-Winner List": ", ".join(no_winner),
        "Domain-Specific Instances": len(domain_specific),
        "Domain-Specific Share": _safe_ratio(len(domain_specific), len(instance_diversity)),
        "Confirmed Winner Rows": len(full),
        "Confirm Feasible Rows": int(confirm_feasible.sum()),
        "Metric-Safe Rows": int(metric_safe.sum()),
        "Strict-Safe Rows": int(strict_safe.sum()),
        "Strict-Safe Rate": _safe_ratio(int(strict_safe.sum()), len(full)),
        "Fully Certified Instances": int(fully_certified["Instance"].nunique()),
        "Certified Domain-Specific Instances": int(certified_diverse["Instance"].nunique()),
        "Certified Domain-Specific Share": _safe_ratio(
            int(certified_diverse["Instance"].nunique()),
            int(fully_certified["Instance"].nunique()),
        ),
        "Ranking Rows": len(ranking),
        "Ranking Flip Instances": int(ranking_flip.sum()),
        "Ranking Flip Rate": _safe_ratio(int(ranking_flip.sum()), len(ranking)),
        "Final Full Required Rows": int(final_full_required.sum()) if len(final_full_required) else 0,
        "Final Full Required Rate": _safe_ratio(int(final_full_required.sum()), len(full))
        if len(final_full_required)
        else np.nan,
        "Top Route Plan": str(route_counts.index[0]) if not route_counts.empty else "",
        "Top Route Plan Count": int(route_counts.iloc[0]) if not route_counts.empty else 0,
        "Top Route Plan Share": _safe_ratio(int(route_counts.iloc[0]), len(winners))
        if not route_counts.empty
        else np.nan,
        "Unique Winning Route Plans": int(winners["Route Plan"].nunique()) if "Route Plan" in winners else 0,
        "Expected Domains": domains_expected,
    }


def _instance_diversity(winners: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame(columns=["Instance", "Domains", "Unique Route Plans"])
    return (
        winners.groupby("Instance", dropna=False)
        .agg(Domains=("Domain", "nunique"), Unique_Route_Plans=("Route Plan", "nunique"))
        .reset_index()
        .rename(columns={"Unique_Route_Plans": "Unique Route Plans"})
    )


def _certified_instance_rows(metric: str, data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    winners = data["winners"]
    full = data["full_confirmation"].copy()
    domains_expected = int(winners["Domain"].nunique()) if not winners.empty else 0
    if full.empty:
        return pd.DataFrame()
    full["Strict Stability Safe Bool"] = _bool_series(full, "Strict Stability Safe")
    rows = []
    for instance, group in full.groupby("Instance", dropna=False):
        strict = group[group["Strict Stability Safe Bool"]]
        strict_domains = int(strict["Domain"].nunique()) if "Domain" in strict else 0
        rows.append(
            {
                "Score Metric": metric,
                "Instance": instance,
                "Winner Domains": int(group["Domain"].nunique()) if "Domain" in group else 0,
                "Strict-Safe Domains": strict_domains,
                "Fully Certified Instance": bool(domains_expected > 0 and strict_domains >= domains_expected),
                "Winner Unique Route Plans": int(group["Route Plan"].nunique()) if "Route Plan" in group else 0,
                "Certified Unique Route Plans": int(strict["Route Plan"].nunique()) if "Route Plan" in strict else 0,
                "Winner Domain-Specific": bool(group["Route Plan"].nunique() > 1) if "Route Plan" in group else False,
                "Certified Domain-Specific": bool(
                    domains_expected > 0 and strict_domains >= domains_expected and strict["Route Plan"].nunique() > 1
                )
                if "Route Plan" in strict
                else False,
            }
        )
    return pd.DataFrame(rows)


def _risk_summary(metric: str, data: dict[str, pd.DataFrame], audit: pd.DataFrame) -> pd.DataFrame:
    audit_cols = [
        "Instance",
        "Overall Audit Risk",
        "Capacity Pressure Risk",
        "Prev OR-Tools Anchor Feasible",
    ]
    available = [col for col in audit_cols if col in audit.columns]
    audit_small = audit[available].drop_duplicates("Instance")

    candidates = data["candidate_results"].merge(audit_small, on="Instance", how="left")
    winners = data["winners"].merge(audit_small, on="Instance", how="left")
    full = data["full_confirmation"].merge(audit_small, on="Instance", how="left")
    full["Strict Stability Safe Bool"] = _bool_series(full, "Strict Stability Safe")

    rows = []
    for risk_col in ["Overall Audit Risk", "Capacity Pressure Risk", "Prev OR-Tools Anchor Feasible"]:
        if risk_col not in candidates.columns:
            continue
        levels = sorted(candidates[risk_col].dropna().unique(), key=lambda value: str(value))
        for level in levels:
            c_group = candidates[candidates[risk_col] == level]
            w_group = winners[winners[risk_col] == level]
            f_group = full[full[risk_col] == level]
            diversity = _instance_diversity(w_group)
            rows.append(
                {
                    "Score Metric": metric,
                    "Risk Dimension": risk_col,
                    "Risk Level": str(level),
                    "Candidate Rows": len(c_group),
                    "Candidate Feasible Rows": int(_bool_series(c_group, "Candidate Feasible").sum()),
                    "Winner Rows": len(w_group),
                    "Winner Instances": int(w_group["Instance"].nunique()) if not w_group.empty else 0,
                    "Domain-Specific Instances": int((diversity["Unique Route Plans"] > 1).sum())
                    if not diversity.empty
                    else 0,
                    "Full Confirmation Rows": len(f_group),
                    "Strict-Safe Rows": int(f_group["Strict Stability Safe Bool"].sum()) if not f_group.empty else 0,
                }
            )
    return pd.DataFrame(rows)


def _write_report(
    path: Path,
    comparison: pd.DataFrame,
    certified: pd.DataFrame,
    risk_summary: pd.DataFrame,
) -> None:
    lines = [
        "# Robust Route Metric Comparison",
        "",
        "## Scope",
        "",
        "This compares first-class X40 robust-route-selection runs. Each run reran route-candidate scoring, LP allocation, and full-scenario winner confirmation under its own `--score-metric`.",
        "",
        "## Comparison",
        "",
        _markdown_table(comparison),
        "",
        "## Certified Instance Diversity",
        "",
        _markdown_table(certified),
        "",
        "## Feasibility / Audit-Risk Coverage",
        "",
        _markdown_table(risk_summary),
        "",
        "## Interpretation Rule",
        "",
        "- `Domain-Specific Instances` counts full-confirmed winner-producing instances where domains selected more than one route plan.",
        "- `Certified Domain-Specific Instances` is stricter: all expected domains in that instance must be `Strict Stability Safe`, and the certified route plans must still differ.",
        "- `Metric-Safe Rows` alone are not decision-ready if stockout ranking flips; use `Strict-Safe Rows` for final claims.",
        "- These runs are OR-Tools-only and proxy-demand benchmark runs; they do not establish solver-agnostic or real-sector demand claims.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _bool_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if frame.empty or column not in frame.columns:
        return pd.Series([False] * len(frame), index=frame.index)
    values = frame[column]
    if pd.api.types.is_bool_dtype(values):
        return values.fillna(False).astype(bool)
    return values.fillna(False).map(lambda value: str(value).strip().lower() in {"true", "1", "yes"})


def _safe_ratio(numerator: int, denominator: int) -> float:
    return float(numerator / denominator) if denominator else np.nan


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


if __name__ == "__main__":
    main()
