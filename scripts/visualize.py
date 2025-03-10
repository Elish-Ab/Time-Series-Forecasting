import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the processed data for each ticker
tickers = ["TSLA", "BND", "SPY"]
data = {}

for ticker in tickers:
    data[ticker] = pd.read_csv(f"data/processed/{ticker}.csv", index_col="Date", parse_dates=True)

# Plotting the stock prices (Close)
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(data[ticker].index, data[ticker]["Price"], label=ticker)
plt.title("Stock Prices Over Time")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plotting the daily returns
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(data[ticker].index, data[ticker]["Returns"], label=f"{ticker} Daily Returns")
plt.title("Daily Returns for TSLA, BND, SPY")
plt.xlabel("Date")
plt.ylabel("Daily Returns")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Summary statistics for each ticker
summary_stats = pd.DataFrame(columns=["Mean", "Std Dev", "Min", "Max", "Skew", "Kurtosis"])

for ticker in tickers:
    ticker_data = data[ticker]["Price"]
    summary_stats.loc[ticker] = [
        ticker_data.mean(),
        ticker_data.std(),
        ticker_data.min(),
        ticker_data.max(),
        ticker_data.skew(),
        ticker_data.kurt()
    ]

print("Summary Statistics for Each Ticker:")
print(summary_stats)

# Correlation matrix between daily returns
returns_data = pd.DataFrame({ticker: data[ticker]["Returns"] for ticker in tickers})
corr_matrix = returns_data.corr()

# Plotting correlation matrix heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0)
plt.title("Correlation Matrix of Daily Returns")
plt.tight_layout()
plt.show()
