import time
from typing import Any, Dict

import community as community_louvain
import networkx as nx

from ..base import CommunityResult


def detect_louvain(G: nx.Graph) -> CommunityResult:
    start = time.perf_counter()
    undirected = G.to_undirected() if G.is_directed() else G
    partition: Dict[Any, int] = community_louvain.best_partition(undirected)
    elapsed = time.perf_counter() - start

    num_communities = len(set(partition.values()))
    community_sizes: Dict[int, int] = {}
    for comm_id in partition.values():
        community_sizes[comm_id] = community_sizes.get(comm_id, 0) + 1

    modularity = community_louvain.modularity(partition, undirected)

    return CommunityResult(
        algorithm="Louvain",
        labels=partition,
        num_communities=num_communities,
        modularity=modularity,
        execution_time=elapsed,
        community_sizes=community_sizes,
    )
