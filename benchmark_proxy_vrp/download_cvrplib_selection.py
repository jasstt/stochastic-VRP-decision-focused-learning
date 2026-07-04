from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

from .cvrplib import parse_cvrplib
from .ortools_baselines import vehicle_count_from_name


DEFAULT_BASE_URL = "https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download"


@dataclass(frozen=True)
class SelectedInstance:
    name: str
    cvrplib_id: int
    bucket: str
    reason: str


VALIDATION_N20 = [
    SelectedInstance("P-n16-k8", 75, "small", "Small/high-vehicle-count edge case; low capacity pressure."),
    SelectedInstance("P-n19-k2", 76, "small", "Existing coordinate-capable smoke instance; high capacity pressure."),
    SelectedInstance("P-n20-k2", 77, "small", "Boundary-small coordinate instance; high capacity pressure."),
    SelectedInstance("P-n21-k2", 78, "small", "Boundary-small coordinate instance used to avoid coordinate-less E-n13-k4."),
    SelectedInstance("E-n23-k3", 56, "medium", "Low capacity pressure medium case from a different CVRPLIB family."),
    SelectedInstance("B-n31-k5", 6, "medium", "Existing coordinate-capable instance; low capacity pressure."),
    SelectedInstance("A-n32-k5", 4, "medium", "Existing coordinate-capable instance; low capacity pressure."),
    SelectedInstance("A-n33-k5", 5, "medium", "Medium Augerat A-family geometry."),
    SelectedInstance("B-n34-k5", 32, "medium", "Medium B-family geometry with higher pressure than A-n32/B-n31."),
    SelectedInstance("B-n38-k6", 34, "medium", "Medium B-family, low capacity pressure."),
    SelectedInstance("A-n45-k6", 16, "medium", "Medium-high pressure A-family case."),
    SelectedInstance("P-n50-k8", 85, "medium", "Medium P-family case with very high capacity pressure."),
    SelectedInstance("E-n51-k5", 60, "large", "Large boundary case with high capacity pressure."),
    SelectedInstance("P-n55-k7", 88, "large", "Large P-family case with lower capacity pressure."),
    SelectedInstance("A-n60-k9", 23, "large", "Large A-family case."),
    SelectedInstance("P-n60-k10", 92, "large", "Large P-family case with different fleet count."),
    SelectedInstance("P-n65-k10", 94, "large", "Large P-family case, moderate-high capacity pressure."),
    SelectedInstance("E-n76-k7", 61, "large", "Large E-family case with lower pressure."),
    SelectedInstance("P-n76-k4", 96, "large", "Large P-family case with high pressure and fewer vehicles."),
    SelectedInstance("B-n78-k10", 53, "large", "Largest selected B-family case under the 100-node target."),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the coordinate-capable CVRPLIB n20 validation set.")
    parser.add_argument("--out-dir", default="benchmarks/cvrplib/raw_n20")
    parser.add_argument("--selection-output", default="instance_selection_v2.md")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for selected in VALIDATION_N20:
        vrp_path = out_dir / f"{selected.name}.vrp"
        sol_path = out_dir / f"{selected.name}.sol"
        _download(args.base_url, "instance", selected.cvrplib_id, vrp_path)
        _download(args.base_url, "instanceSolution", selected.cvrplib_id, sol_path)

        instance = parse_cvrplib(vrp_path, sol_path)
        if instance.name != selected.name:
            raise ValueError(f"CVRPLIB id {selected.cvrplib_id} returned {instance.name}, expected {selected.name}")
        if instance.coordinates is None:
            raise ValueError(f"{instance.name}: coordinates are required for exposure-rank validation")

        vehicles = vehicle_count_from_name(instance.name)
        capacity_pressure = float(instance.demands.sum() / (vehicles * instance.capacity))
        rows.append(
            {
                "Instance": instance.name,
                "CVRPLIB id": selected.cvrplib_id,
                "Bucket": selected.bucket,
                "Nodes": instance.n_nodes,
                "Customers": instance.n_customers,
                "Vehicles": vehicles,
                "Capacity": instance.capacity,
                "Capacity pressure": capacity_pressure,
                "Best known cost": instance.best_known_cost,
                "Reason": selected.reason,
            }
        )

    selection = pd.DataFrame(rows)
    _write_selection_report(selection, Path(args.selection_output))
    print(selection.to_string(index=False))


def _download(base_url: str, kind: str, cvrplib_id: int, out_path: Path) -> None:
    if out_path.exists():
        return
    url = f"{base_url.rstrip('/')}/{kind}/{cvrplib_id}"
    with urlopen(url, timeout=30) as response:
        out_path.write_bytes(response.read())


def _write_selection_report(selection: pd.DataFrame, path: Path) -> None:
    bucket_counts = selection["Bucket"].value_counts().rename_axis("Bucket").reset_index(name="Count")
    low_pressure = int((selection["Capacity pressure"] <= 0.88).sum())
    high_pressure = int((selection["Capacity pressure"] >= 0.95).sum())
    table = _markdown_table(selection)
    bucket_table = _markdown_table(bucket_counts.sort_values("Bucket"))
    text = f"""# Instance Selection v2

This validation set contains 20 coordinate-capable CVRPLIB CVRP instances for the grouping-exposure stockout validation.

`E-n13-k4` is deliberately excluded because it is an explicit-distance instance without coordinates in the current raw snapshot; exposure-rank analysis needs coordinates. The strict CVRPLIB coordinate pool has very few truly tiny n<20 cases, so `P-n20-k2` and `P-n21-k2` are treated as boundary-small instances to keep a four-instance small stratum without reintroducing coordinate-less data.

## Bucket Counts

{bucket_table}

## Capacity Pressure Coverage

- Low-pressure instances (`capacity_pressure <= 0.88`): {low_pressure}
- High-pressure instances (`capacity_pressure >= 0.95`): {high_pressure}

## Selected Instances

{table}
"""
    path.write_text(text, encoding="utf-8")


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    formatted = df.copy()
    for column in formatted.columns:
        if pd.api.types.is_float_dtype(formatted[column]):
            formatted[column] = formatted[column].map(lambda value: f"{value:.4f}")
    headers = list(formatted.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in formatted.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in headers) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
