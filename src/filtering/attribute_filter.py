import networkx as nx


def filter_by_attribute(
    G: nx.Graph,
    attribute: str,
    selected_values: set,
) -> nx.Graph:
    """Return a subgraph containing only nodes whose given attribute value
    is in *selected_values*."""
    nodes_to_keep = [
        node
        for node, data in G.nodes(data=True)
        if data.get(attribute) in selected_values
    ]
    return G.subgraph(nodes_to_keep).copy()
