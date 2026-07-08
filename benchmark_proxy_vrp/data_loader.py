from __future__ import annotations

import argparse
from dataclasses import dataclass
import re
from pathlib import Path
from urllib.request import urlopen

import pandas as pd
import vrplib

from .cvrplib import parse_cvrplib
from .download_cvrplib_selection import _markdown_table
from .ortools_baselines import vehicle_count_from_name


CVRPLIB_INSTANCES_URL = "https://galgos.inf.puc-rio.br/cvrplib/index.php/en/instances"
CVRPLIB_DOWNLOAD_BASE_URL = "https://galgos.inf.puc-rio.br/cvrplib/index.php/en/download"


@dataclass(frozen=True)
class XSelection:
    name: str
    bucket: str
    reason: str


X_SELECTION_V3 = [
    XSelection("X-n101-k25", "small", "Small X baseline; many vehicles relative to size."),
    XSelection("X-n106-k14", "small", "Small X case with moderate fleet count."),
    XSelection("X-n110-k13", "small", "Small X case with tight capacity and lower vehicle count."),
    XSelection("X-n115-k10", "small", "Small X case with lower vehicle count."),
    XSelection("X-n120-k6", "small", "Small X case with very low fleet count."),
    XSelection("X-n125-k30", "small", "Small X case with high route count."),
    XSelection("X-n129-k18", "small", "Small X boundary case."),
    XSelection("X-n134-k13", "small", "Additional small X case added to reach an 8/8/8 X stratification."),
    XSelection("X-n153-k22", "medium", "Medium X entry point after the small bucket."),
    XSelection("X-n157-k13", "medium", "Medium case with small capacity and lower fleet count."),
    XSelection("X-n162-k11", "medium", "Medium case with high capacity and lower route count."),
    XSelection("X-n167-k10", "medium", "Medium case with low vehicle count."),
    XSelection("X-n172-k51", "medium", "Medium case with many active routes."),
    XSelection("X-n176-k26", "medium", "Medium case with moderate-high route count."),
    XSelection("X-n181-k23", "medium", "Medium boundary case."),
    XSelection("X-n190-k8", "medium", "Additional medium X case added to reach an 8/8/8 X stratification."),
    XSelection("X-n223-k34", "large", "Large X case kept below 250 nodes for executable diagnostics."),
    XSelection("X-n228-k23", "large", "Large case with moderate fleet count."),
    XSelection("X-n233-k16", "large", "Large case with lower route count."),
    XSelection("X-n237-k14", "large", "Additional large X case below 250 nodes for executable diagnostics."),
    XSelection("X-n242-k48", "large", "Large case with high route count."),
    XSelection("X-n247-k50", "large", "Additional large X case with high route count."),
    XSelection("X-n251-k28", "large", "Large case around 250 nodes."),
    XSelection("X-n256-k16", "large", "Largest selected case in this executable X diagnostic."),
]


