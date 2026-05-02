import streamlit as st
import pandas as pd
from evaluation import (
    evaluate_clustering,
    compute_nmi,
    compute_ari,
)


def _extract_labels(community_results):
    if hasattr(community_results, "labels"):
        return community_results.labels
    if isinstance(community_results, dict):
        return community_results
    return {}


def get_node_attributes():
    graph = st.session_state.get("graph")
    if graph is None:
        return []
    
    attributes = set()
    for node, data in graph.nodes(data=True):
        attributes.update(data.keys())
    return sorted(attributes)


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

    if st.button("Compute Evaluation Metrics", type="primary", key="eval_metrics"):
        with st.spinner("Computing evaluation metrics..."):
            evaluation = evaluate_clustering(graph, labels)
            st.session_state["eval_result"] = evaluation

    evaluation = st.session_state.get("eval_result")
    if evaluation is None:
        st.info("Click **Compute Evaluation Metrics** to analyze.")
        return

    eval_df = pd.DataFrame([{"Algorithm": algo_name, **evaluation}])

    if eval_df is not None and not eval_df.empty:
        st.dataframe(eval_df, use_container_width=True)

    st.divider()

    st.subheader("External Metrics (Ground Truth)")
    available_attrs = get_node_attributes()
    if available_attrs:
        gt_attr = st.selectbox(
            "Ground Truth Attribute", available_attrs, key="gt_attr_eval"
        )
        if gt_attr:
            gt_labels = {
                str(n): str(graph.nodes[n].get(gt_attr, "")) for n in graph.nodes()
            }

            if st.button("Compute NMI & ARI", key="comp_nmi_ari"):
                with st.spinner("Computing external metrics..."):
                    nmi_score = compute_nmi(gt_labels, labels)
                    ari_score = compute_ari(gt_labels, labels)
                    st.session_state["nmi_score"] = nmi_score
                    st.session_state["ari_score"] = ari_score

            nmi_score = st.session_state.get("nmi_score")
            ari_score = st.session_state.get("ari_score")

            col1, col2 = st.columns(2)
            with col1:
                if nmi_score is not None:
                    st.metric("NMI (Normalized Mutual Info)", f"{nmi_score:.4f}")
                else:
                    st.info("Click **Compute NMI & ARI** above.")

            with col2:
                if ari_score is not None:
                    st.metric("ARI (Adjusted Rand Index)", f"{ari_score:.4f}")
                else:
                    st.info("Click **Compute NMI & ARI** above.")
    else:
        st.info("No node attributes available for ground truth comparison.")

    
