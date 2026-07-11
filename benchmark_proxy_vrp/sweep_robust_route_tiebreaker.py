from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from .apply_robust_route_tiebreaker import (
    _instance_summary,
    _near_tied_candidates,
    _select_tie_breaker_winners,
)
from .run_robust_route_selection import (
    _attach_stability_status,
    _confirm_winners_full_scenario,
    _winner_ranking_stability,
)
from .stochastic_engine import available_lp_backends


KEY_COLUMNS = ["Instance", "Domain", "Candidate", "Routing Provider", "Route Plan"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep near-tie tolerance values for robust route tie-breaker.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v4")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--score-metric", default="mean_domain_loss")
    parser.add_argument("--tolerances", nargs="+", type=float, default=[0.001, 0.005, 0.01])
    parser.add_argument("--confirmation-cache", default=None)
    parser.add_argument("--allow-confirm-missing", action="store_true")
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
    parser.add_argument("--route-cache-dir", default=None)
    parser.add_argument(
        "--route-cache-mode",
        choices=["readwrite", "readonly", "writeonly", "off"],
        default="readwrite",
    )
    parser.add_argument("--risk-group-file", default=None)
    parser.add_argument("--report-name", default="tolerance_sweep_report.md")
    parser.add_argument("--full-x40-report-name", default=None)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = pd.read_csv(Path(args.run_dir) / "robust_route_candidate_results.csv")
    confirmation_cache = _read_confirmation_cache(args.confirmation_cache)
    risk_groups = _read_risk_groups(args.risk_group_file)
    summaries = []
    risk_summaries = []
    full_cache_path = out_dir / "confirmation_cache.csv"

    max_tol_near_count = None
    max_tol = max(args.tolerances)
    for tolerance in args.tolerances:
        label = _tolerance_label(tolerance)
        near_candidates = _near_tied_candidates(candidates, args.score_metric, tolerance)
        if tolerance == max_tol:
            max_tol_near_count = len(near_candidates)
        full_near, cache_misses, confirmation_cache = _full_confirmation_for_near_candidates(
            args=args,
            near_candidates=near_candidates,
            confirmation_cache=confirmation_cache,
        )
        full_near.to_csv(out_dir / f"tiebreaker_near_full_confirmation_tol_{label}.csv", index=False)
        near_candidates.to_csv(out_dir / f"near_tied_candidates_tol_{label}.csv", index=False)
        if not confirmation_cache.empty:
            confirmation_cache.drop_duplicates(KEY_COLUMNS).to_csv(full_cache_path, index=False)

        winners = _select_tie_breaker_winners(full_near)
        ranking = _winner_ranking_stability(winners)
        confirmed = _attach_stability_status(winners, ranking)
        instance_summary = _instance_summary(confirmed)
        winners.to_csv(out_dir / f"tiebreaker_winners_tol_{label}.csv", index=False)
        confirmed.to_csv(out_dir / f"tiebreaker_winner_full_confirmation_tol_{label}.csv", index=False)
        ranking.to_csv(out_dir / f"tiebreaker_winner_ranking_stability_tol_{label}.csv", index=False)
        instance_summary.to_csv(out_dir / f"tiebreaker_instance_diversity_tol_{label}.csv", index=False)

        summary = _summary_row(tolerance, near_candidates, full_near, confirmed, ranking, instance_summary, cache_misses)
        summaries.append(summary)
        if risk_groups:
            risk_summaries.extend(_risk_summary_rows(tolerance, confirmed, ranking, instance_summary, risk_groups))

    summary_df = pd.DataFrame(summaries)
    if max_tol_near_count:
        summary_df["Full-LP Call Reduction vs Max Tolerance"] = (
            1.0 - summary_df["Full-LP Calls Required"] / float(max_tol_near_count)
        )
    else:
        summary_df["Full-LP Call Reduction vs Max Tolerance"] = np.nan
    best_tolerance = _choose_best_tolerance(summary_df)
    summary_df["Selected Best Tradeoff"] = summary_df["Tolerance"] == best_tolerance
    summary_df.to_csv(out_dir / "tolerance_sweep_summary.csv", index=False)

    risk_df = pd.DataFrame(risk_summaries)
    if not risk_df.empty:
        risk_df.to_csv(out_dir / "tiebreaker_risk_group_summary.csv", index=False)

    _write_tolerance_report(out_dir / args.report_name, args, summary_df, risk_df, best_tolerance)
    if args.full_x40_report_name:
        _write_full_x40_report(out_dir / args.full_x40_report_name, summary_df, risk_df, best_tolerance)
    print(f"Saved tie-breaker tolerance sweep outputs to {out_dir}")


