from typing import Any

import networkx as nx
import numpy as np
from collections import Counter


def compute_degree_distribution(G: nx.Graph) -> dict:
    """Compute degree distribution statistics for the graph.

    Args:
        G: A NetworkX graph (directed or undirected).

    Returns:
        Dictionary containing minimum, maximum, mean, standard deviation
        of degrees, the full distribution as a sorted dict, and the raw
        degree list.
    """
    degrees = [int(d) for _, d in G.degree()]

    if not degrees:
        return {
            "min": 0,
            "max": 0,
            "mean": 0.0,
            "std": 0.0,
            "distribution": {},
            "degrees": [],
        }

    distribution_counter = Counter(degrees)
    distribution = dict(sorted(distribution_counter.items()))
    degree_array = np.array(degrees, dtype=float)

    return {
        "min": int(degree_array.min()),
        "max": int(degree_array.max()),
        "mean": float(degree_array.mean()),
        "std": float(degree_array.std()),
        "distribution": distribution,
        "degrees": degrees,
    }
