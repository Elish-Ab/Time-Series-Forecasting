import pandas as pd

def preprocess_data(ticker):
    file_path = f"data/raw/{ticker}.csv"
    
    # Skip first two rows and set the correct column names
    df = pd.read_csv(file_path, skiprows=2, index_col=0, parse_dates=True)
    
    # Rename index to 'Date' for clarity
    df.index.name = "Date"
    
    print(df.head())  # Debugging: Check the output

    # Save the cleaned file
    df.to_csv(f"data/processed/{ticker}_cleaned.csv")

# Example usage
preprocess_data("BND")
