from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from .run_robust_route_selection import (
    _attach_stability_status,
    _confirm_winners_full_scenario,
    _winner_ranking_stability,
)
from .stochastic_engine import available_lp_backends


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Apply a full-confirmed tie-breaker to near-tied robust route candidates. "
            "Primary score remains mean_domain_loss; stockout drift is used only within a tolerance band."
        )
    )
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--run-dir", required=True, help="Expanded robust route selection output directory.")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--score-metric", default="mean_domain_loss")
    parser.add_argument("--primary-rel-tolerance", type=float, default=0.01)
    parser.add_argument("--tie-breaker", choices=["stockout_drift"], default="stockout_drift")
    parser.add_argument("--routing-provider", default="ortools")
    parser.add_argument("--vroom-url", default="http://localhost:3000")
    parser.add_argument("--time-limit-sec", type=int, default=5)
    parser.add_argument("--lp-time-limit-sec", type=int, default=30)
    parser.add_argument("--lp-backend", choices=available_lp_backends(), default="pulp_cbc")
    parser.add_argument("--lp-planning-scenario-limit", type=int, default=60)
    parser.add_argument("--stability-stockout-rel-threshold", type=float, default=0.05)
    parser.add_argument("--stability-cost-rel-threshold", type=float, default=0.05)
    parser.add_argument("--randomized-route-variants", nargs="*", default=None)
    parser.add_argument("--randomized-route-cost-jitter", type=float, default=0.02)
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    candidates = pd.read_csv(run_dir / "robust_route_candidate_results.csv")
    near_candidates = _near_tied_candidates(candidates, args.score_metric, args.primary_rel_tolerance)
    near_candidates.to_csv(out_dir / "near_tied_candidates.csv", index=False)

    confirm_args = SimpleNamespace(
        confirm_winners_full_scenario=True,
        lp_backend=args.lp_backend,
        lp_planning_scenario_limit=args.lp_planning_scenario_limit,
        vroom_url=args.vroom_url,
        time_limit_sec=args.time_limit_sec,
        lp_time_limit_sec=args.lp_time_limit_sec,
        stability_stockout_rel_threshold=args.stability_stockout_rel_threshold,
        stability_cost_rel_threshold=args.stability_cost_rel_threshold,
        randomized_route_variants=args.randomized_route_variants,
        randomized_route_cost_jitter=args.randomized_route_cost_jitter,
    )
    full_near = _confirm_winners_full_scenario(confirm_args, Path(args.data_dir), near_candidates)
    full_near.to_csv(out_dir / "near_tied_candidate_full_confirmation.csv", index=False)

    tie_winners = _select_tie_breaker_winners(full_near)
    tie_winners.to_csv(out_dir / "tiebreaker_winners.csv", index=False)
    ranking = _winner_ranking_stability(tie_winners)
    confirmed = _attach_stability_status(tie_winners, ranking)
    confirmed.to_csv(out_dir / "tiebreaker_winner_full_confirmation.csv", index=False)
    ranking.to_csv(out_dir / "tiebreaker_winner_ranking_stability.csv", index=False)

    instance_summary = _instance_summary(confirmed)
    instance_summary.to_csv(out_dir / "tiebreaker_instance_diversity.csv", index=False)
    _write_report(
        out_dir / "tiebreaker_test_report.md",
        args=args,
        near_candidates=near_candidates,
        full_near=full_near,
        confirmed=confirmed,
        ranking=ranking,
        instance_summary=instance_summary,
    )
    print(f"Saved tie-breaker test outputs to {out_dir}")


def _near_tied_candidates(candidates: pd.DataFrame, score_metric: str, tolerance: float) -> pd.DataFrame:
    feasible = candidates[candidates["Candidate Feasible"].fillna(False).astype(bool)].copy()
    feasible["Primary Score"] = pd.to_numeric(feasible[score_metric], errors="coerce")
    feasible = feasible[feasible["Primary Score"].notna()]
    rows = []
    for _, group in feasible.groupby(["Instance", "Domain"], dropna=False):
        minimum = float(group["Primary Score"].min())
        limit = minimum * (1.0 + float(tolerance)) if abs(minimum) > 1e-12 else minimum + float(tolerance)
        near = group[group["Primary Score"] <= limit].copy()
        near["Primary Score Minimum"] = minimum
        near["Primary Score Relative Gap"] = (near["Primary Score"] - minimum).abs() / max(abs(minimum), 1e-12)
        rows.append(near)
    if not rows:
        return pd.DataFrame()
    out = pd.concat(rows, ignore_index=True)
    return out.sort_values(["Instance", "Domain", "Primary Score", "Candidate"]).reset_index(drop=True)


