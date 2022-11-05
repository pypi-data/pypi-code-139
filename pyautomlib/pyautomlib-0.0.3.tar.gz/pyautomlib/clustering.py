from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import silhouette_score
import pandas as pd
import numpy as np


class Cluster:
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame

    def get_optimum_clusters(self):
        scores = []
        for i in range(2, 20):
            labels = (
                KMeans(n_clusters=i, init="k-means++", random_state=42)
                .fit(self.data_frame)
                .labels_
            )
            score = silhouette_score(
                self.data_frame,
                labels,
                metric="euclidean",
                sample_size=1000,
                random_state=200,
            )
            scores.append(score)
        return np.argmax(scores) + 2

    def grid_search(self):
        kmeans_params = {
            "algorithm": ["auto", "full", "elkan"],
        }
        optimum_clusters = self.get_optimum_clusters()
        kmeans_best_grid = GridSearchCV(
            KMeans(n_clusters=optimum_clusters),
            kmeans_params,
            cv=5,
            n_jobs=-1,
            verbose=True,
        ).fit(self.data_frame)
        return {"n_clusters": optimum_clusters, **kmeans_best_grid.best_params_}

    def run(self):
        self.best_params = self.grid_search()
        self.cluster_model = KMeans(**self.best_params)
        clusters = self.cluster_model.fit_predict(self.data_frame)

        self.data_frame["cluster"] = clusters
        return self.data_frame
