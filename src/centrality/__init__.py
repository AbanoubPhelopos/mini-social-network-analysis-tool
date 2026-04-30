from .degree import compute_degree_centrality
from .betweenness import compute_betweenness_centrality
from .closeness import compute_closeness_centrality
from .eigenvector import compute_eigenvector_centrality
import pandas as pd

def compute_all_centrality(G):
    return {
        "degree": compute_degree_centrality(G),
        "betweenness": compute_betweenness_centrality(G),
        "closeness": compute_closeness_centrality(G),
        "eigenvector": compute_eigenvector_centrality(G),
    }

def get_top_nodes(centrality_dict, n=10):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:n]

def centrality_to_dataframe(results, G=None):
    all_nodes = set()
    for v in results.values():
        all_nodes.update(v.keys())
    rows = []
    for node in sorted(all_nodes, key=str):
        row = {"Node": node}
        if G and G.has_node(node):
            for attr, val in G.nodes[node].items():
                row[attr] = val
        for method, values in results.items():
            row[method] = values.get(node, 0.0)
        rows.append(row)
    return pd.DataFrame(rows)
