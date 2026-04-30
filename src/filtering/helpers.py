from typing import Any

import networkx as nx


def get_attribute_values(G: nx.Graph, attribute: str) -> list[Any]:
    """Return a sorted list of unique values for the given node attribute."""
    values = {
        data.get(attribute) for _, data in G.nodes(data=True) if attribute in data
    }
    return sorted(values, key=lambda v: (v is None, v))


def get_available_attributes(G: nx.Graph) -> list[str]:
    """Return a sorted list of all attribute names present across every node."""
    attributes: set[str] = set()
    for _, data in G.nodes(data=True):
        attributes.update(data.keys())
    return sorted(attributes)
