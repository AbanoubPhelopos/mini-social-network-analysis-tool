from typing import Any, List, Tuple

import networkx as nx


def find_shortest_path(
    G: nx.Graph, source: Any, target: Any
) -> Tuple[List[Any], float]:
    """Find the shortest path between two nodes in a graph.

    Args:
        G: A NetworkX graph.
        source: The starting node.
        target: The destination node.

    Returns:
        A tuple of (path, length) where path is a list of nodes and length is
        the total path weight (or number of edges for unweighted graphs).
        Returns ([], float('inf')) if no path exists or either node is not in
        the graph.
    """
    if source not in G or target not in G:
        return ([], float("inf"))

    try:
        path = nx.shortest_path(G, source=source, target=target)
        length = nx.shortest_path_length(G, source=source, target=target)
        return (path, float(length))
    except nx.NetworkXNoPath:
        return ([], float("inf"))
