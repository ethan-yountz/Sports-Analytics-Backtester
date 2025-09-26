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
    if pd.api.types.is_bool_dtype(results):
        return float(results.mean())

    if pd.api.types.is_numeric_dtype(results):
        s = pd.to_numeric(results, errors="coerce").dropna()
        s = s[(s == 0) | (s == 1)]
        return float((s == 1).mean()) if len(s) else 0.0

    r = results.astype(str).str.strip().str.upper()
    valid = r.isin(["W", "WIN", "L", "LOSS", "TRUE", "FALSE", "1", "0"])
    r = r[valid]
    if r.empty:
        return 0.0
    wins = r.isin(["W", "WIN", "TRUE", "1"]).sum()
    return float(wins / len(r))

