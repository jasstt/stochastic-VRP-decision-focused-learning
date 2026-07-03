from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .cvrplib import CVRPInstance, customer_view


@dataclass(frozen=True)
class ProxyScenarioConfig:
    n_days: int = 365
    n_scenarios: int = 200
    seed: int = 42
    common_shock_sigma: float = 0.11
    node_noise_floor: float = 0.10
    node_noise_range: float = 0.28
    high_demand_shock_prob: float = 0.05
    high_demand_shock_multiplier: float = 1.35


def generate_proxy_demands(
    instance: CVRPInstance,
    config: ProxyScenarioConfig = ProxyScenarioConfig(),
) -> tuple[pd.DataFrame, np.ndarray, pd.DataFrame]:
    """Generate unbiased proxy demand history and SAA scenarios.

    The rules use only benchmark structure known before optimization:
    nominal customer demand, distance from depot, and generic day-level shocks.
    They are intentionally not tuned against SPO+, OR-Tools, or any downstream
    model result.
    """

    rng = np.random.default_rng(config.seed)
    nominal, customer_indices = customer_view(instance)
    n_customers = len(nominal)

    depot = instance.depot_index
    depot_dist = instance.distance_matrix[depot, customer_indices].astype(float)
    demand_rank = _rank01(nominal)
    distance_rank = _rank01(depot_dist)

    node_cv = (
        config.node_noise_floor
        + config.node_noise_range * (0.65 * demand_rank + 0.35 * distance_rank)
    )
    node_cv = np.clip(node_cv, 0.08, 0.45)

    days = pd.date_range("2024-01-01", periods=config.n_days, freq="D")
    history = _sample_days(rng, nominal, node_cv, days, config)
    scenarios = _sample_scenarios(rng, nominal, node_cv, config)

    meta = pd.DataFrame(
        {
            "customer_id": customer_indices + 1,
            "nominal_demand": nominal,
            "distance_from_depot": depot_dist,
            "demand_rank": demand_rank,
            "distance_rank": distance_rank,
            "proxy_cv": node_cv,
        }
    )
    return history, scenarios, meta


def _sample_days(
    rng: np.random.Generator,
    nominal: np.ndarray,
    node_cv: np.ndarray,
    days: pd.DatetimeIndex,
    config: ProxyScenarioConfig,
) -> pd.DataFrame:
    rows = []
    for t, day in enumerate(days):
        dow = day.dayofweek
        weekend = 1.10 if dow >= 5 else 1.0
        weekday_pull = 1.06 if dow in (4, 5) else 1.0
        month_wave = 1.0 + 0.07 * np.sin(2 * np.pi * (day.dayofyear / 365.25))
        common = rng.lognormal(mean=-0.5 * config.common_shock_sigma**2, sigma=config.common_shock_sigma)
        rare = (
            config.high_demand_shock_multiplier
            if rng.random() < config.high_demand_shock_prob
            else 1.0
        )
        noise = rng.lognormal(mean=-0.5 * node_cv**2, sigma=node_cv)
        demand = nominal * weekend * weekday_pull * month_wave * common * rare * noise
        rows.append(demand)
    columns = [f"customer_{i+1:03d}" for i in range(len(nominal))]
    return pd.DataFrame(rows, index=days, columns=columns)


def _sample_scenarios(
    rng: np.random.Generator,
    nominal: np.ndarray,
    node_cv: np.ndarray,
    config: ProxyScenarioConfig,
) -> np.ndarray:
    scenarios = []
    for _ in range(config.n_scenarios):
        common = rng.lognormal(mean=-0.5 * config.common_shock_sigma**2, sigma=config.common_shock_sigma)
        rare = (
            config.high_demand_shock_multiplier
            if rng.random() < config.high_demand_shock_prob
            else 1.0
        )
        noise = rng.lognormal(mean=-0.5 * node_cv**2, sigma=node_cv)
        scenarios.append(nominal * common * rare * noise)
    return np.asarray(scenarios)


def _rank01(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if len(values) == 1:
        return np.zeros_like(values)
    order = values.argsort().argsort().astype(float)
    return order / (len(values) - 1)

