from SRC.utils import kelly_fraction

def flat_stake(bankroll: float, unit: float=1.0) -> float:
    return min(unit, bankroll)

def kelly_stake(bankroll: float, p_win: float, odds: int, frac: float=1.0) -> float:
    f = kelly_fraction(p_win, odds) * frac
    return max(0.0, bankroll * f)
