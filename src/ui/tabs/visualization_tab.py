import tempfile
import streamlit as st
from visualization import create_pyvis_network
from layouts import get_layout


def render_visualization_tab(viz_params):
    graph = viz_params.get("graph")
    if graph is None:
        st.info("Load a graph from the sidebar to visualize it.")
        return

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nodes", num_nodes)
    with col2:
        st.metric("Edges", num_edges)

    if st.button("Generate Visualization", type="primary", key="viz_gen"):
        with st.spinner("Computing layout and generating visualization..."):
            layout_name = viz_params.get("layout", "Spring (Force-Directed)")
            positions = get_layout(graph, layout_name)

            html_content = create_pyvis_network(
                graph,
                positions=positions,
                show_labels=viz_params.get("show_labels", True),
                show_edge_weights=viz_params.get("show_weights", False),
                node_shape=viz_params.get("node_shape", "dot"),
                physics_enabled=viz_params.get("physics", True),
                node_label_attr=viz_params.get("label_by"),
                node_color_attr=viz_params.get("color_by")
                if viz_params.get("color_by") != "None"
                else None,
                node_size_attr=viz_params.get("size_by")
                if viz_params.get("size_by") != "None"
                else None,
            )
            with tempfile.NamedTemporaryFile(
                suffix=".html", delete=False, mode="w", encoding="utf-8"
            ) as tmp:
                tmp.write(html_content)
                tmp_path = tmp.name
            st.session_state["viz_html_path"] = tmp_path

    viz_path = st.session_state.get("viz_html_path")
    if viz_path:
        st.iframe(viz_path, height=700)
    else:
        st.info("Click **Generate Visualization** to render the network.")
