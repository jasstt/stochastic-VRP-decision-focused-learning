from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .cvrplib import CVRPInstance, customer_view
from .routing_providers.base import RouteSet
from .stochastic_engine import DomainObjective, FixedRouteProblem


@dataclass(frozen=True)
class DomainAdapter(ABC):
    """Contract for adding a sector-specific stochastic decision layer.

    A new adapter must implement `objective()`. It receives customer metadata
    from the proxy generator plus route-derived features aligned to customer
    columns. Override `route_features()` or `build_problem()` only when a domain
    needs extra structure beyond per-customer penalties.
    """

    name: str
    description: str

    @abstractmethod
    def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
        """Return penalties aligned to the customer columns in the scenario matrices."""

    def route_features(
        self,
        instance: CVRPInstance,
        anchor_routes: RouteSet,
        node_meta: pd.DataFrame,
    ) -> pd.DataFrame:
        return build_route_features(instance, anchor_routes, node_meta)

    def build_problem(
        self,
        instance: CVRPInstance,
        anchor_routes: RouteSet,
        planning_scenarios: np.ndarray,
        evaluation_scenarios: np.ndarray,
        node_meta: pd.DataFrame,
    ) -> FixedRouteProblem:
        if not anchor_routes.feasible:
            raise ValueError("Anchor route is infeasible")

        route_features = self.route_features(instance, anchor_routes, node_meta)
        anchor_method = anchor_routes.raw_metadata.get("method", anchor_routes.solver_name)
        return FixedRouteProblem(
            name=f"{self.name}_engine_on_{anchor_method}",
            route_groups=_route_groups(instance, anchor_routes),
            route_capacity=float(instance.capacity),
            planning_scenarios=planning_scenarios,
            evaluation_scenarios=evaluation_scenarios,
            route_cost=float(anchor_routes.total_cost),
            objective=self.objective(node_meta, route_features),
        )


class ATMAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(
            name="atm",
            description="High stockout penalty, low surplus cost, mild tail-risk aversion.",
        )

    def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
        criticality = _criticality(node_meta)
        return DomainObjective(
            name=self.name,
            shortage_penalty=3.0 + 1.2 * criticality,
            surplus_penalty=np.full(len(node_meta), 0.15),
            risk_weight=0.15,
            cvar_alpha=0.9,
            description=self.description,
        )


class GroceryAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(
            name="grocery",
            description="Moderate missed-demand penalty with higher waste/overfill cost.",
        )

    def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
        criticality = _criticality(node_meta)
        return DomainObjective(
            name=self.name,
            shortage_penalty=1.6 + 0.7 * criticality,
            surplus_penalty=0.35 + 0.15 * node_meta["distance_rank"].to_numpy(float),
            risk_weight=0.05,
            cvar_alpha=0.9,
            description=self.description,
        )


class CargoAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(
            name="cargo",
            description="Failed first-attempt/overflow penalty, low surplus cost, stronger tail focus.",
        )

    def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
        distance_rank = node_meta["distance_rank"].to_numpy(float)
        demand_rank = node_meta["demand_rank"].to_numpy(float)
        return DomainObjective(
            name=self.name,
            shortage_penalty=2.0 + 1.1 * distance_rank + 0.4 * demand_rank,
            surplus_penalty=np.full(len(node_meta), 0.08),
            risk_weight=0.25,
            cvar_alpha=0.9,
            description=self.description,
        )


class ColdChainAdapter(DomainAdapter):
    def __init__(self) -> None:
        super().__init__(
            name="cold_chain",
            description=(
                "Perishable delivery with shortage, waste, and route-exposure load penalties."
            ),
        )

    def objective(self, node_meta: pd.DataFrame, route_features: pd.DataFrame) -> DomainObjective:
        demand_rank = node_meta["demand_rank"].to_numpy(float)
        distance_rank = node_meta["distance_rank"].to_numpy(float)
        exposure_rank = route_features["arrival_exposure_rank"].to_numpy(float)
        perishability = 0.55 * demand_rank + 0.45 * exposure_rank
        return DomainObjective(
            name=self.name,
            shortage_penalty=2.1 + 0.7 * demand_rank + 0.3 * distance_rank,
            surplus_penalty=0.55 + 0.45 * perishability,
            load_penalty=0.04 + 0.28 * exposure_rank * (0.45 + perishability),
            risk_weight=0.18,
            cvar_alpha=0.9,
            description=self.description,
        )


def build_route_features(
    instance: CVRPInstance,
    anchor_routes: RouteSet,
    node_meta: pd.DataFrame,
) -> pd.DataFrame:
    _, customer_indices = customer_view(instance)
    node_to_col = {int(node): pos for pos, node in enumerate(customer_indices)}
    arrival = np.zeros(len(customer_indices), dtype=float)
    route_id = np.full(len(customer_indices), -1, dtype=int)
    route_position = np.zeros(len(customer_indices), dtype=float)
    route_size = np.ones(len(customer_indices), dtype=float)

    travel_matrix = _travel_cost_matrix(instance)
    for rid, route in enumerate(anchor_routes.routes):
        customer_nodes = [node for node in route if node in node_to_col]
        size = max(1, len(customer_nodes))
        elapsed = 0.0
        previous = route[0]
        seen = 0
        for node in route[1:]:
            elapsed += float(travel_matrix[previous, node])
            if node in node_to_col:
                col = node_to_col[node]
                seen += 1
                arrival[col] = elapsed
                route_id[col] = rid
                route_position[col] = (seen - 1) / max(1, size - 1)
                route_size[col] = size
            previous = node

    features = node_meta.copy()
    features["route_id"] = route_id
    features["route_position_rank"] = route_position
    features["route_size"] = route_size
    features["arrival_cost"] = arrival
    features["arrival_exposure_rank"] = _rank01(arrival)
    return features


def get_adapter(name: str) -> DomainAdapter:
    adapters = {
        "atm": ATMAdapter,
        "grocery": GroceryAdapter,
        "cargo": CargoAdapter,
        "cold_chain": ColdChainAdapter,
    }
    key = name.lower().replace("-", "_")
    if key not in adapters:
        raise ValueError(f"Unknown domain adapter {name!r}. Options: {', '.join(adapters)}")
    return adapters[key]()


def available_adapters() -> list[str]:
    return ["atm", "grocery", "cargo", "cold_chain"]


def _route_groups(instance: CVRPInstance, anchor_routes: RouteSet) -> list[list[int]]:
    _, customer_indices = customer_view(instance)
    node_to_col = {int(node): pos for pos, node in enumerate(customer_indices)}
    groups = []
    for route in anchor_routes.routes:
        cols = [node_to_col[node] for node in route if node in node_to_col]
        if cols:
            groups.append(cols)
    return groups


def _travel_cost_matrix(instance: CVRPInstance) -> np.ndarray:
    if instance.travel_time_seconds_matrix is not None:
        return np.asarray(instance.travel_time_seconds_matrix, dtype=float) / 60.0
    return instance.distance_matrix.astype(float)


def _criticality(node_meta: pd.DataFrame) -> np.ndarray:
    demand_rank = node_meta["demand_rank"].to_numpy(float)
    distance_rank = node_meta["distance_rank"].to_numpy(float)
    return 0.65 * demand_rank + 0.35 * distance_rank


def _rank01(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if len(values) <= 1:
        return np.zeros_like(values)
    order = values.argsort().argsort().astype(float)
    return order / (len(values) - 1)
