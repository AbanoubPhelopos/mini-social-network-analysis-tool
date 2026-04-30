import time
from collections import Counter
from typing import Any, Dict

import networkx as nx

from ..base import CommunityResult


def detect_label_propagation(G: nx.Graph) -> CommunityResult:
    start = time.perf_counter()
    undirected = G.to_undirected() if G.is_directed() else G
    communities = nx.community.label_propagation_communities(undirected)
    elapsed = time.perf_counter() - start

    labels: Dict[Any, int] = {}
    for comm_id, community in enumerate(communities):
        for node in community:
            labels[node] = comm_id

    num_communities = len(communities)
    community_sizes: Dict[int, int] = {
        comm_id: len(community) for comm_id, community in enumerate(communities)
    }

    communities_list = [frozenset(c) for c in communities]
    modularity = nx.community.modularity(undirected, communities_list)

    return CommunityResult(
        algorithm="Label Propagation",
        labels=labels,
        num_communities=num_communities,
        modularity=modularity,
        execution_time=elapsed,
        community_sizes=community_sizes,
    )
