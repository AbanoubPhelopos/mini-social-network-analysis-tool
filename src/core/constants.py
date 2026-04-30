GRAPH_COLORS: list[str] = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#393b79",
    "#637939",
    "#8c6d31",
    "#843c39",
    "#7b4173",
    "#5254a3",
    "#6b6ecf",
    "#9c9ede",
    "#a55194",
    "#ce6dbd",
    "#e7ba52",
    "#b5cf6b",
    "#74c476",
    "#31a354",
    "#e45756",
    "#4c78a8",
    "#f58518",
    "#72b7b2",
    "#54a24b",
    "#eeca3b",
]

LAYOUT_OPTIONS: dict[str, str] = {
    "Spring (Force-Directed)": "spring",
    "Fruchterman-Reingold": "fruchterman_reingold",
    "Circular": "circular",
    "Random": "random",
    "Shell (Concentric)": "shell",
    "Kamada-Kawai": "kamada_kawai",
    "Spectral": "spectral",
}

NODE_SHAPE_OPTIONS: list[str] = [
    "dot",
    "circle",
    "ellipse",
    "box",
    "square",
    "triangle",
    "diamond",
    "star",
    "hexagon",
    "icon",
]

NODE_ID_ALIASES: list[str] = [
    "id",
    "ID",
    "node",
    "Node",
    "name",
    "Name",
    "label",
    "Label",
]

SOURCE_ALIASES: list[str] = [
    "source",
    "Source",
    "src",
    "Src",
    "from",
    "From",
    "node1",
    "Node1",
]

CENTRALITY_METHODS: dict[str, str] = {
    "Degree Centrality": "degree",
    "Betweenness Centrality": "betweenness",
    "Closeness Centrality": "closeness",
    "Eigenvector Centrality": "eigenvector",
}

TARGET_ALIASES: list[str] = [
    "target",
    "Target",
    "tgt",
    "Tgt",
    "to",
    "To",
    "node2",
    "Node2",
    "destination",
    "Destination",
]
