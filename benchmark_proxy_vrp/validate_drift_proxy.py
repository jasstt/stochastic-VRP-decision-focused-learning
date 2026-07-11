from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


KEY_COLUMNS = ["Instance", "Domain", "Candidate", "Routing Provider", "Route Plan"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a cheap drift proxy against full-confirmed stockout drift.")
    parser.add_argument("--near-candidates", required=True)
    parser.add_argument("--full-confirmation", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--drift-threshold", type=float, default=0.05)
    parser.add_argument("--proxy-thresholds", nargs="+", type=float, default=[0.10, 0.15, 0.20, 0.25, 0.30])
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    near = pd.read_csv(args.near_candidates)
    full = pd.read_csv(args.full_confirmation)
    validation = _build_validation_frame(near, full)
    validation.to_csv(out_dir / "drift_proxy_candidate_scores.csv", index=False)
    summary = _threshold_summary(validation, args.drift_threshold, args.proxy_thresholds)
    summary.to_csv(out_dir / "drift_proxy_threshold_summary.csv", index=False)
    _write_report(out_dir / "drift_proxy_validation_report.md", validation, summary, args.drift_threshold)
    print(f"Saved drift proxy validation to {out_dir}")


def _build_validation_frame(near: pd.DataFrame, full: pd.DataFrame) -> pd.DataFrame:
    full_cols = KEY_COLUMNS + ["Confirm Feasible", "Stockout Relative Drift", "Mean Total Cost Relative Drift"]
    frame = near.merge(full[full_cols], on=KEY_COLUMNS, how="inner")
    numeric_cols = [
        "Primary Score Relative Gap",
        "Route Cost",
        "Planned Route Load Ratio",
        "Route Count",
        "stockout_rate",
        "mean_shortfall",
        "mean_load_penalty_loss",
    ]
    for col in numeric_cols:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    pieces = []
    for _, group in frame.groupby(["Instance", "Domain"], dropna=False):
        scored = group.copy()
        scored["proxy_primary_gap"] = (scored["Primary Score Relative Gap"] / 0.01).clip(0, 1)
        scored["proxy_route_cost"] = _normalized_abs_dev(scored["Route Cost"])
        scored["proxy_load_ratio"] = _normalized_abs_dev(scored["Planned Route Load Ratio"])
        mode = scored["Route Count"].mode().iloc[0] if not scored["Route Count"].mode().empty else scored["Route Count"].iloc[0]
        scored["proxy_route_count"] = (scored["Route Count"] != mode).astype(float)
        scored["proxy_fast_stockout"] = _normalized_abs_dev(scored["stockout_rate"])
        scored["proxy_fast_shortfall"] = _normalized_abs_dev(scored["mean_shortfall"])
        scored["proxy_fast_load_penalty"] = _normalized_abs_dev(scored["mean_load_penalty_loss"])
        pieces.append(scored)
    out = pd.concat(pieces, ignore_index=True) if pieces else pd.DataFrame()
    if out.empty:
        return out
    out["Fast Drift Proxy"] = (
        0.20 * out["proxy_primary_gap"]
        + 0.15 * out["proxy_route_cost"]
        + 0.10 * out["proxy_load_ratio"]
        + 0.15 * out["proxy_route_count"]
        + 0.25 * out["proxy_fast_stockout"]
        + 0.10 * out["proxy_fast_shortfall"]
        + 0.05 * out["proxy_fast_load_penalty"]
    )
    return out


def _normalized_abs_dev(values: pd.Series) -> pd.Series:
    values = pd.to_numeric(values, errors="coerce")
    span = float(values.max() - values.min()) if values.notna().any() else 0.0
    if span <= 1e-12:
        return pd.Series([0.0] * len(values), index=values.index)
    return ((values - values.median()).abs() / span).clip(0, 1).fillna(0.0)


def _threshold_summary(frame: pd.DataFrame, drift_threshold: float, proxy_thresholds: list[float]) -> pd.DataFrame:
    rows = []
    if frame.empty:
        return pd.DataFrame()
    actual_high = (frame["Confirm Feasible"].fillna(False).astype(bool)) & (
        pd.to_numeric(frame["Stockout Relative Drift"], errors="coerce") > drift_threshold
    )
    for threshold in proxy_thresholds:
        predicted_high = pd.to_numeric(frame["Fast Drift Proxy"], errors="coerce") >= threshold
        true_positive = int((predicted_high & actual_high).sum())
        false_positive = int((predicted_high & ~actual_high).sum())
        false_negative = int((~predicted_high & actual_high).sum())
        predicted_count = int(predicted_high.sum())
        actual_count = int(actual_high.sum())
        precision = true_positive / predicted_count if predicted_count else np.nan
        false_negative_rate = false_negative / actual_count if actual_count else 0.0
        lp_reduction = int((~predicted_high).sum()) / len(frame) if len(frame) else np.nan
        rows.append(
            {
                "Proxy Threshold": threshold,
                "Rows": len(frame),
                "Actual High Drift Rows": actual_count,
                "Predicted High Drift Rows": predicted_count,
                "True Positives": true_positive,
                "False Positives": false_positive,
                "False Negatives": false_negative,
                "Precision": precision,
                "False Negative Rate": false_negative_rate,
                "Potential Full-LP Reduction": lp_reduction,
                "Proxy Reliable Under FN Rule": bool(false_negative_rate <= 0.10),
            }
        )
    return pd.DataFrame(rows)


def _write_report(path: Path, validation: pd.DataFrame, summary: pd.DataFrame, drift_threshold: float) -> None:
    reliable = bool((summary["Proxy Reliable Under FN Rule"] == True).any()) if not summary.empty else False
    useful = False
    if reliable:
        reliable_rows = summary[summary["Proxy Reliable Under FN Rule"] == True]
        useful = bool((reliable_rows["Potential Full-LP Reduction"] > 0.05).any())
    decision = (
        "proxy passed the false-negative gate"
        if useful
        else "proxy failed as a useful production gate; full LP confirmation should remain mandatory"
    )
    lines = [
        "# Drift Proxy Validation Report",
        "",
        "## Proxy Definition",
        "",
        "The proxy uses only candidate-level fast outputs available before full confirmation: primary-score gap, route cost deviation, planned load-ratio deviation, route-count mismatch, fast stockout deviation, fast shortfall deviation, and fast load-penalty deviation.",
        "",
        "It does not use full-scenario LP results.",
        "",
        "## Validation Summary",
        "",
        f"- High drift threshold: stockout relative drift > {drift_threshold}",
        f"- Validation rows: {len(validation)}",
        f"- Decision: {decision}",
        "",
        _markdown_table(summary),
        "",
        "## Interpretation",
        "",
        "- If false negative rate exceeds 10%, the proxy is not safe: it would skip candidates that later show high full-confirmation drift.",
        "- A threshold that marks nearly every row high-risk is technically safe but not useful because it does not reduce full-LP calls.",
        "- Current OR-Tools does not expose a native `random_seed` field in this environment. Seeded variants are implemented through reproducible search-cost perturbation, with route costs still reported on the original distance matrix. A future validation round should repeat this with a native-seed OR-Tools build if available.",
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


if __name__ == "__main__":
    main()
