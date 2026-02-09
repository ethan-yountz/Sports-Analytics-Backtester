from src.strategies.base import Strategy, BetDecision
from src.engine.bet_types import BetType, BetSide

class CustomTotalOver(Strategy):
    name = "CustomTotalOver"
    bet_type = BetType.OVER_UNDER
    
    def __init__(self, unit=1.0, threshold=200.0):
        self.unit = unit
        self.threshold = threshold

    def decide(self, row) -> BetDecision:
        if "ou_odds" not in row or "ou_line" not in row:
            return BetDecision(0.0, False)
        
        try:
            ou_odds = float(row["ou_odds"])
            ou_line = float(row["ou_line"])
        except Exception:
            return BetDecision(0.0, False)
        
        if ou_line > self.threshold:
            return BetDecision(self.unit, True, bet_type=BetType.OVER_UNDER, bet_side=BetSide.OVER)
        
        return BetDecision(0.0, False)

class CustomTotalUnder(Strategy):
    name = "CustomTotalUnder"
    bet_type = BetType.OVER_UNDER
    
    def __init__(self, unit=1.0, threshold=200.0):
        self.unit = unit
        self.threshold = threshold

    def decide(self, row) -> BetDecision:
        if "ou_odds" not in row or "ou_line" not in row:
            return BetDecision(0.0, False)
        
        try:
            ou_odds = float(row["ou_odds"])
            ou_line = float(row["ou_line"])
        except Exception:
            return BetDecision(0.0, False)
        
        if ou_line < self.threshold:
            return BetDecision(self.unit, True, bet_type=BetType.OVER_UNDER, bet_side=BetSide.UNDER)
        
        return BetDecision(0.0, False)


