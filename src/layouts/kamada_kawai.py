from typing import Any, Dict, Tuple

import networkx as nx


def _largest_connected_component(G: nx.Graph) -> nx.Graph:
    """Return the subgraph of the largest connected component."""
    if nx.is_directed(G):
        if nx.is_weakly_connected(G):
            return G
        largest = max(nx.weakly_connected_components(G), key=len)
        return G.subgraph(largest).copy()
    if nx.is_connected(G):
        return G
    largest = max(nx.connected_components(G), key=len)
    return G.subgraph(largest).copy()


def kamada_kawai_layout(G: nx.Graph, **kwargs) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using the Kamada-Kawai path-length cost function.

    Falls back to the largest connected component if the graph is disconnected.
    """
    subgraph = _largest_connected_component(G)
    return nx.kamada_kawai_layout(subgraph, **kwargs)
