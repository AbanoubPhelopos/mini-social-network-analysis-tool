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


def _scale_positions(
    positions: Dict[Any, tuple], width: int = 800, height: int = 600
) -> Dict[Any, tuple]:
    """Scale NetworkX layout positions from [-1, 1] range to pixel coordinates."""
    if not positions:
        return positions

    x_vals = [float(p[0]) for p in positions.values()]
    y_vals = [float(p[1]) for p in positions.values()]

    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)

    x_range = x_max - x_min if x_max != x_min else 1.0
    y_range = y_max - y_min if y_max != y_min else 1.0

    margin = 50
    usable_w = width - 2 * margin
    usable_h = height - 2 * margin

    scaled = {}
    for node, (x, y) in positions.items():
        sx = margin + ((float(x) - x_min) / x_range) * usable_w
        sy = margin + ((float(y) - y_min) / y_range) * usable_h
        scaled[node] = (sx, sy)

    return scaled


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
    edge_color_attr: Optional[str] = None,
    height: str = "650px",
    width: str = "100%",
) -> str:
    """Build an interactive Pyvis HTML network and return the HTML string."""

    num_edges = G.number_of_edges()
    has_positions = positions is not None and len(positions) > 0

    if has_positions:
        positions = _scale_positions(positions)

    use_physics = physics_enabled and num_edges < 2000 and not has_positions

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

    if has_positions and not use_physics:
        net.set_options("""
        {
            "physics": {
                "enabled": false
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

    edge_color_categories: list = []
    edge_color_map: Dict[Any, str] = {}
    if edge_color_attr:
        edge_color_categories = [
            _native(data.get(edge_color_attr, "")) for _, _, data in G.edges(data=True)
        ]
        edge_color_map = _build_color_map(edge_color_categories)

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

        hover_parts = [f"Node: {native_id}"]
        for attr_key, attr_val in G.nodes[node].items():
            hover_parts.append(f"{attr_key}: {attr_val}")
        if community_labels and node in community_labels:
            hover_parts.append(f"Community: {community_labels[node]}")
        title = "<br>".join(hover_parts)

        node_opts = {
            "label": label,
            "size": size,
            "color": color,
            "shape": node_shape,
            "title": title,
        }

        if positions and node in positions:
            x, y = positions[node]
            node_opts["x"] = float(x)
            node_opts["y"] = float(y)

        net.add_node(native_id, **node_opts)

    for e_idx, (u, v, data) in enumerate(G.edges(data=True)):
        native_u = _native(u)
        native_v = _native(v)
        weight = _native(data.get("weight", 1.0))
        width_val = 1.0
        if isinstance(weight, (int, float)):
            width_val = max(0.3, min(weight, 2.5))

        edge_title_parts = [f"{native_u} → {native_v}"]
        if "weight" in data:
            edge_title_parts.append(f"Weight: {_native(data['weight'])}")
        for ek, ev in data.items():
            if ek != "weight":
                edge_title_parts.append(f"{ek}: {ev}")
        if isinstance(G, (nx.MultiGraph, nx.MultiDiGraph)):
            edge_title_parts.insert(1, f"Edge #{e_idx + 1}")
        edge_title = "<br>".join(edge_title_parts)

        edge_color = "#888"
        if edge_color_attr and e_idx < len(edge_color_categories):
            edge_color = edge_color_map.get(edge_color_categories[e_idx], "#888")

        net.add_edge(
            native_u, native_v, width=width_val, title=edge_title, color=edge_color
        )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w") as tmp:
        net.save_graph(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "r", encoding="utf-8") as f:
        html = f.read()

    return html
