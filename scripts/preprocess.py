import pandas as pd
import os

input_folder = "data/raw/"
output_folder = "data/processed/"
os.makedirs(output_folder, exist_ok=True)

def preprocess_data(ticker):
    """
    Read raw stock data, clean missing values, compute daily returns, and save processed data.
    """
    file_path = f"{input_folder}{ticker}.csv"
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)

    # Keep only Adjusted Close price
    df = df[["Adj Close"]].rename(columns={"Adj Close": "Price"})
    
    # Compute daily returns
    df["Returns"] = df["Price"].pct_change()
    
    # Drop missing values
    df.dropna(inplace=True)
    
    # Save processed data
    processed_file_path = f"{output_folder}{ticker}.csv"
    df.to_csv(processed_file_path)
    print(f"Processed data saved: {processed_file_path}")

    return df

if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    for ticker in tickers:
        preprocess_data(ticker)
