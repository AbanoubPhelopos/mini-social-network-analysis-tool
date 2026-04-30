from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_degree_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute degree centrality for all nodes in the graph.

    Args:
        G: A NetworkX graph.

    Returns:
        Dictionary mapping each node to its degree centrality value.
    """
    G = to_simple_graph(G)
    return nx.degree_centrality(G)
