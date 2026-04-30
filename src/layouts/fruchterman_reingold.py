from typing import Any, Dict, Tuple

import networkx as nx


def fruchterman_reingold_layout(
    G: nx.Graph, **kwargs
) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using the Fruchterman-Reingold force-directed algorithm.

    This is NetworkX's spring_layout with Fruchterman-Reingold variant settings:
    uses repulsion between all node pairs and attraction along edges.
    """
    pos = nx.spring_layout(
        G,
        seed=42,
        iterations=200,
        threshold=1e-4,
        weight="weight",
        **kwargs,
    )
    return pos
