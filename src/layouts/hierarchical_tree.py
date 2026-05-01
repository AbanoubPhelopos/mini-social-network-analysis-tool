from typing import Any, Dict, Tuple
import math

import networkx as nx


def hierarchical_tree_layout(
    G: nx.Graph, **kwargs
) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using hierarchical tree layout.
    
    This layout arranges nodes in a tree structure with levels,
    where parent nodes are positioned above their children.
    Works best for hierarchical or tree-like graphs.
    """
    pos = {}
    
    # Handle disconnected graphs by processing each component separately
    components = list(nx.connected_components(G))
    
    x_offset = 0
    for component_idx, component in enumerate(components):
        subgraph = G.subgraph(component)
        
        # Try to find a root node (node with highest degree or first node)
        if nx.is_tree(subgraph):
            # For trees, find a node that could be root (center or highest degree)
            center_nodes = nx.center(subgraph)
            root = center_nodes[0] if center_nodes else list(subgraph.nodes())[0]
        else:
            # For general graphs, use node with highest degree as root
            degrees = dict(subgraph.degree())
            root = max(degrees, key=degrees.get) if degrees else list(subgraph.nodes())[0]
        
        # Build hierarchy using BFS from root
        levels = {}
        visited = set()
        queue = [(root, 0)]
        
        while queue:
            node, level = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
            
            for neighbor in subgraph.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))
        
        # Position nodes by level
        level_height = kwargs.get('level_height', 2.0)
        node_spacing = kwargs.get('node_spacing', 1.5)
        
        max_nodes_per_level = max(len(nodes) for nodes in levels.values()) if levels else 1
        
        for level, nodes in levels.items():
            y = -level * level_height  # Negative to place root at top
            
            # Distribute nodes horizontally within the level
            level_width = len(nodes) * node_spacing
            start_x = -level_width / 2
            
            for i, node in enumerate(nodes):
                x = start_x + i * node_spacing + node_spacing / 2
                pos[node] = (x + x_offset, y)
        
        # Add spacing between components
        if component_idx < len(components) - 1:
            max_width = max(
                len(nodes) * node_spacing for nodes in levels.values()
            ) if levels else node_spacing
            x_offset += max_width + 3.0
    
    return pos
