import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn import metrics

from training import train_test_split, xgb_prediction, target_scaler, aapl_model, df_aapl, test_rmse_aapl, Y_test_aapl, predictions_aapl, last_row_aapl, df_googl, googl_model, test_rmse_googl, Y_test_googl, predictions_googl, last_row_googl, df_itx, itx_model ,test_rmse_itx, Y_test_itx, predictions_itx, last_row_itx, df_jnj, jnj_model ,test_rmse_jnj, Y_test_jnj, predictions_jnj, last_row_jnj, df_jpm, jpm_model, test_rmse_jpm, Y_test_jpm, predictions_jpm, last_row_jpm, df_tsla, tsla_model, test_rmse_tsla, Y_test_tsla, predictions_tsla, last_row_tsla

def plot_values(df, model ,test_rmse, Y_test, predictions ,percentage=0.2):

    global train, test
    train, test = train_test_split(df ,percentage)
    X, Y = train[:, :-1], train[:, -1]
    train_predictions = model.predict(X)
    
    # desescalar
    train_predictions = target_scaler.inverse_transform(train_predictions.reshape(-1, 1))
    Y = target_scaler.inverse_transform(Y.reshape(-1, 1))
    train_rmse = metrics.root_mean_squared_error(Y, train_predictions)
    
    print(f"Training RMSE: {train_rmse}")
    print(f"Testing RMSE: {test_rmse}")

    # plot actual vs. predicted
    # concatenar Y e Y_test para plotearlo junto
    Y = Y.reshape(-1)
    train_predictions = train_predictions.reshape(-1)
    Y = np.concatenate((Y, Y_test.reshape(-1)), axis=0)
    new_predictions = np.concatenate((train_predictions, predictions.reshape(-1)), axis=0)
    plt.plot(new_predictions, label='Predicted')
    plt.plot(Y, label='Actual')
    plt.legend()
    plt.show()

plot_values(df_aapl,aapl_model,test_rmse_aapl,Y_test_aapl,predictions_aapl)

plot_values(df_googl,googl_model,test_rmse_googl,Y_test_googl,predictions_googl)

plot_values(df_itx,itx_model,test_rmse_itx,Y_test_itx,predictions_itx)

plot_values(df_jnj,jnj_model,test_rmse_jnj,Y_test_jnj,predictions_jnj)

plot_values(df_jpm,jpm_model,test_rmse_jpm,Y_test_jpm,predictions_jpm)

plot_values(df_tsla,tsla_model,test_rmse_tsla,Y_test_tsla,predictions_tsla)



# plt.plot(Y_test.reshape(-1), label='Actual', color='k')
# plt.plot(predictions.reshape(-1), label='Predicted', color='y')
# plt.legend()
# plt.show()

prediction_aapl = xgb_prediction(df_aapl.values, last_row_aapl.values[0][:-1])
print(prediction_aapl)

prediction_googl = xgb_prediction(df_googl.values, last_row_googl.values[0][:-1])
print(prediction_googl)

prediction_itx = xgb_prediction(df_itx.values, last_row_itx.values[0][:-1])
print(prediction_itx)

prediction_jnj = xgb_prediction(df_jnj.values, last_row_jnj.values[0][:-1])
print(prediction_jnj)

prediction_jpm = xgb_prediction(df_jpm.values, last_row_jpm.values[0][:-1])
print(prediction_jpm)

prediction_tsla = xgb_prediction(df_tsla.values, last_row_tsla.values[0][:-1])
print(prediction_tsla)