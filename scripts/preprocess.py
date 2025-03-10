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
    
    # Read CSV while skipping the first two rows
    df = pd.read_csv(file_path, skiprows=2)

    # Rename columns to match the actual structure (6 columns)
    df.columns = ["Date", "Close", "High", "Low", "Open", "Volume"]
    
    # Set Date as index and ensure it's in datetime format
    df.set_index("Date", inplace=True)
    df.index = pd.to_datetime(df.index)
    
    # Keep only the "Close" price for forecasting
    df = df[["Close"]].rename(columns={"Close": "Price"})
    
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
