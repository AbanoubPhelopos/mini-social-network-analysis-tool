import networkx as nx


def compute_modularity(G: nx.Graph, labels: dict) -> float:
    """Compute the modularity score of a graph partition.

    Args:
        G: The networkx graph.
        labels: A dict mapping node IDs to community labels.

    Returns:
        The modularity score as a float.
    """
    communities: dict[int, set] = {}
    for node, label in labels.items():
        communities.setdefault(label, set()).add(node)
    partition = list(communities.values())
    return nx.community.modularity(G, partition)
