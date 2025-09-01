import pandas as pd
import os

from eodhd import APIClient
from statsmodels.tsa.stattools import adfuller

api = APIClient(api_key='68a888ecbf2185.97717291')

TICKERS = ["AAPL.US", "GOOGL.US", "TSLA.US", "JNJ.US", "JPM.US", "ITX.MC"]

os.makedirs("../data/raw", exist_ok=True)

for i in TICKERS:
    df = pd.DataFrame(api.get_eod_historical_stock_market_data(symbol= i, period='d', from_date='2010-01-01'))
    df.to_csv(f'../data/raw/{i}.csv', index=False)


df_aapl = pd.read_csv('../data/raw/AAPL.US.csv', parse_dates=['date'])
df_aapl = df_aapl.sort_values('date').reset_index(drop=True)

df_googl = pd.read_csv('../data/raw/GOOGL.US.csv', parse_dates=['date'])
df_googl = df_googl.sort_values('date').reset_index(drop=True)

df_itx = pd.read_csv('../data/raw/ITX.MC.csv', parse_dates=['date'])
df_itx = df_itx.sort_values('date').reset_index(drop=True)

df_jnj = pd.read_csv('../data/raw/JNJ.US.csv', parse_dates=['date'])
df_jnj = df_jnj.sort_values('date').reset_index(drop=True)

df_jpm = pd.read_csv('../data/raw/JPM.US.csv', parse_dates=['date'])
df_jpm = df_jpm.sort_values('date').reset_index(drop=True)

df_tsla = pd.read_csv('../data/raw/TSLA.US.csv', parse_dates=['date'])
df_tsla = df_tsla.sort_values('date').reset_index(drop=True)

def es_estacionaria(df):
    print('p-value of adjusted close:', adfuller(df.adjusted_close)[1])

    print('p-value of adjusted close diff:', adfuller(df.adjusted_close.diff(periods = 1).dropna())[1])

def feature_eng(df):
    df["close_diff_1"] = df.adjusted_close.diff(periods=1)

    df.index = df["date"]
    df.drop("date", axis=1, inplace=True)

    df.index = pd.to_datetime(df.index)
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

    global last_row
    last_row = df.tail(1)
    df.drop(df.tail(1).index, inplace=True)
    df.dropna(inplace=True)

    return df



print("---------------------------------\n")
print("Apple")
es_estacionaria(df_aapl)
feature_eng(df_aapl)
print("---------------------------------\n")
print("Google")
es_estacionaria(df_googl)
feature_eng(df_googl)
print("---------------------------------\n")
print("Inditex")
es_estacionaria(df_itx)
feature_eng(df_itx)
print("---------------------------------\n")
print("Johnson & Johnson")
es_estacionaria(df_jnj)
feature_eng(df_jnj)
print("---------------------------------\n")
print("JPMorgan Chase & Co")
es_estacionaria(df_jpm)
feature_eng(df_jpm)
print("---------------------------------\n")
print("Tesla")
es_estacionaria(df_tsla)
feature_eng(df_tsla)
print("---------------------------------")

os.makedirs("../data/processed", exist_ok=True)

DATASETS = ['df_aapl','df_googl','df_itx','df_jnj','df_jpm','df_tsla']

df_aapl.to_csv("../data/processed/df_aapl.csv", index = False)
df_googl.to_csv("../data/processed/df_googl.csv", index = False)
df_itx.to_csv("../data/processed/df_itx.csv", index = False)
df_jnj.to_csv("../data/processed/df_jnj.csv", index = False)
df_jpm.to_csv("../data/processed/df_jpm.csv", index = False)
df_tsla.to_csv("../data/processed/df_tsla.csv", index = False)