import pandas as pd


def run(*args: pd.Series) -> pd.Series:
    result = pd.Series(True, index=args[0].index)
    for s in args:
        result &= s
    return result
