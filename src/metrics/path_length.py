from typing import Dict, Tuple

import networkx as nx


def compute_average_path_length(G: nx.Graph) -> Tuple[float, Dict]:
    """Compute the average shortest path length for the graph.

    For disconnected graphs, the computation is performed on the
    largest connected component only.

    Args:
        G: A NetworkX graph (directed or undirected).

    Returns:
        A tuple of (average_path_length, component_info) where
        component_info contains metadata about the component used.
    """
    if G.number_of_nodes() == 0:
        return (0.0, {"component_nodes": 0, "component_edges": 0})

    if G.is_directed():
        if nx.is_strongly_connected(G):
            avg_length = nx.average_shortest_path_length(G)
            return (
                avg_length,
                {
                    "component_nodes": G.number_of_nodes(),
                    "component_edges": G.number_of_edges(),
                },
            )
        largest = max(nx.strongly_connected_components(G), key=len)
    else:
        if nx.is_connected(G):
            avg_length = nx.average_shortest_path_length(G)
            return (
                avg_length,
                {
                    "component_nodes": G.number_of_nodes(),
                    "component_edges": G.number_of_edges(),
                },
            )
        largest = max(nx.connected_components(G), key=len)

    subgraph = G.subgraph(largest).copy()
    avg_length = nx.average_shortest_path_length(subgraph)

    return (
        avg_length,
        {
            "component_nodes": subgraph.number_of_nodes(),
            "component_edges": subgraph.number_of_edges(),
        },
    )
