import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics

from training import train_test_split, xgb_prediction, target_scaler, df, model, test_rmse, Y_test, predictions, last_row

def plot_values(df, percentage=0.2):

    train, test = train_test_split(df, percentage)
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

plot_values(df, 0.2)

plt.plot(Y_test.reshape(-1), label='Actual', color='k')
plt.plot(predictions.reshape(-1), label='Predicted', color='y')
plt.legend()
plt.show()

prediction = xgb_prediction(df.values, last_row.values[0][:-1])
print(prediction)