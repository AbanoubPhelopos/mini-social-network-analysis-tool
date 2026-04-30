import traceback
from typing import Optional

import pandas as pd

from ..constants import NODE_ID_ALIASES


def load_nodes_csv(uploaded_file) -> Optional[pd.DataFrame]:
    """Load and validate a nodes CSV file into a DataFrame.

    Detects the ID column from a list of common aliases, renames it to 'ID',
    strips a UTF-8 BOM, drops duplicate rows, and returns the cleaned
    DataFrame. Returns None on any failure.
    """
    try:
        raw = uploaded_file.read()
        if isinstance(raw, bytes):
            text = raw.decode("utf-8-sig")
        else:
            text = raw

        from io import StringIO

        df = pd.read_csv(StringIO(text))

        if df.empty:
            print("Nodes file is empty.")
            return None

        df.columns = [c.strip() for c in df.columns]

        id_col: Optional[str] = None
        for alias in NODE_ID_ALIASES:
            if alias in df.columns:
                id_col = alias
                break

        if id_col is None:
            print(
                f"No ID column found. Expected one of: {NODE_ID_ALIASES}. "
                f"Got columns: {list(df.columns)}"
            )
            return None

        df = df.rename(columns={id_col: "ID"})
        df["ID"] = df["ID"].astype(str).str.strip()
        df = df.drop_duplicates(subset=["ID"]).reset_index(drop=True)

        return df

    except Exception:
        traceback.print_exc()
        return None
