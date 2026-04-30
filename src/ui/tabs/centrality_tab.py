import streamlit as st
import plotly.express as px
import pandas as pd
from centrality import (
    compute_all_centrality,
    get_top_nodes,
    centrality_to_dataframe,
    compute_degree_centrality,
    compute_betweenness_centrality,
    compute_closeness_centrality,
)
from export import export_centrality_csv


def render_centrality_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    if st.button("Compute All Centralities", type="primary", key="comp_cent"):
        with st.spinner("Computing centralities..."):
            st.session_state.centrality_results = compute_all_centrality(graph)
        st.success("Centralities computed!")

    results = st.session_state.get("centrality_results")
    if results is None:
        st.info("Click 'Compute All Centralities' to begin.")
        return

    st.subheader("Top 10 Nodes by Centrality")
    measures = list(results.keys())
    cols = st.columns(min(len(measures), 4))
    for idx, measure in enumerate(measures[:4]):
        with cols[idx]:
            top = get_top_nodes(results[measure], 10)
            st.markdown(f"**{measure.replace('_', ' ').title()}**")
            for rank, (node, score) in enumerate(top, 1):
                st.write(f"{rank}. {node}: {score:.4f}")

    st.subheader("Centrality Distribution")
    selected_measure = st.selectbox("Select Measure", measures)
    values = list(results[selected_measure].values())
    fig = px.histogram(
        x=values,
        nbins=30,
        title=f"{selected_measure.replace('_', ' ').title()} Distribution",
    )
    fig.update_layout(xaxis_title="Score", yaxis_title="Count")
    st.plotly_chart(fig, width="stretch")

    st.subheader("Full Centrality Table")
    df = centrality_to_dataframe(results)
    st.dataframe(df, width="stretch")

    if st.button("Export Centrality CSV", key="export_cent_tab"):
        path = export_centrality_csv(df)
        with open(path, "rb") as f:
            st.download_button(
                "Download", data=f.read(), file_name="centrality.csv", mime="text/csv"
            )
