import streamlit as st
import plotly.express as px
import pandas as pd
from communities import (
    detect_louvain,
    detect_girvan_newman,
    detect_label_propagation,
    compare_algorithms,
    community_result_to_dataframe,
)


def render_community_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    st.subheader("Run Individual Algorithms")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Louvain", key="comm_louv"):
            with st.spinner("Running Louvain..."):
                st.session_state.community_results = detect_louvain(graph)
                st.session_state.community_algorithm = "Louvain"
            st.success("Louvain detection complete!")

    with col2:
        max_comm = st.slider("Max Communities (GN)", 2, 20, 5, key="gn_max_comm")
        if st.button("Girvan-Newman", key="comm_gn"):
            with st.spinner("Running Girvan-Newman..."):
                st.session_state.community_results = detect_girvan_newman(
                    graph, max_communities=max_comm
                )
                st.session_state.community_algorithm = "Girvan-Newman"
            st.success("Girvan-Newman detection complete!")

    with col3:
        if st.button("Label Propagation", key="comm_lp"):
            with st.spinner("Running Label Propagation..."):
                st.session_state.community_results = detect_label_propagation(graph)
                st.session_state.community_algorithm = "Label Propagation"
            st.success("Label Propagation detection complete!")

    st.divider()
    st.subheader("Algorithm Comparison (Side-by-Side)")

    if st.button("Compare All Algorithms", type="primary", key="compare_all"):
        with st.spinner("Running all 3 algorithms..."):
            results_list = []
            louv_res = detect_louvain(graph)
            results_list.append(louv_res)
            gn_res = detect_girvan_newman(graph, max_communities=5)
            results_list.append(gn_res)
            lp_res = detect_label_propagation(graph)
            results_list.append(lp_res)
            st.session_state["comparison_results"] = results_list
            st.session_state.community_results = louv_res
            st.session_state.community_algorithm = "Louvain"

    comp_results = st.session_state.get("comparison_results")
    if comp_results:
        comp_df = compare_algorithms(comp_results)
        st.dataframe(comp_df, width="stretch", hide_index=True)

        col_a, col_b, col_c = st.columns(3)
        for i, res in enumerate(comp_results):
            target_col = [col_a, col_b, col_c][i]
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
    df = community_result_to_dataframe(results, graph)
    if df is not None and not df.empty:
        community_col = "community"
        size_counts = df[community_col].value_counts().reset_index()
        size_counts.columns = ["Community", "Size"]
        fig = px.bar(size_counts, x="Community", y="Size", title="Community Sizes")
        st.plotly_chart(fig, width="stretch")

    st.subheader("Community Assignments")
    if df is not None:
        st.dataframe(df, width="stretch")

    if st.button("Export Community CSV", key="export_comm"):
        csv_data = df.to_csv(index=False)
        st.download_button(
            "Download", data=csv_data, file_name="communities.csv", mime="text/csv"
        )
