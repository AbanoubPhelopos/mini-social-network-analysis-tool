import streamlit as st
import pandas as pd
from link_analysis import (
    compute_pagerank,
    find_shortest_path,
    compute_hits,
)


def render_link_analysis_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    st.subheader("PageRank")
    if st.button("Compute PageRank", type="primary", key="comp_pr"):
        with st.spinner("Computing PageRank..."):
            pagerank = compute_pagerank(graph)
            st.session_state["link_pagerank"] = pagerank

    pagerank = st.session_state.get("link_pagerank")
    if pagerank:
        pr_df = pd.DataFrame(
            sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:15],
            columns=["Node", "PageRank Score"],
        )
        st.dataframe(pr_df, use_container_width=True, hide_index=True)
    else:
        st.info("Click **Compute PageRank** to analyze node influence.")

    st.subheader("Top Influential Nodes")
    methods = ["degree", "betweenness", "closeness", "pagerank"]
    selected_method = st.selectbox("Influence Method", methods, key="influence_method")
    top_n = st.slider("Top N", 5, 50, 15, key="top_n_influence")

    if st.button("Compute Top Influential", key="comp_influence"):
        with st.spinner(f"Computing {selected_method} centrality..."):
            if selected_method == "pagerank":
                scores = compute_pagerank(graph)
            elif selected_method == "betweenness":
                from centrality import compute_betweenness_centrality

                scores = compute_betweenness_centrality(graph)
            elif selected_method == "closeness":
                from centrality import compute_closeness_centrality

                scores = compute_closeness_centrality(graph)
            elif selected_method == "degree":
                from centrality import compute_degree_centrality

                scores = compute_degree_centrality(graph)
            else:
                scores = compute_pagerank(graph)
            top_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            st.session_state["influence_result"] = (selected_method, top_nodes)

    influence_result = st.session_state.get("influence_result")
    if influence_result:
        method, top_nodes = influence_result
        if top_nodes:
            inf_df = pd.DataFrame(top_nodes, columns=["Node", "Score"])
            st.dataframe(inf_df, use_container_width=True, hide_index=True)
    else:
        st.info("Click **Compute Top Influential** to analyze.")

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
            path_result = find_shortest_path(graph, source_node, target_node)
            path_nodes, path_length = path_result
            if path_nodes:
                st.success(f"Path found (length {int(path_length)}):")
                st.write(" → ".join(str(n) for n in path_nodes))
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
                st.dataframe(hubs_df, use_container_width=True, hide_index=True)
            with col2:
                st.markdown("**Top Authorities**")
                auth_df = pd.DataFrame(
                    sorted(authorities.items(), key=lambda x: x[1], reverse=True)[:15],
                    columns=["Node", "Authority Score"],
                )
                st.dataframe(auth_df, use_container_width=True, hide_index=True)
        else:
            st.info("HITS could not be computed for this graph.")