def _select_tie_breaker_winners(full_near: pd.DataFrame) -> pd.DataFrame:
    feasible = full_near[full_near["Confirm Feasible"].fillna(False).astype(bool)].copy()
    if feasible.empty:
        return pd.DataFrame()
    sort_cols = [
        "Stockout Relative Drift",
        "Full Stockout",
        "Fast Score Value",
        "Full Mean Total Cost",
        "Candidate",
    ]
    for col in sort_cols[:-1]:
        feasible[col] = pd.to_numeric(feasible[col], errors="coerce")
    winners = (
        feasible.sort_values(sort_cols, ascending=[True, True, True, True, True])
        .groupby(["Instance", "Domain"], as_index=False, dropna=False)
        .first()
    )
    winners["Winner Rank Metric"] = "mean_domain_loss_with_stockout_drift_tiebreaker"
    return winners.sort_values(["Instance", "Domain"]).reset_index(drop=True)


def _instance_summary(confirmed: pd.DataFrame) -> pd.DataFrame:
    if confirmed.empty:
        return pd.DataFrame()
    rows = []
    confirmed = confirmed.copy()
    confirmed["Strict Bool"] = _bool_series(confirmed, "Strict Stability Safe")
    for instance, group in confirmed.groupby("Instance", dropna=False):
        strict = group[group["Strict Bool"]]
        rows.append(
            {
                "Instance": instance,
                "Winner Domains": int(group["Domain"].nunique()),
                "Winner Unique Route Plans": int(group["Route Plan"].nunique()),
                "Winner Domain-Specific": bool(group["Route Plan"].nunique() > 1),
                "Strict-Safe Domains": int(strict["Domain"].nunique()),
                "Certified Unique Route Plans": int(strict["Route Plan"].nunique()),
                "Fully Certified Instance": bool(strict["Domain"].nunique() >= group["Domain"].nunique()),
                "Certified Domain-Specific": bool(
                    strict["Domain"].nunique() >= group["Domain"].nunique()
                    and strict["Route Plan"].nunique() > 1
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("Instance").reset_index(drop=True)


def _write_report(
    path: Path,
    args: argparse.Namespace,
    near_candidates: pd.DataFrame,
    full_near: pd.DataFrame,
    confirmed: pd.DataFrame,
    ranking: pd.DataFrame,
    instance_summary: pd.DataFrame,
) -> None:
    strict_rows = int(_bool_series(confirmed, "Strict Stability Safe").sum()) if not confirmed.empty else 0
    certified_diverse = int(_bool_series(instance_summary, "Certified Domain-Specific").sum()) if not instance_summary.empty else 0
    fully_certified = int(_bool_series(instance_summary, "Fully Certified Instance").sum()) if not instance_summary.empty else 0
    domain_diverse = int(_bool_series(instance_summary, "Winner Domain-Specific").sum()) if not instance_summary.empty else 0
    lines = [
        "# Robust Route Tie-Breaker Test",
        "",
        "## Scope",
        "",
        f"- Run dir: `{args.run_dir}`",
        f"- Primary score metric: `{args.score_metric}`",
        f"- Primary relative tolerance: `{args.primary_rel_tolerance}`",
        f"- Tie-breaker: `{args.tie_breaker}`",
        "- Tie-breaker candidates were full-confirmed before final selection.",
        "",
        "## Summary",
        "",
        f"- Near-tied candidate rows: {len(near_candidates)}",
        f"- Near-tied full-confirmation rows: {len(full_near)}",
        f"- Tie-breaker winner rows: {len(confirmed)}",
        f"- Strict-safe winner rows: {strict_rows}",
        f"- Winner domain-specific instances: {domain_diverse}",
        f"- Fully certified instances: {fully_certified}",
        f"- Certified domain-specific instances: {certified_diverse}",
        "",
        "## Instance Summary",
        "",
        _markdown_table(instance_summary),
        "",
        "## Ranking Stability",
        "",
        _markdown_table(ranking),
        "",
        "## Interpretation",
        "",
        "- This is a medium-risk subset diagnostic, not a full X40 replacement.",
        "- The primary objective remains `mean_domain_loss`; stockout drift only breaks near ties.",
        "- If certified diversity improves without increasing ranking flips, this is a safer next direction.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _bool_series(frame: pd.DataFrame, column: str) -> pd.Series:
    if frame.empty or column not in frame.columns:
        return pd.Series([False] * len(frame), index=frame.index)
    values = frame[column]
    if pd.api.types.is_bool_dtype(values):
        return values.fillna(False).astype(bool)
    return values.fillna(False).map(lambda value: str(value).strip().lower() in {"true", "1", "yes"})


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
