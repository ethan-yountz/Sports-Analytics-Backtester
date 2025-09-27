import streamlit as st
import pandas as pd
from SRC.backtester import run_backtest
from SRC.Strategies.flat_underdog import FlatUnderdog
from SRC.Strategies.flat_favorite import FlatFavorite
from SRC.data_loader import load_games
from SRC.metrics import roi, win_rate, max_drawdown
import altair as alt

st.title("Sports Analaytics Backtester")

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
    with st.spinner("Running backtest…"):
        bets, equity = run_backtest(Df, finalstrat, bankroll)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.write(f"Total bets: {len(bets)}")
        st.write(f"Ending Bankroll: {equity.iloc[-1]:.2f}")
        st.write(f"ROI: {roi(bets['pnl'], bets['stake']) * 100:.2f}%")
        st.write(f"Win rate: {win_rate(bets['result']) * 100:.2f}%")
        st.write(f"Max drawdown: {max_drawdown(equity):.3f}")

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