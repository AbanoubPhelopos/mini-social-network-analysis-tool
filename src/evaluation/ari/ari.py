from sklearn.metrics import adjusted_rand_score


def compute_ari(true_labels: dict, pred_labels: dict) -> float:
    """Compute the Adjusted Rand Index between two label assignments.

    Args:
        true_labels: A dict mapping node IDs to ground-truth community labels.
        pred_labels: A dict mapping node IDs to predicted community labels.

    Returns:
        The ARI score as a float.
    """
    common_nodes = set(true_labels.keys()) & set(pred_labels.keys())
    if not common_nodes:
        return 0.0

    true_list = [true_labels[node] for node in sorted(common_nodes)]
    pred_list = [pred_labels[node] for node in sorted(common_nodes)]

    return adjusted_rand_score(true_list, pred_list)
