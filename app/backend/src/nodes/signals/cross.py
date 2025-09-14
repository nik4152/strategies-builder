import pandas as pd


def run(a: pd.Series, b: pd.Series, dir: str = "up") -> pd.Series:
    if dir == "up":
        cond = (a.shift(1) < b.shift(1)) & (a >= b)
    else:
        cond = (a.shift(1) > b.shift(1)) & (a <= b)
    return cond
