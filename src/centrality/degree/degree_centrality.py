from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_degree_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute degree centrality for all nodes."""
    G = to_simple_graph(G)
    return nx.degree_centrality(G)
