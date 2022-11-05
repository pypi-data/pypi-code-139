import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import mean_squared_log_error
pd.options.mode.chained_assignment = None  # default='warn'


def model_evaluation(X_train, X_test, y_train, y_test, randomForest_model):
    encoder = load('../models/encoder.joblib')
    scaler = load('../models/scaler.joblib')
    enc = pd.DataFrame(encoder.transform(X_test[['SaleCondition', 'Street']]))
    enc.index = X_test.index
    X_test.drop(X_test[['SaleCondition', 'Street']], inplace=True, axis=1)
    test = pd.concat([X_test, enc], axis=1)
    scaler.transform(test[['LotArea', '1stFlrSF', '2ndFlrSF']])
    y_pred = randomForest_model.predict(test)
    return compute_rmsle(y_test, y_pred)


def compute_rmsle(y_test, pred, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test, pred))
    return {"rmsle": rmsle}
