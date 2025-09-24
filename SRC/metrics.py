import numpy as np
import pandas as pd

def roi(pnl_series: pd.Series) -> float:
    invested = np.abs(pnl_series[pnl_series<0]).sum()
    return (pnl_series.sum() / invested) if invested > 0 else 0.0

def max_drawdown(equity: pd.Series) -> float:
    peaks = equity.cummax()
    dd = (equity - peaks) / peaks.replace(0,np.nan)
    return dd.min() if len(dd) else 0.0

def win_rate(results: pd.Series) -> float:
    wins = (results == "win").sum()
    total = results.isin(["win","loss"]).sum()
    return wins/total if total else 0.0
