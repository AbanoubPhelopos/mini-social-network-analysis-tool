import networkx as nx


def compute_conductance(G: nx.Graph, labels: dict) -> float:
    """Compute the average conductance across all communities.

    Conductance(S) = cut(S, V\\S) / min(vol(S), vol(V\\S))

    Args:
        G: The networkx graph.
        labels: A dict mapping node IDs to community labels.

    Returns:
        The average conductance score as a float.
    """
    communities: dict[int, set] = {}
    for node, label in labels.items():
        communities.setdefault(label, set()).add(node)

    if not communities:
        return 0.0

    total_volume = sum(dict(G.degree()).values())
    conductances: list[float] = []

    for community in communities.values():
        cut_size = 0
        volume = 0
        for node in community:
            degree = G.degree(node)
            volume += degree
            for neighbor in G.neighbors(node):
                if neighbor not in community:
                    cut_size += 1

        complement_volume = total_volume - volume
        denominator = min(volume, complement_volume)
        if denominator == 0:
            conductances.append(0.0)
        else:
            conductances.append(cut_size / denominator)

    return sum(conductances) / len(conductances)
