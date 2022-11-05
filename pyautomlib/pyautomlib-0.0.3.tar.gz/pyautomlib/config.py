from typing import Callable
from sklearn.preprocessing import StandardScaler


class PreprocessModel:
    scale: bool = True
    scaler: Callable = StandardScaler
    label_encode: bool = True
    one_hot_encode: bool = True
    perform_PCA: bool = False
    replace_outliers: bool = False
    remove_outliers: bool = True
    categorical_threshold: int = 10
    cardinal_threshold: int = 20
    drop_cardinals: bool = True
    handle_missing: bool = True
    missing_handling_method: str = "delete"  # "mean", "median", "delete"
    test_size: float = 0.2


class ClassificationModel:
    knn_params: dict = {
        "n_neighbors": [3, 5, 11, 19],
        "weights": ["uniform", "distance"],
    }
    cart_params: dict = {"max_depth": range(1, 20), "min_samples_split": range(2, 30)}
    rf_params: dict = {
        "max_depth": [8, 15, None],
        "max_features": [5, 7, "auto"],
        "min_samples_split": [15, 20],
        "n_estimators": [200, 300],
    }
    xgb_params: dict = {
        "learning_rate": [0.1, 0.01],
        "max_depth": [5, 8],
        "n_estimators": [100, 200],
        "colsample_bytree": [0.5, 1],
    }
    lightgbm_params: dict = {
        "learning_rate": [0.01, 0.1],
        "n_estimators": [300, 500],
        "colsample_bytree": [0.7, 1],
    }
    gbm_params: dict = {
        "learning_rate": [0.01, 0.1],
        "n_estimators": [300, 500],
    }
    adaboost_params: dict = {
        "learning_rate": [0.01, 0.1],
        "n_estimators": [300, 500],
    }
    scoring: str = "roc_auc"
    number_of_folds: int = 5
    number_of_models: int = 3


class RegressionModel:
    scoring: str = "r2"
    number_of_folds: int = 5
    number_of_models: int = 3
    rf_params: dict = {
        "max_depth": [8, 15, None],
        "max_features": [5, 7, "auto"],
        "min_samples_split": [15, 20],
        "n_estimators": [200, 300]
    }
    xgboost_params: dict = {
        "learning_rate": [0.1, 0.01],
        "max_depth": [5, 8],
        "n_estimators": [100, 200],
        "colsample_bytree": [0.5, 1],
    }
    lightgbm_params: dict = {
        "learning_rate": [0.01, 0.1],
        "n_estimators": [300, 500],
        "colsample_bytree": [0.7, 1],
    }
    gbm_params: dict = {
        "learning_rate": [0.01, 0.1],
        "n_estimators": [300, 500],
    }
    adaboost_params: dict = {
        "learning_rate": [0.01, 0.1, 1],
        "n_estimators": [10, 30, 50, 70, 100, 300, 500],
    }
    dtr_params: dict = {"max_depth": [None, *range(1, 10)], "min_samples_split": range(2, 30)}
