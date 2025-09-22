import pandas as pd


def run(df: pd.DataFrame, zone_low: float = 0.382, zone_high: float = 0.618) -> pd.Series:
    low = df["low"].min()
    high = df["high"].max()
    level_low = low + (high - low) * zone_low
    level_high = low + (high - low) * zone_high
    return df["close"].between(level_low, level_high)
