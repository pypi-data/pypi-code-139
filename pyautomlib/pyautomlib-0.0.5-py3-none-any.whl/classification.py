import numpy as np
import pandas as pd
import warnings
import joblib
from lightgbm import LGBMClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    VotingClassifier,
    AdaBoostClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from .config import ClassificationModel

warnings.simplefilter(action="ignore", category=Warning)


class Classification:
    def __init__(self, x: pd.DataFrame, y: pd.DataFrame, config: ClassificationModel):
        self.X = x
        self.y = y
        self.config = config
        self.classifiers = []
        self.model = None

    def get_base_models(self):
        print("Base Models....")
        classifiers = [
            ("KNN", KNeighborsClassifier(), self.config.knn_params),
            ("CART", DecisionTreeClassifier(), self.config.cart_params),
            ("RF", RandomForestClassifier(), self.config.rf_params),
            ("XGBoost", XGBClassifier(), self.config.xgb_params),
            ("LightGBM", LGBMClassifier(), self.config.lightgbm_params),
            ("GBM", GradientBoostingClassifier(), self.config.gbm_params),
            ("AdaBoost", AdaBoostClassifier(), self.config.adaboost_params),
            ("LR", LogisticRegression(), {}),
            ("SVM", SVC(probability=True), {}),
        ]
        scores = []

        scoring = self.config.scoring
        cv = self.config.number_of_folds
        for name, classifier, _ in classifiers:
            cv_results = cross_validate(
                classifier, self.X, self.y, cv=cv, scoring=scoring
            )
            score = round(cv_results["test_score"].mean(), 4)
            scores.append(score)

        # Sort classifiers by score
        sorted_classifiers = np.array(classifiers)[np.argsort(scores)[::-1]]
        best_n_models = sorted_classifiers[: self.config.number_of_models]

        print(
            f"Best {self.config.number_of_models} models: {[name for name, _, _ in best_n_models]}"
        )
        return best_n_models

    def hyperparameter_optimization(self):
        classifiers = self.get_base_models()
        best_models = []
        scoring = self.config.scoring
        cv = self.config.number_of_folds
        print("Hyperparameter Optimization....")
        for name, classifier, params in classifiers:
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

    def create_model(self) -> VotingClassifier:
        estimators = self.hyperparameter_optimization()
        self.model = VotingClassifier(estimators=estimators, voting="soft")
        cv_results = cross_validate(
            self.model,
            self.X,
            self.y,
            cv=self.config.number_of_folds,
            scoring=["accuracy", "f1", "roc_auc"],
            error_score="raise",
        )
        self.model.fit(self.X, self.y)
        print(f"Accuracy: {cv_results['test_accuracy'].mean()}")
        print(f"F1Score: {cv_results['test_f1'].mean()}")
        print(f"ROC_AUC: {cv_results['test_roc_auc'].mean()}")

        return self.model

    def save_model(self, model_name):
        joblib.dump(self.model, f"{model_name}.pkl")
