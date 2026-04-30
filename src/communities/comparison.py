from typing import Any, Dict, List

import networkx as nx
import pandas as pd

from .base import CommunityResult


def compare_algorithms(results: List[CommunityResult]) -> pd.DataFrame:
    """Compare multiple community detection results in a side-by-side table.

    Args:
        results: List of CommunityResult objects to compare.

    Returns:
        DataFrame with one row per algorithm showing key metrics.
    """
    rows = []
    for result in results:
        sizes = result.get_community_sizes_list()
        rows.append(
            {
                "Algorithm": result.algorithm,
                "Communities": result.num_communities,
                "Modularity": round(result.modularity, 4),
                "Time (s)": round(result.execution_time, 4),
                "Largest Community": sizes[0] if sizes else 0,
                "Smallest Community": sizes[-1] if sizes else 0,
                "Avg Community Size": (
                    round(sum(sizes) / len(sizes), 2) if sizes else 0
                ),
            }
        )
    return pd.DataFrame(rows)


def community_result_to_dataframe(result: CommunityResult, G: nx.Graph) -> pd.DataFrame:
    """Convert a CommunityResult to a DataFrame with node-level details.

    Args:
        result: CommunityResult to convert.
        G: The original graph (used for degree information).

    Returns:
        DataFrame with columns: node, community, degree.
    """
    rows = []
    for node, comm_id in result.labels.items():
        rows.append(
            {
                "node": node,
                "community": comm_id,
                "degree": G.degree(node) if node in G else 0,
            }
        )
    return pd.DataFrame(rows)
