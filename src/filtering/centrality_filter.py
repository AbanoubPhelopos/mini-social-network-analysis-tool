import networkx as nx


def filter_by_centrality_range(
    G: nx.Graph,
    centrality_dict: dict,
    min_val: float = 0.0,
    max_val: float = 1.0,
) -> nx.Graph:
    """Return a subgraph containing only nodes whose centrality value falls
    within [min_val, max_val]."""
    nodes_to_keep = [
        node
        for node in G.nodes()
        if min_val <= centrality_dict.get(node, 0.0) <= max_val
    ]
    return G.subgraph(nodes_to_keep).copy()
