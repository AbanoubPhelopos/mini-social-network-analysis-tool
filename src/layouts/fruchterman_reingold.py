from typing import Any, Dict, Tuple

import networkx as nx


def fruchterman_reingold_layout(
    G: nx.Graph, **kwargs
) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using the Fruchterman-Reingold force-directed algorithm."""
    return nx.spring_layout(G, seed=42, iterations=100, scale=2.0, **kwargs)
