import pandas as pd
from SRC.utils import payout_per_unit  # net profit per 1 unit from American odds
from SRC.bet_types import BetType, BetSide

def _win_profit(stake: float, odds: int) -> float:
    return stake * payout_per_unit(int(odds))

def _determine_bet_result(row, decision):
    bet_type = decision.bet_type
    bet_side = decision.bet_side
    
    if bet_type == BetType.MONEYLINE:
        return int(row["result"])  # 1 = win, 0 = loss
    
    elif bet_type == BetType.OVER_UNDER:
        if "ou_result" not in row:
            return 0
        
        ou_result = row["ou_result"]
        if bet_side == BetSide.OVER:
            if ou_result > 0:
                return 1
            elif ou_result == 0:
                return 0.5
            else:
                return 0
        elif bet_side == BetSide.UNDER:
            if ou_result < 0:
                return 1
            elif ou_result == 0:
                return 0.5
            else:
                return 0
        else:
            return 0
    
    return 0

def _get_odds_for_bet_type(row, bet_type):
    if bet_type == BetType.MONEYLINE:
        return row.get("odds")
    elif bet_type == BetType.OVER_UNDER:
        return row.get("ou_odds")
    return row.get("odds")

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
            odds = int(_get_odds_for_bet_type(row, decision.bet_type))
            res = _determine_bet_result(row, decision)
        except Exception:
            continue  

        if res == 1:
            pnl = _win_profit(stake, odds)
        elif res == 0.5:
            pnl = 0
        else:
            pnl = -stake

        bankroll += pnl

        records.append({
            "date": row["date"],
            "selection": row.get("selection"),
            "odds": odds,
            "result": res,
            "stake": stake,
            "pnl": pnl,
            "bankroll_after": bankroll,
            "bet_type": decision.bet_type.value,
            "bet_side": decision.bet_side.value if decision.bet_side else None,
        })

    bets = pd.DataFrame.from_records(records)

    if bets.empty:
        equity = pd.Series([start_bankroll], name="equity")
        return bets, equity

    equity = bets["bankroll_after"].astype(float).reset_index(drop=True)
    equity.name = "equity"

    return bets, equity







