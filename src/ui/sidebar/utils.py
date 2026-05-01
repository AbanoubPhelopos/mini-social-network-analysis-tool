import streamlit as st


def get_active_graph():
    """Get the currently active graph (filtered or original)."""
    if st.session_state.get("filtered_graph") is not None:
        return st.session_state.filtered_graph
    return st.session_state.get("graph")


def get_node_attributes():
    """Get node attributes from the current graph."""
    graph = st.session_state.get("graph")
    if graph is None:
        return []
    
    attributes = set()
    for node, data in graph.nodes(data=True):
        attributes.update(data.keys())
    return sorted(attributes)


def get_attribute_values(attribute):
    """Get values for a specific attribute."""
    graph = st.session_state.get("graph")
    if graph is None:
        return []
    
    values = set()
    for node, data in graph.nodes(data=True):
        if attribute in data:
            values.add(data[attribute])
    return sorted(values)
