import networkx as nx


def filter_by_community(
    G: nx.Graph,
    community_labels: dict,
    selected_communities: set,
) -> nx.Graph:
    """Return a subgraph containing only nodes belonging to one of the
    selected communities."""
    nodes_to_keep = [
        node for node in G.nodes() if community_labels.get(node) in selected_communities
    ]
    return G.subgraph(nodes_to_keep).copy()
