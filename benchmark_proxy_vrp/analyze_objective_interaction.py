from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze_stockout_mechanisms import (
    _bootstrap_ci,
    _ci_contains_zero,
    _evidence_label,
    _markdown_table,
    _ols_influence,
    _pearson,
    _unique_level_count,
)


PREDICTORS = [
    ("route_cost_diff", "Route Cost Diff"),
    ("planned_load_total_diff", "Planned Load Total Diff"),
    ("mean_domain_loss_diff", "Mean Domain Loss Diff"),
    ("mean_load_penalty_loss_diff", "Mean Load Penalty Loss Diff"),
    ("mean_surplus_diff", "Mean Surplus Diff"),
    ("mean_shortfall_diff", "Mean Shortfall Diff"),
    ("mean_total_cost_diff", "Mean Total Cost Diff"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnose objective-interaction effects on stockout differences.")
    parser.add_argument("--ortools-results", default="benchmarks/proxy_cvrplib_x_v3/domain_engine_results_ortools_provider.csv")
    parser.add_argument("--vroom-results", default="benchmarks/proxy_cvrplib_x_v3/domain_engine_results_vroom_provider.csv")
    parser.add_argument("--load-allocation-diffs", default="benchmarks/proxy_cvrplib_x_v3/load_allocation_diffs.csv")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib_x_v3")
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=3030)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    frame = _objective_diff_frame(args.ortools_results, args.vroom_results, args.load_allocation_diffs)
    correlations = _correlation_tests(frame, args.bootstrap_samples, args.seed)
    partial = _partial_correlation_tests(frame, args.bootstrap_samples, args.seed + 5000)
    leverage = _leverage_control(frame)
    leave_one_out = _leave_one_out_if_needed(frame, leverage, args.bootstrap_samples, args.seed + 10000)
    summary = _summary(frame)

    frame.to_csv(out_dir / "objective_interaction_diffs.csv", index=False)
    correlations.to_csv(out_dir / "objective_interaction_correlations.csv", index=False)
    partial.to_csv(out_dir / "objective_interaction_partial_correlations.csv", index=False)
    leverage.to_csv(out_dir / "objective_interaction_leverage.csv", index=False)
    leave_one_out.to_csv(out_dir / "objective_interaction_leave_one_out.csv", index=False)
    _write_report(
        out_dir / "objective_interaction_diagnosis_report.md",
        summary=summary,
        correlations=correlations,
        partial=partial,
        leverage=leverage,
        leave_one_out=leave_one_out,
    )

    print("Objective interaction summary")
    print(summary.to_string(index=False))
    print("\nCorrelations")
    print(correlations.to_string(index=False))
    print("\nPartial correlations")
    print(partial.to_string(index=False))


def _objective_diff_frame(ortools_path: str, vroom_path: str, load_allocation_path: str) -> pd.DataFrame:
    ortools = pd.read_csv(ortools_path)
    vroom = pd.read_csv(vroom_path)
    load_allocation = pd.read_csv(load_allocation_path)
    feasible_o = ortools[(ortools["feasible"] == True) & (ortools["domain"] != "all")].copy()
    feasible_v = vroom[(vroom["feasible"] == True) & (vroom["domain"] != "all")].copy()
    columns = [
        "instance",
        "domain",
        "route_cost",
        "planned_load_total",
        "mean_domain_loss",
        "mean_load_penalty_loss",
        "mean_surplus",
        "mean_shortfall",
        "mean_total_cost",
        "stockout_rate",
    ]
    merged = feasible_o[columns].merge(
        feasible_v[columns],
        on=["instance", "domain"],
        suffixes=("_ortools", "_vroom"),
    )
    for metric in columns[2:]:
        merged[f"{metric}_diff"] = merged[f"{metric}_ortools"] - merged[f"{metric}_vroom"]
    merged = merged.rename(columns={"instance": "Instance", "domain": "Domain"})
    merged["stockout_diff_signed"] = merged["stockout_rate_diff"]
    merged["stockout_diff_abs"] = merged["stockout_diff_signed"].abs()
    return merged.merge(
        load_allocation[["Instance", "Common Route Feasible", "Gini Diff", "Load Variance Diff"]],
        on="Instance",
        how="left",
    ).sort_values(["Domain", "Instance"])


def _correlation_tests(frame: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    common = frame[frame["Common Route Feasible"] == True].copy()
    for domain, group in common.groupby("Domain"):
        for column, label in PREDICTORS:
            x = group[column].to_numpy(float)
            y = group["stockout_diff_signed"].to_numpy(float)
            rows.append(_test_row(domain, label, x, y, bootstrap_samples, rng))
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _partial_correlation_tests(frame: pd.DataFrame, bootstrap_samples: int, seed: int) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    common = frame[frame["Common Route Feasible"] == True].copy()
    for domain, group in common.groupby("Domain"):
        y = group["stockout_diff_signed"].to_numpy(float)
        control = group["Load Variance Diff"].to_numpy(float)
        for column, label in PREDICTORS:
            x = group[column].to_numpy(float)
            if _unique_level_count(x) < 3 or _unique_level_count(control) < 3 or len(group) < 15:
                rows.append(
                    {
                        "Domain": domain,
                        "Predictor": label,
                        "Control": "Load Variance Diff",
                        "n": int(len(group)),
                        "Unique x Levels": int(_unique_level_count(x)),
                        "Pearson r": np.nan,
                        "p-value": np.nan,
                        "Bootstrap CI Low": np.nan,
                        "Bootstrap CI High": np.nan,
                        "CI Contains Zero": False,
                        "Evidence Label": "insufficient_variation_or_n",
                    }
                )
                continue
            residual_x = _residualize(x, control)
            residual_y = _residualize(y, control)
            r, p_value = _pearson(residual_x, residual_y)
            ci_low, ci_high = _partial_bootstrap_ci(x, y, control, bootstrap_samples, rng)
            rows.append(
                {
                    "Domain": domain,
                    "Predictor": label,
                    "Control": "Load Variance Diff",
                    "n": int(len(group)),
                    "Unique x Levels": int(_unique_level_count(x)),
                    "Pearson r": r,
                    "p-value": p_value,
                    "Bootstrap CI Low": ci_low,
                    "Bootstrap CI High": ci_high,
                    "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
                    "Evidence Label": _evidence_label(r, p_value, ci_low, ci_high),
                }
            )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor"])


def _test_row(
    domain: str,
    label: str,
    x: np.ndarray,
    y: np.ndarray,
    bootstrap_samples: int,
    rng: np.random.Generator,
) -> dict[str, object]:
    unique_x = _unique_level_count(x)
    if len(x) < 15:
        r, p_value = _pearson(x, y)
        ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
        evidence = "diagnostic_signal_n_lt_15"
    elif unique_x < 3:
        r, p_value, ci_low, ci_high = np.nan, np.nan, np.nan, np.nan
        evidence = "insufficient_x_variation"
    else:
        r, p_value = _pearson(x, y)
        ci_low, ci_high = _bootstrap_ci(x, y, bootstrap_samples, rng)
        evidence = _evidence_label(r, p_value, ci_low, ci_high)
    return {
        "Domain": domain,
        "Predictor": label,
        "n": int(len(x)),
        "Unique x Levels": int(unique_x),
        "Pearson r": r,
        "p-value": p_value,
        "Bootstrap CI Low": ci_low,
        "Bootstrap CI High": ci_high,
        "CI Contains Zero": _ci_contains_zero(ci_low, ci_high),
        "Evidence Label": evidence,
    }


def _partial_bootstrap_ci(
    x: np.ndarray,
    y: np.ndarray,
    control: np.ndarray,
    samples: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    values = []
    n = len(x)
    for _ in range(samples):
        idx = rng.integers(0, n, n)
        sx = x[idx]
        sy = y[idx]
        sc = control[idx]
        if _unique_level_count(sx) < 3 or _unique_level_count(sc) < 3:
            continue
        rx = _residualize(sx, sc)
        ry = _residualize(sy, sc)
        r, _ = _pearson(rx, ry)
        if np.isfinite(r):
            values.append(r)
    if not values:
        return float("nan"), float("nan")
    return float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))


def _residualize(values: np.ndarray, control: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(control)), control])
    beta = np.linalg.lstsq(design, values, rcond=None)[0]
    return values - design @ beta


