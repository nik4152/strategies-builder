import pandas as pd


def run(df: pd.DataFrame, period: int = 20, mult: float = 1.2) -> dict[str, pd.Series]:
    sma = df["volume"].rolling(window=period).mean()
    above = df["volume"] > sma * mult
    return {"vol_ma": sma, "above": above}
