from typing import Any, Dict, Tuple

import networkx as nx


def compute_clustering_coefficients(G: nx.Graph) -> Tuple[float, Dict[Any, float]]:
    """Compute the average clustering coefficient and per-node values.

    Uses the undirected definition of clustering regardless of whether
    the input graph is directed.

    Args:
        G: A NetworkX graph.

    Returns:
        A tuple of (average_clustering, per_node_dict) where
        per_node_dict maps each node to its clustering coefficient.
    """
    if G.is_directed():
        G = G.to_undirected()

    per_node = nx.clustering(G)
    average = nx.average_clustering(G)

    return (average, dict(per_node))