X_SELECTION_V4 = [
    XSelection("X-n101-k25", "x100_143", "Small X baseline; many vehicles relative to size."),
    XSelection("X-n106-k14", "x100_143", "Small X case with moderate fleet count."),
    XSelection("X-n110-k13", "x100_143", "Small X case with tight capacity and lower vehicle count."),
    XSelection("X-n115-k10", "x100_143", "Small X case with lower vehicle count."),
    XSelection("X-n120-k6", "x100_143", "Small X case with very low fleet count."),
    XSelection("X-n125-k30", "x100_143", "Small X case with high route count."),
    XSelection("X-n129-k18", "x100_143", "Small X boundary case."),
    XSelection("X-n134-k13", "x100_143", "Additional small X case from v3."),
    XSelection("X-n139-k10", "x100_143", "New small X case for v4 density."),
    XSelection("X-n143-k7", "x100_143", "Upper edge of the first X-size band."),
    XSelection("X-n148-k46", "x148_190", "High-vehicle case at the start of the second band."),
    XSelection("X-n153-k22", "x148_190", "Medium X entry point after the small bucket."),
    XSelection("X-n157-k13", "x148_190", "Medium case with small capacity and lower fleet count."),
    XSelection("X-n162-k11", "x148_190", "Medium case with high capacity and lower route count."),
    XSelection("X-n167-k10", "x148_190", "Medium case with low vehicle count."),
    XSelection("X-n172-k51", "x148_190", "Medium case with many active routes."),
    XSelection("X-n176-k26", "x148_190", "Medium case with moderate-high route count."),
    XSelection("X-n181-k23", "x148_190", "Medium boundary case."),
    XSelection("X-n186-k15", "x148_190", "New medium case for v4 density."),
    XSelection("X-n190-k8", "x148_190", "Upper edge of the second X-size band."),
    XSelection("X-n195-k51", "x195_237", "High-route case at the start of the third band."),
    XSelection("X-n200-k36", "x195_237", "Third-band case with moderate-high route count."),
    XSelection("X-n204-k19", "x195_237", "Third-band case with moderate route count."),
    XSelection("X-n209-k16", "x195_237", "Third-band case with lower route count."),
    XSelection("X-n214-k11", "x195_237", "Third-band low-route case."),
    XSelection("X-n219-k73", "x195_237", "Third-band high-route stress case."),
    XSelection("X-n223-k34", "x195_237", "Large X case kept below 250 nodes for executable diagnostics."),
    XSelection("X-n228-k23", "x195_237", "Large case with moderate fleet count."),
    XSelection("X-n233-k16", "x195_237", "Large case with lower route count."),
    XSelection("X-n237-k14", "x195_237", "Upper edge of the third X-size band."),
    XSelection("X-n242-k48", "x242_284", "Fourth-band case with high route count."),
    XSelection("X-n247-k50", "x242_284", "Fourth-band case with high route count."),
    XSelection("X-n251-k28", "x242_284", "Fourth-band case around 250 nodes."),
    XSelection("X-n256-k16", "x242_284", "Fourth-band lower-route case."),
    XSelection("X-n261-k13", "x242_284", "Fourth-band low-route case."),
    XSelection("X-n266-k58", "x242_284", "Fourth-band high-route stress case."),
    XSelection("X-n270-k35", "x242_284", "Fourth-band moderate-high route case."),
    XSelection("X-n275-k28", "x242_284", "Fourth-band moderate route case."),
    XSelection("X-n280-k17", "x242_284", "Fourth-band lower-route case."),
    XSelection("X-n284-k15", "x242_284", "Upper edge of the executable v4 set."),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and validate a stratified executable CVRPLIB X dataset.")
    parser.add_argument("--out-dir", default="benchmarks/cvrplib/raw_x_v3")
    parser.add_argument("--selection-output", default="instance_selection_v3.md")
    parser.add_argument("--selection", choices=["v3", "v4"], default="v3")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    name_to_id = _cvrplib_x_instance_ids()
    rows = []
    selected_instances = X_SELECTION_V4 if args.selection == "v4" else X_SELECTION_V3
    for selected in selected_instances:
        if selected.name not in name_to_id:
            raise ValueError(f"{selected.name} was not found on CVRPLIB instance index")
        cvrplib_id = name_to_id[selected.name]
        vrp_path = out_dir / f"{selected.name}.vrp"
        sol_path = out_dir / f"{selected.name}.sol"
        _download("instance", cvrplib_id, vrp_path)
        _download("bks", cvrplib_id, sol_path)

        parsed = parse_cvrplib(vrp_path, sol_path)
        vrplib_instance = vrplib.read_instance(str(vrp_path), instance_format="vrplib")
        if parsed.name != selected.name:
            raise ValueError(f"CVRPLIB id {cvrplib_id} returned {parsed.name}, expected {selected.name}")
        if int(vrplib_instance["dimension"]) != parsed.n_nodes:
            raise ValueError(f"{selected.name}: vrplib dimension mismatch")
        if parsed.coordinates is None:
            raise ValueError(f"{selected.name}: coordinates are required")

        vehicles = vehicle_count_from_name(parsed.name)
        capacity_pressure = float(parsed.demands.sum() / (vehicles * parsed.capacity))
        rows.append(
            {
                "Instance": parsed.name,
                "CVRPLIB id": cvrplib_id,
                "Bucket": selected.bucket,
                "Nodes": parsed.n_nodes,
                "Customers": parsed.n_customers,
                "Vehicles": vehicles,
                "Capacity": parsed.capacity,
                "Capacity pressure": capacity_pressure,
                "Best known cost": parsed.best_known_cost,
                "Reason": selected.reason,
            }
        )

    selection = pd.DataFrame(rows)
    _write_selection_report(selection, Path(args.selection_output))
    print(selection.to_string(index=False))


def _cvrplib_x_instance_ids() -> dict[str, int]:
    with urlopen(CVRPLIB_INSTANCES_URL, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")
    pattern = re.compile(
        r'href="/cvrplib/index\.php/en/download/instance/(\d+)"[^>]*>\s*(X-n\d+-k\d+)\s*</a>',
        re.S,
    )
    return {name: int(instance_id) for instance_id, name in pattern.findall(html)}


def _download(kind: str, cvrplib_id: int, out_path: Path) -> None:
    if out_path.exists():
        return
    url = f"{CVRPLIB_DOWNLOAD_BASE_URL}/{kind}/{cvrplib_id}"
    with urlopen(url, timeout=60) as response:
        out_path.write_bytes(response.read())


def _write_selection_report(selection: pd.DataFrame, path: Path) -> None:
    bucket_counts = selection["Bucket"].value_counts().rename_axis("Bucket").reset_index(name="Count")
    pressure_quantiles = selection["Capacity pressure"].quantile([0.25, 0.5, 0.75]).reset_index()
    pressure_quantiles.columns = ["Quantile", "Capacity pressure"]
    text = f"""# Instance Selection v3

This file records the actually downloaded CVRPLIB X-set expansion used by the load-allocation diagnostic.

The `vrplib` Python package is installed and used to validate the downloaded VRPLIB files. Downloads are performed through the official CVRPLIB instance endpoints because `vrplib==2.2.0` provides readers/writers, not a downloader API.

## Bucket Counts

{_markdown_table(bucket_counts.sort_values("Bucket"))}

## Capacity Pressure Quantiles

{_markdown_table(pressure_quantiles)}

## Selected Instances

{_markdown_table(selection)}
"""
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
