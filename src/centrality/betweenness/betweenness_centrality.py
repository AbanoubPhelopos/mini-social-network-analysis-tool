from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_betweenness_centrality(
    G: nx.Graph, normalized: bool = True
) -> Dict[Any, float]:
    """Compute betweenness centrality for all nodes."""
    G = to_simple_graph(G)
    return nx.betweenness_centrality(G, normalized=normalized)
