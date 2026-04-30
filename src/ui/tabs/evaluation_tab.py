import streamlit as st
import pandas as pd
from evaluation import (
    evaluate_clustering,
    compute_modularity,
    compute_conductance,
    compute_nmi,
    compute_ari,
)
from filtering import get_available_attributes, get_attribute_values


def _extract_labels(community_results):
    if hasattr(community_results, "labels"):
        return community_results.labels
    if isinstance(community_results, dict):
        return community_results
    return {}


def render_evaluation_tab():
    graph = st.session_state.get("graph")
    community_results = st.session_state.get("community_results")

    if graph is None:
        st.info("Load a graph first.")
        return

    if not community_results or community_results is None:
        st.info("Run a community detection algorithm from the Community tab first.")
        return

    labels = _extract_labels(community_results)
    if not labels:
        st.info("No community labels found.")
        return

    algo_name = st.session_state.get("community_algorithm", "Detected")

    st.subheader("Evaluation Metrics")

    evaluation = evaluate_clustering(graph, labels)
    eval_df = pd.DataFrame([{"Algorithm": algo_name, **evaluation}])

    if eval_df is not None and not eval_df.empty:
        st.dataframe(eval_df, width="stretch")

    st.divider()

    st.subheader("External Metrics (Ground Truth)")
    available_attrs = get_available_attributes(graph)
    if available_attrs:
        gt_attr = st.selectbox(
            "Ground Truth Attribute", available_attrs, key="gt_attr_eval"
        )
        if gt_attr:
            gt_values = get_attribute_values(graph, gt_attr)
            gt_labels = {n: str(v) for n, v in zip(graph.nodes(), gt_values)}

            col1, col2 = st.columns(2)
            with col1:
                nmi_score = compute_nmi(gt_labels, labels)
                if nmi_score is not None:
                    st.metric("NMI (Normalized Mutual Info)", f"{nmi_score:.4f}")
                else:
                    st.info("NMI could not be computed.")

            with col2:
                ari_score = compute_ari(gt_labels, labels)
                if ari_score is not None:
                    st.metric("ARI (Adjusted Rand Index)", f"{ari_score:.4f}")
                else:
                    st.info("ARI could not be computed.")
    else:
        st.info("No node attributes available for ground truth comparison.")

    st.divider()
    st.subheader("Metrics Explanation")
    st.markdown("""
    - **Modularity**: Measures the strength of division of a network into communities. Range: [-0.5, 1]. Higher is better.
    - **Conductance**: Fraction of total edge volume that points outside the community. Lower is better.
    - **NMI**: Normalized Mutual Information between detected communities and ground truth. Range: [0, 1]. Higher is better.
    - **ARI**: Adjusted Rand Index comparing detected vs ground truth assignments. Range: [-1, 1]. Higher is better.
    """)
