from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_INPUTS = {
    "candidate_results": "robust_route_candidate_results.csv",
    "winners": "robust_route_winners.csv",
}

OPTIONAL_INPUTS = {
    "full_confirmation": "robust_route_winner_full_confirmation.csv",
    "ranking_stability": "robust_route_winner_ranking_stability.csv",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize robust route selection outputs into decision-readiness metrics."
    )
    parser.add_argument("--out-dir", required=True, help="Directory produced by run_robust_route_selection.py.")
    parser.add_argument(
        "--analysis-out-dir",
        default=None,
        help="Where summary CSV/MD files should be written. Defaults to --out-dir.",
    )
    parser.add_argument("--top-n", type=int, default=10, help="Rows to include in report frequency tables.")
    args = parser.parse_args()

    source_dir = Path(args.out_dir)
    analysis_dir = Path(args.analysis_out_dir) if args.analysis_out_dir else source_dir
    analysis_dir.mkdir(parents=True, exist_ok=True)

    frames = _read_inputs(source_dir)
    candidate_results = frames["candidate_results"]
    winners = frames["winners"]
    full_confirmation = frames.get("full_confirmation", pd.DataFrame())
    ranking_stability = frames.get("ranking_stability", pd.DataFrame())

    aggregate_summary = _aggregate_summary(candidate_results, winners, full_confirmation, ranking_stability)
    domain_diversity = _domain_winner_diversity(winners, full_confirmation)
    candidate_frequency = _candidate_frequency(winners)
    instance_diversity = _instance_diversity(winners, full_confirmation)
    certification_summary = _certification_summary(winners, full_confirmation, ranking_stability)
    final_full_required = _final_full_required(full_confirmation)

    outputs = {
        "robust_route_aggregate_summary.csv": aggregate_summary,
        "robust_route_winner_diversity_by_domain.csv": domain_diversity,
        "robust_route_candidate_frequency.csv": candidate_frequency,
        "robust_route_instance_diversity.csv": instance_diversity,
        "robust_route_certification_summary.csv": certification_summary,
        "robust_route_final_full_required.csv": final_full_required,
    }
    for filename, frame in outputs.items():
        frame.to_csv(analysis_dir / filename, index=False)

    _write_report(
        analysis_dir / "robust_route_selection_analysis_report.md",
        source_dir=source_dir,
        aggregate_summary=aggregate_summary,
        domain_diversity=domain_diversity,
        candidate_frequency=candidate_frequency,
        instance_diversity=instance_diversity,
        certification_summary=certification_summary,
        final_full_required=final_full_required,
        ranking_stability=ranking_stability,
        top_n=args.top_n,
    )

    print(f"Saved robust route selection analysis to {analysis_dir}")


def _read_inputs(source_dir: Path) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    missing = []
    for key, filename in REQUIRED_INPUTS.items():
        path = source_dir / filename
        if not path.exists():
            missing.append(str(path))
            continue
        frames[key] = pd.read_csv(path)
    if missing:
        raise FileNotFoundError("Missing required robust route selection outputs: " + ", ".join(missing))

    for key, filename in OPTIONAL_INPUTS.items():
        path = source_dir / filename
        frames[key] = pd.read_csv(path) if path.exists() else pd.DataFrame()
    return frames


def _aggregate_summary(
    candidate_results: pd.DataFrame,
    winners: pd.DataFrame,
    full_confirmation: pd.DataFrame,
    ranking_stability: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        {"Metric": "instances", "Value": _safe_nunique(candidate_results, "Instance")},
        {"Metric": "domains", "Value": _safe_nunique(candidate_results, "Domain")},
        {"Metric": "candidate_rows", "Value": len(candidate_results)},
        {"Metric": "candidate_feasible_rows", "Value": _safe_bool_sum(candidate_results, "Candidate Feasible")},
        {"Metric": "winner_rows", "Value": len(winners)},
        {"Metric": "winner_domains", "Value": _safe_nunique(winners, "Domain")},
        {"Metric": "unique_winning_candidates", "Value": _safe_nunique(winners, "Candidate")},
        {"Metric": "unique_winning_route_plans", "Value": _safe_nunique(winners, "Route Plan")},
        {"Metric": "unique_winning_providers", "Value": _safe_nunique(winners, "Routing Provider")},
    ]

    if not full_confirmation.empty:
        rows.extend(
            [
                {"Metric": "confirmed_winner_rows", "Value": len(full_confirmation)},
                {
                    "Metric": "confirm_feasible_rate",
                    "Value": _safe_bool_mean(full_confirmation, "Confirm Feasible"),
                },
                {
                    "Metric": "metric_stability_safe_rate",
                    "Value": _safe_bool_mean(full_confirmation, "Metric Stability Safe"),
                },
                {
                    "Metric": "strict_stability_safe_rate",
                    "Value": _safe_bool_mean(full_confirmation, "Strict Stability Safe"),
                },
                {
                    "Metric": "final_full_required_rows",
                    "Value": int((full_confirmation.get("Stability Status", pd.Series(dtype=object)) != "safe").sum()),
                },
                {
                    "Metric": "max_stockout_relative_drift",
                    "Value": _safe_numeric_max(full_confirmation, "Stockout Relative Drift"),
                },
                {
                    "Metric": "max_mean_total_cost_relative_drift",
                    "Value": _safe_numeric_max(full_confirmation, "Mean Total Cost Relative Drift"),
                },
            ]
        )
    else:
        rows.append({"Metric": "full_confirmation_present", "Value": 0})

    if not ranking_stability.empty:
        rows.extend(
            [
                {"Metric": "ranking_rows", "Value": len(ranking_stability)},
                {"Metric": "ranking_flip_rate", "Value": _safe_bool_mean(ranking_stability, "Ranking Flip")},
                {"Metric": "mean_stockout_spearman", "Value": _safe_numeric_mean(ranking_stability, "Stockout Spearman")},
            ]
        )
    else:
        rows.append({"Metric": "ranking_stability_present", "Value": 0})

    return pd.DataFrame(rows)


