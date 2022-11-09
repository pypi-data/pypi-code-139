from house_prices.preprocess import preprocess
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import pandas as pd


def build_model(input_data: pd.DataFrame) -> dict[str, str]:
    new_df, target = preprocess(input_data)
    X = new_df
    y = target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    accuracy = 1 - rmse / y_test.mean()
    joblib.dump(model, 'model.joblib')
    result_dict = {'rmse': rmse, 'accuracy': accuracy}
    return result_dict
