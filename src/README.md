# Mini Social Networks Analysis Tool

An interactive desktop/web tool for network analysis and visualization built with Python, Streamlit, and NetworkX.

## Features

### 1. Data Loading
- Upload nodes and edges CSV files
- Automatic column detection (flexible naming conventions)
- Data preview before processing
- Support for directed and undirected graphs
- Handle missing values and duplicate edges

### 2. Interactive Visualization
- Interactive graph display with zoom, pan, and hover info
- Node hover shows all attributes and metrics
- Edge hover shows weight and attributes
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
- Map any attribute to node size
- Map any attribute to node color
- Map any attribute to node labels
- Choose node shapes (dot, circle, triangle, diamond, star, square)
- Toggle edge weight display

### 5. Graph Metrics & Statistics
- Number of nodes and edges
- Graph density
- Average degree
- Average clustering coefficient
- Transitivity
- Connected components analysis
- Degree distribution (histogram)
- Average shortest path length

### 6. Centrality Analysis
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- Eigenvector Centrality
- Top-N node rankings
- Centrality distribution plots

### 7. Filtering
- Filter by centrality range (3+ measures)
- Filter by community membership
- Filter by node attribute values
- Filter by degree range

### 8. Community Detection
- **Louvain Algorithm** - Fast modularity optimization
- **Girvan-Newman Algorithm** - Hierarchical edge betweenness
- **Label Propagation** - Fast heuristic approach
- Side-by-side algorithm comparison
- Community size visualization

### 9. Clustering Evaluation (3+ metrics)
- **Modularity** (Internal) - Community strength measure
- **Conductance** (Internal) - Cross-community edge fraction
- **NMI** (External) - Normalized Mutual Information
- **ARI** (External) - Adjusted Rand Index

### 10. Link Analysis
- **PageRank** scores and rankings
- **HITS** algorithm (Hubs & Authorities)
- **Shortest Path** finder between any two nodes
- Top influential nodes identification

### 11. Export
- Export metrics as CSV
- Export centrality results as CSV
- Export community assignments as CSV
- Export graph as GraphML
- Export graph visualization as PNG image

## Installation

```bash
cd task2
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
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
Optional weight column.

Example:
```
Source,Target,weight
1558,1567,3
1560,1570,1
```

## Project Structure

```
task2/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/                  # Sample CSV data files
│   ├── nodes.csv
│   └── edges.csv
├── utils/                 # Shared utilities
│   ├── __init__.py
│   ├── constants.py       # Color palettes, layout options, aliases
│   └── helpers.py         # Common helper functions
└── modules/               # Feature modules
    ├── __init__.py
    ├── loader.py           # CSV loading and validation
    ├── graph_builder.py    # NetworkX graph construction
    ├── layouts.py          # Layout algorithm computation
    ├── metrics.py          # Graph statistics and metrics
    ├── centrality.py       # Centrality measure computation
    ├── filtering.py        # Graph filtering operations
    ├── communities.py      # Community detection algorithms
    ├── clustering.py       # Graph clustering methods
    ├── evaluation.py       # Clustering evaluation metrics
    ├── link_analysis.py    # PageRank, HITS, shortest path
    ├── visualization.py    # Pyvis and Plotly visualization
    └── export.py           # Data and image export
```

## Tech Stack

- **Python 3.x**
- **Streamlit** - Web UI framework
- **NetworkX** - Graph analysis
- **Pandas** - Data handling
- **Plotly** - Charts and plots
- **Pyvis** - Interactive network visualization
- **python-louvain** - Louvain community detection
- **scikit-learn** - Evaluation metrics (NMI, ARI)
- **Matplotlib** - Static graph image export
