import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Mini Social Networks Analysis Tool",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.sidebar import render_sidebar, get_active_graph
from ui.tabs.visualization_tab import render_visualization_tab
from ui.tabs.metrics_tab import render_metrics_tab
from ui.tabs.centrality_tab import render_centrality_tab
from ui.tabs.community_tab import render_community_tab
from ui.tabs.evaluation_tab import render_evaluation_tab
from ui.tabs.link_analysis_tab import render_link_analysis_tab
from ui.tabs.export_tab import render_export_tab


def init_session_state():
    defaults = {
        "graph": None,
        "nodes_df": None,
        "edges_df": None,
        "graph_loaded": False,
        "centrality_results": {},
        "community_results": {},
        "filtered_graph": None,
        "viz_html_content": None,
        "metrics_basic": None,
        "metrics_degree_dist": None,
        "metrics_components": None,
        "metrics_clustering": None,
        "metrics_avg_path": None,
        "link_pagerank": None,
        "influence_result": None,
        "eval_result": None,
        "comparison_results": None,
        "community_algorithm": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def main():
    st.title("Mini Social Networks Analysis Tool")
    st.markdown(
        "An interactive tool for network analysis, visualization, "
        "community detection, and link analysis."
    )

    init_session_state()
    viz_params = render_sidebar()

    if not st.session_state.graph_loaded:
        st.markdown("---")
        st.markdown("### Getting Started")
        st.markdown("""
        1. Use the **sidebar** to load graph data from the `data/` folder or upload CSV files.
        2. Select whether the graph is **directed** or **undirected**.
        3. Click **Load Graph** to build the network.
        4. Use the tabs below to explore metrics, centrality, communities, and more.

        **Expected CSV formats:**
        - **Nodes:** Must have an ID column (id, ID, node, etc.) + any attributes
        - **Edges:** Must have Source and Target columns + optional weight
        """)
        return

    active_tab = st.radio(
        "Section",
        [
            "Visualization",
            "Metrics",
            "Centrality",
            "Communities",
            "Evaluation",
            "Link Analysis",
            "Export",
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="active_section",
    )

    if active_tab == "Visualization":
        render_visualization_tab(viz_params)
    elif active_tab == "Metrics":
        render_metrics_tab()
    elif active_tab == "Centrality":
        render_centrality_tab()
    elif active_tab == "Communities":
        render_community_tab()
    elif active_tab == "Evaluation":
        render_evaluation_tab()
    elif active_tab == "Link Analysis":
        render_link_analysis_tab()
    elif active_tab == "Export":
        render_export_tab()


if __name__ == "__main__":
    main()
