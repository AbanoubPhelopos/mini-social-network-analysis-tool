import io
import os
import streamlit as st
from core.loader import load_nodes_csv, load_edges_csv
from core.graph_builder import build_graph, get_graph_info
from core.constants import NODE_SHAPE_OPTIONS
from layouts import get_available_layouts
from centrality import compute_all_centrality
from communities import detect_louvain
from filtering import (
    filter_by_centrality_range,
    filter_by_community,
    filter_by_attribute,
    filter_by_degree_range,
)


def get_active_graph():
    if st.session_state.get("filtered_graph") is not None:
        return st.session_state.filtered_graph
    return st.session_state.get("graph")


def _cache_node_attributes():
    """Cache node attributes in session_state to avoid scanning graph on every rerun."""
    graph = st.session_state.get("graph")
    if graph is None:
        return
    cache_key = f"attr_cache_{id(graph)}"
    if cache_key not in st.session_state:
        attributes = set()
        degrees = []
        for node, data in graph.nodes(data=True):
            attributes.update(data.keys())
            degrees.append(graph.degree(node))
        st.session_state[cache_key] = sorted(attributes)
        values_cache = {}
        for attr in attributes:
            values = {
                data.get(attr) for _, data in graph.nodes(data=True) if attr in data
            }
            values_cache[attr] = sorted(values, key=lambda v: (v is None, v))
        st.session_state[f"values_cache_{id(graph)}"] = values_cache
        st.session_state[f"degree_cache_{id(graph)}"] = degrees


def _get_cached_attributes():
    graph = st.session_state.get("graph")
    if graph is None:
        return []
    return st.session_state.get(f"attr_cache_{id(graph)}", [])


def _get_cached_values(attribute):
    graph = st.session_state.get("graph")
    if graph is None:
        return []
    vc = st.session_state.get(f"values_cache_{id(graph)}", {})
    return vc.get(attribute, [])


def _auto_detect_files(data_dir):
    nodes_file = None
    edges_file = None
    if os.path.isdir(data_dir):
        for fname in os.listdir(data_dir):
            lower = fname.lower()
            if lower.endswith(".csv"):
                if "node" in lower or "metadata" in lower:
                    if nodes_file is None:
                        nodes_file = os.path.join(data_dir, fname)
                elif "edge" in lower:
                    if edges_file is None:
                        edges_file = os.path.join(data_dir, fname)
    return nodes_file, edges_file


def render_sidebar() -> dict:
    with st.sidebar:
        st.header("Data Loading")

        directed = st.checkbox("Directed Graph", value=False, key="graph_directed")

        load_mode = st.radio("Source", ["From data/ folder", "Upload Files"], index=0)

        nodes_path = None
        edges_path = None

        if load_mode == "From data/ folder":
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
            )
            auto_nodes, auto_edges = _auto_detect_files(data_dir)

            if auto_nodes and auto_edges:
                st.success(f"Auto-detected files")
                st.caption(f"Nodes: {os.path.basename(auto_nodes)}")
                st.caption(f"Edges: {os.path.basename(auto_edges)}")
                nodes_path = auto_nodes
                edges_path = auto_edges
            else:
                csv_files = []
                if os.path.isdir(data_dir):
                    csv_files = [
                        f for f in os.listdir(data_dir) if f.lower().endswith(".csv")
                    ]

                if not csv_files:
                    st.warning("No CSV files found in data/ folder.")
                else:
                    nodes_file = st.selectbox("Nodes CSV", csv_files, index=0)
                    edges_file = st.selectbox(
                        "Edges CSV", csv_files, index=min(1, len(csv_files) - 1)
                    )
                    if nodes_file:
                        nodes_path = os.path.join(data_dir, nodes_file)
                    if edges_file:
                        edges_path = os.path.join(data_dir, edges_file)
        else:
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

                    _cache_node_attributes()

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

        viz_params = {}
        active_graph = None

        if st.session_state.get("graph_loaded"):
            graph = st.session_state.graph

            st.divider()
            st.header("Visualization")

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

            st.divider()
            st.header("Filters")

            filter_type = st.selectbox(
                "Filter By", ["None", "Centrality", "Community", "Attribute", "Degree"]
            )

            if filter_type == "Centrality":
                if st.session_state.centrality_results is None:
                    if st.button(
                        "Compute Centralities for Filtering", key="comp_cent_filt"
                    ):
                        st.session_state.centrality_results = compute_all_centrality(
                            graph
                        )
                        st.rerun()
                if st.session_state.centrality_results:
                    cent_measures = list(st.session_state.centrality_results.keys())
                    cent_measure = st.selectbox("Centrality Measure", cent_measures)
                    values = list(
                        st.session_state.centrality_results[cent_measure].values()
                    )
                    min_val, max_val = min(values), max(values)
                    range_val = st.slider("Range", min_val, max_val, (min_val, max_val))
                    if st.button("Apply Centrality Filter", key="apply_cent_filt"):
                        st.session_state.filtered_graph = filter_by_centrality_range(
                            graph,
                            st.session_state.centrality_results[cent_measure],
                            range_val[0],
                            range_val[1],
                        )

            elif filter_type == "Community":
                if st.session_state.community_results is None:
                    if st.button(
                        "Detect Communities for Filtering", key="det_comm_filt"
                    ):
                        st.session_state.community_results = detect_louvain(graph)
                        st.rerun()
                if st.session_state.community_results:
                    comm_res = st.session_state.community_results
                    labels = (
                        comm_res.labels if hasattr(comm_res, "labels") else comm_res
                    )
                    if hasattr(labels, "values"):
                        communities = set(labels.values())
                    else:
                        communities = set()
                    selected = st.multiselect("Communities", sorted(communities))
                    if selected and st.button(
                        "Apply Community Filter", key="apply_comm_filt"
                    ):
                        st.session_state.filtered_graph = filter_by_community(
                            graph,
                            labels,
                            set(str(c) for c in selected),
                        )

            elif filter_type == "Attribute":
                available_attrs = _get_cached_attributes()
                if available_attrs:
                    attr = st.selectbox("Attribute", available_attrs)
                    values = _get_cached_values(attr)
                    selected_values = st.multiselect("Values", sorted(set(values)))
                    if selected_values and st.button(
                        "Apply Attribute Filter", key="apply_attr_filt"
                    ):
                        st.session_state.filtered_graph = filter_by_attribute(
                            graph, attr, selected_values
                        )
                else:
                    st.info("No node attributes available.")

            elif filter_type == "Degree":
                degrees = st.session_state.get(
                    f"degree_cache_{id(graph)}", [d for _, d in graph.degree()]
                )
                if degrees:
                    min_deg, max_deg = min(degrees), max(degrees)
                    deg_range = st.slider(
                        "Degree Range", min_deg, max_deg, (min_deg, max_deg)
                    )
                    if st.button("Apply Degree Filter", key="apply_deg_filt"):
                        st.session_state.filtered_graph = filter_by_degree_range(
                            graph, deg_range[0], deg_range[1]
                        )

            if st.session_state.get("filtered_graph") is not None:
                if st.button("Reset Filters", key="reset_filt"):
                    st.session_state.filtered_graph = None
                    st.rerun()

        active_graph = get_active_graph()
        viz_params["graph"] = active_graph

    return viz_params
