from typing import Any, Dict
import networkx as nx


def compute_betweenness_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Compute betweenness centrality for all nodes in the graph.
    
    Betweenness centrality measures the number of times a node acts 
    as a bridge along the shortest path between two other nodes.
    
    Args:
        G: NetworkX graph
        
    Returns:
        Dictionary mapping nodes to their betweenness centrality scores
    """
    return nx.betweenness_centrality(G, normalized=True)
