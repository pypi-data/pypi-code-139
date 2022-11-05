from sklearn.ensemble import RandomForestRegressor
from joblib import dump
import pandas as pd


def model_training(X_train, X_test, y_train, y_test):
    from evaluate import model_evaluation
    randomForest_model = RandomForestRegressor(n_estimators=100, random_state=1)
    randomForest_model.fit(X_train, y_train)
    dump(randomForest_model, '../models/model.joblib')
    return model_evaluation(X_train, X_test, y_train, y_test, randomForest_model)


def build_model(data: pd.DataFrame) -> dict[str, str]:
    from load import load_data
    score = load_data(data)
    print(score)
