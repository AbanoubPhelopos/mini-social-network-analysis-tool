from .metrics_export import export_metrics_csv
from .graph_export import export_graph_graphml
from .image_export import export_graph_image
from .centrality_export import export_centrality_csv, export_community_csv


def get_download_data(filepath: str) -> bytes:
    with open(filepath, "rb") as f:
        return f.read()
