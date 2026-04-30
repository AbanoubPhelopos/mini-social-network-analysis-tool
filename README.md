# Mini Social Networks Analysis Tool

An interactive web tool for network analysis and visualization built with Python, Streamlit, and NetworkX.

## Features

### 1. Data Loading
- Load from `data/` folder (auto-detect CSV files) or upload via browser
- Automatic column detection (flexible naming conventions)
- Support for directed and undirected graphs
- UTF-8 BOM handling and duplicate edge aggregation

### 2. Interactive Visualization
- Interactive graph display with zoom, pan, and hover info
- 7 layout algorithms applied to the visualization
- Node hover shows attributes; edge hover shows weight
- Toggle labels, edge weights, and physics simulation
- Powered by Pyvis for rich interactivity

### 3. Layout Algorithms
- Spring (Force-Directed)
- Fruchterman-Reingold
- Circular
- Shell (Radial)
- Kamada-Kawai
- Spectral
- Random

### 4. Node & Edge Attributes
- Map any node attribute to size, color, or labels
- Choose from 10 node shapes (dot, circle, ellipse, box, square, triangle, diamond, star, hexagon, icon)
- Toggle edge weight display on hover
- Edge color by attribute

### 5. Graph Metrics & Statistics
- Number of nodes and edges
- Graph density, average degree
- Average clustering coefficient, transitivity
- Connected components analysis
- Degree distribution (histogram)
- Average shortest path length

### 6. Centrality Analysis
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- Eigenvector Centrality
- Top-N node rankings and distribution plots

### 7. Filtering
- Filter by centrality range (4 measures)
- Filter by community membership
- Filter by node attribute values
- Filter by degree range

### 8. Community Detection
- **Louvain Algorithm** - Fast modularity optimization
- **Girvan-Newman Algorithm** - Optimized with subgraph sampling and BFS approximation
- **Label Propagation** - Fast heuristic approach
- Side-by-side algorithm comparison table with modularity, time, and community sizes

### 9. Clustering Evaluation (4 metrics)
- **Modularity** (Internal) - Community strength measure
- **Conductance** (Internal) - Cross-community edge fraction
- **NMI** (External) - Normalized Mutual Information vs ground truth
- **ARI** (External) - Adjusted Rand Index vs ground truth

### 10. Link Analysis
- **PageRank** scores and rankings
- **HITS** algorithm (Hubs & Authorities)
- **Shortest Path** finder between any two nodes
- Top influential nodes identification (4 methods)

### 11. Export
- Export metrics as CSV
- Export centrality results as CSV
- Export community assignments as CSV
- Export graph as GraphML

## Installation

```bash
cd src
pip install -r requirements.txt
```

## Running

```bash
cd src
streamlit run app.py --server.port 8501 --server.headless true
```

The app will open in your browser at `http://localhost:8501`.

## Data Format

### Nodes CSV
Must contain an ID column (named: `id`, `ID`, `node`, `Node`, `name`, `Name`, `label`, `Label`).
Any additional columns are treated as node attributes.

Example:
```
ID,Class,Gender
1426,5B,M
1427,5B,F
```

### Edges CSV
Must contain Source and Target columns (named: `source`, `Source`, `src`, etc.).
Duplicate edges are aggregated into weighted counts.

Example:
```
Source,Target
1558,1567
1558,1567
1560,1570
```

## Project Structure

```
src/
├── app.py                              # Main Streamlit entry point
├── requirements.txt                    # Python dependencies
├── .streamlit/config.toml              # Streamlit configuration
├── data/                               # Sample CSV data files
│   ├── nodes.csv
│   └── edges.csv
│
├── core/                               # Core data layer
│   ├── constants.py                    # Colors, layout options, column aliases
│   ├── loader/
│   │   ├── nodes_loader.py             # Nodes CSV loading + validation
│   │   └── edges_loader.py             # Edges CSV loading + aggregation
│   └── graph_builder/
│       └── builder.py                  # NetworkX graph construction
│
├── layouts/                            # Layout algorithms (one file each)
│   ├── spring.py
│   ├── fruchterman_reingold.py
│   ├── circular.py
│   ├── shell.py
│   ├── kamada_kawai.py
│   ├── spectral.py
│   └── random.py
│
├── metrics/                            # Graph statistics
│   ├── basic_metrics.py
│   ├── degree_distribution.py
│   ├── clustering_coefficient.py
│   ├── path_length.py
│   └── connected_components.py
│
├── centrality/                         # Centrality measures (one folder each)
│   ├── degree/
│   ├── betweenness/
│   ├── closeness/
│   └── eigenvector/
│
├── filtering/                          # Graph filtering
│   ├── centrality_filter.py
│   ├── community_filter.py
│   ├── attribute_filter.py
│   ├── degree_filter.py
│   └── helpers.py
│
├── communities/                        # Community detection
│   ├── base.py                         # CommunityResult dataclass
│   ├── comparison.py                   # Side-by-side comparison
│   ├── louvain/
│   ├── girvan_newman/                  # Optimized with subgraph sampling
│   └── label_propagation/
│
├── evaluation/                         # Clustering evaluation metrics
│   ├── modularity/
│   ├── conductance/
│   ├── nmi/
│   └── ari/
│
├── link_analysis/                      # Link analysis algorithms
│   ├── pagerank/
│   ├── hits/
│   └── shortest_path/
│
├── visualization/                      # Rendering
│   ├── pyvis_viz.py                    # Interactive Pyvis network
│   └── plotly_viz.py                   # Plotly static charts
│
├── export/                             # Data export
│   ├── metrics_export.py
│   ├── centrality_export.py
│   ├── graph_export.py
│   └── image_export.py
│
└── ui/                                 # Streamlit UI layer
    ├── sidebar.py                      # Sidebar: loading, viz controls, filters
    └── tabs/
        ├── visualization_tab.py
        ├── metrics_tab.py
        ├── centrality_tab.py
        ├── community_tab.py
        ├── evaluation_tab.py
        ├── link_analysis_tab.py
        └── export_tab.py
```

## Tech Stack

- **Python 3.12**
- **Streamlit** - Web UI framework
- **NetworkX** - Graph analysis
- **Pandas** - Data handling
- **Plotly** - Charts and plots
- **Pyvis** - Interactive network visualization
- **python-louvain** - Louvain community detection
- **scikit-learn** - Evaluation metrics (NMI, ARI)
- **NumPy** - Numerical operations
