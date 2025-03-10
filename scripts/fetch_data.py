import yfinance as yf
import pandas as pd
import os

# Create data directories if they don’t exist
os.makedirs("data/raw", exist_ok=True)

def fetch_data(ticker, start="2015-01-01", end="2025-01-31"):
    """
    Fetch historical data from Yahoo Finance and save as CSV.
    """
    print(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start, end=end)
    file_path = f"data/raw/{ticker}.csv"
    data.to_csv(file_path)
    print(f"Saved {ticker} data to {file_path}")
    return data

if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    for ticker in tickers:
        fetch_data(ticker)