def _domain_winner_diversity(winners: pd.DataFrame, full_confirmation: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()

    rows = []
    for domain, group in winners.groupby("Domain", dropna=False):
        candidate_counts = group["Candidate"].value_counts(dropna=False)
        route_plan_counts = group["Route Plan"].value_counts(dropna=False)
        top_candidate = str(candidate_counts.index[0]) if not candidate_counts.empty else ""
        top_route_plan = str(route_plan_counts.index[0]) if not route_plan_counts.empty else ""
        row = {
            "Domain": domain,
            "Winner Rows": len(group),
            "Instances": group["Instance"].nunique(),
            "Unique Winning Candidates": group["Candidate"].nunique(),
            "Unique Winning Route Plans": group["Route Plan"].nunique(),
            "Unique Winning Providers": group["Routing Provider"].nunique()
            if "Routing Provider" in group.columns
            else np.nan,
            "Winner Candidate Entropy": _entropy(candidate_counts),
            "Winner Route Plan Entropy": _entropy(route_plan_counts),
            "Normalized Winner Candidate Entropy": _normalized_entropy(candidate_counts),
            "Top Candidate": top_candidate,
            "Top Candidate Count": int(candidate_counts.iloc[0]) if not candidate_counts.empty else 0,
            "Top Candidate Share": float(candidate_counts.iloc[0] / len(group)) if len(group) else np.nan,
            "Top Route Plan": top_route_plan,
            "Top Route Plan Count": int(route_plan_counts.iloc[0]) if not route_plan_counts.empty else 0,
            "Top Route Plan Share": float(route_plan_counts.iloc[0] / len(group)) if len(group) else np.nan,
        }
        if not full_confirmation.empty and "Domain" in full_confirmation.columns:
            confirmed = full_confirmation[full_confirmation["Domain"] == domain]
            row.update(
                {
                    "Confirmed Rows": len(confirmed),
                    "Strict Stability Safe Rate": _safe_bool_mean(confirmed, "Strict Stability Safe"),
                    "Metric Stability Safe Rate": _safe_bool_mean(confirmed, "Metric Stability Safe"),
                    "Final Full Required Rows": int(
                        (confirmed.get("Stability Status", pd.Series(dtype=object)) != "safe").sum()
                    )
                    if not confirmed.empty
                    else 0,
                    "Max Stockout Relative Drift": _safe_numeric_max(confirmed, "Stockout Relative Drift"),
                    "Max Mean Total Cost Relative Drift": _safe_numeric_max(
                        confirmed, "Mean Total Cost Relative Drift"
                    ),
                }
            )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["Domain"]).reset_index(drop=True)


