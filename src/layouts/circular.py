from typing import Any, Dict, Tuple

import networkx as nx


def circular_layout(G: nx.Graph, **kwargs) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions on a circle."""
    return nx.circular_layout(G, **kwargs)
