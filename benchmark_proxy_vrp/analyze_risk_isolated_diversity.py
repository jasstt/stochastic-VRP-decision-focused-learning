from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split certified route diversity by X40 audit-risk bucket."
    )
    parser.add_argument(
        "--comparison-dir",
        required=True,
        help="Directory from compare_robust_route_selection_runs.py.",
    )
    parser.add_argument("--audit-file", required=True, help="X40 feasibility audit CSV.")
    parser.add_argument("--out-dir", required=True, help="Output directory for risk-isolation reports.")
    args = parser.parse_args()

    comparison_dir = Path(args.comparison_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    certified = pd.read_csv(comparison_dir / "robust_route_certified_instance_diversity.csv")
    comparison = pd.read_csv(comparison_dir / "robust_route_metric_comparison.csv")
    audit = pd.read_csv(args.audit_file)

    labelled = _label_instances(certified, audit)
    summary = _summarize(labelled)
    decision = _decision(summary)
    medium_instances = _medium_instance_list(audit)

    labelled.to_csv(out_dir / "risk_isolated_instance_diversity.csv", index=False)
    summary.to_csv(out_dir / "risk_isolated_diversity_summary.csv", index=False)
    pd.DataFrame({"Instance": medium_instances}).to_csv(out_dir / "anchor_feasible_medium_risk_instances.csv", index=False)
    _write_diversity_report(out_dir / "risk_isolated_diversity_report.md", summary, labelled)
    _write_decision_report(
        out_dir / "risk_isolation_decision_report.md",
        summary=summary,
        decision=decision,
        comparison=comparison,
        medium_instances=medium_instances,
    )
    print(f"Saved risk-isolated diversity analysis to {out_dir}")


def _label_instances(certified: pd.DataFrame, audit: pd.DataFrame) -> pd.DataFrame:
    audit_small = audit[
        [
            "Instance",
            "Overall Audit Risk",
            "Capacity Pressure Risk",
            "Prev OR-Tools Anchor Feasible",
        ]
    ].drop_duplicates("Instance")
    labelled = certified.merge(audit_small, on="Instance", how="left")
    anchor_feasible = _bool_series(labelled, "Prev OR-Tools Anchor Feasible")
    medium_or_low = labelled["Overall Audit Risk"].fillna("").str.lower().isin(["medium", "low"])
    labelled["Risk Isolation Group"] = np.where(
        anchor_feasible & medium_or_low,
        "anchor_feasible_medium_risk",
        "high_risk_or_anchor_infeasible",
    )
    return labelled


def _summarize(labelled: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric, metric_group in labelled.groupby("Score Metric", dropna=False):
        for risk_group, group in metric_group.groupby("Risk Isolation Group", dropna=False):
            fully = _bool_series(group, "Fully Certified Instance")
            certified_diverse = _bool_series(group, "Certified Domain-Specific")
            winner_diverse = _bool_series(group, "Winner Domain-Specific")
            rows.append(
                {
                    "Score Metric": metric,
                    "Risk Isolation Group": risk_group,
                    "Instances": int(group["Instance"].nunique()),
                    "Winner Domain-Specific Instances": int(winner_diverse.sum()),
                    "Fully Certified Instances": int(fully.sum()),
                    "Certified Domain-Specific Instances": int(certified_diverse.sum()),
                    "Certified Diversity Share": _safe_ratio(int(certified_diverse.sum()), int(fully.sum())),
                    "Certified Domain-Specific Instance List": ", ".join(
                        sorted(group.loc[certified_diverse, "Instance"].astype(str).tolist())
                    ),
                }
            )
    return pd.DataFrame(rows).sort_values(["Score Metric", "Risk Isolation Group"]).reset_index(drop=True)


def _decision(summary: pd.DataFrame) -> dict[str, object]:
    focus = summary[
        (summary["Score Metric"].isin(["mean_domain_loss", "stockout_rate"]))
        & (summary["Risk Isolation Group"] == "anchor_feasible_medium_risk")
    ]
    max_clean = int(focus["Certified Domain-Specific Instances"].max()) if not focus.empty else 0
    mean_domain_clean = _metric_clean_count(summary, "mean_domain_loss")
    stockout_clean = _metric_clean_count(summary, "stockout_rate")
    clean_signal = max_clean >= 2
    if clean_signal:
        verdict = (
            "Risk isolation passed: certified diversity is not only a high-risk artifact. "
            f"Clean subset counts are mean_domain_loss={mean_domain_clean}, stockout_rate={stockout_clean}."
        )
        branch_status = "KISMEN/POSITIVE_DIAGNOSTIC"
    else:
        verdict = (
            "Risk isolation did not pass: certified diversity largely disappears in the "
            "anchor-feasible medium-risk subset."
        )
        branch_status = "KISMEN"
    return {
        "Clean Signal": clean_signal,
        "Max Clean Certified Diversity": max_clean,
        "Mean Domain Loss Clean Certified Diversity": mean_domain_clean,
        "Stockout Rate Clean Certified Diversity": stockout_clean,
        "Verdict": verdict,
        "Branch Status": branch_status,
    }


def _metric_clean_count(summary: pd.DataFrame, metric: str) -> int:
    row = summary[
        (summary["Score Metric"] == metric)
        & (summary["Risk Isolation Group"] == "anchor_feasible_medium_risk")
    ]
    if row.empty:
        return 0
    return int(row.iloc[0]["Certified Domain-Specific Instances"])


def _medium_instance_list(audit: pd.DataFrame) -> list[str]:
    anchor_feasible = _bool_series(audit, "Prev OR-Tools Anchor Feasible")
    medium_or_low = audit["Overall Audit Risk"].fillna("").str.lower().isin(["medium", "low"])
    return sorted(audit.loc[anchor_feasible & medium_or_low, "Instance"].astype(str).tolist())


def _write_diversity_report(path: Path, summary: pd.DataFrame, labelled: pd.DataFrame) -> None:
    pivot_rows = []
    for metric in ["mean_domain_loss", "stockout_rate"]:
        medium = _summary_row(summary, metric, "anchor_feasible_medium_risk")
        high = _summary_row(summary, metric, "high_risk_or_anchor_infeasible")
        pivot_rows.append(
            {
                "Score metric": metric,
                "Medium-risk subset certified diversity": _format_diversity(medium),
                "High-risk subset certified diversity": _format_diversity(high),
            }
        )
    lines = [
        "# Risk-Isolated Diversity Report",
        "",
        "## Risk Groups",
        "",
        "- `anchor_feasible_medium_risk`: `Prev OR-Tools Anchor Feasible == yes` and `Overall Audit Risk in {medium, low}`.",
        "- `high_risk_or_anchor_infeasible`: all remaining instances.",
        "",
        "## Diversity Split",
        "",
        _markdown_table(pd.DataFrame(pivot_rows)),
        "",
        "## Full Summary",
        "",
        _markdown_table(summary),
        "",
        "## Certified Domain-Specific Instances",
        "",
        _markdown_table(
            labelled[_bool_series(labelled, "Certified Domain-Specific")][
                [
                    "Score Metric",
                    "Instance",
                    "Risk Isolation Group",
                    "Certified Unique Route Plans",
                    "Overall Audit Risk",
                    "Prev OR-Tools Anchor Feasible",
                ]
            ]
        ),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_decision_report(
    path: Path,
    summary: pd.DataFrame,
    decision: dict[str, object],
    comparison: pd.DataFrame,
    medium_instances: list[str],
) -> None:
    clean_signal = bool(decision["Clean Signal"])
    if clean_signal:
        decision_text = (
            "Risk izolasyonu gecildi. `mean_domain_loss` ile devam etmek guvenli "
            "temel uzerinde duruyor. Sonraki adim: candidate pool genisletme "
            "ve multi-objective tie-breaker."
        )
        next_step = (
            "Candidate pool genisletme ve tie-breaker testi yalnizca "
            "`anchor_feasible_medium_risk` subset'inde calistirilacak."
        )
    else:
        decision_text = (
            "Certified diversity buyuk olcude high-risk instance kaynakli gorunuyor. "
            "Bu, K-adaptive route selection'in su anki haliyle guvenilir bir "
            "sektorel-akillilik mekanizmasi oldugunu kanitlamiyor. Branch KISMEN "
            "durumunda kalmali, FAIL degil ama PASS de degil."
        )
        next_step = "Risk izolasyonu gecilemedigi icin candidate pool genisletme ertelendi."

    lines = [
        "# Risk Isolation Decision Report",
        "",
        "## Bulgu",
        "",
        decision["Verdict"],
        "",
        _markdown_table(summary),
        "",
        "## Karar",
        "",
        decision_text,
        "",
        f"- Branch status: `{decision['Branch Status']}`",
        f"- Max clean certified diversity: `{decision['Max Clean Certified Diversity']}`",
        f"- Medium-risk instance count: `{len(medium_instances)}`",
        "",
        "## Onceki Turlar",
        "",
        "- TUR 1 post-hoc: `mean_total_cost` domain-specific choice uretmedi; `mean_domain_loss` ve `stockout_rate` re-ranking sinyali verdi.",
        "- TUR 2 real run: `mean_domain_loss` ve `stockout_rate` gercek kosuda domain-specific winner uretirken strict-safe oran %50'ye dustu.",
        "- TUR 3 risk isolation: temiz subset'te certified diversity yukaridaki tabloda ayrildi.",
        "",
        "## Baseline Comparison",
        "",
        _markdown_table(
            comparison[
                [
                    "Score Metric",
                    "Domain-Specific Instances",
                    "Fully Certified Instances",
                    "Certified Domain-Specific Instances",
                    "Ranking Flip Rate",
                    "Top Route Plan Share",
                ]
            ]
        ),
        "",
        "## Sonraki Adim",
        "",
        next_step,
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _summary_row(summary: pd.DataFrame, metric: str, risk_group: str) -> pd.Series:
    row = summary[(summary["Score Metric"] == metric) & (summary["Risk Isolation Group"] == risk_group)]
    if row.empty:
        return pd.Series(dtype=object)
    return row.iloc[0]


def _format_diversity(row: pd.Series) -> str:
    if row.empty:
        return "0 / 0"
    certified = int(row["Certified Domain-Specific Instances"])
    fully = int(row["Fully Certified Instances"])
    instances = row.get("Certified Domain-Specific Instance List", "")
    if instances:
        return f"{certified} / {fully} ({instances})"
    return f"{certified} / {fully}"


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
