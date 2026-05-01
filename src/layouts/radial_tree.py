from typing import Any, Dict, Tuple
import math

import networkx as nx


def radial_tree_layout(
    G: nx.Graph, **kwargs
) -> Dict[Any, Tuple[float, float]]:
    """Compute node positions using radial tree layout.
    
    This layout arranges nodes in concentric circles around a root node,
    with each level of the tree on its own circle. Works best for 
    hierarchical or tree-like graphs.
    """
    pos = {}
    
    # Handle disconnected graphs by processing each component separately
    components = list(nx.connected_components(G))
    
    for component_idx, component in enumerate(components):
        subgraph = G.subgraph(component)
        
        # Try to find a root node
        if nx.is_tree(subgraph):
            # For trees, use center node as root
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
        
        # Position nodes radially by level
        radius_increment = kwargs.get('radius_increment', 2.0)
        min_radius = kwargs.get('min_radius', 0.5)  # Root node radius
        
        for level, nodes in levels.items():
            radius = min_radius + level * radius_increment
            
            if level == 0:
                # Root node at center
                pos[nodes[0]] = (0, 0)
            else:
                # Distribute nodes evenly around the circle
                num_nodes = len(nodes)
                angle_step = 2 * math.pi / num_nodes
                
                # Start angle offset for better visualization
                start_angle = kwargs.get('start_angle', -math.pi / 2)
                
                for i, node in enumerate(nodes):
                    angle = start_angle + i * angle_step
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    pos[node] = (x, y)
    
    return pos
