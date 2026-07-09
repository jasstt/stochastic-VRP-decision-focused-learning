from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np
import pulp
from ortools.linear_solver import pywraplp


SUPPORTED_LP_BACKENDS = ("pulp_cbc", "ortools_glop", "ortools_pdlp")
_ORTOOLS_BACKENDS = {"ortools_glop": "GLOP", "ortools_pdlp": "PDLP"}


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
    route_load_targets: list[float] | None = None

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

    def __init__(self, lp_backend: str = "pulp_cbc") -> None:
        self.lp_backend = normalize_lp_backend(lp_backend)

    def solve(self, problem: FixedRouteProblem, time_limit_sec: int = 30) -> EngineSolution:
        _validate_problem(problem)
        if self.lp_backend == "pulp_cbc":
            return _solve_pulp_cbc(problem, time_limit_sec)
        if self.lp_backend in _ORTOOLS_BACKENDS:
            return _solve_ortools_linear(problem, time_limit_sec, self.lp_backend)
        raise ValueError(f"Unsupported LP backend: {self.lp_backend}")


def available_lp_backends() -> list[str]:
    return list(SUPPORTED_LP_BACKENDS)


def normalize_lp_backend(lp_backend: str) -> str:
    key = lp_backend.lower().replace("-", "_")
    aliases = {
        "cbc": "pulp_cbc",
        "pulp": "pulp_cbc",
        "pulp_cbc": "pulp_cbc",
        "glop": "ortools_glop",
        "ortools_glop": "ortools_glop",
        "pdlp": "ortools_pdlp",
        "ortools_pdlp": "ortools_pdlp",
    }
    if key not in aliases:
        raise ValueError(f"Unknown LP backend {lp_backend!r}. Options: {', '.join(SUPPORTED_LP_BACKENDS)}")
    return aliases[key]


