from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class RouteSet:
    """Motor-agnostic standard route output."""

    routes: list[list[int]]
    route_costs: list[float]
    total_cost: float
    vehicle_assignments: dict[int, int]
    feasible: bool
    solver_name: str
    raw_metadata: dict = field(default_factory=dict)


class RoutingSolutionProvider(ABC):
    @abstractmethod
    def solve(
        self,
        nodes: pd.DataFrame,
        demands: pd.DataFrame,
        vehicle_capacity: float,
        num_vehicles: int,
        distance_matrix: pd.DataFrame | None = None,
    ) -> RouteSet:
        """Return a standard RouteSet from standard node/demand inputs."""

    @abstractmethod
    def solver_name(self) -> str:
        ...
