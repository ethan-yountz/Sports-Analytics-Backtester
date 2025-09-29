from SRC.Strategies.base import Strategy, BetDecision
from SRC.bet_types import BetType, BetSide

class FlatOver(Strategy):
    name = "FlatOver"
    bet_type = BetType.OVER_UNDER
    
    def __init__(self, unit=1.0):
        self.unit = unit

    def decide(self, row) -> BetDecision:
        # Check if we have over/under data
        if "ou_odds" not in row or "ou_line" not in row:
            return BetDecision(0.0, False)
        
        try:
            ou_odds = float(row["ou_odds"])
            ou_line = float(row["ou_line"])
        except Exception:
            return BetDecision(0.0, False)
        
        # Always bet over
        return BetDecision(self.unit, True, BetType.OVER_UNDER, BetSide.OVER)

class FlatUnder(Strategy):
    name = "FlatUnder"
    bet_type = BetType.OVER_UNDER
    
    def __init__(self, unit=1.0):
        self.unit = unit

    def decide(self, row) -> BetDecision:
        # Check if we have over/under data
        if "ou_odds" not in row or "ou_line" not in row:
            return BetDecision(0.0, False)
        
        try:
            ou_odds = float(row["ou_odds"])
            ou_line = float(row["ou_line"])
        except Exception:
            return BetDecision(0.0, False)
        
        # Always bet under
        return BetDecision(self.unit, True, BetType.OVER_UNDER, BetSide.UNDER)

class LowTotalUnder(Strategy):
    name = "LowTotalUnder"
    bet_type = BetType.OVER_UNDER
    
    def __init__(self, unit=1.0, threshold=200.0):
        self.unit = unit
        self.threshold = threshold

    def decide(self, row) -> BetDecision:
        # Check if we have over/under data
        if "ou_odds" not in row or "ou_line" not in row:
            return BetDecision(0.0, False)
        
        try:
            ou_odds = float(row["ou_odds"])
            ou_line = float(row["ou_line"])
        except Exception:
            return BetDecision(0.0, False)
        
        # Only bet under when total is below threshold
        if ou_line < self.threshold:
            return BetDecision(self.unit, True, BetType.OVER_UNDER, BetSide.UNDER)
        
        return BetDecision(0.0, False)
