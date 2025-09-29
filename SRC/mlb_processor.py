import pandas as pd
import numpy as np
from pathlib import Path

def process_mlb_data(raw_data_path: str, output_path: str = None):
    
    df = pd.read_csv(raw_data_path, parse_dates=['date'])
    
    processed_records = []
    
    for _, row in df.iterrows():
        date = row['date']
        team = row['team']
        opponent = row['opponent']
        runs = row['runs']
        opp_runs = row['oppRuns']
        
        moneyline = row['moneyLine']
        opp_moneyline = row['oppMoneyLine']
        
        team_result = 1 if runs > opp_runs else 0
        opp_result = 1 if opp_runs > runs else 0
        
        ou_line = row['total']
        over_odds = row['overOdds']
        under_odds = row['underOdds']
        
        total_runs = runs + opp_runs
        ou_result = total_runs - ou_line
        processed_records.append({
            'date': date,
            'selection': team,
            'odds': moneyline,
            'result': team_result,
            'ou_line': ou_line,
            'ou_odds': over_odds,
            'ou_result': ou_result,
            'total_points': total_runs,
            'location': 'home' if team == row.get('team', '') else 'away'
        })
        processed_records.append({
            'date': date,
            'selection': opponent,
            'odds': opp_moneyline,
            'result': opp_result,
            'ou_line': ou_line,
            'ou_odds': under_odds,
            'ou_result': ou_result,
            'total_points': total_runs,
            'location': 'away' if opponent == row.get('opponent', '') else 'home'
        })
    
    processed_df = pd.DataFrame(processed_records)
    processed_df = processed_df.sort_values('date').reset_index(drop=True)
    
    if output_path:
        processed_df.to_csv(output_path, index=False)
        print(f"Processed {len(processed_df)} MLB records and saved to {output_path}")
    else:
        print(f"Processed {len(processed_df)} MLB records")
    
    return processed_df

if __name__ == "__main__":
    raw_path = "Data/Raw/MLB/oddsDataMLB.csv"
    output_path = "Data/Processed/mlb_dataset.csv"
    
    if Path(raw_path).exists():
        process_mlb_data(raw_path, output_path)
    else:
        print(f"Raw MLB data not found at {raw_path}")
