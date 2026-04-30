from typing import Any, Dict

import networkx as nx


def compute_closeness_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute closeness centrality for all nodes, handling disconnected graphs.

    For disconnected graphs, uses the improved formula so that nodes in small
    components are not unfairly penalized.

    Args:
        G: A NetworkX graph (may be disconnected).

    Returns:
        Dictionary mapping each node to its closeness centrality value.
    """
    if G.is_directed():
        connected = nx.is_strongly_connected(G)
    else:
        connected = nx.is_connected(G)

    if connected:
        return nx.closeness_centrality(G)

    return nx.closeness_centrality(G, wf_improved=True)
