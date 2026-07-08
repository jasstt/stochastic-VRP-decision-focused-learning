from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .analyze_stockout_mechanisms import _markdown_table
from .data_loader import X_SELECTION_V3
from .ortools_baselines import vehicle_count_from_name


PROVIDERS = {
    "OR-Tools": "domain_engine_results_ortools_provider.csv",
    "VROOM": "domain_engine_results_vroom_provider.csv",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize the executed CVRPLIB X dataset expansion.")
    parser.add_argument("--data-dir", default="benchmarks/proxy_cvrplib_x_v3")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_path = Path(args.out) if args.out else data_dir / "x_dataset_expansion_report.md"
    manifest = pd.read_csv(data_dir / "manifest.csv")
    selection = pd.DataFrame(
        [{"name": item.name, "Bucket": item.bucket, "Selection Reason": item.reason} for item in X_SELECTION_V3]
    )
    manifest = manifest.merge(selection, on="name", how="left")
    manifest["vehicles"] = manifest["name"].map(vehicle_count_from_name)
    manifest["capacity_pressure"] = (
        manifest["mean_nominal_demand"] * manifest["customers"] / (manifest["vehicles"] * manifest["capacity"])
    )
    results = {provider: pd.read_csv(data_dir / filename) for provider, filename in PROVIDERS.items()}

    dataset_summary = _dataset_summary(manifest)
    feasibility = _feasibility_summary(results)
    domain_summary = _domain_summary(results)
    stockout_rank = _stockout_ranking(results)
    runtime = _runtime_summary(results, manifest)
    common_feasible = _common_feasible_instances(results)

    _write_report(
        out_path,
        manifest=manifest,
        dataset_summary=dataset_summary,
        feasibility=feasibility,
        domain_summary=domain_summary,
        stockout_rank=stockout_rank,
        runtime=runtime,
        common_feasible=common_feasible,
    )
    print(f"Saved {out_path}")
    print("Feasibility")
    print(feasibility.to_string(index=False))
    print("\nDomain summary")
    print(domain_summary.to_string(index=False))
    print("\nRuntime")
    print(runtime.to_string(index=False))


def _dataset_summary(manifest: pd.DataFrame) -> pd.DataFrame:
    return (
        manifest.groupby("Bucket")
        .agg(
            instances=("name", "count"),
            min_nodes=("nodes", "min"),
            max_nodes=("nodes", "max"),
            mean_capacity_pressure=("capacity_pressure", "mean"),
        )
        .reset_index()
        .sort_values("Bucket")
    )


def _feasibility_summary(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for provider, df in results.items():
        feasible = df[df["feasible"] == True]
        failed = sorted(df[(df["domain"] == "all") & (df["feasible"] == False)]["instance"].unique())
        rows.append(
            {
                "Provider": provider,
                "Total Instances": int(df["instance"].nunique()),
                "Feasible Instances": int(feasible["instance"].nunique()),
                "Feasible Domain Rows": int(len(feasible)),
                "Failed Instances": ", ".join(failed) if failed else "",
            }
        )
    common = _common_feasible_instances(results)
    rows.append(
        {
            "Provider": "Common OR-Tools and VROOM",
            "Total Instances": int(next(iter(results.values()))["instance"].nunique()),
            "Feasible Instances": int(len(common)),
            "Feasible Domain Rows": int(len(common) * 4),
            "Failed Instances": "",
        }
    )
    return pd.DataFrame(rows)


def _common_feasible_instances(results: dict[str, pd.DataFrame]) -> list[str]:
    feasible_sets = []
    for df in results.values():
        feasible_sets.append(set(df[df["feasible"] == True]["instance"].unique()))
    common = set.intersection(*feasible_sets) if feasible_sets else set()
    return sorted(common)


def _domain_summary(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for provider, df in results.items():
        feasible = df[df["feasible"] == True].copy()
        summary = (
            feasible.groupby("domain")
            .agg(
                feasible_instances=("instance", "nunique"),
                avg_mean_total_cost=("mean_total_cost", "mean"),
                avg_stockout_rate=("stockout_rate", "mean"),
                avg_runtime_sec=("runtime_sec", "mean"),
                avg_mean_load_penalty_loss=("mean_load_penalty_loss", "mean"),
            )
            .reset_index()
            .sort_values("avg_mean_total_cost")
        )
        summary.insert(0, "Provider", provider)
        rows.append(summary)
    return pd.concat(rows, ignore_index=True)


def _stockout_ranking(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for provider, df in results.items():
        feasible = df[df["feasible"] == True].copy()
        ranked = (
            feasible.groupby("domain")
            .agg(avg_stockout_rate=("stockout_rate", "mean"))
            .reset_index()
            .sort_values("avg_stockout_rate", ascending=False)
        )
        rows.append(
            {
                "Provider": provider,
                "Stockout Ranking High-to-Low": " > ".join(ranked["domain"].tolist()),
            }
        )
    return pd.DataFrame(rows)


def _runtime_summary(results: dict[str, pd.DataFrame], manifest: pd.DataFrame) -> pd.DataFrame:
    rows = []
    bucket_map = dict(zip(manifest["name"], manifest["Bucket"]))
    for provider, df in results.items():
        feasible = df[df["feasible"] == True].copy()
        feasible["Bucket"] = feasible["instance"].map(bucket_map)
        for bucket, group in feasible.groupby("Bucket"):
            rows.append(
                {
                    "Provider": provider,
                    "Bucket": bucket,
                    "Rows": int(len(group)),
                    "Instances": int(group["instance"].nunique()),
                    "Avg Runtime Sec Per Domain Row": float(group["runtime_sec"].mean()),
                    "P90 Runtime Sec Per Domain Row": float(group["runtime_sec"].quantile(0.9)),
                    "Max Runtime Sec Per Domain Row": float(group["runtime_sec"].max()),
                }
            )
    return pd.DataFrame(rows).sort_values(["Provider", "Bucket"])


def _write_report(
    path: Path,
    manifest: pd.DataFrame,
    dataset_summary: pd.DataFrame,
    feasibility: pd.DataFrame,
    domain_summary: pd.DataFrame,
    stockout_rank: pd.DataFrame,
    runtime: pd.DataFrame,
    common_feasible: list[str],
) -> None:
    cost_rank_rows = []
    for provider, group in domain_summary.groupby("Provider"):
        ranked = group.sort_values("avg_mean_total_cost")
        cost_rank_rows.append(
            {
                "Provider": provider,
                "Cost Ranking Low-to-High": " < ".join(ranked["domain"].tolist()),
            }
        )
    cost_rank = pd.DataFrame(cost_rank_rows)

    text = f"""# X Dataset Expansion Report

## Scope

The CVRPLIB X expansion was actually executed, not only designed. The selected set contains {manifest["name"].nunique()} instances with an 8/8/8 small/medium/large split. The proxy generator used the existing project pipeline with `history_rows=180`, `scenario_count=100`, seed `31415`, and CVRPLIB distance matrices.

`vrplib==2.2.0` was installed and used to validate downloaded VRPLIB files. Downloads used the official CVRPLIB instance and BKS endpoints because this `vrplib` release has readers/writers but no download API.

## Dataset Balance

{_markdown_table(dataset_summary)}

## Selected Instances

{_markdown_table(manifest[["name", "Bucket", "nodes", "customers", "capacity", "best_known_cost"]])}

## Feasibility Health Check

{_markdown_table(feasibility)}

Common feasible instances for OR-Tools and VROOM: {len(common_feasible)}.

```text
{", ".join(common_feasible)}
```

This is an important health result: VROOM solved more X anchors than OR-Tools under the selected limits. Therefore X-set claims should distinguish all downloaded instances (n={manifest["name"].nunique()}) from common provider-feasible instances (n={len(common_feasible)}).

## Domain Cost Ranking

{_markdown_table(cost_rank)}

Detailed provider/domain averages:

{_markdown_table(domain_summary)}

## Stockout Ranking

{_markdown_table(stockout_rank)}

The domain cost ordering is broadly stable in the sense that `grocery` remains the cheapest and `cold_chain` remains the most expensive under both providers. Stockout ordering is not stable across providers, which preserves A.8 as a live mechanism question.

## Runtime

Runtime is reported from the project `runtime_sec` field per feasible provider-domain row. This includes the anchor route solve time plus that domain LP solve time; anchor time is repeated across the four domain rows, so these values should be read as per-row diagnostic runtime rather than exact end-to-end wall time.

{_markdown_table(runtime)}
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
