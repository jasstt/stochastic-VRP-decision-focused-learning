from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np
import pulp

from .cvrplib import CVRPInstance, customer_view
from .ortools_baselines import RouteSolution


@dataclass(frozen=True)
class LoadingSolution:
    method: str
    feasible: bool
    loads: np.ndarray
    objective_value: float
    runtime_sec: float
    reason: str = ""


def solve_stochastic_loading_lp(
    instance: CVRPInstance,
    anchor_routes: RouteSolution,
    planning_scenarios: np.ndarray,
    method: str,
    stockout_penalty: float = 3.0,
    overfill_cost: float = 0.15,
    time_limit_sec: int = 30,
) -> LoadingSolution:
    """Optimize fixed-route customer loads against demand scenarios.

    Routes come from a baseline CVRP solver. This LP only decides how much
    capacity to allocate to each customer on those fixed routes.
    """

    if not anchor_routes.feasible:
        return LoadingSolution(method, False, np.array([]), float("nan"), 0.0, "anchor_route_infeasible")

    customer_demands, customer_indices = customer_view(instance)
    node_to_customer_col = {int(node): pos for pos, node in enumerate(customer_indices)}
    n_customers = len(customer_demands)
    n_scenarios = len(planning_scenarios)
    route_groups = _route_groups(anchor_routes, node_to_customer_col)

    if sorted(col for group in route_groups for col in group) != list(range(n_customers)):
        return LoadingSolution(method, False, np.array([]), float("nan"), 0.0, "routes_do_not_cover_customers")

    prob = pulp.LpProblem(method, pulp.LpMinimize)
    load = pulp.LpVariable.dicts("load", range(n_customers), lowBound=0, cat="Continuous")
    short = pulp.LpVariable.dicts(
        "short",
        [(i, s) for i in range(n_customers) for s in range(n_scenarios)],
        lowBound=0,
        cat="Continuous",
    )
    over = pulp.LpVariable.dicts(
        "over",
        [(i, s) for i in range(n_customers) for s in range(n_scenarios)],
        lowBound=0,
        cat="Continuous",
    )

    prob += (1.0 / n_scenarios) * pulp.lpSum(
        stockout_penalty * short[(i, s)] + overfill_cost * over[(i, s)]
        for i in range(n_customers)
        for s in range(n_scenarios)
    )

    for route_id, cols in enumerate(route_groups):
        prob += (
            pulp.lpSum(load[i] for i in cols) <= float(instance.capacity),
            f"route_capacity_{route_id}",
        )

    for i in range(n_customers):
        for s in range(n_scenarios):
            demand = float(planning_scenarios[s, i])
            prob += short[(i, s)] >= demand - load[i]
            prob += over[(i, s)] >= load[i] - demand

    started = time.time()
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit_sec))
    runtime = time.time() - started
    status_name = pulp.LpStatus.get(status, str(status))
    if status_name not in {"Optimal", "Not Solved"}:
        return LoadingSolution(method, False, np.array([]), float("nan"), runtime, f"lp_status_{status_name}")
    if status_name == "Not Solved":
        return LoadingSolution(method, False, np.array([]), float("nan"), runtime, "lp_time_limit")

    loads = np.array([max(0.0, float(pulp.value(load[i]) or 0.0)) for i in range(n_customers)])
    return LoadingSolution(
        method=method,
        feasible=True,
        loads=loads,
        objective_value=float(pulp.value(prob.objective) or 0.0),
        runtime_sec=runtime,
    )


def _route_groups(anchor_routes: RouteSolution, node_to_customer_col: dict[int, int]) -> list[list[int]]:
    groups: list[list[int]] = []
    for route in anchor_routes.routes:
        cols = [node_to_customer_col[node] for node in route if node in node_to_customer_col]
        if cols:
            groups.append(cols)
    return groups