def _candidate_frequency(winners: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()
    keys = ["Domain", "Candidate", "Routing Provider", "Route Plan"]
    existing = [col for col in keys if col in winners.columns]
    counts = winners.groupby(existing, dropna=False).size().reset_index(name="Winner Count")
    domain_totals = winners.groupby("Domain", dropna=False).size().rename("Domain Winner Rows").reset_index()
    counts = counts.merge(domain_totals, on="Domain", how="left")
    counts["Winner Share Within Domain"] = counts["Winner Count"] / counts["Domain Winner Rows"]
    return counts.sort_values(["Domain", "Winner Count", "Candidate"], ascending=[True, False, True]).reset_index(
        drop=True
    )


def _instance_diversity(winners: pd.DataFrame, full_confirmation: pd.DataFrame) -> pd.DataFrame:
    if winners.empty:
        return pd.DataFrame()
    rows = []
    for instance, group in winners.groupby("Instance", dropna=False):
        candidate_counts = group["Candidate"].value_counts(dropna=False)
        route_plan_counts = group["Route Plan"].value_counts(dropna=False)
        row = {
            "Instance": instance,
            "Customers": _first_number(group, "Customers"),
            "Domains": group["Domain"].nunique(),
            "Winner Rows": len(group),
            "Unique Winning Candidates Across Domains": group["Candidate"].nunique(),
            "Unique Winning Route Plans Across Domains": group["Route Plan"].nunique(),
            "Route Plan Entropy Across Domains": _entropy(route_plan_counts),
            "Normalized Route Plan Entropy Across Domains": _normalized_entropy(route_plan_counts),
            "Candidate Entropy Across Domains": _entropy(candidate_counts),
            "All Domains Same Candidate": bool(group["Candidate"].nunique() <= 1),
            "All Domains Same Route Plan": bool(group["Route Plan"].nunique() <= 1),
        }
        if not full_confirmation.empty and "Instance" in full_confirmation.columns:
            confirmed = full_confirmation[full_confirmation["Instance"] == instance]
            row.update(
                {
                    "Confirmed Winner Rows": len(confirmed),
                    "Strict Stability Safe Rows": _safe_bool_sum(confirmed, "Strict Stability Safe"),
                    "Final Full Required Rows": int(
                        (confirmed.get("Stability Status", pd.Series(dtype=object)) != "safe").sum()
                    )
                    if not confirmed.empty
                    else 0,
                    "Ranking Flip": bool(confirmed["Ranking Flip"].fillna(False).astype(bool).any())
                    if "Ranking Flip" in confirmed.columns and not confirmed.empty
                    else False,
                    "Max Stockout Relative Drift": _safe_numeric_max(confirmed, "Stockout Relative Drift"),
                    "Max Mean Total Cost Relative Drift": _safe_numeric_max(
                        confirmed, "Mean Total Cost Relative Drift"
                    ),
                }
            )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["Instance"]).reset_index(drop=True)


def _certification_summary(
    winners: pd.DataFrame,
    full_confirmation: pd.DataFrame,
    ranking_stability: pd.DataFrame,
) -> pd.DataFrame:
    if full_confirmation.empty:
        return pd.DataFrame(
            [
                {
                    "Scope": "all",
                    "Winner Rows": len(winners),
                    "Confirmed Rows": 0,
                    "Strict Stability Safe Rows": 0,
                    "Strict Stability Safe Rate": np.nan,
                    "Final Full Required Rows": np.nan,
                    "Ranking Flip Rows": np.nan,
                }
            ]
        )

    rows = [
        {
            "Scope": "all",
            "Winner Rows": len(winners),
            "Confirmed Rows": len(full_confirmation),
            "Confirm Feasible Rows": _safe_bool_sum(full_confirmation, "Confirm Feasible"),
            "Metric Stability Safe Rows": _safe_bool_sum(full_confirmation, "Metric Stability Safe"),
            "Strict Stability Safe Rows": _safe_bool_sum(full_confirmation, "Strict Stability Safe"),
            "Strict Stability Safe Rate": _safe_bool_mean(full_confirmation, "Strict Stability Safe"),
            "Final Full Required Rows": int(
                (full_confirmation.get("Stability Status", pd.Series(dtype=object)) != "safe").sum()
            ),
            "Ranking Flip Rows": _safe_bool_sum(ranking_stability, "Ranking Flip")
            if not ranking_stability.empty
            else np.nan,
        }
    ]
    for domain, group in full_confirmation.groupby("Domain", dropna=False):
        rows.append(
            {
                "Scope": f"domain:{domain}",
                "Winner Rows": len(winners[winners["Domain"] == domain]) if "Domain" in winners.columns else np.nan,
                "Confirmed Rows": len(group),
                "Confirm Feasible Rows": _safe_bool_sum(group, "Confirm Feasible"),
                "Metric Stability Safe Rows": _safe_bool_sum(group, "Metric Stability Safe"),
                "Strict Stability Safe Rows": _safe_bool_sum(group, "Strict Stability Safe"),
                "Strict Stability Safe Rate": _safe_bool_mean(group, "Strict Stability Safe"),
                "Final Full Required Rows": int(
                    (group.get("Stability Status", pd.Series(dtype=object)) != "safe").sum()
                ),
                "Ranking Flip Rows": _safe_bool_sum(group, "Ranking Flip") if "Ranking Flip" in group.columns else np.nan,
            }
        )
    return pd.DataFrame(rows)


