from typing import Any, Dict, List, Tuple

import networkx as nx


def shell_layout(G: nx.Graph, **kwargs) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions in concentric circles, handling disconnected graphs gracefully."""
    if not nx.is_connected(G):
        shells: List[List[Any]] = [
            list(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)
        ]
        return nx.shell_layout(G, nlist=shells, **kwargs)
    return nx.shell_layout(G, **kwargs)
