import pandas as pd


def run(df: pd.DataFrame, signal: pd.Series) -> dict[str, float]:
    returns = df["close"].pct_change().fillna(0)
    equity = (1 + returns * signal.shift(1).fillna(0)).cumprod()
    cagr = equity.iloc[-1] - 1
    return {"CAGR": float(cagr)}
