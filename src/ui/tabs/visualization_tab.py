import tempfile
import streamlit as st
import streamlit.components.v1 as components
from visualization import create_pyvis_network
from layouts import get_layout


def render_visualization_tab(viz_params):
    graph = viz_params.get("graph")
    if graph is None:
        st.info("Load a graph from the sidebar to visualize it.")
        return

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nodes", num_nodes)
    with col2:
        st.metric("Edges", num_edges)
    with col3:
        is_directed = graph.is_directed()
        st.metric("Graph Type", "Directed" if is_directed else "Undirected")
    with col4:
        is_multi = hasattr(graph, "is_multigraph") and graph.is_multigraph()
        st.metric("Edge Mode", "Multi" if is_multi else "Simple")

    if num_edges > 10000:
        st.warning(
            f"This graph has **{num_edges:,} edges**. "
            f"Visualization may take 30-90 seconds to generate. "
            f"Consider using **Unique Edges (Aggregated)** mode in the sidebar for faster rendering."
        )

    # Show graph type information
    graph_type = "Directed" if graph.is_directed() else "Undirected"
    st.info(f"Graph Type: {graph_type} - Visualization will respect edge directions accordingly.")
    
    if st.button("Generate Visualization", type="primary", key="viz_gen"):
        with st.spinner(
            f"Computing layout and generating visualization ({num_edges:,} edges)..."
        ):
            layout_name = viz_params.get("layout", "Spring (Force-Directed)")
            positions = get_layout(graph, layout_name)

            community_labels = st.session_state.get("community_labels")
            centrality_values = st.session_state.get("centrality_values")

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
                edge_color_attr=viz_params.get("edge_color_by")
                if viz_params.get("edge_color_by") != "None"
                else None,
                community_labels=community_labels,
                centrality_values=centrality_values,
            )
            st.session_state["viz_html_content"] = html_content

    html_content = st.session_state.get("viz_html_content")
    if html_content:
        components.html(html_content, height=700, scrolling=True)
    else:
        st.info("Click **Generate Visualization** to render the network.")
