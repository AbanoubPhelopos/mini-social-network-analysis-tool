import tempfile
from typing import Any

import networkx as nx


def export_graph_graphml(G: nx.Graph, filename: str = "graph.graphml") -> str:
    """Export a NetworkX graph to GraphML format.

    Args:
        G: NetworkX graph to export.
        filename: Name of the output file.

    Returns:
        Absolute path to the written GraphML file.
    """
    tmp_dir = tempfile.gettempdir()
    path = f"{tmp_dir}\\{filename}"
    nx.write_graphml(G, path)
    return path
