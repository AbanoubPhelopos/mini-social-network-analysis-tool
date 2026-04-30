from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_pagerank(G: nx.Graph, alpha: float = 0.85) -> Dict[Any, float]:
    """Compute the PageRank of nodes in a graph.

    Args:
        G: A NetworkX graph.
        alpha: Damping factor for PageRank (default 0.85).

    Returns:
        A dictionary mapping each node to its PageRank score. Returns an empty
        dictionary if computation fails.
    """
    try:
        G = to_simple_graph(G)
        return nx.pagerank(G, alpha=alpha)
    except Exception:
        return {}
