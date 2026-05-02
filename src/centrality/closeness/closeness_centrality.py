from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_closeness_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute closeness centrality for all nodes, handling disconnected graphs."""
    G = to_simple_graph(G)

    if G.is_directed():
        connected = nx.is_strongly_connected(G)
    else:
        connected = nx.is_connected(G)

    if connected:
        return nx.closeness_centrality(G)

    return nx.closeness_centrality(G, wf_improved=True)
