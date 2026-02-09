import matplotlib.pyplot as plt

def plot_equity(equity):
    plt.figure()
    equity.plot(title="Equity Curve")
    plt.xlabel("Bet #"); plt.ylabel("Bankroll")
    plt.tight_layout()


