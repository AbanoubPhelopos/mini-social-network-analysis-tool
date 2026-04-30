from typing import Any, Dict

import networkx as nx

from core.graph_utils import to_simple_graph


def compute_eigenvector_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute eigenvector centrality on the largest connected component.

    Eigenvector centrality is undefined for disconnected graphs (values
    collapse to near-zero). This implementation finds the largest component,
    computes centrality there, and assigns 0 to all other nodes.

    Args:
        G: A NetworkX graph.

    Returns:
        Dictionary mapping each node to its eigenvector centrality value.
    """
    G = to_simple_graph(G)
    result = {node: 0.0 for node in G.nodes()}

    if G.is_directed():
        components = list(nx.strongly_connected_components(G))
    else:
        components = list(nx.connected_components(G))

    if not components:
        return result

    largest = max(components, key=len)
    subgraph = G.subgraph(largest)

    try:
        cent = nx.eigenvector_centrality(subgraph, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        try:
            cent = nx.eigenvector_centrality_numpy(subgraph)
        except Exception:
            return result

    for node, val in cent.items():
        result[node] = val

    return result
