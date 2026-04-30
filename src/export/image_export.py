import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

from core.constants import LAYOUT_OPTIONS
from layouts import get_layout


def export_graph_image(
    G: nx.Graph,
    layout_name: str = "Spring (Force-Directed)",
    filename: str = "graph.png",
) -> str:
    """Render a graph to a PNG image using matplotlib.

    Args:
        G: NetworkX graph to render.
        layout_name: Display name of the layout algorithm.
        filename: Name of the output image file.

    Returns:
        Absolute path to the written PNG file.
    """
    layout_key = LAYOUT_OPTIONS.get(layout_name, "spring")
    layout_func_name = {
        "spring": "Spring",
        "circular": "Circular",
        "random": "Random",
        "shell": "Shell",
        "kamada_kawai": "Kamada-Kawai",
        "spectral": "Spectral",
    }.get(layout_key, "Spring")

    positions = get_layout(G, layout_func_name)

    fig, ax = plt.subplots(figsize=(12, 10))
    nx.draw_networkx_edges(G, positions, alpha=0.3, ax=ax)
    nx.draw_networkx_nodes(
        G,
        positions,
        node_size=80,
        node_color="#1f77b4",
        edgecolors="white",
        linewidths=0.5,
        ax=ax,
    )

    if G.number_of_nodes() <= 100:
        nx.draw_networkx_labels(G, positions, font_size=7, ax=ax)

    ax.set_title(f"Network Graph — {layout_name}")
    ax.axis("off")
    fig.tight_layout()

    tmp_dir = tempfile.gettempdir()
    path = f"{tmp_dir}\\{filename}"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path
