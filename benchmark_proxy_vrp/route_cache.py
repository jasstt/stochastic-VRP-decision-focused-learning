from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterable
from uuid import uuid4

import numpy as np

from .routing_providers.base import RouteSet


def route_cache_key(
    *,
    instance_name: str,
    routing_provider: str,
    route_plan: str,
    planned_customer_loads: Iterable[float],
    time_limit_sec: int,
    route_random_seed: int | None,
    route_cost_jitter: float,
) -> str:
    loads = np.asarray(list(planned_customer_loads), dtype=float)
    payload = {
        "instance_name": instance_name,
        "routing_provider": routing_provider,
        "route_plan": route_plan,
        "planned_load_sha256": hashlib.sha256(loads.tobytes()).hexdigest(),
        "planned_load_count": int(loads.size),
        "planned_load_sum": float(np.sum(loads)),
        "time_limit_sec": int(time_limit_sec),
        "route_random_seed": route_random_seed,
        "route_cost_jitter": float(route_cost_jitter),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_route(cache_dir: Path | None, key: str) -> RouteSet | None:
    if cache_dir is None:
        return None
    path = _cache_path(cache_dir, key)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    route_set = RouteSet(
        routes=[[int(node) for node in route] for route in payload.get("routes", [])],
        route_costs=[float(value) for value in payload.get("route_costs", [])],
        total_cost=float(payload.get("total_cost", 0.0)),
        vehicle_assignments={int(k): int(v) for k, v in payload.get("vehicle_assignments", {}).items()},
        feasible=bool(payload.get("feasible", False)),
        solver_name=str(payload.get("solver_name", "cache")),
        raw_metadata=dict(payload.get("raw_metadata", {})),
    )
    original_runtime = float(route_set.raw_metadata.get("runtime_sec", 0.0) or 0.0)
    route_set.raw_metadata["cache_hit"] = True
    route_set.raw_metadata["cache_original_runtime_sec"] = original_runtime
    route_set.raw_metadata["runtime_sec"] = 0.0
    return route_set


def store_route(cache_dir: Path | None, key: str, route_set: RouteSet) -> None:
    if cache_dir is None:
        return
    cache_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "routes": route_set.routes,
        "route_costs": route_set.route_costs,
        "total_cost": route_set.total_cost,
        "vehicle_assignments": {str(k): int(v) for k, v in route_set.vehicle_assignments.items()},
        "feasible": route_set.feasible,
        "solver_name": route_set.solver_name,
        "raw_metadata": dict(route_set.raw_metadata),
    }
    path = _cache_path(cache_dir, key)
    temp_path = path.with_name(f"{path.stem}.{os.getpid()}.{uuid4().hex[:8]}.tmp")
    temp_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    temp_path.replace(path)


def _cache_path(cache_dir: Path, key: str) -> Path:
    return cache_dir / f"{key[:32]}.json"
