from __future__ import annotations

from dataclasses import dataclass
import re
import time

import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from .cvrplib import CVRPInstance, customer_view


@dataclass(frozen=True)
class RouteSolution:
    method: str
    feasible: bool
    route_cost: float
    routes: list[list[int]]
    runtime_sec: float
    reason: str = ""


def vehicle_count_from_name(name: str) -> int:
    match = re.search(r"-k(\d+)$", name)
    if match:
        return int(match.group(1))
    raise ValueError(f"Cannot infer vehicle count from instance name: {name}")


def solve_cvrp_ortools(
    instance: CVRPInstance,
    planned_customer_loads: np.ndarray,
    method: str,
    time_limit_sec: int = 5,
) -> RouteSolution:
    n_vehicles = vehicle_count_from_name(instance.name)
    planned_node_loads = _customer_loads_to_nodes(instance, planned_customer_loads)
    demand_int = np.rint(planned_node_loads).astype(int)

    if demand_int.max(initial=0) > instance.capacity:
        return RouteSolution(method, False, float("nan"), [], 0.0, "single_node_exceeds_capacity")
    if demand_int.sum() > n_vehicles * instance.capacity:
        return RouteSolution(method, False, float("nan"), [], 0.0, "total_load_exceeds_fleet_capacity")

    manager = pywrapcp.RoutingIndexManager(instance.n_nodes, n_vehicles, instance.depot_index)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index: int, to_index: int) -> int:
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(instance.distance_matrix[from_node, to_node])

    transit_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_index)

    def demand_callback(from_index: int) -> int:
        from_node = manager.IndexToNode(from_index)
        return int(demand_int[from_node])

    demand_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_index,
        0,
        [int(instance.capacity)] * n_vehicles,
        True,
        "Capacity",
    )

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_params.time_limit.FromSeconds(time_limit_sec)

    started = time.time()
    solution = routing.SolveWithParameters(search_params)
    runtime = time.time() - started
    if solution is None:
        return RouteSolution(method, False, float("nan"), [], runtime, "ortools_no_solution")

    routes: list[list[int]] = []
    route_cost = 0
    for vehicle_id in range(n_vehicles):
        index = routing.Start(vehicle_id)
        route: list[int] = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            prev_index = index
            index = solution.Value(routing.NextVar(index))
            route_cost += routing.GetArcCostForVehicle(prev_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        if len(route) > 2:
            routes.append(route)

    return RouteSolution(method, True, float(route_cost), routes, runtime)


def build_plans(history: np.ndarray, nominal: np.ndarray) -> dict[str, np.ndarray]:
    mean = history.mean(axis=0)
    std = history.std(axis=0)
    return {
        "nominal_or_tools": nominal,
        "proxy_mean_or_tools": mean,
        "quantile_p75_or_tools": np.quantile(history, 0.75, axis=0),
        "quantile_p90_or_tools": np.quantile(history, 0.90, axis=0),
        "robust_mean_1std_or_tools": mean + std,
        "robust_mean_2std_or_tools": mean + 2.0 * std,
    }


def add_capacity_projected_plans(
    plans: dict[str, np.ndarray],
    fleet_capacity: float,
    safety: float = 0.995,
) -> dict[str, np.ndarray]:
    """Add transparent capacity-projected variants for otherwise overloaded plans."""
    out = dict(plans)
    limit = fleet_capacity * safety
    for name, loads in plans.items():
        if name == "nominal_or_tools":
            continue
        total = float(np.sum(loads))
        if total > limit:
            factor = limit / total
            out[name.replace("_or_tools", "_scaled_or_tools")] = loads * factor
    return out


def evaluate_fixed_load_plan(
    planned_customer_loads: np.ndarray,
    scenarios: np.ndarray,
    route_cost: float,
    stockout_penalty: float = 3.0,
    overfill_cost: float = 0.15,
) -> dict[str, float]:
    shortfall = np.maximum(0.0, scenarios - planned_customer_loads[None, :])
    overfill = np.maximum(0.0, planned_customer_loads[None, :] - scenarios)
    total_costs = route_cost + stockout_penalty * shortfall.sum(axis=1) + overfill_cost * overfill.sum(axis=1)
    return {
        "mean_total_cost": float(total_costs.mean()),
        "p90_total_cost": float(np.quantile(total_costs, 0.90)),
        "mean_shortfall": float(shortfall.sum(axis=1).mean()),
        "p90_shortfall": float(np.quantile(shortfall.sum(axis=1), 0.90)),
        "stockout_rate": float((shortfall > 0).mean()),
        "mean_overfill": float(overfill.sum(axis=1).mean()),
    }


def _customer_loads_to_nodes(instance: CVRPInstance, customer_loads: np.ndarray) -> np.ndarray:
    _, customer_indices = customer_view(instance)
    out = np.zeros(instance.n_nodes, dtype=float)
    out[customer_indices] = np.asarray(customer_loads, dtype=float)
    return out
