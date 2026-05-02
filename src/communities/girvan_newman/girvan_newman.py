import random
import time
from collections import Counter, defaultdict
from typing import Any, Dict, List, Set, Tuple

import networkx as nx

from core.graph_utils import to_simple_undirected

from ..base import CommunityResult


def _single_source_bfs_edge_betweenness(
    G: nx.Graph, source: Any
) -> Dict[Tuple[Any, Any], float]:
    """Compute edge betweenness contribution from a single BFS source.

    Uses Brandes' accumulation approach for a single shortest-path tree.

    Args:
        G: The graph to traverse.
        source: Starting node for BFS.

    Returns:
        Dictionary mapping edges to their betweenness contribution from this source.
    """
    edges: Dict[Tuple[Any, Any], float] = defaultdict(float)
    predecessors: Dict[Any, List[Any]] = defaultdict(list)
    shortest_paths: Dict[Any, int] = defaultdict(int)
    distance: Dict[Any, int] = {}
    stack: List[Any] = []

    shortest_paths[source] = 1
    distance[source] = 0
    queue = [source]
    head = 0

    while head < len(queue):
        node = queue[head]
        head += 1
        stack.append(node)
        for neighbor in G[node]:
            if neighbor not in distance:
                queue.append(neighbor)
                distance[neighbor] = distance[node] + 1
            if distance[neighbor] == distance[node] + 1:
                shortest_paths[neighbor] += shortest_paths[node]
                predecessors[neighbor].append(node)

    dependency: Dict[Any, float] = defaultdict(float)
    while stack:
        node = stack.pop()
        for pred in predecessors[node]:
            edge = (pred, node) if pred < node else (node, pred)
            contribution = (shortest_paths[pred] / shortest_paths[node]) * (
                1.0 + dependency[node]
            )
            edges[edge] += contribution
            dependency[pred] += contribution

    return edges


def _compute_approx_betweenness(
    G: nx.Graph, seeds: List[Any]
) -> Dict[Tuple[Any, Any], float]:
    """Compute approximate edge betweenness from sampled seed nodes.

    Args:
        G: The graph to analyze.
        seeds: List of seed nodes to sample from.

    Returns:
        Dictionary mapping edges to their approximate betweenness scores.
    """
    betweenness: Dict[Tuple[Any, Any], float] = defaultdict(float)
    for seed in seeds:
        contribution = _single_source_bfs_edge_betweenness(G, seed)
        for edge, value in contribution.items():
            betweenness[edge] += value

    norm = 2.0 / (len(seeds) * max(len(G) - 1, 1))
    for edge in betweenness:
        betweenness[edge] *= norm

    return betweenness


