from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np

from .cvrplib import CVRPInstance


DEFAULT_OSRM_BASE_URL = "https://router.project-osrm.org"
DEFAULT_OSRM_BBOX = (13.30, 52.45, 13.55, 52.60)


@dataclass(frozen=True)
class OSRMMatrix:
    cost_matrix: np.ndarray
    duration_seconds: np.ndarray
    distance_meters: np.ndarray
    lonlat: np.ndarray
    source: str


def build_osrm_instance(
    instance: CVRPInstance,
    base_url: str = DEFAULT_OSRM_BASE_URL,
    profile: str = "driving",
    coordinate_mode: str = "scale-to-bbox",
    bbox: tuple[float, float, float, float] = DEFAULT_OSRM_BBOX,
    cost_unit: str = "duration_minutes",
    timeout_sec: int = 30,
    cache_dir: str | Path | None = "benchmarks/osrm_cache",
) -> CVRPInstance:
    """Return a copy of a CVRP instance with OSRM-derived road costs."""

    matrix = fetch_osrm_matrix(
        instance,
        base_url=base_url,
        profile=profile,
        coordinate_mode=coordinate_mode,
        bbox=bbox,
        cost_unit=cost_unit,
        timeout_sec=timeout_sec,
        cache_dir=cache_dir,
    )
    return CVRPInstance(
        name=instance.name,
        capacity=instance.capacity,
        demands=instance.demands,
        distance_matrix=matrix.cost_matrix,
        depot_index=instance.depot_index,
        coordinates=instance.coordinates,
        edge_weight_type=instance.edge_weight_type,
        best_known_cost=instance.best_known_cost,
        source_path=instance.source_path,
        distance_matrix_source=matrix.source,
        travel_time_seconds_matrix=matrix.duration_seconds,
        road_distance_meters_matrix=matrix.distance_meters,
        osrm_coordinates=matrix.lonlat,
    )


def fetch_osrm_matrix(
    instance: CVRPInstance,
    base_url: str = DEFAULT_OSRM_BASE_URL,
    profile: str = "driving",
    coordinate_mode: str = "scale-to-bbox",
    bbox: tuple[float, float, float, float] = DEFAULT_OSRM_BBOX,
    cost_unit: str = "duration_minutes",
    timeout_sec: int = 30,
    cache_dir: str | Path | None = "benchmarks/osrm_cache",
) -> OSRMMatrix:
    if instance.coordinates is None:
        raise ValueError(f"{instance.name}: OSRM requires node coordinates")

    lonlat = coordinates_to_lonlat(instance.coordinates, coordinate_mode, bbox)
    payload = _load_or_query(
        lonlat=lonlat,
        base_url=base_url,
        profile=profile,
        timeout_sec=timeout_sec,
        cache_dir=Path(cache_dir) if cache_dir else None,
        n_nodes=instance.n_nodes,
    )

    durations = _matrix_from_payload(payload, "durations", instance.n_nodes)
    distances = _matrix_from_payload(payload, "distances", instance.n_nodes)
    cost_matrix = _cost_matrix(durations, distances, cost_unit)
    source = (
        f"osrm:{profile}:{cost_unit}:{coordinate_mode}:"
        f"{base_url.rstrip('/')}"
    )
    return OSRMMatrix(
        cost_matrix=cost_matrix,
        duration_seconds=durations,
        distance_meters=distances,
        lonlat=lonlat,
        source=source,
    )


def coordinates_to_lonlat(
    coordinates: np.ndarray,
    coordinate_mode: str,
    bbox: tuple[float, float, float, float],
) -> np.ndarray:
    coords = np.asarray(coordinates, dtype=float)
    if coords.ndim != 2 or coords.shape[1] != 2:
        raise ValueError(f"Expected Nx2 coordinates, got shape {coords.shape}")

    if coordinate_mode == "lonlat":
        return coords.copy()
    if coordinate_mode != "scale-to-bbox":
        raise ValueError(f"Unsupported OSRM coordinate mode: {coordinate_mode!r}")

    min_lon, min_lat, max_lon, max_lat = bbox
    x = coords[:, 0]
    y = coords[:, 1]
    lon = _scale_axis(x, min_lon, max_lon)
    lat = _scale_axis(y, min_lat, max_lat)
    return np.column_stack([lon, lat])


def parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [float(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("--osrm-bbox must be min_lon,min_lat,max_lon,max_lat")
    min_lon, min_lat, max_lon, max_lat = parts
    if min_lon >= max_lon or min_lat >= max_lat:
        raise ValueError("--osrm-bbox min values must be smaller than max values")
    return min_lon, min_lat, max_lon, max_lat


def _scale_axis(values: np.ndarray, out_min: float, out_max: float) -> np.ndarray:
    in_min = float(np.min(values))
    in_max = float(np.max(values))
    if math.isclose(in_min, in_max):
        midpoint = out_min + 0.5 * (out_max - out_min)
        return np.full_like(values, midpoint, dtype=float)
    return out_min + (values - in_min) * (out_max - out_min) / (in_max - in_min)


def _load_or_query(
    lonlat: np.ndarray,
    base_url: str,
    profile: str,
    timeout_sec: int,
    cache_dir: Path | None,
    n_nodes: int,
) -> dict:
    cache_path = _cache_path(lonlat, base_url, profile, cache_dir)
    if cache_path and cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    payload = _query_osrm_table(lonlat, base_url, profile, timeout_sec)
    _matrix_from_payload(payload, "durations", n_nodes)
    _matrix_from_payload(payload, "distances", n_nodes)
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _query_osrm_table(
    lonlat: np.ndarray,
    base_url: str,
    profile: str,
    timeout_sec: int,
) -> dict:
    coords = ";".join(f"{lon:.6f},{lat:.6f}" for lon, lat in lonlat)
    query = urlencode({"annotations": "duration,distance", "skip_waypoints": "true"})
    url = f"{base_url.rstrip('/')}/table/v1/{profile}/{coords}?{query}"
    request = Request(url, headers={"User-Agent": "benchmark-proxy-vrp/0.1"})
    try:
        with urlopen(request, timeout=timeout_sec) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OSRM request failed with HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"OSRM request failed: {exc.reason}") from exc

    if payload.get("code") != "Ok":
        raise RuntimeError(f"OSRM returned {payload.get('code')}: {payload.get('message', '')}")
    return payload


def _matrix_from_payload(payload: dict, key: str, n_nodes: int) -> np.ndarray:
    if key not in payload:
        raise RuntimeError(f"OSRM payload does not include {key!r}")
    matrix = np.asarray(payload[key], dtype=float)
    if matrix.shape != (n_nodes, n_nodes):
        raise RuntimeError(f"OSRM {key} shape {matrix.shape}, expected {(n_nodes, n_nodes)}")
    if not np.isfinite(matrix).all():
        raise RuntimeError(f"OSRM {key} includes null or non-finite cells")
    np.fill_diagonal(matrix, 0.0)
    return matrix


def _cost_matrix(
    durations: np.ndarray,
    distances: np.ndarray,
    cost_unit: str,
) -> np.ndarray:
    if cost_unit == "duration_minutes":
        values = np.ceil(durations / 60.0)
    elif cost_unit == "duration_seconds":
        values = np.ceil(durations)
    elif cost_unit == "distance_km":
        values = np.ceil(distances / 1000.0)
    elif cost_unit == "distance_meters":
        values = np.ceil(distances)
    else:
        raise ValueError(f"Unsupported OSRM cost unit: {cost_unit!r}")
    values = values.astype(int)
    np.fill_diagonal(values, 0)
    return values


def _cache_path(
    lonlat: np.ndarray,
    base_url: str,
    profile: str,
    cache_dir: Path | None,
) -> Path | None:
    if cache_dir is None:
        return None
    key_payload = {
        "base_url": base_url.rstrip("/"),
        "profile": profile,
        "lonlat": np.round(lonlat, 6).tolist(),
        "annotations": "duration,distance",
    }
    digest = hashlib.sha256(json.dumps(key_payload, sort_keys=True).encode("utf-8")).hexdigest()
    return cache_dir / f"osrm_table_{digest[:16]}.json"
