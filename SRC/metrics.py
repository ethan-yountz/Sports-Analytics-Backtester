import numpy as np
import pandas as pd

def roi(pnl: pd.Series, stake: pd.Series | None = None) -> float:
    total_staked = pd.to_numeric(stake, errors="coerce").fillna(0).sum()
    total_pnl = pd.to_numeric(pnl, errors="coerce").fillna(0).sum()
    return (total_pnl / total_staked) if total_staked > 0 else 0.0


def max_drawdown(equity: pd.Series) -> float:
    equity = pd.to_numeric(equity, errors="coerce")
    peaks = equity.cummax()
    dd = equity - peaks
    return float(dd.min()) if len(dd) else 0.0



def win_rate(results: pd.Series) -> float:
        return float(results.mean())


   

