import pandas as pd
from SRC.utils import payout_per_unit  # net profit per 1 unit from American odds

def _win_profit(stake: float, odds: int) -> float:
    return stake * payout_per_unit(int(odds))

def run_backtest(df: pd.DataFrame, strategy, start_bankroll: float = 1000.0):
    df_iter = df.sort_values("date").reset_index(drop=True)

    records = []
    bankroll = float(start_bankroll)

    for _, row in df_iter.iterrows():
        r = row.copy()
        r["bankroll"] = bankroll

        decision = strategy.decide(r)  
        if not getattr(decision, "take", False):
            continue  

        raw_stake = float(getattr(decision, "stake", 0.0))
        if raw_stake <= 0.0 or bankroll <= 0.0:
            continue
        stake = min(raw_stake, bankroll)

        try:
            odds = int(row["odds"])
            res  = int(row["result"])  # 1 = win, 0 = loss
        except Exception:
            continue  

        pnl = _win_profit(stake, odds) if res == 1 else -stake

        bankroll += pnl

        records.append({
            "date": row["date"],
            "selection": row.get("selection"),
            "odds": odds,
            "result": res,
            "stake": stake,
            "pnl": pnl,
            "bankroll_after": bankroll,
        })

    bets = pd.DataFrame.from_records(records)

    if bets.empty:
        equity = pd.Series([start_bankroll], name="equity")
        return bets, equity

    equity = bets["bankroll_after"].astype(float).reset_index(drop=True)
    equity.name = "equity"

    return bets, equity







