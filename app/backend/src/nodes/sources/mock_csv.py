from pathlib import Path
from typing import Any

import pandas as pd


def run(path: str) -> pd.DataFrame:
    file_path = Path(__file__).resolve().parent.parent / ".." / path
    return pd.read_csv(file_path, parse_dates=["ts"], index_col="ts")
