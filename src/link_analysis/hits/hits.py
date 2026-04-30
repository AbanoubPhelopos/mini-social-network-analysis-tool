from typing import Any, Dict, Tuple

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_hits(G: nx.Graph) -> Tuple[Dict[Any, float], Dict[Any, float]]:
    """Compute HITS (Hyperlink-Induced Topic Search) hubs and authorities scores.

    Args:
        G: A NetworkX graph.

    Returns:
        A tuple of (hubs, authorities) where each is a dictionary mapping nodes
        to their respective scores. Falls back to zero-valued dictionaries if
        computation fails.
    """
    try:
        G = to_simple_graph(G)
        hubs, authorities = nx.hits(G)
        return (hubs, authorities)
    except Exception:
        hubs = {node: 0.0 for node in G.nodes()}
        authorities = {node: 0.0 for node in G.nodes()}
        return (hubs, authorities)
