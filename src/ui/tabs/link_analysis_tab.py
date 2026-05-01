import streamlit as st
import pandas as pd
from link_analysis import compute_pagerank, compute_betweenness_centrality


def render_link_analysis_tab():
    """Render link analysis tab with PageRank and Betweenness Centrality."""
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
            sorted(pagerank.items(), key=lambda x: x[1], reverse=True),
            columns=["Node", "PageRank Score"],
        )
        st.dataframe(pr_df, use_container_width=True, hide_index=True)
    else:
        st.info("Click **Compute PageRank** to analyze node influence.")

    st.subheader("Betweenness Centrality")
    if st.button("Compute Betweenness Centrality", type="primary", key="comp_bc"):
        with st.spinner("Computing Betweenness Centrality..."):
            betweenness = compute_betweenness_centrality(graph)
            st.session_state["link_betweenness"] = betweenness

    betweenness = st.session_state.get("link_betweenness")
    if betweenness:
        bc_df = pd.DataFrame(
            sorted(betweenness.items(), key=lambda x: x[1], reverse=True),
            columns=["Node", "Betweenness Centrality"],
        )
        st.dataframe(bc_df, use_container_width=True, hide_index=True)
    else:
        st.info("Click **Compute Betweenness Centrality** to analyze node importance.")
