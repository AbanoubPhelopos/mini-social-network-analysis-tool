"""Shared graph utilities for MultiGraph compatibility and common operations."""

from typing import Any

import networkx as nx


def to_simple_graph(G: nx.Graph) -> nx.Graph:
    """Convert a MultiGraph/MultiDiGraph to a simple Graph/DiGraph.

    Parallel edges are collapsed by summing their weights.
    Node attributes are preserved. If the graph is already simple,
    it is returned unchanged.

    Args:
        G: A NetworkX graph (simple or multi).

    Returns:
        A simple Graph or DiGraph with summed edge weights.
    """
    if not G.is_multigraph():
        return G
    simple = nx.DiGraph() if G.is_directed() else nx.Graph()
    simple.add_nodes_from(G.nodes(data=True))
    for u, v, data in G.edges(data=True):
        if simple.has_edge(u, v):
            simple[u][v]["weight"] += data.get("weight", 1)
        else:
            simple.add_edge(u, v, **data)
    return simple


def to_simple_undirected(G: nx.Graph) -> nx.Graph:
    """Convert any graph to a simple undirected Graph.

    MultiGraphs are collapsed (weights summed), directed graphs are
    converted to undirected. Node attributes are preserved.

    Args:
        G: A NetworkX graph.

    Returns:
        A simple undirected Graph.
    """
    simple = to_simple_graph(G)
    if simple.is_directed():
        return simple.to_undirected()
    return simple


def safe_is_connected(G: nx.Graph) -> bool:
    """Check connectivity safely for any graph type.

    Args:
        G: A NetworkX graph.

    Returns:
        True if the graph is connected (or strongly connected for directed).
    """
    if G.is_directed():
        return nx.is_strongly_connected(G)
    return nx.is_connected(G)


def safe_number_components(G: nx.Graph) -> int:
    """Count connected components safely for any graph type.

    Args:
        G: A NetworkX graph.

    Returns:
        Number of connected (or strongly connected) components.
    """
    if G.is_directed():
        return nx.number_strongly_connected_components(G)
    return nx.number_connected_components(G)
