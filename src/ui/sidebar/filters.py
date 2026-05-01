import streamlit as st
from centrality import compute_all_centrality
from communities import detect_louvain
from filtering import (
    filter_by_centrality_range,
    filter_by_community,
    filter_by_attribute,
    filter_by_degree_range,
)
from .utils import get_node_attributes, get_attribute_values


def render_filters_section():
    """Render the filters section of the sidebar."""
    if not st.session_state.get("graph_loaded"):
        return
    
    graph = st.session_state.graph
    
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
        available_attrs = get_node_attributes()
        if available_attrs:
            attr = st.selectbox("Attribute", available_attrs)
            values = get_attribute_values(attr)
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
        degrees = [d for _, d in graph.degree()]
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
