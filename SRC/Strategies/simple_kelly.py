import math
from .base import Strategy, BetDecision
from ..bankroll import kelly_stake

class SimpleKelly(Strategy):
    name = "SimpleKelly"
    def __init__(self, frac=0.5, p_col="implied_prob", min_edge=0.0):
        self.frac, self.p_col, self.min_edge = frac, p_col, min_edge

    def decide(self, row) -> BetDecision:
        p = float(row.get(self.p_col, float("nan")))
        if not (0 < p < 1): return BetDecision(0, False)
        # edge threshold vs fair (decimal odds)
        # expected value per $1: p*(b) - (1-p); require EV > min_edge
        from ..utils import payout_per_unit
        b = payout_per_unit(int(row["odds"]))
        ev = p*b - (1-p)
        if ev <= self.min_edge: return BetDecision(0, False)
        stake = kelly_stake(row["bankroll"], p, int(row["odds"]), self.frac)
        return BetDecision(stake, stake > 0)
