from dataclasses import dataclass
from src.engine.bet_types import BetType, BetSide

@dataclass
class BetDecision:
    stake: float      # stake size in units
    take: bool        # whether to place the bet
    bet_type: BetType = BetType.MONEYLINE
    bet_side: BetSide = None  # side used for spread/OU bets

class Strategy:
    name = "BASE"
    bet_type = BetType.MONEYLINE
    
    def decide(self, row) -> BetDecision:
        raise NotImplementedError


