import streamlit as st
import pandas as pd
from pathlib import Path
from SRC.backtester import run_backtest
from SRC.Strategies.flat_underdog import FlatUnderdog
from SRC.Strategies.flat_favorite import FlatFavorite
from SRC.data_loader import load_games

bankroll = st.number_input("Starting Bankroll", value = 100, min_value=1, step = 10, key= "bankroll")
unit = st.number_input("Unit Size", value = 1.0, min_value= 0.01, step = 0.1, key= "Unit")

finalstrat = None
strat = st.selectbox("Select Strategy", ["","Flat Bet Favorite", "Flat Bet Underdog"])
if strat == "Flat Bet Favorite":
    finalstrat = FlatFavorite(unit)
else:
    finalstrat = FlatUnderdog(unit)

Df = None
Data = st.selectbox("Select Data Set", ["", "NBA Set 2012 - 2019"])
if Data == "NBA Set 2012 - 2019":
    Df = load_games("Data/Processed/games_clean.csv")


run = st.button('Run Simulation')

if run:
    bets, equity = run_backtest(Df, finalstrat, bankroll )
    st.write(f"Strategy: {strat}")
    st.write(Df)
    st.write(f"Total bets: {len(bets)}")

    # st.write(st.session_state.bankroll)