import pandas as pd

REQUIRED = ["date","selection","odds","result"]

def load_games(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing: raise ValueError(f"Missing columns: {missing}")
    return df.sort_values("date").reset_index(drop=True)