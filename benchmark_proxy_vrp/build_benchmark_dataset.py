from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import CVRPInstance, parse_cvrplib
from .proxy_scenarios import ProxyScenarioConfig, generate_proxy_demands


def main() -> None:
    parser = argparse.ArgumentParser(description="Build normalized CVRPLIB proxy datasets.")
    parser.add_argument("--raw-dir", default="benchmarks/cvrplib/raw")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--scenarios", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    config = ProxyScenarioConfig(
        n_days=args.days,
        n_scenarios=args.scenarios,
        seed=args.seed,
    )

    manifest_rows = []
    for vrp_path in sorted(raw_dir.glob("*.vrp")):
        sol_path = vrp_path.with_suffix(".sol")
        instance = parse_cvrplib(vrp_path, sol_path if sol_path.exists() else None)
        instance_dir = out_dir / instance.name
        instance_dir.mkdir(parents=True, exist_ok=True)

        history, scenarios, proxy_meta = generate_proxy_demands(instance, config)
        _write_instance_json(instance, instance_dir / "instance.json")
        history.to_csv(instance_dir / "proxy_demand_history.csv", index_label="date")
        proxy_meta.to_csv(instance_dir / "proxy_node_meta.csv", index=False)
        np.save(instance_dir / "proxy_saa_scenarios.npy", scenarios)

        manifest_rows.append(
            {
                "name": instance.name,
                "nodes": instance.n_nodes,
                "customers": instance.n_customers,
                "capacity": instance.capacity,
                "edge_weight_type": instance.edge_weight_type,
                "best_known_cost": instance.best_known_cost,
                "history_rows": len(history),
                "scenario_count": len(scenarios),
                "mean_nominal_demand": float(instance.demands[instance.demands > 0].mean()),
                "mean_proxy_demand": float(history.to_numpy().mean()),
                "scenario_mean": float(scenarios.mean()),
            }
        )

    manifest = pd.DataFrame(manifest_rows)
    manifest.to_csv(out_dir / "manifest.csv", index=False)
    print(manifest.to_string(index=False))


def _write_instance_json(instance: CVRPInstance, path: Path) -> None:
    payload = {
        "name": instance.name,
        "capacity": instance.capacity,
        "demands": instance.demands.astype(float).tolist(),
        "distance_matrix": instance.distance_matrix.astype(int).tolist(),
        "depot_index": instance.depot_index,
        "coordinates": None if instance.coordinates is None else instance.coordinates.astype(float).tolist(),
        "edge_weight_type": instance.edge_weight_type,
        "best_known_cost": instance.best_known_cost,
        "source_path": instance.source_path,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

