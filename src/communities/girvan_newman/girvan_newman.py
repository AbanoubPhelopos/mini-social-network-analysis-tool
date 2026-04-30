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
    max_communities: int = 8,
    max_nodes: int = 50,
    sample_k: int = 20,
) -> CommunityResult:
    """Detect communities using a highly optimized approximate Girvan-Newman algorithm.

    Uses a subgraph of the highest-degree nodes, approximates edge betweenness
    by sampling BFS seed nodes (not all-pairs), and propagates labels to
    remaining nodes via neighbor majority vote.

    Args:
        G: NetworkX graph to analyze.
        max_communities: Target number of communities to find.
        max_nodes: Maximum number of nodes in the working subgraph.
        sample_k: Number of seed nodes for approximate betweenness per iteration.

    Returns:
        CommunityResult with partition labels, modularity, and timing.
    """
    start = time.perf_counter()

    undirected = to_simple_undirected(G)
    all_nodes = list(undirected.nodes())
    remaining_nodes: List[Any] = []

    if len(all_nodes) > max_nodes:
        sorted_by_degree = sorted(
            all_nodes, key=lambda n: undirected.degree(n), reverse=True
        )
        top_nodes = sorted_by_degree[:max_nodes]
        remaining_nodes = sorted_by_degree[max_nodes:]
        working_graph = undirected.subgraph(top_nodes).copy()
    else:
        working_graph = undirected.copy()

    node_list = list(working_graph.nodes())
    max_iterations = 500
    iteration = 0

    while working_graph.number_of_edges() > 0 and iteration < max_iterations:
        if _count_components(working_graph) >= max_communities:
            break

        k = min(sample_k, len(node_list))
        seeds = random.sample(node_list, k)

        betweenness = _compute_approx_betweenness(working_graph, seeds)

        if not betweenness:
            break

        sorted_edges = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        num_to_remove = max(1, len(sorted_edges) // 10)

        for edge, _ in sorted_edges[:num_to_remove]:
            if working_graph.has_edge(*edge):
                working_graph.remove_edge(*edge)
            if _count_components(working_graph) >= max_communities:
                break

        iteration += 1

    labels = _get_component_labels(working_graph)

    if remaining_nodes:
        labels = _assign_remaining_by_vote(labels, remaining_nodes, undirected)

    num_communities = len(set(labels.values()))
    community_sizes: Dict[int, int] = Counter(labels.values())

    all_labeled_nodes = list(labels.keys())
    subgraph_for_mod = undirected.subgraph(all_labeled_nodes)
    if subgraph_for_mod.number_of_edges() > 0:
        communities_sets: Dict[int, Set[Any]] = defaultdict(set)
        for node, comm in labels.items():
            communities_sets[comm].add(node)
        modularity = nx.community.modularity(
            subgraph_for_mod, communities_sets.values()
        )
    else:
        modularity = -1.0

    elapsed = time.perf_counter() - start

    return CommunityResult(
        algorithm="Girvan-Newman (Optimized)",
        labels=labels,
        num_communities=num_communities,
        modularity=modularity,
        execution_time=elapsed,
        community_sizes=dict(community_sizes),
    )
