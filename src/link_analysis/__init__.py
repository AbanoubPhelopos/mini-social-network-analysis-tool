from .pagerank import compute_pagerank
from .shortest_path import find_shortest_path
from .hits import compute_hits
import networkx as nx

def get_top_influential_nodes(G, method="pagerank", n=10):
    if method == "pagerank":
        scores = compute_pagerank(G)
    elif method == "betweenness":
        scores = dict(nx.betweenness_centrality(G, normalized=True))
    elif method == "degree":
        scores = dict(nx.degree_centrality(G))
    elif method == "closeness":
        scores = dict(nx.closeness_centrality(G))
    else:
        scores = compute_pagerank(G)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
