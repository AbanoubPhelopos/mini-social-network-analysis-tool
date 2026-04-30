from .modularity import compute_modularity
from .conductance import compute_conductance
from .nmi import compute_nmi
from .ari import compute_ari
import pandas as pd

def evaluate_clustering(G, labels, true_labels=None):
    results = {
        "Modularity": compute_modularity(G, labels),
        "Conductance": compute_conductance(G, labels),
        "Num Communities": len(set(labels.values())),
    }
    if true_labels:
        results["NMI"] = compute_nmi(true_labels, labels)
        results["ARI"] = compute_ari(true_labels, labels)
    return results

def evaluate_to_dataframe(evaluations):
    rows = []
    for algo, metrics in evaluations.items():
        row = {"Algorithm": algo}
        row.update(metrics)
        rows.append(row)
    return pd.DataFrame(rows)
