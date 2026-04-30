from typing import Any, Dict, Optional

import networkx as nx
import plotly.graph_objects as go

from core.constants import GRAPH_COLORS


def create_plotly_figure(
    G: nx.Graph,
    positions: Dict[Any, tuple],
    node_color_attr: Optional[str] = None,
    node_size_attr: Optional[str] = None,
    community_labels: Optional[Dict[Any, Any]] = None,
) -> go.Figure:
    """Create a Plotly Figure with nodes and edges rendered as scatter traces.

    Args:
        G: NetworkX graph to visualize.
        positions: Mapping of node -> (x, y) positions.
        node_color_attr: Node attribute used for coloring.
        node_size_attr: Node attribute used for sizing.
        community_labels: Mapping of node -> community id for coloring.

    Returns:
        A Plotly Figure containing the graph visualization.
    """
    fig = go.Figure()

    edge_x: list = []
    edge_y: list = []
    for u, v in G.edges():
        if u in positions and v in positions:
            x0, y0 = positions[u]
            x1, y1 = positions[v]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            showlegend=False,
        )
    )

    node_x: list = []
    node_y: list = []
    node_labels: list = []
    node_colors: list = []
    node_sizes: list = []
    node_texts: list = []

    color_key = node_color_attr
    if community_labels is not None:
        color_key = "__community__"

    color_categories: list = []
    for node in G.nodes():
        if color_key == "__community__":
            color_categories.append(community_labels.get(node, 0))
        elif color_key is not None:
            color_categories.append(G.nodes[node].get(color_key, ""))
        else:
            color_categories.append("")

    unique_cats = sorted(set(color_categories)) if color_key else []
    color_map = {
        cat: GRAPH_COLORS[i % len(GRAPH_COLORS)] for i, cat in enumerate(unique_cats)
    }

    for idx, node in enumerate(G.nodes()):
        if node not in positions:
            continue
        x, y = positions[node]
        node_x.append(float(x))
        node_y.append(float(y))
        node_labels.append(str(node))

        if color_key and idx < len(color_categories):
            node_colors.append(color_map.get(color_categories[idx], "#1f77b4"))
        else:
            node_colors.append("#1f77b4")

        if node_size_attr and node_size_attr in G.nodes[node]:
            raw = G.nodes[node][node_size_attr]
            if isinstance(raw, (int, float)):
                node_sizes.append(max(5, min(raw * 20, 40)))
            else:
                node_sizes.append(10)
        else:
            node_sizes.append(10)

        hover_parts = [f"Node: {node}"]
        for attr_key, attr_val in G.nodes[node].items():
            hover_parts.append(f"{attr_key}: {attr_val}")
        if community_labels and node in community_labels:
            hover_parts.append(f"community: {community_labels[node]}")
        node_texts.append("<br>".join(hover_parts))

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text" if len(node_x) < 200 else "markers",
            text=node_labels,
            textposition="top center",
            hoverinfo="text",
            hovertext=node_texts,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=1, color="#fff"),
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="white",
    )

    return fig
