from __future__ import annotations

import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

from .base import RouteSet, RoutingSolutionProvider


class VroomProvider(RoutingSolutionProvider):
    def __init__(
        self,
        vroom_url: str = "http://localhost:3000",
        method: str = "vroom_provider",
        timeout_sec: int = 30,
    ) -> None:
        self.url = vroom_url.rstrip("/")
        self.method = method
        self.timeout_sec = timeout_sec

    def solve(
        self,
        nodes: pd.DataFrame,
        demands: pd.DataFrame,
        vehicle_capacity: float,
        num_vehicles: int,
        distance_matrix: pd.DataFrame | None = None,
    ) -> RouteSet:
        payload = _build_payload(nodes, demands, vehicle_capacity, num_vehicles, distance_matrix)
        started = time.time()
        response = self._post(payload)
        runtime = time.time() - started
        route_set = _route_set_from_response(response, nodes, self.solver_name(), self.method)
        route_set.raw_metadata["runtime_sec"] = runtime
        return route_set

    def solver_name(self) -> str:
        return "vroom"

    def _post(self, payload: dict) -> dict:
        request = Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout_sec) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"VROOM HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            raise RuntimeError(f"VROOM is not reachable at {self.url}: {exc.reason}") from exc


def _build_payload(
    nodes: pd.DataFrame,
    demands: pd.DataFrame,
    vehicle_capacity: float,
    num_vehicles: int,
    distance_matrix: pd.DataFrame | None,
) -> dict:
    node_ids = [int(node_id) for node_id in nodes["id"].tolist()]
    depot_id = _depot_id(nodes)
    demand_by_node = {int(row.node_id): int(round(float(row.demand))) for row in demands.itertuples(index=False)}

    vehicles = [
        {
            "id": vehicle_id,
            "profile": "car",
            "start_index": depot_id,
            "end_index": depot_id,
            "capacity": [int(round(vehicle_capacity))],
        }
        for vehicle_id in range(num_vehicles)
    ]
    jobs = [
        {
            "id": node_id,
            "location_index": node_id,
            "delivery": [max(0, int(demand_by_node.get(node_id, 0)))],
        }
        for node_id in node_ids
        if node_id != depot_id and max(0, int(demand_by_node.get(node_id, 0))) > 0
    ]
    payload = {"vehicles": vehicles, "jobs": jobs}
    if distance_matrix is not None:
        matrix = _distance_matrix_to_int_lists(distance_matrix, node_ids)
        payload["matrices"] = {
            "car": {
                "durations": matrix,
                "costs": matrix,
            }
        }
    else:
        _add_locations(payload, nodes, depot_id)
    return payload


def _route_set_from_response(response: dict, nodes: pd.DataFrame, solver_name: str, method: str) -> RouteSet:
    if int(response.get("code", -1)) != 0:
        return RouteSet(
            routes=[],
            route_costs=[],
            total_cost=float("nan"),
            vehicle_assignments={},
            feasible=False,
            solver_name=solver_name,
            raw_metadata={"method": method, "response": response, "reason": response.get("error", "vroom_error")},
        )

    depot_id = _depot_id(nodes)
    unassigned = response.get("unassigned", [])
    route_costs = []
    routes = []
    vehicle_assignments = {}
    for route_idx, route_payload in enumerate(response.get("routes", [])):
        steps = route_payload.get("steps", [])
        route = [_node_from_step(step, depot_id) for step in steps]
        if len(route) > 2:
            routes.append(route)
            route_costs.append(float(route_payload.get("cost", route_payload.get("duration", 0.0))))
            vehicle_assignments[len(routes) - 1] = int(route_payload.get("vehicle", route_idx))

    summary = response.get("summary", {})
    total_cost = float(summary.get("cost", np.sum(route_costs)))
    feasible = len(unassigned) == 0
    return RouteSet(
        routes=routes if feasible else [],
        route_costs=route_costs if feasible else [],
        total_cost=total_cost if feasible else float("nan"),
        vehicle_assignments=vehicle_assignments if feasible else {},
        feasible=feasible,
        solver_name=solver_name,
        raw_metadata={
            "method": method,
            "response": response,
            "unassigned": unassigned,
            "reason": "unassigned_jobs" if unassigned else "",
        },
    )


def _distance_matrix_to_int_lists(distance_matrix: pd.DataFrame, node_ids: list[int]) -> list[list[int]]:
    if set(["from", "to", "cost"]).issubset(distance_matrix.columns):
        out = np.zeros((len(node_ids), len(node_ids)), dtype=int)
        for _, row in distance_matrix.iterrows():
            out[int(row["from"]), int(row["to"])] = int(round(float(row["cost"])))
        return out.tolist()
    return distance_matrix.loc[node_ids, node_ids].round().astype(int).values.tolist()


def _add_locations(payload: dict, nodes: pd.DataFrame, depot_id: int) -> None:
    if not {"lon", "lat"}.issubset(nodes.columns):
        raise ValueError("VroomProvider requires lon/lat columns when no custom matrix is provided")
    location_by_node = {
        int(row.id): [float(row.lon), float(row.lat)]
        for row in nodes[["id", "lon", "lat"]].itertuples(index=False)
    }
    for vehicle in payload["vehicles"]:
        vehicle.pop("start_index", None)
        vehicle.pop("end_index", None)
        vehicle["start"] = location_by_node[depot_id]
        vehicle["end"] = location_by_node[depot_id]
    for job in payload["jobs"]:
        node_id = int(job["id"])
        job.pop("location_index", None)
        job["location"] = location_by_node[node_id]


def _depot_id(nodes: pd.DataFrame) -> int:
    if "is_depot" in nodes.columns and bool(nodes["is_depot"].any()):
        return int(nodes.loc[nodes["is_depot"] == True, "id"].iloc[0])
    return int(nodes["id"].iloc[0])


def _node_from_step(step: dict, depot_id: int) -> int:
    if step.get("type") in {"start", "end"}:
        return int(step.get("location_index", depot_id))
    if step.get("type") == "job":
        return int(step["id"])
    return int(step.get("location_index", depot_id))
