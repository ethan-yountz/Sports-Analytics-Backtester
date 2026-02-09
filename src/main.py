import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse

from src.data.data_loader import load_games
from src.strategies.flat_underdog import FlatUnderdog
from src.strategies.flat_favorite import FlatFavorite
from src.strategies.base import Strategy
from src.engine.backtester import run_backtest
from src.engine.metrics import roi, max_drawdown, win_rate
from src.engine.plotting import plot_equity

def resource_path(rel: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    if not hasattr(sys, "_MEIPASS"):
        base = Path(__file__).resolve().parent.parent
    return (base / rel).resolve()

def main():
    ap = argparse.ArgumentParser(description="backtest info")

    ap.add_argument("--data", default=resource_path("data/Processed/games_clean.csv"),
                    help="Path to CSV (default:data/Processed/games_clean.csv)")
    ap.add_argument("--start", type=float, default=100.0,
                    help="Starting bankroll (default: 100)")
    ap.add_argument("--unit", type=float, default=1.0,
                    help="Flat stake size per bet (default: 1.0)")
    ap.add_argument("--strat", type=Strategy, default=FlatUnderdog,
                    help="Selected Strategy (Default: FlatUnderdog)")
    ap.add_argument("--no_plot", action="store_true",
                    help="Disable equity plot")

    args = ap.parse_args()

    df = load_games(str(args.data))

    strat = args.strat(unit=args.unit)

    bets, equity = run_backtest(df, strat, start_bankroll=args.start)

    print(f"Strategy: {args.strat.name}")
    print(f"Data: {args.data}")
    print(f"Total bets: {len(bets)}")
    print(f"Final bankroll: {equity.iloc[-1]:.2f}")
    print(f"ROI: {roi(bets['pnl'], bets['stake']) * 100:.2f}%")
    print(f"Win rate: {win_rate(bets['result']):.3f}")
    print(f"Max drawdown: {max_drawdown(equity):.3f}")

if __name__ == "__main__":
    main()




