from dataclasses import dataclass

@dataclass
class BetDecision:
    stake: float      # units
    take: bool        # place bet or skip

class Strategy:
    name = "BASE"
    def decide(self, row) -> BetDecision:
        raise NotImplementedError
