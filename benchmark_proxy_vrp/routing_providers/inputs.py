from __future__ import annotations

import numpy as np
import pandas as pd

from ..cvrplib import CVRPInstance, customer_view


def instance_to_provider_inputs(
    instance: CVRPInstance,
    planned_customer_loads: np.ndarray,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    nodes = _nodes_frame(instance)
    demands = _demands_frame(instance, planned_customer_loads)
    distance_matrix = pd.DataFrame(
        instance.distance_matrix.astype(float),
        index=list(range(instance.n_nodes)),
        columns=list(range(instance.n_nodes)),
    )
    return nodes, demands, distance_matrix


def _nodes_frame(instance: CVRPInstance) -> pd.DataFrame:
    rows = []
    lonlat = instance.osrm_coordinates
    for node_id in range(instance.n_nodes):
        row = {"id": node_id, "is_depot": node_id == instance.depot_index}
        if lonlat is not None:
            row["lon"] = float(lonlat[node_id, 0])
            row["lat"] = float(lonlat[node_id, 1])
        elif instance.coordinates is not None:
            row["x"] = float(instance.coordinates[node_id, 0])
            row["y"] = float(instance.coordinates[node_id, 1])
            row["lon"] = float(instance.coordinates[node_id, 0])
            row["lat"] = float(instance.coordinates[node_id, 1])
        rows.append(row)
    return pd.DataFrame(rows)


def _demands_frame(instance: CVRPInstance, planned_customer_loads: np.ndarray) -> pd.DataFrame:
    _, customer_indices = customer_view(instance)
    demand_by_node = {int(node): float(load) for node, load in zip(customer_indices, planned_customer_loads)}
    return pd.DataFrame(
        {
            "node_id": list(range(instance.n_nodes)),
            "demand": [demand_by_node.get(node_id, 0.0) for node_id in range(instance.n_nodes)],
        }
    )
