import streamlit as st
import pandas as pd
from SRC.backtester import run_backtest
from SRC.Strategies.flat_underdog import FlatUnderdog
from SRC.Strategies.flat_favorite import FlatFavorite
from SRC.Strategies.flat_over_under import FlatOver, FlatUnder, LowTotalUnder
from SRC.Strategies.custom_total import CustomTotalOver, CustomTotalUnder
from SRC.data_loader import load_games
from SRC.data_processor import process_vegas_data
from SRC.nhl_processor import process_nhl_data
from SRC.mlb_processor import process_mlb_data
from SRC.metrics import roi, win_rate, max_drawdown
import altair as alt
from pathlib import Path

st.markdown("<h1>Sports Analytics Backtester</h1>", unsafe_allow_html=True)

st.markdown("<h2>Multi-League Backtesting Platform</h2>", unsafe_allow_html=True)
st.markdown("**NBA (2012-2019) • NHL (2022-2023) • MLB (2012-2023)**")

bankroll = st.number_input("Starting Bankroll", value = 100, min_value=1, step = 10, key= "bankroll")
unit = st.number_input("Unit Size", value = 1.0, min_value= 0.01, step = 0.1, key= "Unit")

finalstrat = None
strat = st.selectbox("Select Strategy", [
    "",
    "Flat Bet Favorite", 
    "Flat Bet Underdog",
    "Always Over",
    "Always Under",
    "Custom Total Over/Under"
])

if strat == "Flat Bet Favorite":
    finalstrat = FlatFavorite(unit)
elif strat == "Flat Bet Underdog":
    finalstrat = FlatUnderdog(unit)
elif strat == "Always Over":
    finalstrat = FlatOver(unit)
elif strat == "Always Under":
    finalstrat = FlatUnder(unit)
elif strat == "Custom Total Over/Under":
    col1, col2 = st.columns([1, 1])
    with col1:
        custom_total = st.number_input("Total Line", min_value=1.0, max_value=None, value=6.0, step=0.5, key="custom_total")
    with col2:
        bet_choice = st.radio("Bet Selection", ["Select Option", "Bet Over", "Bet Under"], key="bet_choice")
    
    if bet_choice == "Bet Over":
        finalstrat = CustomTotalOver(unit, custom_total)
        st.success(f"Selected: Bet OVER on totals > {custom_total}")
    elif bet_choice == "Bet Under":
        finalstrat = CustomTotalUnder(unit, custom_total)
        st.success(f"Selected: Bet UNDER on totals < {custom_total}")
    else:
        st.info("Please select Over or Under to proceed")

Df = None
Data = st.selectbox("Select Data Set", ["", "NBA Dataset (2012-2019)", "NHL Dataset (2022-2023)", "MLB Dataset (2012-2023)"])

if Data == "NBA Dataset (2012-2019)":
    # Check if comprehensive processed data exists, if not create it
    processed_path = "Data/Processed/nba_complete_dataset.csv"
    
    if not Path(processed_path).exists():
        with st.spinner("Processing complete NBA dataset with moneyline, spread, and over/under..."):
            # Process all NBA seasons
            all_seasons_data = []
            seasons = ["2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19"]
            
            for season in seasons:
                raw_path = f"Data/Raw/NBA/{season}/vegas.txt"
                if Path(raw_path).exists():
                    try:
                        season_df = process_vegas_data(raw_path, f"Data/Processed/temp_{season}.csv")
                        all_seasons_data.append(season_df)
                        st.write(f"Processed {season}: {len(season_df)} games")
                    except Exception as e:
                        st.write(f"Error processing {season}: {e}")
            
            if all_seasons_data:
                # Combine all seasons
                combined_df = pd.concat(all_seasons_data, ignore_index=True)
                combined_df = combined_df.sort_values('date').reset_index(drop=True)
                
                # Save combined dataset
                combined_df.to_csv(processed_path, index=False)
                actual_games = len(combined_df) // 2
                st.success(f"Created complete dataset with {len(combined_df)} betting records ({actual_games} games) from {len(all_seasons_data)} seasons")
                
                # Clean up temp files
                for season in seasons:
                    temp_path = f"Data/Processed/temp_{season}.csv"
                    if Path(temp_path).exists():
                        Path(temp_path).unlink()
            else:
                st.error("No NBA data found to process")
                st.info("Falling back to existing moneyline data")
                if Path("Data/Processed/games_clean.csv").exists():
                    Df = load_games("Data/Processed/games_clean.csv")
                else:
                    st.error("No data available")
    
    # Load the complete dataset
    if Path(processed_path).exists():
        Df = load_games(processed_path)
        actual_games = len(Df) // 2
        st.success(f"Loaded complete NBA dataset: {len(Df)} betting records ({actual_games} games)")
        
