import warnings
import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor,
    AdaBoostRegressor,
)
from sklearn.model_selection import GridSearchCV, cross_validate
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from .config import RegressionModel

warnings.simplefilter(action="ignore", category=Warning)


class Regression:
    def __init__(self, x: pd.DataFrame, y: pd.DataFrame, config: RegressionModel):
        self.X = x
        self.y = y
        self.config = config
        self.classifiers = []
        self.model = None

    def get_base_models(self):
        print("Base Models....")
        regressors = [
            ("RF", RandomForestRegressor(), self.config.rf_params),
            ("GBM", GradientBoostingRegressor(), self.config.gbm_params),
            (
                "XGBoost",
                XGBRegressor(use_label_encoder=False, eval_metric="logloss"),
                self.config.xgboost_params,
            ),
            ("LightGBM", LGBMRegressor(), self.config.lightgbm_params),
            ("AdaBoost", AdaBoostRegressor(), self.config.adaboost_params),
            ("DecisionTree", DecisionTreeRegressor(), self.config.dtr_params),
            ("Linear", LinearRegression(), {}),
            ("Ridge", Ridge(), {}),
            ("Lasso", Lasso(), {}),
            ("SVR", SVR(), {}),
        ]
        scores = []

        scoring = self.config.scoring
        cv = self.config.number_of_folds
        for name, classifier, _ in regressors:
            cv_results = cross_validate(
                classifier, self.X, self.y, cv=cv, scoring=scoring
            )
            score = round(cv_results["test_score"].mean(), 4)
            scores.append(score)

        # Sort regressors by score
        sorted_regressors = np.array(regressors)[np.argsort(scores)[::-1]]
        best_n_models = sorted_regressors[: self.config.number_of_models]

        print(
            f"Best {self.config.number_of_models} models: {[name for name, _, _ in best_n_models]}"
        )
        return best_n_models

    def hyperparameter_optimization(self):
        regressors = self.get_base_models()
        best_models = []
        scoring = self.config.scoring
        cv = self.config.number_of_folds
        print("Hyperparameter Optimization....")
        for name, classifier, params in regressors:
            gs_best = GridSearchCV(
                classifier, params, cv=cv, n_jobs=-1, verbose=False
            ).fit(self.X, self.y)
            final_model = classifier.set_params(**gs_best.best_params_)

            cv_results = cross_validate(
                final_model, self.X, self.y, cv=cv, scoring=scoring
            )
            score = round(cv_results["test_score"].mean(), 4)
            print(f"{name} best score : {score}", end="\n\n")
            best_models.append((name, final_model))

        return best_models

    def create_model(self) -> VotingRegressor:
        estimators = self.hyperparameter_optimization()
        self.model = VotingRegressor(estimators=estimators)
        cv_results = cross_validate(
            self.model,
            self.X,
            self.y,
            cv=self.config.number_of_folds,
            scoring=self.config.scoring,
            error_score=1,
        )
        self.model.fit(self.X, self.y)
        print(f"R2: {cv_results['test_score'].mean()}")

        return self.model

    def save_model(self, model_name):
        joblib.dump(self.model, f"{model_name}.pkl")
