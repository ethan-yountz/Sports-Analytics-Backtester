import pandas as pd
import numpy as np
from pathlib import Path

def process_nhl_data(raw_data_path: str, output_path: str = None):
    
    df = pd.read_csv(raw_data_path)
    
    processed_records = []
    
    for _, row in df.iterrows():
        date = row['date']
        away_team = row['a__team']
        home_team = row['h__team']
        away_goals = row['a__goals_total']
        home_goals = row['h__goals_total']
        moneyline = row['moneyline']
        fav = row['fav']
        over_under_line = row['over_under']
        
        total_goals = away_goals + home_goals
        
        if fav == 'Home':
            home_ml_result = 1 if home_goals > away_goals else 0
            away_ml_result = 1 if away_goals > home_goals else 0
            home_ml_odds = moneyline
            away_ml_odds = abs(moneyline)
        else:
            home_ml_result = 1 if home_goals > away_goals else 0
            away_ml_result = 1 if away_goals > home_goals else 0
            home_ml_odds = abs(moneyline)
            away_ml_odds = moneyline
        
        ou_result = total_goals - over_under_line
        processed_records.append({
            'date': date,
            'selection': home_team,
            'odds': home_ml_odds,
            'result': home_ml_result,
            'ou_line': over_under_line,
            'ou_odds': -110,
            'ou_result': ou_result,
            'total_points': total_goals,
            'location': 'home'
        })
        
        processed_records.append({
            'date': date,
            'selection': away_team,
            'odds': away_ml_odds,
            'result': away_ml_result,
            'ou_line': over_under_line,
            'ou_odds': -110,
            'ou_result': ou_result,
            'total_points': total_goals,
            'location': 'away'
        })
    
    processed_df = pd.DataFrame(processed_records)
    processed_df['date'] = pd.to_datetime(processed_df['date'])
    processed_df = processed_df.sort_values('date').reset_index(drop=True)
    
    if output_path:
        processed_df.to_csv(output_path, index=False)
        print(f"Processed {len(processed_df)} NHL records and saved to {output_path}")
    else:
        print(f"Processed {len(processed_df)} NHL records")
    
    return processed_df

if __name__ == "__main__":
    raw_path = "data/Raw/NHL/sportsbook-nhl-2022-2023.csv"
    output_path = "data/Processed/nhl_2022_2023.csv"
    
    if Path(raw_path).exists():
        process_nhl_data(raw_path, output_path)
    else:
        print(f"Raw NHL data file not found: {raw_path}")