def _solve_pulp_cbc(problem: FixedRouteProblem, time_limit_sec: int) -> EngineSolution:
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
        if problem.route_load_targets is not None:
            prob += (
                pulp.lpSum(load[i] for i in cols) == float(problem.route_load_targets[route_id]),
                f"route_load_target_{route_id}",
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


def _solve_ortools_linear(problem: FixedRouteProblem, time_limit_sec: int, lp_backend: str) -> EngineSolution:
    solver_type = _ORTOOLS_BACKENDS[lp_backend]
    solver = pywraplp.Solver.CreateSolver(solver_type)
    if solver is None:
        return EngineSolution(problem.name, False, np.array([]), float("nan"), 0.0, f"lp_backend_unavailable_{lp_backend}")

    solver.SuppressOutput()
    if time_limit_sec > 0:
        solver.SetTimeLimit(int(time_limit_sec * 1000))

    n_customers = problem.n_customers
    n_scenarios = problem.n_planning_scenarios
    objective = problem.objective
    load_penalty = _load_penalty(objective, n_customers)
    infinity = solver.infinity()

    load = [solver.NumVar(0.0, infinity, f"load_{i}") for i in range(n_customers)]
    short = [solver.NumVar(0.0, infinity, "") for _ in range(n_customers * n_scenarios)]
    surplus = [solver.NumVar(0.0, infinity, "") for _ in range(n_customers * n_scenarios)]

    lp_objective = solver.Objective()
    lp_objective.SetMinimization()
    for i in range(n_customers):
        lp_objective.SetCoefficient(load[i], float(load_penalty[i]))
        shortage_coeff = float(objective.shortage_penalty[i]) / n_scenarios
        surplus_coeff = float(objective.surplus_penalty[i]) / n_scenarios
        for s in range(n_scenarios):
            idx = _scenario_index(s, i, n_customers)
            lp_objective.SetCoefficient(short[idx], shortage_coeff)
            lp_objective.SetCoefficient(surplus[idx], surplus_coeff)

    if objective.risk_weight > 0:
        eta = solver.NumVar(0.0, infinity, "cvar_eta")
        excess = [solver.NumVar(0.0, infinity, "") for _ in range(n_scenarios)]
        lp_objective.SetCoefficient(eta, float(objective.risk_weight))
        excess_coeff = float(objective.risk_weight) / ((1.0 - objective.cvar_alpha) * n_scenarios)
        for s in range(n_scenarios):
            lp_objective.SetCoefficient(excess[s], excess_coeff)
            cvar_constraint = solver.Constraint(0.0, infinity, "")
            cvar_constraint.SetCoefficient(excess[s], 1.0)
            cvar_constraint.SetCoefficient(eta, 1.0)
            for i in range(n_customers):
                idx = _scenario_index(s, i, n_customers)
                cvar_constraint.SetCoefficient(short[idx], -float(objective.shortage_penalty[i]))
                cvar_constraint.SetCoefficient(surplus[idx], -float(objective.surplus_penalty[i]))

    for route_id, cols in enumerate(problem.route_groups):
        capacity_constraint = solver.Constraint(-infinity, float(problem.route_capacity), f"route_capacity_{route_id}")
        for i in cols:
            capacity_constraint.SetCoefficient(load[i], 1.0)
        if problem.route_load_targets is not None:
            target = float(problem.route_load_targets[route_id])
            target_constraint = solver.Constraint(target, target, f"route_load_target_{route_id}")
            for i in cols:
                target_constraint.SetCoefficient(load[i], 1.0)

    for s in range(n_scenarios):
        for i in range(n_customers):
            idx = _scenario_index(s, i, n_customers)
            demand = float(problem.planning_scenarios[s, i])

            short_constraint = solver.Constraint(demand, infinity, "")
            short_constraint.SetCoefficient(short[idx], 1.0)
            short_constraint.SetCoefficient(load[i], 1.0)

            surplus_constraint = solver.Constraint(-demand, infinity, "")
            surplus_constraint.SetCoefficient(surplus[idx], 1.0)
            surplus_constraint.SetCoefficient(load[i], -1.0)

    started = time.time()
    status = solver.Solve()
    runtime = time.time() - started
    if status == pywraplp.Solver.NOT_SOLVED:
        return EngineSolution(problem.name, False, np.array([]), float("nan"), runtime, "lp_time_limit")
    if status != pywraplp.Solver.OPTIMAL:
        return EngineSolution(
            problem.name,
            False,
            np.array([]),
            float("nan"),
            runtime,
            f"lp_status_{_ortools_status_name(status)}",
        )

    loads = np.array([max(0.0, float(var.solution_value())) for var in load])
    return EngineSolution(
        method=problem.name,
        feasible=True,
        loads=loads,
        objective_value=float(lp_objective.Value()),
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


def _scenario_index(scenario_id: int, customer_id: int, n_customers: int) -> int:
    return scenario_id * n_customers + customer_id


def _ortools_status_name(status: int) -> str:
    names = {
        pywraplp.Solver.OPTIMAL: "Optimal",
        pywraplp.Solver.FEASIBLE: "Feasible",
        pywraplp.Solver.INFEASIBLE: "Infeasible",
        pywraplp.Solver.UNBOUNDED: "Unbounded",
        pywraplp.Solver.ABNORMAL: "Abnormal",
        pywraplp.Solver.MODEL_INVALID: "ModelInvalid",
        pywraplp.Solver.NOT_SOLVED: "NotSolved",
    }
    return names.get(status, str(status))


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
    if problem.route_load_targets is not None:
        if len(problem.route_load_targets) != len(problem.route_groups):
            raise ValueError("route_load_targets length must match route_groups")
        for target in problem.route_load_targets:
            if target < -1e-9:
                raise ValueError("route_load_targets cannot contain negative values")
            if target > float(problem.route_capacity) + 1e-9:
                raise ValueError("route_load_targets cannot exceed route_capacity")
    if not (0.0 < problem.objective.cvar_alpha < 1.0):
        raise ValueError("cvar_alpha must be in (0, 1)")


def _load_penalty(objective: DomainObjective, n_customers: int) -> np.ndarray:
    if objective.load_penalty is None:
        return np.zeros(n_customers, dtype=float)
    return np.asarray(objective.load_penalty, dtype=float)
