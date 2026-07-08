from __future__ import annotations

import numpy as np


def select_representative_scenarios(scenarios: np.ndarray, max_scenarios: int | None) -> np.ndarray:
    """Return a deterministic total-demand-stratified subset for fast LP diagnostics."""

    scenarios = np.asarray(scenarios)
    if max_scenarios is None or max_scenarios <= 0 or max_scenarios >= len(scenarios):
        return scenarios
    if max_scenarios == 1:
        totals = scenarios.sum(axis=1)
        median_position = int(np.argsort(totals, kind="mergesort")[len(scenarios) // 2])
        return scenarios[[median_position]]

    totals = scenarios.sum(axis=1)
    severity_order = np.argsort(totals, kind="mergesort")
    selected_positions = _even_positions(len(scenarios), max_scenarios)
    selected_indices = np.sort(severity_order[selected_positions])
    return scenarios[selected_indices]


def scenario_reduction_summary(original: np.ndarray, reduced: np.ndarray) -> dict[str, float | int | bool]:
    original_totals = np.asarray(original).sum(axis=1)
    reduced_totals = np.asarray(reduced).sum(axis=1)
    return {
        "lp_planning_scenarios_original": int(len(original)),
        "lp_planning_scenarios_used": int(len(reduced)),
        "lp_scenario_reduced": bool(len(reduced) < len(original)),
        "lp_original_total_demand_mean": float(original_totals.mean()) if len(original_totals) else 0.0,
        "lp_reduced_total_demand_mean": float(reduced_totals.mean()) if len(reduced_totals) else 0.0,
        "lp_original_total_demand_p90": float(np.quantile(original_totals, 0.90)) if len(original_totals) else 0.0,
        "lp_reduced_total_demand_p90": float(np.quantile(reduced_totals, 0.90)) if len(reduced_totals) else 0.0,
    }


def _even_positions(n_items: int, n_selected: int) -> np.ndarray:
    positions = np.rint(np.linspace(0, n_items - 1, n_selected)).astype(int)
    if len(np.unique(positions)) == n_selected:
        return positions

    selected: list[int] = []
    seen: set[int] = set()
    for pos in positions:
        pos = int(pos)
        if pos not in seen:
            selected.append(pos)
            seen.add(pos)
    for pos in range(n_items):
        if len(selected) == n_selected:
            break
        if pos not in seen:
            selected.append(pos)
            seen.add(pos)
    return np.asarray(sorted(selected), dtype=int)
