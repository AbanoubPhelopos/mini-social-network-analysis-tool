import streamlit as st
from .data_loading import render_data_loading_section
from .visualization_settings import render_visualization_settings_section
from .filters import render_filters_section
from .utils import get_active_graph


def render_sidebar() -> dict:
    """Render the main sidebar using modular components."""
    with st.sidebar:
        # Render data loading section
        render_data_loading_section()
        
        # Initialize visualization parameters
        viz_params = {}
        
        # Render visualization settings if graph is loaded
        if st.session_state.get("graph_loaded"):
            viz_params = render_visualization_settings_section()
            
            # Render filters section
            render_filters_section()
        
        # Get the active graph (filtered or original)
        active_graph = get_active_graph()
        viz_params["graph"] = active_graph

    return viz_params