def _read_confirmation_cache(path: str | None) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    cache_path = Path(path)
    if not cache_path.exists():
        return pd.DataFrame()
    return pd.read_csv(cache_path).drop_duplicates(KEY_COLUMNS)


def _read_risk_groups(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    frame = pd.read_csv(path)
    medium = set(frame["Instance"].astype(str))
    return {
        instance: "anchor_feasible_medium_risk" if instance in medium else "high_risk_or_anchor_infeasible"
        for instance in medium
    }


def _risk_group(instance: str, risk_groups: dict[str, str]) -> str:
    return risk_groups.get(str(instance), "high_risk_or_anchor_infeasible")


def _full_confirmation_for_near_candidates(
    *,
    args: argparse.Namespace,
    near_candidates: pd.DataFrame,
    confirmation_cache: pd.DataFrame,
) -> tuple[pd.DataFrame, int, pd.DataFrame]:
    if near_candidates.empty:
        return pd.DataFrame(), 0, confirmation_cache
    cached = _take_cached_confirmations(near_candidates, confirmation_cache)
    missing = _missing_near_candidates(near_candidates, cached)
    cache_misses = len(missing)
    if not missing.empty:
        if not args.allow_confirm_missing:
            missing_keys = missing[KEY_COLUMNS].head(10).to_dict("records")
            raise ValueError(f"{len(missing)} near-tied rows are missing full confirmation; examples={missing_keys}")
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
            route_cache_dir=args.route_cache_dir,
            route_cache_mode=args.route_cache_mode,
        )
        new_full = _confirm_winners_full_scenario(confirm_args, Path(args.data_dir), missing)
        confirmation_cache = pd.concat([confirmation_cache, new_full], ignore_index=True).drop_duplicates(KEY_COLUMNS)
        cached = pd.concat([cached, new_full], ignore_index=True)
    return cached.sort_values(KEY_COLUMNS).reset_index(drop=True), cache_misses, confirmation_cache


def _take_cached_confirmations(near_candidates: pd.DataFrame, cache: pd.DataFrame) -> pd.DataFrame:
    if cache.empty:
        return pd.DataFrame(columns=KEY_COLUMNS)
    keys = near_candidates[KEY_COLUMNS].drop_duplicates()
    return keys.merge(cache, on=KEY_COLUMNS, how="inner")


def _missing_near_candidates(near_candidates: pd.DataFrame, cached: pd.DataFrame) -> pd.DataFrame:
    if cached.empty:
        return near_candidates.copy()
    cached_keys = cached[KEY_COLUMNS].drop_duplicates()
    marked = near_candidates.merge(cached_keys.assign(_cached=True), on=KEY_COLUMNS, how="left")
    return marked[marked["_cached"].isna()].drop(columns=["_cached"]).reset_index(drop=True)


def _summary_row(
    tolerance: float,
    near_candidates: pd.DataFrame,
    full_near: pd.DataFrame,
    confirmed: pd.DataFrame,
    ranking: pd.DataFrame,
    instance_summary: pd.DataFrame,
    cache_misses: int,
) -> dict[str, object]:
    certified = int(_bool_series(instance_summary, "Certified Domain-Specific").sum())
    fully = int(_bool_series(instance_summary, "Fully Certified Instance").sum())
    flips = int(_bool_series(ranking, "Ranking Flip").sum())
    ranking_rows = int(len(ranking))
    strict_rows = int(_bool_series(confirmed, "Strict Stability Safe").sum())
    return {
        "Tolerance": tolerance,
        "Near-tied Candidates": len(near_candidates),
        "Full-LP Calls Required": len(near_candidates),
        "New Full-LP Calls This Run": cache_misses,
        "Full-Confirmed Rows": len(full_near),
        "Winner Rows": len(confirmed),
        "Fully Certified Instances": fully,
        "Certified Domain-Specific Instances": certified,
        "Certified Diversity": f"{certified} / {fully}",
        "Ranking Flips": flips,
        "Ranking Rows": ranking_rows,
        "Flip Rate": flips / ranking_rows if ranking_rows else np.nan,
        "Strict-Safe Rows": strict_rows,
    }


