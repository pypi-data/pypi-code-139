from sklearn.model_selection import train_test_split
from preprocess import preprocessing_df
import pandas as pd


def load_data(train_master: pd.DataFrame):
    features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'SaleCondition', 'Street']
    train_master.dropna(subset=['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'SaleCondition', 'Street', 'SalePrice'], inplace=True)
    y = train_master.SalePrice
    X = train_master[features]
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=1)
    return preprocessing_df(X_train, X_test, y_train, y_test)
