import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def arima_forecast(df, steps=30):
    """
    Train an ARIMA model and forecast next `steps` days.
    """
    model = ARIMA(df["Price"], order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

def sarima_forecast(df, steps=30):
    """
    Train a SARIMA model and forecast next `steps` days.
    """
    model = SARIMAX(df["Price"], order=(1,1,1), seasonal_order=(1,1,1,12))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

def lstm_forecast(df, steps=30):
    """
    Train an LSTM model and forecast next `steps` days.
    """
    data = df["Price"].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0,1))
    data_scaled = scaler.fit_transform(data)

    X, y = [], []
    for i in range(len(data_scaled)-30):
        X.append(data_scaled[i:i+30])
        y.append(data_scaled[i+30])

    X, y = np.array(X), np.array(y)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(30,1)),
        LSTM(50),
        Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=10, batch_size=16, verbose=0)

    last_30_days = data_scaled[-30:].reshape(1,30,1)
    forecast_scaled = model.predict(last_30_days)
    forecast = scaler.inverse_transform(forecast_scaled)
    
    return forecast.flatten()

if __name__ == "__main__":
    df = pd.read_csv("data/processed/TSLA.csv", index_col="Date", parse_dates=True)

    arima_pred = arima_forecast(df)
    sarima_pred = sarima_forecast(df)
    lstm_pred = lstm_forecast(df)

    print("ARIMA Prediction:", arima_pred)
    print("SARIMA Prediction:", sarima_pred)
    print("LSTM Prediction:", lstm_pred)
