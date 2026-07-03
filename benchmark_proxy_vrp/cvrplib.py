from __future__ import annotations

from dataclasses import dataclass
import json
import math
import re
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class CVRPInstance:
    name: str
    capacity: int
    demands: np.ndarray
    distance_matrix: np.ndarray
    depot_index: int
    coordinates: np.ndarray | None
    edge_weight_type: str
    best_known_cost: int | None
    source_path: str

    @property
    def n_nodes(self) -> int:
        return int(len(self.demands))

    @property
    def n_customers(self) -> int:
        return self.n_nodes - 1


def parse_solution_cost(path: str | Path) -> int | None:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"\bCost\s+(\d+)", text)
    return int(match.group(1)) if match else None


def parse_cvrplib(path: str | Path, solution_path: str | Path | None = None) -> CVRPInstance:
    raw_path = Path(path)
    lines = [
        line.strip()
        for line in raw_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if line.strip()
    ]

    meta: dict[str, str] = {}
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in lines:
        upper = line.upper()
        if upper == "EOF":
            break
        if upper.endswith("_SECTION") or upper == "EDGE_WEIGHT_SECTION":
            current = upper
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip().upper()] = value.strip()

    name = meta.get("NAME", raw_path.stem)
    capacity = int(meta["CAPACITY"])
    dimension = int(meta["DIMENSION"])
    edge_weight_type = meta.get("EDGE_WEIGHT_TYPE", "").upper()

    demands = np.zeros(dimension, dtype=float)
    for line in sections.get("DEMAND_SECTION", []):
        parts = line.split()
        if len(parts) >= 2:
            node_id = int(parts[0])
            demands[node_id - 1] = float(parts[1])

    depot_ids = []
    for line in sections.get("DEPOT_SECTION", []):
        value = int(line.split()[0])
        if value == -1:
            break
        depot_ids.append(value)
    depot_index = (depot_ids[0] - 1) if depot_ids else 0

    coordinates = _parse_coordinates(sections.get("NODE_COORD_SECTION", []), dimension)
    if edge_weight_type == "EUC_2D":
        if coordinates is None:
            raise ValueError(f"{name}: EUC_2D instance has no coordinates")
        distance_matrix = _euc_2d_matrix(coordinates)
    elif edge_weight_type == "EXPLICIT":
        distance_matrix = _parse_explicit_matrix(
            sections.get("EDGE_WEIGHT_SECTION", []),
            dimension,
            meta.get("EDGE_WEIGHT_FORMAT", "").upper(),
        )
    else:
        raise ValueError(f"{name}: unsupported EDGE_WEIGHT_TYPE={edge_weight_type!r}")

    best_known = None
    if solution_path and Path(solution_path).exists():
        best_known = parse_solution_cost(solution_path)
    if best_known is None:
        match = re.search(r"Optimal value:\s*(\d+)", meta.get("COMMENT", ""))
        best_known = int(match.group(1)) if match else None

    return CVRPInstance(
        name=name,
        capacity=capacity,
        demands=demands,
        distance_matrix=distance_matrix,
        depot_index=depot_index,
        coordinates=coordinates,
        edge_weight_type=edge_weight_type,
        best_known_cost=best_known,
        source_path=str(raw_path),
    )


def _parse_coordinates(lines: list[str], dimension: int) -> np.ndarray | None:
    if not lines:
        return None
    coords = np.zeros((dimension, 2), dtype=float)
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            node_id = int(parts[0])
            coords[node_id - 1] = [float(parts[1]), float(parts[2])]
    return coords


def _euc_2d_matrix(coords: np.ndarray) -> np.ndarray:
    n = len(coords)
    out = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.hypot(coords[i, 0] - coords[j, 0], coords[i, 1] - coords[j, 1])
            rounded = int(math.floor(dist + 0.5))
            out[i, j] = rounded
            out[j, i] = rounded
    return out


def _parse_explicit_matrix(lines: list[str], dimension: int, fmt: str) -> np.ndarray:
    values: list[int] = []
    for line in lines:
        values.extend(int(x) for x in line.split())

    matrix = np.zeros((dimension, dimension), dtype=int)
    if fmt == "LOWER_ROW":
        expected = dimension * (dimension - 1) // 2
        if len(values) != expected:
            raise ValueError(f"LOWER_ROW expected {expected} values, got {len(values)}")
        idx = 0
        for i in range(1, dimension):
            for j in range(i):
                matrix[i, j] = values[idx]
                matrix[j, i] = values[idx]
                idx += 1
        return matrix
    raise ValueError(f"Unsupported EDGE_WEIGHT_FORMAT={fmt!r}")


def customer_view(instance: CVRPInstance) -> tuple[np.ndarray, np.ndarray]:
    mask = np.ones(instance.n_nodes, dtype=bool)
    mask[instance.depot_index] = False
    return instance.demands[mask], np.where(mask)[0]


def load_instance_json(path: str | Path) -> CVRPInstance:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    coords = payload.get("coordinates")
    return CVRPInstance(
        name=payload["name"],
        capacity=int(payload["capacity"]),
        demands=np.asarray(payload["demands"], dtype=float),
        distance_matrix=np.asarray(payload["distance_matrix"], dtype=int),
        depot_index=int(payload["depot_index"]),
        coordinates=None if coords is None else np.asarray(coords, dtype=float),
        edge_weight_type=payload["edge_weight_type"],
        best_known_cost=payload.get("best_known_cost"),
        source_path=payload.get("source_path", ""),
    )
