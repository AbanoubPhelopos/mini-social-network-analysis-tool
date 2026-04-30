import networkx as nx

from core.graph_utils import to_simple_graph


def filter_by_degree_range(
    G: nx.Graph,
    min_degree: int = 0,
    max_degree: int | None = None,
) -> nx.Graph:
    """Return a subgraph containing only nodes whose degree falls within
    [min_degree, max_degree].  If *max_degree* is ``None`` no upper bound
    is applied."""
    simple = to_simple_graph(G)
    nodes_to_keep = [
        node
        for node in simple.nodes()
        if simple.degree(node) >= min_degree
        and (max_degree is None or simple.degree(node) <= max_degree)
    ]
    return G.subgraph(nodes_to_keep).copy()
