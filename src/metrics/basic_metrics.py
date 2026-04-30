import networkx as nx

from core.graph_utils import to_simple_graph


def compute_basic_metrics(G: nx.Graph) -> dict:
    """Compute fundamental graph-level metrics.

    Args:
        G: A NetworkX graph (directed or undirected).

    Returns:
        Dictionary containing node count, edge count, density,
        directed flag, connected flag, component count, average degree,
        average clustering coefficient, and transitivity.
    """
    simple = to_simple_graph(G)
    num_nodes = simple.number_of_nodes()
    num_edges = simple.number_of_edges()
    density = nx.density(simple)
    is_directed = simple.is_directed()
    is_connected = (
        nx.is_connected(simple) if not is_directed else nx.is_strongly_connected(simple)
    )
    num_components = (
        nx.number_connected_components(simple)
        if not is_directed
        else nx.number_strongly_connected_components(simple)
    )
    degrees = [d for _, d in simple.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0.0
    avg_clustering = nx.average_clustering(simple)
    transitivity = nx.transitivity(simple)

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
