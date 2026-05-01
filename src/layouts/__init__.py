from .spring import spring_layout
from .fruchterman_reingold import fruchterman_reingold_layout
from .circular import circular_layout
from .shell import shell_layout
from .kamada_kawai import kamada_kawai_layout
from .spectral import spectral_layout
from .random import random_layout
from .hierarchical_tree import hierarchical_tree_layout
from .radial_tree import radial_tree_layout

LAYOUT_REGISTRY = {
    "Spring (Force-Directed)": spring_layout,
    "Fruchterman-Reingold": fruchterman_reingold_layout,
    "Circular": circular_layout,
    "Shell (Radial)": shell_layout,
    "Kamada-Kawai": kamada_kawai_layout,
    "Spectral": spectral_layout,
    "Random": random_layout,
    "Hierarchical Tree": hierarchical_tree_layout,
    "Radial Tree": radial_tree_layout,
}


def get_available_layouts():
    return list(LAYOUT_REGISTRY.keys())


def get_layout(G, name, **kwargs):
    undirected = G.to_undirected() if G.is_directed() else G
    func = LAYOUT_REGISTRY.get(name, spring_layout)
    positions = func(undirected, **kwargs)
    return positions
