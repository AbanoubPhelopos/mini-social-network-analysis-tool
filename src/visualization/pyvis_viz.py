import tempfile
from typing import Any, Dict, Optional

import networkx as nx
import numpy as np
from pyvis.network import Network

from core.constants import GRAPH_COLORS


def _native(val: Any) -> Any:
    """Convert numpy scalar types to native Python int/float."""
    if isinstance(val, np.integer):
        return int(val)
    if isinstance(val, np.floating):
        return float(val)
    return val


def _build_color_map(categories: list) -> Dict[Any, str]:
    """Map unique categories to colors from GRAPH_COLORS."""
    unique = sorted(set(categories))
    return {cat: GRAPH_COLORS[i % len(GRAPH_COLORS)] for i, cat in enumerate(unique)}


def _normalize_values(data: Dict[Any, Any]) -> Dict[Any, float]:
    """Min-max normalize dictionary values to [0, 1]. Skips non-numeric."""
    numeric = {}
    for k, v in data.items():
        v = _native(v)
        if isinstance(v, (int, float)):
            numeric[k] = float(v)
    if not numeric:
        return {}
    vals = list(numeric.values())
    mn = min(vals)
    mx = max(vals)
    span = mx - mn if mx != mn else 1.0
    return {k: (v - mn) / span for k, v in numeric.items()}


def create_pyvis_network(
    G: nx.Graph,
    positions: Optional[Dict[Any, tuple]] = None,
    node_size_attr: Optional[str] = None,
    node_color_attr: Optional[str] = None,
    node_label_attr: Optional[str] = None,
    show_labels: bool = True,
    show_edge_weights: bool = False,
    node_shape: str = "dot",
    physics_enabled: bool = True,
    community_labels: Optional[Dict[Any, Any]] = None,
    centrality_values: Optional[Dict[Any, float]] = None,
    height: str = "650px",
    width: str = "100%",
) -> str:
    """Build an interactive Pyvis HTML network and return the HTML string."""

    num_edges = G.number_of_edges()
    use_physics = physics_enabled and num_edges < 2000

    net = Network(height=height, width=width, directed=G.is_directed())
    net.toggle_physics(use_physics)

    if use_physics:
        net.set_options("""
        {
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "springLength": 100,
                    "springConstant": 0.04
                },
                "stabilization": {"iterations": 50}
            }
        }
        """)

    size_values: Dict[Any, float] = {}
    if centrality_values:
        size_values = _normalize_values(centrality_values)
    elif node_size_attr:
        raw = {n: G.nodes[n].get(node_size_attr, 1.0) for n in G.nodes()}
        size_values = _normalize_values(raw)

    color_categories: list = []
    color_attr_key = node_color_attr
    if community_labels is not None:
        color_attr_key = "__community__"

    if color_attr_key is not None:
        if color_attr_key == "__community__":
            color_categories = [_native(community_labels.get(n, 0)) for n in G.nodes()]
        else:
            color_categories = [
                _native(G.nodes[n].get(color_attr_key, "")) for n in G.nodes()
            ]

    color_map = _build_color_map(color_categories) if color_categories else {}

    node_list = list(G.nodes())
    for idx, node in enumerate(node_list):
        native_id = _native(node)

        if show_labels:
            if node_label_attr and node_label_attr in G.nodes[node]:
                label = str(_native(G.nodes[node][node_label_attr]))
            else:
                label = str(native_id)
        else:
            label = ""

        if node in size_values:
            size = 10 + size_values[node] * 40
        else:
            size = 15

        if color_categories and idx < len(color_categories):
            color = color_map.get(color_categories[idx], "#97c2fc")
        else:
            color = "#97c2fc"

        title = str(native_id)

        net.add_node(
            native_id,
            label=label,
            size=size,
            color=color,
            shape=node_shape,
            title=title,
        )

    for u, v, data in G.edges(data=True):
        native_u = _native(u)
        native_v = _native(v)
        weight = _native(data.get("weight", 1.0))
        width_val = 1.0
        if isinstance(weight, (int, float)):
            width_val = max(0.5, min(weight, 3.0))

        edge_title = ""
        if show_edge_weights and "weight" in data:
            edge_title = f"w={_native(data['weight'])}"

        net.add_edge(native_u, native_v, width=width_val, title=edge_title)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as tmp:
        net.save_graph(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "r", encoding="utf-8") as f:
        html = f.read()

    return html
