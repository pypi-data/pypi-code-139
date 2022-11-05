from joblib import dump
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd


def preprocessing_df(X_train, X_test, y_train, y_test):
    from train import model_training
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    encoder.fit(X_train[['SaleCondition', 'Street']])
    encoded_cat_cols = pd.DataFrame(encoder.transform(X_train[['SaleCondition', 'Street']]))
    dump(encoder, '../models/encoder.joblib')
    encoded_cat_cols.index = X_train.index
    X_train.drop(['SaleCondition', 'Street'], inplace=True, axis=1)
    X_train_cp = pd.concat([X_train, encoded_cat_cols], axis=1)
    cols = ['LotArea', '1stFlrSF', '2ndFlrSF']
    X_train_scaled = X_train_cp.copy()
    scaler = StandardScaler()
    X_train_scaled[cols] = scaler.fit(X_train_cp[cols])
    X_train_scaled[cols] = scaler.transform(X_train_cp[cols])
    dump(scaler, '../models/scaler.joblib')
    return model_training(X_train_scaled, X_test, y_train, y_test)
