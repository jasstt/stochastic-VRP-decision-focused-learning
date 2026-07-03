from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize benchmark proxy baseline results.")
    parser.add_argument("--results", default="benchmarks/proxy_cvrplib/baseline_results.csv")
    args = parser.parse_args()

    result_path = Path(args.results)
    out_dir = result_path.parent
    df = pd.read_csv(result_path)
    feasible = df[df["feasible"] == True].copy()

    nominal = (
        feasible[feasible["method"] == "nominal_or_tools"]
        .set_index("instance")[["mean_total_cost", "stockout_rate"]]
        .rename(columns={"mean_total_cost": "nominal_cost", "stockout_rate": "nominal_stockout"})
    )
    feasible = feasible.join(nominal, on="instance")
    feasible["cost_ratio_vs_nominal"] = feasible["mean_total_cost"] / feasible["nominal_cost"]
    feasible["stockout_delta_vs_nominal"] = feasible["stockout_rate"] - feasible["nominal_stockout"]

    best_cost = feasible.loc[feasible.groupby("instance")["mean_total_cost"].idxmin()].copy()
    best_stockout = feasible.loc[feasible.groupby("instance")["stockout_rate"].idxmin()].copy()
    best = best_cost[
        ["instance", "method", "mean_total_cost", "stockout_rate", "route_cost", "planned_load_total"]
    ].rename(columns={"method": "best_cost_method", "mean_total_cost": "best_cost"})
    best = best.merge(
        best_stockout[["instance", "method", "stockout_rate", "mean_total_cost"]].rename(
            columns={"method": "best_stockout_method", "stockout_rate": "best_stockout"}
        ),
        on="instance",
        how="left",
    )

    summary = (
        feasible.groupby("method")
        .agg(
            feasible_instances=("instance", "nunique"),
            avg_cost_ratio_vs_nominal=("cost_ratio_vs_nominal", "mean"),
            avg_stockout_delta_vs_nominal=("stockout_delta_vs_nominal", "mean"),
            avg_stockout_rate=("stockout_rate", "mean"),
            avg_p90_total_cost=("p90_total_cost", "mean"),
            avg_mean_shortfall=("mean_shortfall", "mean"),
        )
        .reset_index()
        .sort_values(["feasible_instances", "avg_cost_ratio_vs_nominal"], ascending=[False, True])
    )

    win_cost_methods = best_cost["method"].value_counts().rename_axis("method").reset_index(name="cost_wins")
    win_stockout_methods = best_stockout["method"].value_counts().rename_axis("method").reset_index(name="stockout_wins")
    summary = summary.merge(win_cost_methods, on="method", how="left")
    summary = summary.merge(win_stockout_methods, on="method", how="left")
    summary[["cost_wins", "stockout_wins"]] = summary[["cost_wins", "stockout_wins"]].fillna(0).astype(int)

    best.to_csv(out_dir / "best_by_instance.csv", index=False)
    summary.to_csv(out_dir / "method_summary.csv", index=False)

    print("Best by instance")
    print(best.to_string(index=False))
    print("\nMethod summary")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

