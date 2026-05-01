import streamlit as st
from layouts import get_available_layouts
from core.constants import NODE_SHAPE_OPTIONS


def render_visualization_settings_section():
    """Render the visualization settings section of the sidebar."""
    if not st.session_state.get("graph_loaded"):
        return {}
    
    graph = st.session_state.graph
    
    st.divider()
    st.header("Visualization")

    viz_params = {}

    layouts = get_available_layouts()
    layout_names = (
        list(layouts.keys()) if isinstance(layouts, dict) else layouts
    )
    viz_params["layout"] = st.selectbox("Layout", layout_names)

    viz_params["show_labels"] = st.checkbox("Show Labels", value=True)
    viz_params["show_weights"] = st.checkbox("Show Edge Weights", value=False)
    viz_params["physics"] = st.checkbox("Enable Physics", value=True)

    if st.session_state.nodes_df is not None:
        node_cols = list(st.session_state.nodes_df.columns)
        viz_params["color_by"] = st.selectbox(
            "Color Nodes By", ["None"] + node_cols
        )
        viz_params["size_by"] = st.selectbox(
            "Size Nodes By", ["None"] + node_cols
        )
        viz_params["label_by"] = st.selectbox(
            "Label Nodes By", node_cols, index=0
        )

    viz_params["node_shape"] = st.selectbox(
        "Node Shape",
        list(NODE_SHAPE_OPTIONS.keys())
        if isinstance(NODE_SHAPE_OPTIONS, dict)
        else NODE_SHAPE_OPTIONS,
    )

    edge_cols = ["Weight"]
    if st.session_state.edges_df is not None:
        edge_cols = list(st.session_state.edges_df.columns)
    viz_params["edge_color_by"] = st.selectbox(
        "Edge Color By", ["None"] + edge_cols, key="edge_color"
    )

    return viz_params
