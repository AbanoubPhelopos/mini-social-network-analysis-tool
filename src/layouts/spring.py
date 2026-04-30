from typing import Any, Dict, Tuple

import networkx as nx


def spring_layout(G: nx.Graph, **kwargs) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using the spring layout algorithm."""
    return nx.spring_layout(G, seed=42, **kwargs)