def _count_components(G: nx.Graph) -> int:
    """Count connected components using a fast BFS-based approach.

    Args:
        G: The graph to analyze.

    Returns:
        Number of connected components.
    """
    visited: Set[Any] = set()
    count = 0
    for node in G:
        if node not in visited:
            count += 1
            queue = [node]
            head = 0
            while head < len(queue):
                current = queue[head]
                head += 1
                if current in visited:
                    continue
                visited.add(current)
                for neighbor in G[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
    return count


def _get_component_labels(G: nx.Graph) -> Dict[Any, int]:
    """Assign a community label to each node based on connected components.

    Args:
        G: The graph to analyze.

    Returns:
        Dictionary mapping each node to its component label.
    """
    visited: Set[Any] = set()
    labels: Dict[Any, int] = {}
    component_id = 0
    for node in G:
        if node not in visited:
            queue = [node]
            head = 0
            while head < len(queue):
                current = queue[head]
                head += 1
                if current in visited:
                    continue
                visited.add(current)
                labels[current] = component_id
                for neighbor in G[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            component_id += 1
    return labels


def _assign_remaining_by_vote(
    labels: Dict[Any, int],
    remaining_nodes: List[Any],
    original_graph: nx.Graph,
) -> Dict[Any, int]:
    """Assign community labels to leftover nodes via neighbor majority vote.

    Args:
        labels: Existing labels for the core subgraph nodes.
        remaining_nodes: Nodes that were excluded from the subgraph.
        original_graph: The full original graph for neighbor lookups.

    Returns:
        Updated labels dictionary including all remaining nodes.
    """
    for node in remaining_nodes:
        neighbor_votes: Dict[int, int] = Counter()
        for neighbor in original_graph[node]:
            if neighbor in labels:
                neighbor_votes[labels[neighbor]] += 1
        if neighbor_votes:
            labels[node] = neighbor_votes.most_common(1)[0][0]
        else:
            labels[node] = 0
    return labels


def detect_girvan_newman(
    G: nx.Graph,
    k: int = 1,
    max_nodes: int = 50,
) -> CommunityResult:
    """
    Girvan-Newman community detection.

    Steps:
    1. Compute edge betweenness
    2. Remove edge with highest betweenness
    3. Recompute betweenness
    4. Repeat until stopping condition

    Stopping conditions:
    - If k = 1  -> continue until no edges remain
    - If k > 1  -> stop when every community size <= k
    """

    start = time.perf_counter()

    undirected = to_simple_undirected(G)
    all_nodes = list(undirected.nodes())
    remaining_nodes = []

    # Performance trimming
    if len(all_nodes) > max_nodes:
        sorted_nodes = sorted(
            all_nodes, key=lambda n: undirected.degree(n), reverse=True
        )
        keep_nodes = sorted_nodes[:max_nodes]
        remaining_nodes = sorted_nodes[max_nodes:]
        working_graph = undirected.subgraph(keep_nodes).copy()
    else:
        working_graph = undirected.copy()

    iteration = 0
    removed_edges = []
    communities_by_iteration = []
    modularities_by_iteration = []
    num_communities_by_iteration = []

    best_labels = {n: 0 for n in working_graph.nodes()}
    best_modularity = -1.0
    best_iteration = 0

    while working_graph.number_of_edges() > 0:

        # STEP 1: calculate betweenness
        edge_betweenness = nx.edge_betweenness_centrality(
            working_graph, normalized=False
        )

        if not edge_betweenness:
            break

        # STEP 2: remove highest edge
        edge_to_remove, score = max(
            edge_betweenness.items(),
            key=lambda x: x[1]
        )

        working_graph.remove_edge(*edge_to_remove)

        removed_edges.append(
            (edge_to_remove[0], edge_to_remove[1], score)
        )

        # Communities after removal
        labels = _get_component_labels(working_graph)
        communities_by_iteration.append(labels.copy())

        num_comms = len(set(labels.values()))
        num_communities_by_iteration.append(num_comms)

        # Build community sets
        communities_sets = defaultdict(set)
        for node, comm in labels.items():
            communities_sets[comm].add(node)

        # Compute modularity on subgraph containing only nodes in communities
        # This ensures all nodes in the partition are present in the graph
        community_nodes = set()
        for community in communities_sets.values():
            community_nodes.update(community)
        
        subgraph_for_mod = undirected.subgraph(community_nodes)
        mod = nx.community.modularity(
            subgraph_for_mod,
            communities_sets.values()
        )

        modularities_by_iteration.append(mod)

        # Keep best partition
        if mod > best_modularity:
            best_modularity = mod
            best_labels = labels.copy()
            best_iteration = iteration

        # ---------------------------
        # STOPPING CONDITIONS
        # ---------------------------

        if k > 1:
            sizes = [len(c) for c in communities_sets.values()]
            if all(size <= k for size in sizes):
                break

        iteration += 1

    # If k=1 and edges exhausted, final labels already best_labels

    labels = best_labels

    if remaining_nodes:
        labels = _assign_remaining_by_vote(
            labels, remaining_nodes, undirected
        )

    num_communities = len(set(labels.values()))
    community_sizes = dict(Counter(labels.values()))

    elapsed = time.perf_counter() - start

    result = CommunityResult(
        algorithm="Girvan-Newman",
        labels=labels,
        num_communities=num_communities,
        modularity=best_modularity,
        execution_time=elapsed,
        community_sizes=community_sizes,
    )

    result.iteration_data = {
        "communities_by_iteration": communities_by_iteration,
        "removed_edges": removed_edges,
        "modularities_by_iteration": modularities_by_iteration,
        "num_communities_by_iteration": num_communities_by_iteration,
        "best_iteration": best_iteration,
        "best_modularity": best_modularity,
        "total_iterations": iteration + 1,
    }

    return result
