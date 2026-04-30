import networkx as nx


def compute_basic_metrics(G: nx.Graph) -> dict:
    """Compute fundamental graph-level metrics.

    Args:
        G: A NetworkX graph (directed or undirected).

    Returns:
        Dictionary containing node count, edge count, density,
        directed flag, connected flag, component count, average degree,
        average clustering coefficient, and transitivity.
    """
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    is_directed = G.is_directed()
    is_connected = (
        nx.is_connected(G) if not is_directed else nx.is_strongly_connected(G)
    )
    num_components = (
        nx.number_connected_components(G)
        if not is_directed
        else nx.number_strongly_connected_components(G)
    )
    degrees = [d for _, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0.0
    avg_clustering = nx.average_clustering(G)
    transitivity = nx.transitivity(G)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "is_directed": is_directed,
        "is_connected": is_connected,
        "num_components": num_components,
        "avg_degree": avg_degree,
        "avg_clustering": avg_clustering,
        "transitivity": transitivity,
    }
