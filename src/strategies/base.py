from dataclasses import dataclass
from src.engine.bet_types import BetType, BetSide

@dataclass
class BetDecision:
    stake: float      # units
    take: bool        # place bet or skip
    bet_type: BetType = BetType.MONEYLINE
    bet_side: BetSide = None  # For spread/OU bets

class Strategy:
    name = "BASE"
    bet_type = BetType.MONEYLINE
    
    def decide(self, row) -> BetDecision:
        raise NotImplementedError


