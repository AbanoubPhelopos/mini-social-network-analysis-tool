import streamlit as st
import pandas as pd
from link_analysis import (
    compute_pagerank,
    find_shortest_path,
    get_top_influential_nodes,
    compute_hits,
)


def render_link_analysis_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    st.subheader("PageRank")
    pagerank = compute_pagerank(graph)
    if pagerank:
        pr_df = pd.DataFrame(
            sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:15],
            columns=["Node", "PageRank Score"],
        )
        st.dataframe(pr_df, width="stretch", hide_index=True)

    st.subheader("Top Influential Nodes")
    methods = ["degree", "betweenness", "closeness", "pagerank"]
    selected_method = st.selectbox("Influence Method", methods, key="influence_method")
    top_n = st.slider("Top N", 5, 50, 15, key="top_n_influence")

    top_nodes = get_top_influential_nodes(graph, method=selected_method, n=top_n)
    if top_nodes:
        inf_df = pd.DataFrame(top_nodes, columns=["Node", "Score"])
        st.dataframe(inf_df, width="stretch", hide_index=True)

    st.subheader("Shortest Path Finder")
    node_list = list(graph.nodes())
    node_labels = [str(n) for n in node_list]
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("Source Node", node_labels, key="sp_source")
    with col2:
        target = st.selectbox(
            "Target Node",
            node_labels,
            index=len(node_labels) - 1 if len(node_labels) > 1 else 0,
            key="sp_target",
        )

    if st.button("Find Shortest Path", key="find_sp"):
        if source == target:
            st.warning("Source and target must be different.")
        else:
            source_node = node_list[node_labels.index(source)]
            target_node = node_list[node_labels.index(target)]
            path = find_shortest_path(graph, source_node, target_node)
            if path is not None:
                st.success(f"Path found (length {len(path) - 1}):")
                st.write(" → ".join(str(n) for n in path))
            else:
                st.error("No path exists between these nodes.")

    st.subheader("HITS (Hubs & Authorities)")
    if st.button("Compute HITS", key="comp_hits"):
        hubs, authorities = compute_hits(graph)
        if hubs and authorities:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Top Hubs**")
                hubs_df = pd.DataFrame(
                    sorted(hubs.items(), key=lambda x: x[1], reverse=True)[:15],
                    columns=["Node", "Hub Score"],
                )
                st.dataframe(hubs_df, width="stretch", hide_index=True)
            with col2:
                st.markdown("**Top Authorities**")
                auth_df = pd.DataFrame(
                    sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:15],
                    columns=["Node", "Authority Score"],
                )
                st.dataframe(auth_df, width="stretch", hide_index=True)
        else:
            st.info("HITS could not be computed for this graph.")
