from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize common engine domain-adapter results.")
    parser.add_argument("--results", default="benchmarks/proxy_cvrplib/domain_engine_results.csv")
    args = parser.parse_args()

    result_path = Path(args.results)
    out_dir = result_path.parent
    df = pd.read_csv(result_path)
    if "mean_load_penalty_loss" not in df.columns:
        df["mean_load_penalty_loss"] = 0.0
    feasible = df[df["feasible"] == True].copy()

    domain_summary = (
        feasible.groupby("domain")
        .agg(
            feasible_instances=("instance", "nunique"),
            avg_mean_total_cost=("mean_total_cost", "mean"),
            avg_p90_total_cost=("p90_total_cost", "mean"),
            avg_cvar90_total_cost=("cvar90_total_cost", "mean"),
            avg_stockout_rate=("stockout_rate", "mean"),
            avg_mean_shortfall=("mean_shortfall", "mean"),
            avg_mean_surplus=("mean_surplus", "mean"),
            avg_mean_load_penalty_loss=("mean_load_penalty_loss", "mean"),
            avg_planned_load_total=("planned_load_total", "mean"),
        )
        .reset_index()
        .sort_values("avg_mean_total_cost")
    )

    best_by_instance_domain = feasible.loc[feasible.groupby("instance")["mean_total_cost"].idxmin()][
        [
            "instance",
            "domain",
            "method",
            "mean_total_cost",
            "stockout_rate",
            "planned_load_total",
            "anchor_method",
        ]
    ]

    domain_summary.to_csv(out_dir / "domain_summary.csv", index=False)
    best_by_instance_domain.to_csv(out_dir / "domain_best_by_instance.csv", index=False)

    print("Domain summary")
    print(domain_summary.to_string(index=False))
    print("\nBest domain by instance")
    print(best_by_instance_domain.to_string(index=False))


if __name__ == "__main__":
    main()
