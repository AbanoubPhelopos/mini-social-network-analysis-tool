import hashlib
import streamlit as st
import plotly.express as px
import pandas as pd
from metrics import (
    compute_basic_metrics,
    compute_degree_distribution,
    compute_clustering_coefficients,
    compute_average_path_length,
    get_connected_components,
)


def _graph_key(graph):
    return hashlib.md5(
        f"{graph.number_of_nodes()}_{graph.number_of_edges()}".encode()
    ).hexdigest()[:8]


def render_metrics_tab():
    graph = st.session_state.get("graph")
    if graph is None:
        st.info("Load a graph first.")
        return

    gk = _graph_key(graph)

    if st.button("Compute Metrics", type="primary", key=f"compute_metrics_{gk}"):
        with st.spinner("Computing metrics..."):
            basic = compute_basic_metrics(graph)
            degree_dist = compute_degree_distribution(graph)
            components = get_connected_components(graph)
            clustering_result = compute_clustering_coefficients(graph)
            st.session_state["metrics_basic"] = basic
            st.session_state["metrics_degree_dist"] = degree_dist
            st.session_state["metrics_components"] = components
            st.session_state["metrics_clustering"] = clustering_result

    basic = st.session_state.get("metrics_basic")
    if basic is None:
        st.info("Click **Compute Metrics** to analyze the graph.")
        return

    # Show graph type
    graph_type = "Directed" if basic.get("is_directed", False) else "Undirected"
    st.info(f"Graph Type: {graph_type}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nodes", basic.get("num_nodes", 0))
    with col2:
        st.metric("Edges", basic.get("num_edges", 0))
    with col3:
        st.metric("Density", f"{basic.get('density', 0):.4f}")
    with col4:
        st.metric("Avg Degree", f"{basic.get('avg_degree', 0):.2f}")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Avg Clustering", f"{basic.get('avg_clustering', 0):.4f}")
    with col6:
        st.metric("Transitivity", f"{basic.get('transitivity', 0):.4f}")
    with col7:
        st.metric("Connected", "Yes" if basic.get("is_connected", False) else "No")
    with col8:
        st.metric("Components", basic.get("num_components", 0))

    degree_dist = st.session_state.get("metrics_degree_dist")
    if degree_dist and degree_dist.get("distribution"):
        st.subheader("Degree Distribution")
        
        # Check if graph is directed and show appropriate degree info
        if basic.get("is_directed", False):
            # For directed graphs, calculate in-degree and out-degree distributions
            graph = st.session_state.get("graph")
            in_degrees = [d for _, d in graph.in_degree()]
            out_degrees = [d for _, d in graph.out_degree()]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**In-Degree Distribution**")
                in_dist_df = pd.DataFrame([
                    {"Degree": deg, "Count": in_degrees.count(deg)} 
                    for deg in sorted(set(in_degrees))
                ])
                fig1 = px.bar(in_dist_df, x="Degree", y="Count", title="In-Degree Distribution")
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                st.write("**Out-Degree Distribution**")
                out_dist_df = pd.DataFrame([
                    {"Degree": deg, "Count": out_degrees.count(deg)} 
                    for deg in sorted(set(out_degrees))
                ])
                fig2 = px.bar(out_dist_df, x="Degree", y="Count", title="Out-Degree Distribution")
                st.plotly_chart(fig2, use_container_width=True)
                
            # Show in/out degree statistics
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Min In-Degree", min(in_degrees) if in_degrees else 0)
            col_b.metric("Max In-Degree", max(in_degrees) if in_degrees else 0)
            col_c.metric("Min Out-Degree", min(out_degrees) if out_degrees else 0)
            col_d.metric("Max Out-Degree", max(out_degrees) if out_degrees else 0)
        else:
            # For undirected graphs, show regular degree distribution
            dist_df = pd.DataFrame(
                list(degree_dist["distribution"].items()),
                columns=["Degree", "Count"],
            )
            fig = px.bar(dist_df, x="Degree", y="Count", title="Degree Distribution")
            st.plotly_chart(fig, use_container_width=True)
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Min Degree", degree_dist["min"])
            col_b.metric("Max Degree", degree_dist["max"])
            col_c.metric("Mean Degree", f"{degree_dist['mean']:.2f}")
            col_d.metric("Std Dev", f"{degree_dist['std']:.2f}")

    st.subheader("Average Path Length")
    # Show different info for directed vs undirected graphs
    if basic.get("is_directed", False):
        st.info("For directed graphs, path length is computed on strongly connected components.")
        if st.button("Compute Average Path Length", key=f"apl_{gk}"):
            with st.spinner("Computing (may take a moment)..."):
                avg_path = compute_average_path_length(graph)
                st.session_state["metrics_avg_path"] = avg_path

        avg_path = st.session_state.get("metrics_avg_path")
        if avg_path is not None:
            avg_val, component_info = avg_path
            st.write(f"**Average Path Length:** {avg_val:.4f}")
            st.write(f"**Computed on component with:** {component_info['component_nodes']} nodes, {component_info['component_edges']} edges")
        else:
            st.info("Click **Compute Average Path Length** (can be slow on large graphs).")
    else:
        st.info("For undirected graphs, path length is computed on connected components.")
        if st.button("Compute Average Path Length", key=f"apl_{gk}"):
            with st.spinner("Computing (may take a moment)..."):
                avg_path = compute_average_path_length(graph)
                st.session_state["metrics_avg_path"] = avg_path

        avg_path = st.session_state.get("metrics_avg_path")
        if avg_path is not None:
            avg_val, component_info = avg_path
            st.write(f"**Average Path Length:** {avg_val:.4f}")
            st.write(f"**Computed on component with:** {component_info['component_nodes']} nodes, {component_info['component_edges']} edges")
        else:
            st.info("Click **Compute Average Path Length** (can be slow on large graphs).")

    components = st.session_state.get("metrics_components")
    if components:
        if basic.get("is_directed", False):
            st.subheader("Strongly Connected Components")
            st.info("For directed graphs, showing strongly connected components.")
        else:
            st.subheader("Connected Components")
            st.info("For undirected graphs, showing connected components.")
            
        comp_df = pd.DataFrame(
            [{"Component": i + 1, "Size": len(c)} for i, c in enumerate(components)]
        )
        st.dataframe(comp_df, use_container_width=True)

    clustering_result = st.session_state.get("metrics_clustering")
    if clustering_result is not None:
        st.subheader("Clustering Coefficients")
        avg_clust, per_node = clustering_result
        st.write(f"**Average Clustering Coefficient:** {avg_clust:.4f}")
        clust_df = pd.DataFrame(
            list(per_node.items()), columns=["Node", "Clustering Coefficient"]
        ).sort_values("Clustering Coefficient", ascending=False)
        st.dataframe(clust_df, use_container_width=True)

