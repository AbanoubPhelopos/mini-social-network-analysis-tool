import tempfile

import pandas as pd


def export_centrality_csv(df: pd.DataFrame, filename: str = "centrality.csv") -> str:
    """Write a centrality DataFrame to a CSV file.

    Args:
        df: DataFrame containing centrality measures per node.
        filename: Name of the output file.

    Returns:
        Absolute path to the written CSV file.
    """
    tmp_dir = tempfile.gettempdir()
    path = f"{tmp_dir}\\{filename}"
    df.to_csv(path, index=True)
    return path


def export_community_csv(df: pd.DataFrame, filename: str = "communities.csv") -> str:
    """Write a community assignment DataFrame to a CSV file.

    Args:
        df: DataFrame containing community assignments per node.
        filename: Name of the output file.

    Returns:
        Absolute path to the written CSV file.
    """
    tmp_dir = tempfile.gettempdir()
    path = f"{tmp_dir}\\{filename}"
    df.to_csv(path, index=True)
    return path
