from typing import Any

import networkx as nx
import pandas as pd


def build_graph(
    nodes_df: pd.DataFrame,
    edges_df: pd.DataFrame,
    directed: bool = False,
) -> nx.Graph:
    """Build a NetworkX graph from nodes and edges DataFrames.

    Adds all node attributes from the nodes DataFrame and creates edges
    with aggregated weights from the edges DataFrame.
    """
    G = nx.DiGraph() if directed else nx.Graph()

    for _, row in nodes_df.iterrows():
        node_id = str(row["ID"])
        attrs: dict[str, Any] = {
            col: row[col] for col in nodes_df.columns if col != "ID"
        }
        G.add_node(node_id, **attrs)

    for _, row in edges_df.iterrows():
        source = str(row["Source"])
        target = str(row["Target"])
        weight = int(row.get("Weight", 1))

        if G.has_edge(source, target):
            G[source][target]["weight"] += weight
        else:
            G.add_edge(source, target, weight=weight)

    return G


def get_graph_info(G: nx.Graph) -> dict[str, Any]:
    """Return summary metadata about a NetworkX graph."""
    edge_attrs: set[str] = set()
    for _u, _v, data in G.edges(data=True):
        edge_attrs.update(data.keys())

    node_attrs: set[str] = set()
    for _n, data in G.nodes(data=True):
        node_attrs.update(data.keys())

    is_weighted = any(data.get("weight", 0) != 1 for _u, _v, data in G.edges(data=True))

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "is_directed": G.is_directed(),
        "is_weighted": is_weighted,
        "node_attributes": sorted(node_attrs),
        "edge_attributes": sorted(edge_attrs),
    }
