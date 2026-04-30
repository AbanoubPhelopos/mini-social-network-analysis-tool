import csv
import tempfile
from typing import Dict


def export_metrics_csv(
    metrics: Dict[str, object], filename: str = "metrics.csv"
) -> str:
    """Write graph metrics to a CSV file and return the file path.

    Args:
        metrics: Dictionary of metric names to values.
        filename: Name of the output file.

    Returns:
        Absolute path to the written temporary CSV file.
    """
    tmp_dir = tempfile.gettempdir()
    path = f"{tmp_dir}\\{filename}"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, val in metrics.items():
            if isinstance(val, dict):
                for sub_key, sub_val in val.items():
                    writer.writerow([f"{key}.{sub_key}", sub_val])
            elif isinstance(val, list):
                writer.writerow([key, len(val)])
            else:
                writer.writerow([key, val])
    return path
