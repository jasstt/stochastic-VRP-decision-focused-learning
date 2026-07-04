from __future__ import annotations

import argparse
from dataclasses import replace
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .cvrplib import CVRPInstance, parse_cvrplib
from .osrm_matrix import DEFAULT_OSRM_BASE_URL, build_osrm_instance, parse_bbox
from .proxy_scenarios import ProxyScenarioConfig, generate_proxy_demands


def main() -> None:
    parser = argparse.ArgumentParser(description="Build normalized CVRPLIB proxy datasets.")
    parser.add_argument("--raw-dir", default="benchmarks/cvrplib/raw")
    parser.add_argument("--out-dir", default="benchmarks/proxy_cvrplib")
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--scenarios", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--distance-source", choices=["cvrplib", "osrm"], default="cvrplib")
    parser.add_argument("--osrm-base-url", default=DEFAULT_OSRM_BASE_URL)
    parser.add_argument("--osrm-profile", default="driving")
    parser.add_argument("--osrm-coordinate-mode", choices=["scale-to-bbox", "lonlat"], default="scale-to-bbox")
    parser.add_argument("--osrm-bbox", default="13.30,52.45,13.55,52.60")
    parser.add_argument(
        "--osrm-cost-unit",
        choices=["duration_minutes", "duration_seconds", "distance_km", "distance_meters"],
        default="duration_minutes",
    )
    parser.add_argument("--osrm-timeout-sec", type=int, default=30)
    parser.add_argument("--osrm-cache-dir", default="benchmarks/osrm_cache")
    parser.add_argument("--osrm-missing-coordinates", choices=["fallback", "error"], default="fallback")
    parser.add_argument(
        "--proxy-feature-source",
        choices=["cvrplib", "active-distance"],
        default="cvrplib",
        help=(
            "Source used to generate proxy demand features. Use cvrplib for "
            "controlled OSRM comparisons where demand stays fixed across bboxes."
        ),
    )
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
        base_instance = parse_cvrplib(vrp_path, sol_path if sol_path.exists() else None)
        instance = base_instance
        if args.distance_source == "osrm":
            if instance.coordinates is None and args.osrm_missing_coordinates == "fallback":
                instance = replace(instance, distance_matrix_source="cvrplib:no_coordinates")
            else:
                instance = build_osrm_instance(
                    instance,
                    base_url=args.osrm_base_url,
                    profile=args.osrm_profile,
                    coordinate_mode=args.osrm_coordinate_mode,
                    bbox=parse_bbox(args.osrm_bbox),
                    cost_unit=args.osrm_cost_unit,
                    timeout_sec=args.osrm_timeout_sec,
                    cache_dir=args.osrm_cache_dir,
                )
        proxy_feature_instance = base_instance if args.proxy_feature_source == "cvrplib" else instance
        instance_dir = out_dir / instance.name
        instance_dir.mkdir(parents=True, exist_ok=True)

        history, scenarios, proxy_meta = generate_proxy_demands(proxy_feature_instance, config)
        _write_instance_json(instance, instance_dir / "instance.json", args.proxy_feature_source)
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
                "distance_matrix_source": instance.distance_matrix_source,
                "proxy_feature_source": args.proxy_feature_source,
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


def _write_instance_json(instance: CVRPInstance, path: Path, proxy_feature_source: str) -> None:
    payload = {
        "name": instance.name,
        "capacity": instance.capacity,
        "demands": instance.demands.astype(float).tolist(),
        "distance_matrix": instance.distance_matrix.astype(int).tolist(),
        "distance_matrix_source": instance.distance_matrix_source,
        "proxy_feature_source": proxy_feature_source,
        "depot_index": instance.depot_index,
        "coordinates": None if instance.coordinates is None else instance.coordinates.astype(float).tolist(),
        "osrm_coordinates": (
            None if instance.osrm_coordinates is None else instance.osrm_coordinates.astype(float).tolist()
        ),
        "travel_time_seconds_matrix": (
            None
            if instance.travel_time_seconds_matrix is None
            else instance.travel_time_seconds_matrix.astype(float).tolist()
        ),
        "road_distance_meters_matrix": (
            None
            if instance.road_distance_meters_matrix is None
            else instance.road_distance_meters_matrix.astype(float).tolist()
        ),
        "edge_weight_type": instance.edge_weight_type,
        "best_known_cost": instance.best_known_cost,
        "source_path": instance.source_path,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
