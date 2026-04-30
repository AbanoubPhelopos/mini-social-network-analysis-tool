from sklearn.metrics import normalized_mutual_info_score


def compute_nmi(true_labels: dict, pred_labels: dict) -> float:
    """Compute the Normalized Mutual Information between two label assignments.

    Args:
        true_labels: A dict mapping node IDs to ground-truth community labels.
        pred_labels: A dict mapping node IDs to predicted community labels.

    Returns:
        The NMI score as a float between 0 and 1.
    """
    common_nodes = set(true_labels.keys()) & set(pred_labels.keys())
    if not common_nodes:
        return 0.0

    true_list = [true_labels[node] for node in sorted(common_nodes)]
    pred_list = [pred_labels[node] for node in sorted(common_nodes)]

    return normalized_mutual_info_score(true_list, pred_list)