def _risk_summary_rows(
    tolerance: float,
    confirmed: pd.DataFrame,
    ranking: pd.DataFrame,
    instance_summary: pd.DataFrame,
    risk_groups: dict[str, str],
) -> list[dict[str, object]]:
    rows = []
    if confirmed.empty:
        return rows
    instance_summary = instance_summary.copy()
    instance_summary["Risk Group"] = instance_summary["Instance"].map(lambda value: _risk_group(value, risk_groups))
    ranking = ranking.copy()
    if not ranking.empty:
        ranking["Risk Group"] = ranking["Instance"].map(lambda value: _risk_group(value, risk_groups))
    for group_name in ["anchor_feasible_medium_risk", "high_risk_or_anchor_infeasible"]:
        inst_group = instance_summary[instance_summary["Risk Group"] == group_name]
        rank_group = ranking[ranking["Risk Group"] == group_name] if not ranking.empty else pd.DataFrame()
        certified = int(_bool_series(inst_group, "Certified Domain-Specific").sum())
        fully = int(_bool_series(inst_group, "Fully Certified Instance").sum())
        flips = int(_bool_series(rank_group, "Ranking Flip").sum())
        ranking_rows = int(len(rank_group))
        rows.append(
            {
                "Tolerance": tolerance,
                "Risk Group": group_name,
                "Instances": int(inst_group["Instance"].nunique()) if not inst_group.empty else 0,
                "Fully Certified Instances": fully,
                "Certified Domain-Specific Instances": certified,
                "Certified Diversity": f"{certified} / {fully}",
                "Ranking Flips": flips,
                "Ranking Rows": ranking_rows,
                "Flip Rate": flips / ranking_rows if ranking_rows else np.nan,
            }
        )
    return rows


def _choose_best_tolerance(summary: pd.DataFrame) -> float:
    if summary.empty:
        return np.nan
    max_certified = float(summary["Certified Domain-Specific Instances"].max())
    floor = max_certified * 0.8
    eligible = summary[summary["Certified Domain-Specific Instances"] >= floor].copy()
    if eligible.empty:
        eligible = summary.copy()
    eligible = eligible.sort_values(
        ["Full-LP Calls Required", "Flip Rate", "Certified Domain-Specific Instances"],
        ascending=[True, True, False],
    )
    return float(eligible.iloc[0]["Tolerance"])


def _write_tolerance_report(
    path: Path,
    args: argparse.Namespace,
    summary_df: pd.DataFrame,
    risk_df: pd.DataFrame,
    best_tolerance: float,
) -> None:
    lines = [
        "# Tie-Breaker Tolerance Sweep Report",
        "",
        "## Scope",
        "",
        f"- Run dir: `{args.run_dir}`",
        f"- Score metric: `{args.score_metric}`",
        f"- Tolerances: {', '.join(str(t) for t in args.tolerances)}",
        f"- Confirmation cache input: `{args.confirmation_cache}`",
        f"- Missing confirmation allowed: `{args.allow_confirm_missing}`",
        "",
        "## Summary",
        "",
        _markdown_table(summary_df),
        "",
        "## Best Trade-Off",
        "",
        f"Selected tolerance: `{best_tolerance}`.",
        "",
        "Selection rule: keep at least 80% of the maximum certified domain-specific diversity, then minimize full-LP calls, then ranking flip rate.",
        "",
    ]
    if not risk_df.empty:
        lines.extend(["## Risk Group Split", "", _markdown_table(risk_df), ""])
    lines.extend(
        [
            "## Interpretation",
            "",
            "- `Full-LP Calls Required` is the scientific cost implied by the tolerance.",
            "- `New Full-LP Calls This Run` can be lower when an existing confirmation cache is reused.",
            "- A lower tolerance is only better if it preserves certified diversity and does not increase ranking flips.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_full_x40_report(path: Path, summary_df: pd.DataFrame, risk_df: pd.DataFrame, best_tolerance: float) -> None:
    selected = summary_df[summary_df["Tolerance"] == best_tolerance]
    lines = [
        "# Full X40 Tie-Breaker Report",
        "",
        "## Selected Tolerance Result",
        "",
        _markdown_table(selected),
        "",
    ]
    if not risk_df.empty:
        selected_risk = risk_df[risk_df["Tolerance"] == best_tolerance].copy()
        lines.extend(["## Risk Group Result", "", _markdown_table(selected_risk), ""])
    lines.extend(
        [
            "## Decision",
            "",
            "This is the full X40 application of the tolerance-controlled tie-breaker. It should be compared against the previous medium-risk-only diagnostic before upgrading the branch status.",
        ]
    )
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


def _tolerance_label(tolerance: float) -> str:
    return str(tolerance).replace(".", "p")


if __name__ == "__main__":
    main()
