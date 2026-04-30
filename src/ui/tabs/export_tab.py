import streamlit as st
import pandas as pd
from export import (
    export_metrics_csv,
    export_graph_graphml,
    export_centrality_csv,
    export_community_csv,
)
from metrics import compute_basic_metrics


def render_export_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Export Metrics")
        if st.button("Generate Metrics CSV", key="exp_metrics"):
            basic = compute_basic_metrics(graph)
            path = export_metrics_csv(basic)
            with open(path, "rb") as f:
                st.download_button(
                    "Download Metrics CSV",
                    data=f.read(),
                    file_name="metrics.csv",
                    mime="text/csv",
                    key="dl_metrics",
                )

    with col2:
        st.subheader("Export Graph")
        fmt = st.selectbox("Format", ["GraphML", "PNG"], key="export_graph_fmt")
        if st.button("Export Graph", key="exp_graph"):
            try:
                if fmt == "GraphML":
                    path = export_graph_graphml(graph, "graph_export.graphml")
                    with open(path, "rb") as f:
                        st.download_button(
                            "Download GraphML",
                            data=f.read(),
                            file_name="graph_export.graphml",
                            mime="application/xml",
                            key="dl_graph",
                        )
                else:
                    st.info(
                        "PNG export requires the graph visualization to be rendered."
                    )
            except Exception as e:
                st.error(f"Export failed: {e}")

    with col3:
        st.subheader("Export Centrality")
        centrality_results = st.session_state.get("centrality_results")
        if centrality_results:
            if st.button("Export Centrality CSV", key="exp_cent"):
                from centrality import centrality_to_dataframe

                df = centrality_to_dataframe(centrality_results)
                path = export_centrality_csv(df)
                with open(path, "rb") as f:
                    st.download_button(
                        "Download Centrality CSV",
                        data=f.read(),
                        file_name="centrality.csv",
                        mime="text/csv",
                        key="dl_cent",
                    )
        else:
            st.info("Compute centralities from the Centrality tab first.")
