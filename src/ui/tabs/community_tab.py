import streamlit as st
import plotly.express as px
import pandas as pd
from communities import (
    detect_louvain,
    detect_girvan_newman,
    compare_algorithms,
    community_result_to_dataframe,
)


def render_community_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    st.subheader("Run Individual Algorithms")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Louvain", key="comm_louv"):
            with st.spinner("Running Louvain..."):
                st.session_state.community_results = detect_louvain(graph)
                st.session_state.community_algorithm = "Louvain"
            st.success("Louvain detection complete!")

    with col2:
        if st.button("Girvan-Newman", key="comm_gn"):
            with st.spinner("Running Girvan-Newman..."):
                st.session_state.community_results = detect_girvan_newman(graph)
                st.session_state.community_algorithm = "Girvan-Newman"
            st.success("Girvan-Newman detection complete!")

    st.divider()
    st.subheader("Algorithm Comparison (Side-by-Side)")

    if st.button("Compare All Algorithms", type="primary", key="compare_all"):
        with st.spinner("Running Girvan-Newman and Louvain algorithms..."):
            results_list = []
            louv_res = detect_louvain(graph)
            results_list.append(louv_res)
            gn_res = detect_girvan_newman(graph)
            results_list.append(gn_res)
            st.session_state["comparison_results"] = results_list
            st.session_state.community_results = louv_res
            st.session_state.community_algorithm = "Louvain"

    comp_results = st.session_state.get("comparison_results")
    if comp_results:
        comp_df = compare_algorithms(comp_results)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        col_a, col_b = st.columns(2)
        for i, res in enumerate(comp_results):
            target_col = [col_a, col_b][i]
            with target_col:
                st.markdown(f"**{res.algorithm}**")
                st.metric("Communities", res.num_communities)
                st.metric("Modularity", f"{res.modularity:.4f}")
                st.metric("Time", f"{res.execution_time:.2f}s")
                st.metric("Largest Community", res.get_community_sizes_list()[0])

    st.divider()
    results = st.session_state.get("community_results")
    if results is None:
        st.info("Run a community detection algorithm above.")
        return

    algo_name = st.session_state.get("community_algorithm", "Unknown")
    st.subheader(f"Latest Result: {algo_name}")

    if hasattr(results, "num_communities"):
        st.metric("Communities", results.num_communities)
        st.metric("Modularity", f"{results.modularity:.4f}")
        st.metric("Time", f"{results.execution_time:.2f}s")

    st.subheader("Community Sizes")
    cache_key = f"comm_df_{st.session_state.get('community_algorithm', '')}_{st.session_state.get('graph') is not None}"
    if cache_key not in st.session_state:
        df = community_result_to_dataframe(results, graph)
        st.session_state[cache_key] = df
    else:
        df = st.session_state[cache_key]

    if df is not None and not df.empty:
        community_col = "community"
        size_counts = df[community_col].value_counts().reset_index()
        size_counts.columns = ["Community", "Size"]
        fig = px.bar(size_counts, x="Community", y="Size", title="Community Sizes")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Community Assignments")
    if df is not None:
        st.dataframe(df, use_container_width=True)

    