def _final_full_required(full_confirmation: pd.DataFrame) -> pd.DataFrame:
    if full_confirmation.empty or "Stability Status" not in full_confirmation.columns:
        return pd.DataFrame()
    required = full_confirmation[full_confirmation["Stability Status"] != "safe"].copy()
    cols = [
        "Instance",
        "Domain",
        "Candidate",
        "Route Plan",
        "Routing Provider",
        "Confirm Feasible",
        "Stockout Relative Drift",
        "Mean Total Cost Relative Drift",
        "Metric Stability Safe",
        "Ranking Flip",
        "Strict Stability Safe",
        "Stability Status",
    ]
    return required[[col for col in cols if col in required.columns]].reset_index(drop=True)


def _write_report(
    path: Path,
    source_dir: Path,
    aggregate_summary: pd.DataFrame,
    domain_diversity: pd.DataFrame,
    candidate_frequency: pd.DataFrame,
    instance_diversity: pd.DataFrame,
    certification_summary: pd.DataFrame,
    final_full_required: pd.DataFrame,
    ranking_stability: pd.DataFrame,
    top_n: int,
) -> None:
    lines = [
        "# Robust Route Selection Analysis",
        "",
        "## Scope",
        "",
        f"- Source directory: `{source_dir}`",
        "- This report summarizes route-candidate winners after the common stochastic decision layer.",
        "- `Strict Stability Safe` means full-scenario confirmation is feasible, metric drift is within thresholds, and no domain stockout ranking flip was observed.",
        "",
        "## Aggregate Summary",
        "",
        _markdown_table(aggregate_summary),
        "",
        "## Domain-Specific Winner Diversity",
        "",
        _markdown_table(domain_diversity),
        "",
        "## Top Candidate Frequencies",
        "",
        _markdown_table(candidate_frequency.head(top_n)),
        "",
        "## Instance-Level Route Plan Diversity",
        "",
        _markdown_table(instance_diversity),
        "",
        "## Certified Winner Rate",
        "",
        _markdown_table(certification_summary),
        "",
        "## Final Full Required Rows",
        "",
    ]
    if final_full_required.empty:
        lines.append("No non-safe full-confirmed winner rows were found.")
    else:
        lines.append(_markdown_table(final_full_required))

    lines.extend(["", "## Ranking Stability", ""])
    if ranking_stability.empty:
        lines.append("No ranking stability file was present or produced.")
    else:
        lines.append(_markdown_table(ranking_stability))

    lines.extend(
        [
            "",
            "## Suggested Interpretation",
            "",
            "- Winner diversity is the main signal for whether sector objectives change route choice.",
            "- Certified winner rate is the decision-readiness signal; low certification means route winners remain exploratory.",
            "- Route plan entropy across domains separates one-size-fits-all routing from genuinely domain-specific choices.",
            "- `final_full_required` rows should not support final claims until rerun or inspected with full planning history.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _entropy(counts: pd.Series) -> float:
    total = float(counts.sum())
    if total <= 0:
        return np.nan
    probabilities = [float(count) / total for count in counts if count > 0]
    entropy = float(-sum(prob * math.log(prob, 2) for prob in probabilities))
    return 0.0 if abs(entropy) <= 1e-12 else entropy


def _normalized_entropy(counts: pd.Series) -> float:
    if len(counts) <= 1:
        return 0.0 if len(counts) == 1 else np.nan
    entropy = _entropy(counts)
    return float(entropy / math.log(len(counts), 2)) if not pd.isna(entropy) else np.nan


def _safe_nunique(frame: pd.DataFrame, column: str) -> int:
    return int(frame[column].nunique()) if column in frame.columns and not frame.empty else 0


def _safe_bool_sum(frame: pd.DataFrame, column: str) -> int:
    if frame.empty or column not in frame.columns:
        return 0
    return int(frame[column].fillna(False).astype(bool).sum())


def _safe_bool_mean(frame: pd.DataFrame, column: str) -> float:
    if frame.empty or column not in frame.columns:
        return np.nan
    return float(frame[column].fillna(False).astype(bool).mean())


def _safe_numeric_mean(frame: pd.DataFrame, column: str) -> float:
    if frame.empty or column not in frame.columns:
        return np.nan
    values = pd.to_numeric(frame[column], errors="coerce")
    return float(values.mean()) if values.notna().any() else np.nan


def _safe_numeric_max(frame: pd.DataFrame, column: str) -> float:
    if frame.empty or column not in frame.columns:
        return np.nan
    values = pd.to_numeric(frame[column], errors="coerce")
    return float(values.max()) if values.notna().any() else np.nan


def _first_number(frame: pd.DataFrame, column: str) -> float:
    if frame.empty or column not in frame.columns:
        return np.nan
    values = pd.to_numeric(frame[column], errors="coerce").dropna()
    return float(values.iloc[0]) if not values.empty else np.nan


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
    headers = [str(col) for col in display.columns]
    rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for _, row in display.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(rows)


if __name__ == "__main__":
    main()
