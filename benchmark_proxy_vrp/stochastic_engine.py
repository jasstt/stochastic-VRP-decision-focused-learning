from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np
import pulp


@dataclass(frozen=True)
class DomainObjective:
    name: str
    shortage_penalty: np.ndarray
    surplus_penalty: np.ndarray
    load_penalty: np.ndarray | None = None
    risk_weight: float = 0.0
    cvar_alpha: float = 0.9
    description: str = ""


@dataclass(frozen=True)
class FixedRouteProblem:
    name: str
    route_groups: list[list[int]]
    route_capacity: float
    planning_scenarios: np.ndarray
    evaluation_scenarios: np.ndarray
    route_cost: float
    objective: DomainObjective

    @property
    def n_customers(self) -> int:
        return int(self.planning_scenarios.shape[1])

    @property
    def n_planning_scenarios(self) -> int:
        return int(self.planning_scenarios.shape[0])


@dataclass(frozen=True)
class EngineSolution:
    method: str
    feasible: bool
    loads: np.ndarray
    objective_value: float
    runtime_sec: float
    reason: str = ""


class StochasticDecisionEngine:
    """Reusable stochastic capacity-allocation engine for fixed route groups."""

    def solve(self, problem: FixedRouteProblem, time_limit_sec: int = 30) -> EngineSolution:
        _validate_problem(problem)

        n_customers = problem.n_customers
        n_scenarios = problem.n_planning_scenarios
        objective = problem.objective

        prob = pulp.LpProblem(problem.name, pulp.LpMinimize)
        load = pulp.LpVariable.dicts("load", range(n_customers), lowBound=0, cat="Continuous")
        short = pulp.LpVariable.dicts(
            "short",
            [(i, s) for i in range(n_customers) for s in range(n_scenarios)],
            lowBound=0,
            cat="Continuous",
        )
        surplus = pulp.LpVariable.dicts(
            "surplus",
            [(i, s) for i in range(n_customers) for s in range(n_scenarios)],
            lowBound=0,
            cat="Continuous",
        )

        scenario_losses = []
        for s in range(n_scenarios):
            loss_s = pulp.lpSum(
                float(objective.shortage_penalty[i]) * short[(i, s)]
                + float(objective.surplus_penalty[i]) * surplus[(i, s)]
                for i in range(n_customers)
            )
            scenario_losses.append(loss_s)

        load_penalty = _load_penalty(objective, n_customers)
        planned_load_loss = pulp.lpSum(float(load_penalty[i]) * load[i] for i in range(n_customers))
        expected_loss = (1.0 / n_scenarios) * pulp.lpSum(scenario_losses)
        if objective.risk_weight > 0:
            eta = pulp.LpVariable("cvar_eta", lowBound=0, cat="Continuous")
            excess = pulp.LpVariable.dicts("cvar_excess", range(n_scenarios), lowBound=0, cat="Continuous")
            for s, loss_s in enumerate(scenario_losses):
                prob += excess[s] >= loss_s - eta
            cvar = eta + (1.0 / ((1.0 - objective.cvar_alpha) * n_scenarios)) * pulp.lpSum(
                excess[s] for s in range(n_scenarios)
            )
            prob += expected_loss + planned_load_loss + float(objective.risk_weight) * cvar
        else:
            prob += expected_loss + planned_load_loss

        for route_id, cols in enumerate(problem.route_groups):
            prob += (
                pulp.lpSum(load[i] for i in cols) <= float(problem.route_capacity),
                f"route_capacity_{route_id}",
            )

        for i in range(n_customers):
            for s in range(n_scenarios):
                demand = float(problem.planning_scenarios[s, i])
                prob += short[(i, s)] >= demand - load[i]
                prob += surplus[(i, s)] >= load[i] - demand

        started = time.time()
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=time_limit_sec))
        runtime = time.time() - started
        status_name = pulp.LpStatus.get(status, str(status))
        if status_name == "Not Solved":
            return EngineSolution(problem.name, False, np.array([]), float("nan"), runtime, "lp_time_limit")
        if status_name != "Optimal":
            return EngineSolution(problem.name, False, np.array([]), float("nan"), runtime, f"lp_status_{status_name}")

        loads = np.array([max(0.0, float(pulp.value(load[i]) or 0.0)) for i in range(n_customers)])
        return EngineSolution(
            method=problem.name,
            feasible=True,
            loads=loads,
            objective_value=float(pulp.value(prob.objective) or 0.0),
            runtime_sec=runtime,
        )


def evaluate_solution(problem: FixedRouteProblem, loads: np.ndarray) -> dict[str, float]:
    objective = problem.objective
    scenarios = problem.evaluation_scenarios
    shortfall = np.maximum(0.0, scenarios - loads[None, :])
    surplus = np.maximum(0.0, loads[None, :] - scenarios)
    load_penalty = _load_penalty(objective, len(loads))
    losses = (
        shortfall @ objective.shortage_penalty.astype(float)
        + surplus @ objective.surplus_penalty.astype(float)
    )
    load_penalty_loss = float(loads @ load_penalty.astype(float))
    total_costs = problem.route_cost + losses + load_penalty_loss
    return {
        "mean_total_cost": float(total_costs.mean()),
        "p90_total_cost": float(np.quantile(total_costs, 0.90)),
        "cvar90_total_cost": float(_empirical_cvar(total_costs, 0.90)),
        "mean_shortfall": float(shortfall.sum(axis=1).mean()),
        "p90_shortfall": float(np.quantile(shortfall.sum(axis=1), 0.90)),
        "stockout_rate": float((shortfall > 0).mean()),
        "mean_surplus": float(surplus.sum(axis=1).mean()),
        "mean_domain_loss": float(losses.mean()),
        "mean_load_penalty_loss": load_penalty_loss,
    }


def _empirical_cvar(values: np.ndarray, alpha: float) -> float:
    threshold = np.quantile(values, alpha)
    tail = values[values >= threshold]
    return float(tail.mean()) if len(tail) else float(threshold)


def _validate_problem(problem: FixedRouteProblem) -> None:
    n_customers = problem.n_customers
    if problem.evaluation_scenarios.shape[1] != n_customers:
        raise ValueError("Planning/evaluation scenario customer dimensions differ")
    if len(problem.objective.shortage_penalty) != n_customers:
        raise ValueError("shortage_penalty length does not match customers")
    if len(problem.objective.surplus_penalty) != n_customers:
        raise ValueError("surplus_penalty length does not match customers")
    if problem.objective.load_penalty is not None and len(problem.objective.load_penalty) != n_customers:
        raise ValueError("load_penalty length does not match customers")
    covered = sorted(col for group in problem.route_groups for col in group)
    if covered != list(range(n_customers)):
        raise ValueError("Route groups must cover each customer exactly once")
    if not (0.0 < problem.objective.cvar_alpha < 1.0):
        raise ValueError("cvar_alpha must be in (0, 1)")


def _load_penalty(objective: DomainObjective, n_customers: int) -> np.ndarray:
    if objective.load_penalty is None:
        return np.zeros(n_customers, dtype=float)
    return np.asarray(objective.load_penalty, dtype=float)