elif Data == "NHL Dataset (2022-2023)":
    # Check if NHL processed data exists, if not create it
    nhl_processed_path = "Data/Processed/nhl_2022_2023.csv"
    nhl_raw_path = "Data/Raw/NHL/sportsbook-nhl-2022-2023.csv"
    
    if not Path(nhl_processed_path).exists():
        if Path(nhl_raw_path).exists():
            with st.spinner("Processing NHL dataset..."):
                try:
                    nhl_df = process_nhl_data(nhl_raw_path, nhl_processed_path)
                    st.success(f"Created NHL dataset with {len(nhl_df)} betting records ({len(nhl_df)//2} games)")
                except Exception as e:
                    st.error(f"Error processing NHL data: {e}")
                    st.info("Falling back to existing data if available")
        else:
            st.error(f"NHL raw data not found at {nhl_raw_path}")
    
    # Load the NHL dataset
    if Path(nhl_processed_path).exists():
        Df = load_games(nhl_processed_path)
        actual_games = len(Df) // 2
        st.success(f"Loaded NHL dataset: {len(Df)} betting records ({actual_games} games)")
    else:
        st.error("Could not create NHL dataset")

elif Data == "MLB Dataset (2012-2023)":
    # Check if MLB processed data exists, if not create it
    mlb_processed_path = "Data/Processed/mlb_dataset.csv"
    mlb_raw_path = "Data/Raw/MLB/oddsDataMLB.csv"

    if not Path(mlb_processed_path).exists():
        if Path(mlb_raw_path).exists():
            with st.spinner("Processing MLB dataset..."):
                try:
                    mlb_df = process_mlb_data(mlb_raw_path, mlb_processed_path)
                    st.success(f"Created MLB dataset with {len(mlb_df)} betting records ({len(mlb_df)//2} games)")
                except Exception as e:
                    st.error(f"Error processing MLB data: {e}")
                    st.info("Falling back to existing data if available")
        else:
            st.error(f"MLB raw data not found at {mlb_raw_path}")
            st.info("Please download the MLB dataset from Kaggle and place it in Data/Raw/MLB/")

    # Load the MLB dataset
    if Path(mlb_processed_path).exists():
        Df = load_games(mlb_processed_path)
        actual_games = len(Df) // 2
        st.success(f"Loaded MLB dataset: {len(Df)} betting records ({actual_games} games)")
    else:
        st.error("Could not create MLB dataset")


run = st.button('Run Simulation')

if run and Df is None:
    st.error("Please select a dataset first")
elif run and finalstrat is None:
    st.error("Please select a strategy and configure it properly")
elif run and Df is not None and finalstrat is not None:
    with st.spinner("Running backtest…"):
        bets, equity = run_backtest(Df, finalstrat, bankroll)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.write(f"Total bets: {len(bets)}")
        st.write(f"Ending Bankroll: ${equity.iloc[-1]:.2f}")
        
        if len(bets) > 0:
            st.write(f"ROI: {roi(bets['pnl'], bets['stake']) * 100:.2f}%")
            st.write(f"Win rate: {win_rate(bets['result']) * 100:.2f}%")
            st.write(f"Max drawdown: {max_drawdown(equity):.3f}")
            
            # Show additional info for over/under strategies
            if strat in ["Always Over", "Always Under", "Custom Total Over/Under"] and 'ou_line' in bets.columns:
                avg_total = bets['ou_line'].mean() if 'ou_line' in bets.columns else "N/A"
                st.write(f"Average total line: {avg_total:.1f}")
        else:
            st.write("ROI: N/A (no bets placed)")
            st.write("Win rate: N/A (no bets placed)")
            st.write("Max drawdown: N/A (no bets placed)")

    eq_df = equity.reset_index(drop=True).to_frame(name="bankroll")
    eq_df["bet"] = eq_df.index + 1 

    equity_line = (
        alt.Chart(eq_df)
        .mark_line()
        .encode(
            x=alt.X("bet:Q", title="Bet #"),
            y=alt.Y("bankroll:Q",
                    title="Bankroll",
                    axis=alt.Axis(format="$,.2f")),
            tooltip=[
                alt.Tooltip("bet:Q", title="Bet #"),
                alt.Tooltip("bankroll:Q", title="Bankroll", format="$,.2f"),
            ],
        )
        .properties(height=260)
    )

    start_rule = (
        alt.Chart(pd.DataFrame({"y": [float(bankroll)]}))
        .mark_rule(strokeDash=[4, 4])
        .encode(y="y:Q")
    )

    with right:
        st.caption("Equity Curve")
        st.altair_chart(equity_line + start_rule, use_container_width=True)