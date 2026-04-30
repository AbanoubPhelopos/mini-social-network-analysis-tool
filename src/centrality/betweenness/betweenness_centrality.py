from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_betweenness_centrality(
    G: nx.Graph, normalized: bool = True
) -> Dict[Any, float]:
    """Compute betweenness centrality for all nodes in the graph.

    Args:
        G: A NetworkX graph.
        normalized: If True, normalize values to [0, 1]. Defaults to True.

    Returns:
        Dictionary mapping each node to its betweenness centrality value.
    """
    G = to_simple_graph(G)
    return nx.betweenness_centrality(G, normalized=normalized)
