import pandas as pd
import os
from statsmodels.tsa.stattools import adfuller


from eodhd import APIClient

api = APIClient(api_key='68a888ecbf2185.97717291')

TICKERS = ["AAPL.US", "GOOGL.US", "TSLA.US", "JNJ.US", "JPM.US", "ITX.MC"]

os.makedirs("../data", exist_ok=True)

for i in TICKERS:
    df = pd.DataFrame(api.get_eod_historical_stock_market_data(symbol= i, period='d', from_date='2010-01-01'))
    df.to_csv(f'../data/{i}.csv', index=False)

df = pd.read_csv('../data/AAPL.US.csv', parse_dates=['date'])    #asegurar que los datos estan en orden
df = df.sort_values('date').reset_index(drop=True)

print('p-value:', adfuller(df.adjusted_close)[1])

print('p-value:', adfuller(df.adjusted_close.diff(periods = 1).dropna())[1])

df["close_diff_1"] = df.adjusted_close.diff(periods=1)

df.index = df["date"]
df.drop("date", axis=1, inplace=True)

df.index = pd.to_datetime(df.index)
df = df.copy()
df['dayofweek'] = df.index.dayofweek
df['quarter'] = df.index.quarter
df['month'] = df.index.month
df['year'] = df.index.year
df['dayofyear'] = df.index.dayofyear
df['dayofmonth'] = df.index.day
df['weekofyear'] = df.index.isocalendar().week

df["adjusted_close(-1)"] = df['adjusted_close'].shift(1)

df["SMA"] = df["adjusted_close"].rolling(window= 13).mean()

df["EMA"] = df["adjusted_close"].ewm(span=9).mean()

short_EMA = df["adjusted_close"].ewm(span=24).mean()
long_EMA = df["adjusted_close"].ewm(span=52).mean()

df["MACD"] = short_EMA - long_EMA

delta = df["adjusted_close"].diff()
delta = delta[1:]
up = delta.clip(lower=0)
down = -delta.clip(upper=0)
ema_up = up.ewm(com =14-1, min_periods=14).mean()
ema_down = down.ewm(com=14-1, min_periods=14).mean()

df["rsi_14"] = ema_up/ema_down

middle_band = df["adjusted_close"].rolling(window=10).mean()
std_dev = df["adjusted_close"].rolling(window=10).std()

df["Upper_Band"] = middle_band + (std_dev*2)
df["Lower_Band"] = middle_band - (std_dev*2)

df["H_L_diff"] = df["high"] - df["low"]

df.drop("close", axis=1, inplace=True)
df.drop("high", axis=1, inplace=True)
df.drop("low", axis=1, inplace=True)

df["Bands_diff"] = df["Upper_Band"] - df["Lower_Band"]

df.drop("Upper_Band", axis=1, inplace=True)
df.drop("Lower_Band", axis=1, inplace=True)

df["target"] = df["adjusted_close"].shift(-1)

last_row = df.tail(1)
df.drop(df.tail(1).index, inplace=True)
df.dropna(inplace=True)