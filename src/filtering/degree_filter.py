import networkx as nx


def filter_by_degree_range(
    G: nx.Graph,
    min_degree: int = 0,
    max_degree: int | None = None,
) -> nx.Graph:
    """Return a subgraph containing only nodes whose degree falls within
    [min_degree, max_degree].  If *max_degree* is ``None`` no upper bound
    is applied."""
    nodes_to_keep = [
        node
        for node in G.nodes()
        if G.degree(node) >= min_degree
        and (max_degree is None or G.degree(node) <= max_degree)
    ]
    return G.subgraph(nodes_to_keep).copy()
