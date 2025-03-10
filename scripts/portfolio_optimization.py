import pandas as pd
import numpy as np
import scipy.optimize as opt

def optimize_portfolio(tickers):
    """
    Optimize asset allocation to maximize returns & minimize risk.
    """
    dfs = [pd.read_csv(f"data/processed/{ticker}.csv", index_col="Date", parse_dates=True) for ticker in tickers]
    returns = pd.concat([df["Returns"] for df in dfs], axis=1)
    returns.columns = tickers

    # Compute mean returns & covariance matrix
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    # Define optimization function (Sharpe Ratio)
    def sharpe_ratio(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility

    # Optimize asset allocation
    constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
    bounds = tuple((0, 1) for _ in range(len(tickers)))
    initial_guess = [1/len(tickers)] * len(tickers)

    result = opt.minimize(sharpe_ratio, initial_guess, bounds=bounds, constraints=constraints)
    optimized_weights = result.x

    print("Optimized Portfolio Weights:", optimized_weights)
    return optimized_weights

if __name__ == "__main__":
    tickers = ["TSLA", "BND", "SPY"]
    optimize_portfolio(tickers)