def _leverage_control(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    common = frame[frame["Common Route Feasible"] == True].copy()
    for domain, domain_group in common.groupby("Domain"):
        domain_group = domain_group.sort_values("Instance")
        y = domain_group["stockout_diff_signed"].to_numpy(float)
        for column, label in PREDICTORS:
            x = domain_group[column].to_numpy(float)
            n = len(domain_group)
            cook_threshold = 4.0 / n if n else np.nan
            severe_threshold = 3.0 * cook_threshold if n else np.nan
            if _unique_level_count(x) < 2 or np.allclose(y, y[0]):
                leverage = np.full(n, np.nan)
                cooks = np.full(n, np.nan)
                residuals = np.full(n, np.nan)
            else:
                leverage, cooks, residuals = _ols_influence(x, y)
            for idx, row in enumerate(domain_group.itertuples(index=False)):
                rows.append(
                    {
                        "Domain": domain,
                        "Predictor": label,
                        "Instance": row.Instance,
                        "x": x[idx],
                        "Stockout Diff Signed": y[idx],
                        "Leverage": leverage[idx],
                        "Cook's Distance": cooks[idx],
                        "Cook Threshold 4/n": cook_threshold,
                        "Severe Threshold 3x": severe_threshold,
                        "Severe Cook Flag": bool(np.isfinite(cooks[idx]) and cooks[idx] > severe_threshold),
                        "Residual": residuals[idx],
                    }
                )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor", "Cook's Distance"], ascending=[True, True, False])


def _leave_one_out_if_needed(
    frame: pd.DataFrame,
    leverage: pd.DataFrame,
    bootstrap_samples: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(seed)
    common = frame[frame["Common Route Feasible"] == True].copy()
    flagged = leverage[leverage["Severe Cook Flag"]]
    if flagged.empty:
        return pd.DataFrame(
            columns=[
                "Domain",
                "Predictor",
                "Dropped Instance",
                "n",
                "Unique x Levels",
                "Pearson r",
                "p-value",
                "Bootstrap CI Low",
                "Bootstrap CI High",
                "CI Contains Zero",
                "Evidence Label",
            ]
        )
    label_to_column = {label: column for column, label in PREDICTORS}
    for (domain, predictor), group_flags in flagged.groupby(["Domain", "Predictor"]):
        dropped = group_flags.sort_values("Cook's Distance", ascending=False).iloc[0]["Instance"]
        reduced = common[(common["Domain"] == domain) & (common["Instance"] != dropped)]
        column = label_to_column[predictor]
        x = reduced[column].to_numpy(float)
        y = reduced["stockout_diff_signed"].to_numpy(float)
        rows.append(
            {
                **_test_row(domain, predictor, x, y, bootstrap_samples, rng),
                "Dropped Instance": dropped,
            }
        )
    return pd.DataFrame(rows).sort_values(["Domain", "Predictor", "Dropped Instance"])


def _summary(frame: pd.DataFrame) -> pd.DataFrame:
    common = frame[frame["Common Route Feasible"] == True].copy()
    return (
        common.groupby("Domain")
        .agg(
            n=("Instance", "nunique"),
            mean_stockout_diff=("stockout_diff_signed", "mean"),
            mean_route_cost_diff=("route_cost_diff", "mean"),
            mean_planned_load_total_diff=("planned_load_total_diff", "mean"),
            mean_domain_loss_diff=("mean_domain_loss_diff", "mean"),
            mean_load_penalty_loss_diff=("mean_load_penalty_loss_diff", "mean"),
            mean_total_cost_diff=("mean_total_cost_diff", "mean"),
        )
        .reset_index()
    )


def _write_report(
    path: Path,
    summary: pd.DataFrame,
    correlations: pd.DataFrame,
    partial: pd.DataFrame,
    leverage: pd.DataFrame,
    leave_one_out: pd.DataFrame,
) -> None:
    candidate = correlations[correlations["Evidence Label"] == "candidate_mechanism"]
    partial_candidate = partial[partial["Evidence Label"] == "candidate_mechanism"]
    severe = leverage[leverage["Severe Cook Flag"]]

    if partial_candidate.empty:
        interpretation = (
            "Objective-component diffs show associations with stockout in the raw correlations, but after controlling "
            "for Load Variance Diff they do not provide a clean independent mechanism. This supports the current view "
            "that route-level load allocation is the primary measured mechanism, while objective interaction remains "
            "a downstream or coupled effect rather than an independent explanation."
        )
    else:
        interpretation = (
            "At least one objective-component diff remains a candidate signal after controlling for Load Variance Diff. "
            "This means objective interaction may add explanatory information beyond route-level load allocation."
        )

    if severe.empty:
        leverage_text = "Cook's Distance control found no severe 3x(4/n) dominating point."
        loo_text = ""
    else:
        leverage_text = "Cook's Distance control found severe points; leave-one-out is reported below."
        loo_text = "\n\n" + _markdown_table(leave_one_out)

    text = f"""# Objective Interaction Diagnosis Report

## Scope

This report tests the remaining A.8 candidate: objective interaction. The analysis uses the executed CVRPLIB X24 expansion and the common OR-Tools/VROOM feasible subset. No new LP solve is required; this diagnostic compares already produced provider-domain result components.

Predictors are OR-Tools minus VROOM differences for route cost, planned load total, domain loss, load penalty loss, surplus, shortfall, and total cost. The target is signed stockout diff.

## Provider-Domain Difference Summary

{_markdown_table(summary)}

## Raw Correlations

{_markdown_table(correlations)}

Raw candidate rows: {len(candidate)}.

## Partial Correlations Controlling Load Allocation

Because load allocation already produced a strong candidate mechanism, objective interaction must be tested against that confound. The table below residualizes both the objective predictor and stockout diff against `Load Variance Diff`.

{_markdown_table(partial)}

Partial candidate rows: {len(partial_candidate)}.

## Leverage Control

{leverage_text}

{_markdown_table(leverage[["Domain", "Predictor", "Instance", "Cook's Distance", "Cook Threshold 4/n", "Severe Threshold 3x", "Severe Cook Flag"]])}{loo_text}

## Finding

{interpretation}

## Correct Sentence

Objective interaction is coupled with stockout changes, but on the current X24 common-feasible set it should not replace route-level load allocation as the primary measured mechanism unless it remains significant after controlling for load allocation.

## Next Step

Run a controlled model with both predictors in the same regression: `stockout_diff ~ load_variance_diff + objective_component_diff`, then repeat on a larger X set with a stronger non-demo LP backend or a route-feasible instance filter fixed before seeing outcomes.
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
