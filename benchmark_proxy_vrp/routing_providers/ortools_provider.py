from __future__ import annotations

import time

import numpy as np
import pandas as pd

from ..cvrplib import CVRPInstance
from ..ortools_baselines import solve_cvrp_ortools
from .base import RouteSet, RoutingSolutionProvider


class OrToolsProvider(RoutingSolutionProvider):
    def __init__(
        self,
        method: str = "ortools_provider",
        time_limit_sec: int = 5,
        random_seed: int | None = None,
        cost_jitter: float = 0.0,
    ) -> None:
        self.method = method
        self.time_limit_sec = time_limit_sec
        self.random_seed = random_seed
        self.cost_jitter = cost_jitter

    def solve(
        self,
        nodes: pd.DataFrame,
        demands: pd.DataFrame,
        vehicle_capacity: float,
        num_vehicles: int,
        distance_matrix: pd.DataFrame | None = None,
    ) -> RouteSet:
        instance, planned_customer_loads = _provider_inputs_to_instance(
            nodes=nodes,
            demands=demands,
            vehicle_capacity=vehicle_capacity,
            num_vehicles=num_vehicles,
            distance_matrix=distance_matrix,
        )
        solution = solve_cvrp_ortools(
            instance,
            planned_customer_loads,
            method=self.method,
            time_limit_sec=self.time_limit_sec,
            random_seed=self.random_seed,
            cost_jitter=self.cost_jitter,
        )
        route_costs = _route_costs(solution.routes, instance.distance_matrix)
        return RouteSet(
            routes=solution.routes,
            route_costs=route_costs,
            total_cost=solution.route_cost,
            vehicle_assignments={idx: idx for idx, _ in enumerate(solution.routes)},
            feasible=solution.feasible,
            solver_name=self.solver_name(),
            raw_metadata={
                "method": solution.method,
                "runtime_sec": solution.runtime_sec,
                "reason": solution.reason,
                "random_seed": self.random_seed,
                "cost_jitter": self.cost_jitter,
            },
        )

    def solver_name(self) -> str:
        return "ortools"


def _provider_inputs_to_instance(
    nodes: pd.DataFrame,
    demands: pd.DataFrame,
    vehicle_capacity: float,
    num_vehicles: int,
    distance_matrix: pd.DataFrame | None,
) -> tuple[CVRPInstance, np.ndarray]:
    node_ids = [int(node_id) for node_id in nodes["id"].tolist()]
    if node_ids != list(range(len(node_ids))):
        raise ValueError("OrToolsProvider expects zero-based contiguous node ids")

    if distance_matrix is None:
        raise ValueError("OrToolsProvider requires a distance_matrix")

    matrix = _distance_matrix_to_numpy(distance_matrix, node_ids)
    demand_by_node = {int(row.node_id): float(row.demand) for row in demands.itertuples(index=False)}
    all_demands = np.asarray([demand_by_node.get(node_id, 0.0) for node_id in node_ids], dtype=float)
    depot_index = int(nodes.loc[nodes.get("is_depot", False) == True, "id"].iloc[0]) if "is_depot" in nodes else 0
    customer_loads = np.asarray([all_demands[node_id] for node_id in node_ids if node_id != depot_index], dtype=float)

    coordinates = None
    if {"x", "y"}.issubset(nodes.columns):
        coordinates = nodes[["x", "y"]].to_numpy(dtype=float)
    elif {"lon", "lat"}.issubset(nodes.columns):
        coordinates = nodes[["lon", "lat"]].to_numpy(dtype=float)

    instance = CVRPInstance(
        name=f"provider-k{num_vehicles}",
        capacity=int(round(vehicle_capacity)),
        demands=all_demands,
        distance_matrix=matrix,
        depot_index=depot_index,
        coordinates=coordinates,
        edge_weight_type="EXPLICIT",
        best_known_cost=None,
        source_path="routing_provider",
    )
    return instance, customer_loads


def _distance_matrix_to_numpy(distance_matrix: pd.DataFrame, node_ids: list[int]) -> np.ndarray:
    if set(["from", "to", "cost"]).issubset(distance_matrix.columns):
        out = np.zeros((len(node_ids), len(node_ids)), dtype=int)
        for _, row in distance_matrix.iterrows():
            out[int(row["from"]), int(row["to"])] = int(round(float(row["cost"])))
        return out
    return distance_matrix.loc[node_ids, node_ids].to_numpy(dtype=int)


def _route_costs(routes: list[list[int]], matrix: np.ndarray) -> list[float]:
    costs = []
    for route in routes:
        total = 0.0
        for i in range(len(route) - 1):
            total += float(matrix[route[i], route[i + 1]])
        costs.append(total)
    return costs
