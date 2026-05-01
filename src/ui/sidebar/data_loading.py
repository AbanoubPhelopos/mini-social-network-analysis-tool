import io
import os
import streamlit as st
from core.loader import load_nodes_csv, load_edges_csv
from core.graph_builder import build_graph, get_graph_info


def render_data_loading_section():
    """Render the data loading section of the sidebar."""
    st.header("Data Loading")

    directed = st.checkbox("Directed Graph", value=False, key="graph_directed")

   
    nodes_path = None
    edges_path = None
    
    uploaded_nodes = st.file_uploader(
        "Upload Nodes CSV", type=["csv"], key="upload_nodes"
    )
    uploaded_edges = st.file_uploader(
        "Upload Edges CSV", type=["csv"], key="upload_edges"
    )
    nodes_path = uploaded_nodes
    edges_path = uploaded_edges

    edge_mode = st.radio(
        "Edge Mode",
        ["Unique Edges (Aggregated)", "All Edges (Raw)"],
        index=0,
        key="edge_mode",
        help="Unique Edges merges duplicate contacts into weighted edges. "
        "All Edges keeps every individual contact as a separate edge.",
    )
    use_multigraph = edge_mode == "All Edges (Raw)"

    if st.button("Load Graph", type="primary", key="load_graph"):
        if nodes_path and edges_path:
            try:
                if isinstance(nodes_path, str):
                    with open(nodes_path, "rb") as f:
                        nodes_df = load_nodes_csv(io.BytesIO(f.read()))
                    with open(edges_path, "rb") as f:
                        edges_df = load_edges_csv(
                            io.BytesIO(f.read()), aggregate=not use_multigraph
                        )
                else:
                    nodes_df = load_nodes_csv(nodes_path)
                    edges_df = load_edges_csv(
                        edges_path, aggregate=not use_multigraph
                    )
                graph = build_graph(
                    nodes_df,
                    edges_df,
                    directed=directed,
                    use_multigraph=use_multigraph,
                )

                st.session_state.graph = graph
                st.session_state.nodes_df = nodes_df
                st.session_state.edges_df = edges_df
                st.session_state.graph_loaded = True
                st.session_state.centrality_results = None
                st.session_state.community_results = None
                st.session_state.filtered_graph = None

                
                info = get_graph_info(graph)
                kind = "directed" if directed else "undirected"
                st.success(
                    f"Graph loaded ({kind}): {info.get('num_nodes', 0)} nodes, "
                    f"{info.get('num_edges', 0)} edges"
                )
            except Exception as e:
                st.error(f"Error loading graph: {e}")
        else:
            st.warning("Please provide both nodes and edges files.")
