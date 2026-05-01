import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(

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


def init_session_state():
    # Initialize basic session state variables
    if "graph" not in st.session_state:
        st.session_state.graph = None
    if "nodes_df" not in st.session_state:
        st.session_state.nodes_df = None
    if "edges_df" not in st.session_state:
        st.session_state.edges_df = None
    if "graph_loaded" not in st.session_state:
        st.session_state.graph_loaded = False
    if "centrality_results" not in st.session_state:
        st.session_state.centrality_results = {}
    if "community_results" not in st.session_state:
        st.session_state.community_results = {}
    if "filtered_graph" not in st.session_state:
        st.session_state.filtered_graph = None
    if "link_pagerank" not in st.session_state:
        st.session_state.link_pagerank = None
    if "link_betweenness" not in st.session_state:
        st.session_state.link_betweenness = None
    if "eval_result" not in st.session_state:
        st.session_state.eval_result = None
    if "nmi_score" not in st.session_state:
        st.session_state.nmi_score = None
    if "ari_score" not in st.session_state:
        st.session_state.ari_score = None


def main():
  
    init_session_state()
    viz_params = render_sidebar()

    if not st.session_state.graph_loaded:
       
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


if __name__ == "__main__":
    main()
