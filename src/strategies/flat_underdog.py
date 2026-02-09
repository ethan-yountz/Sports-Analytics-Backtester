from src.strategies.base import Strategy, BetDecision

class FlatUnderdog(Strategy):
    name = "FlatUnderdog"
    def __init__(self, unit=1.0, odds_col="odds"):
        self.unit = unit
        self.odds_col = odds_col

    def decide(self, row) -> BetDecision:
        odds = row.get(self.odds_col)
        try:
            odds = float(odds)
        except Exception:
            return BetDecision(0.0, False)
        return BetDecision(self.unit, True) if odds > 0 else BetDecision(0.0, False)



