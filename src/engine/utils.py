def american_to_decimal(odds: int) -> float:
    return 1 + (100/abs(odds)) if odds < 0 else 1 + (odds/100)

def payout_per_unit(odds: int) -> float:
    dec = american_to_decimal(odds)
    return dec - 1.0  # profit per unit staked

def kelly_fraction(p_win: float, odds_american: int) -> float:
    b = payout_per_unit(odds_american)
    return max(0.0, (b*p_win - (1-p_win))/b)



