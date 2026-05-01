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

   
    measures = list(results.keys())
    st.subheader("Full Centrality Table")
    df = centrality_to_dataframe(results)
    st.dataframe(df, use_container_width=True)

    st.subheader("Centrality Distribution")
    selected_measure = st.selectbox("Select Measure", measures)
    values = list(results[selected_measure].values())
    fig = px.histogram(
        x=values,
        nbins=30,
        title=f"{selected_measure.replace('_', ' ').title()} Distribution",
    )
    fig.update_layout(xaxis_title="Score", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

    
