import numpy as np

from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

from data_processing import df_aapl,df_googl,df_itx,df_jnj,df_jpm,df_tsla

def initialize(df):
    df.index = df["date"]
    df.drop("date", axis=1, inplace=True)

    global last_row
    last_row = df.tail(1)
    df.drop(df.tail(1).index, inplace=True)
    df.dropna(inplace=True)

initialize(df_aapl)
initialize(df_googl)
initialize(df_itx)
initialize(df_jnj)
initialize(df_jpm)
initialize(df_tsla)

feature_scaler = MinMaxScaler()
target_scaler = MinMaxScaler()

def train_test_split(df, test_size=0.2):
    data = df.values
    
    feature_scaler.fit(data[:, :-1]) 
    target_scaler.fit(data[:, -1:]) 
    scaled_data = feature_scaler.transform(data[:, :-1])
    scaled_target = target_scaler.transform(data[:, -1:])
    data_scaled = np.concatenate((scaled_data, scaled_target), axis=1)
    
    
    n = int(len(data_scaled) * (1 - test_size))
    return data_scaled[:n], data_scaled[n:]

def xgb_prediction(train, value):
    train = np.array(train)
    X, Y = train[:, :-1], train[:, -1]
    global model
    model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)

    model.fit(X, Y)
    val = np.array(value).reshape(1, -1)
    prediction = model.predict(val)
    return prediction[0] 

def walk_forward_validation(data, percentage=0.2):
    # In this case -1 is the target column (last one)
    train, test = train_test_split(data, percentage)
    predictions = []
    history = [x for x in train]

    for i in range(len(test)):
        test_X, test_Y = test[i, :-1], test[i, -1]
        pred = xgb_prediction(history, test_X)
        predictions.append(pred)
        history.append(test[i])
    
    Y_test = target_scaler.inverse_transform(test[:, -1:].reshape(1, -1))
    Y_pred = target_scaler.inverse_transform(np.array(predictions).reshape(1, -1))
    test_rmse = metrics.root_mean_squared_error(Y_test, Y_pred)

    return test_rmse, Y_test, Y_pred

test_rmse_aapl, Y_test_aapl, predictions_aapl = walk_forward_validation(df_aapl, 0.2)

test_rmse_googl, Y_test_googl, predictions_googl = walk_forward_validation(df_googl, 0.2)

test_rmse_itx, Y_test_itx, predictions_itx = walk_forward_validation(df_itx, 0.2)

test_rmse_jnj, Y_test_jnj, predictions_jnj = walk_forward_validation(df_jnj, 0.2)

test_rmse_jpm, Y_test_jpm, predictions_jpm = walk_forward_validation(df_jpm, 0.2)

test_rmse_tsla, Y_test_tsla, predictions_tsla = walk_forward_validation(df_tsla, 0.2)