from typing import List

import networkx as nx


def get_connected_components(G: nx.Graph) -> List[List]:
    """Return connected components sorted by size in descending order.

    For directed graphs, uses strongly connected components.

    Args:
        G: A NetworkX graph (directed or undirected).

    Returns:
        List of components, each represented as a list of nodes,
        sorted from largest to smallest.
    """
    if G.is_directed():
        components = list(nx.strongly_connected_components(G))
    else:
        components = list(nx.connected_components(G))

    sorted_components = sorted(components, key=len, reverse=True)
    return [list(c) for c in sorted_components]
