from typing import Any, Dict, Tuple

import networkx as nx


def random_layout(G: nx.Graph, **kwargs) -> Dict[Any, Tuple[float, float]]:
    """Compute random node positions with a fixed seed for reproducibility."""
    return nx.random_layout(G, seed=42, **kwargs)
