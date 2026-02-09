import pandas as pd
import numpy as np
from pathlib import Path

def process_vegas_data(raw_data_path: str, output_path: str = None):
    
    df = pd.read_csv(raw_data_path)
    
    processed_records = []
    
    for game_id, game_data in df.groupby('GameId'):
        if len(game_data) != 2:
            continue
            
        home_team = game_data[game_data['Location'] == 'home'].iloc[0]
        away_team = game_data[game_data['Location'] == 'away'].iloc[0]
        
        date = home_team['Date']
        home_selection = home_team['Team']
        away_selection = away_team['Team']
        
        home_ml_odds = home_team['Average_Line_ML']
        away_ml_odds = away_team['Average_Line_ML']
        home_ml_result = 1 if home_team['Result'] == 'W' else 0
        away_ml_result = 1 if away_team['Result'] == 'W' else 0
        
        
        ou_line = home_team['Average_Line_OU']
        home_ou_odds = home_team['Average_Odds_OU']
        away_ou_odds = away_team['Average_Odds_OU']
        
        total_points = home_team['Total']
        ou_result = total_points - ou_line
        
        processed_records.append({
            'date': date,
            'selection': home_selection,
            'odds': home_ml_odds,
            'result': home_ml_result,
            'ou_line': ou_line,
            'ou_odds': home_ou_odds,
            'ou_result': ou_result,
            'total_points': total_points,
            'location': 'home'
        })
        
        processed_records.append({
            'date': date,
            'selection': away_selection,
            'odds': away_ml_odds,
            'result': away_ml_result,
            'ou_line': ou_line,
            'ou_odds': away_ou_odds,
            'ou_result': ou_result,
            'total_points': total_points,
            'location': 'away'
        })
    
    processed_df = pd.DataFrame(processed_records)
    processed_df['date'] = pd.to_datetime(processed_df['date'])
    processed_df = processed_df.sort_values('date').reset_index(drop=True)
    
    if output_path:
        processed_df.to_csv(output_path, index=False)
        print(f"Processed {len(processed_df)} records and saved to {output_path}")
    else:
        print(f"Processed {len(processed_df)} records")
    
    return processed_df

if __name__ == "__main__":
    raw_path = "data/Raw/NBA/2012-13/vegas.txt"
    output_path = "data/Processed/games_with_spread_ou.csv"
    
    if Path(raw_path).exists():
        process_vegas_data(raw_path, output_path)
    else:
        print(f"Raw data file not found: {raw_path}")


