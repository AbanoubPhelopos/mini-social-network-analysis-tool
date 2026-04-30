import traceback
from typing import Optional

import pandas as pd

from ..constants import SOURCE_ALIASES, TARGET_ALIASES


def load_edges_csv(uploaded_file, aggregate: bool = True) -> Optional[pd.DataFrame]:
    """Load and validate an edges CSV file into a DataFrame.

    Detects the Source and Target columns from lists of common aliases,
    renames them to 'Source' and 'Target', strips a UTF-8 BOM.

    If aggregate=True (default), duplicate edges are merged and counted
    into a 'Weight' column. If aggregate=False, all raw rows are kept
    with weight=1 for each.

    Returns None on any failure.
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
            print("Edges file is empty.")
            return None

        df.columns = [c.strip() for c in df.columns]

        source_col: Optional[str] = None
        for alias in SOURCE_ALIASES:
            if alias in df.columns:
                source_col = alias
                break

        target_col: Optional[str] = None
        for alias in TARGET_ALIASES:
            if alias in df.columns:
                target_col = alias
                break

        if source_col is None:
            print(
                f"No Source column found. Expected one of: {SOURCE_ALIASES}. "
                f"Got columns: {list(df.columns)}"
            )
            return None

        if target_col is None:
            print(
                f"No Target column found. Expected one of: {TARGET_ALIASES}. "
                f"Got columns: {list(df.columns)}"
            )
            return None

        df = df.rename(columns={source_col: "Source", target_col: "Target"})
        df["Source"] = df["Source"].astype(str).str.strip()
        df["Target"] = df["Target"].astype(str).str.strip()

        if aggregate:
            df = df.groupby(["Source", "Target"]).size().reset_index(name="Weight")
        else:
            df["Weight"] = 1

        return df

    except Exception:
        traceback.print_exc()
        return None
