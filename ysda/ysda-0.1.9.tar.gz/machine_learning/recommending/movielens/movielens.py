import abc
import torch
import wandb

from my_tools.entrypoints import ConfigConstructorBase

from .. import als
from .. import baseline
from .. import bpmf
from .. import callbacks
from .. import metrics
from ..entrypoints import LitRecommenderBase, NonGradientRecommenderMixin
from ..pmf import PMFRecommender
from ..recommender import RatingsToRecommendations
from ..slim import SLIMRecommender
from .data import MovieLens
from . import callbacks as movielens_callbacks


class MovieLensRecommender(LitRecommenderBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ratings_to_recommendations = None

    def recommend(self, *args, **kwargs):
        if self.ratings_to_recommendations is None:
            self.ratings_to_recommendations = RatingsToRecommendations(
                explicit_feedback=self.train_explicit, model=self
            )
        return self.ratings_to_recommendations(*args, **kwargs)

    @property
    def movielens(self):
        return MovieLens(self.hparams["datamodule_config"]["directory"])

    @property
    def train_explicit(self):
        if file := self.hparams["datamodule_config"].get("train_explicit_file"):
            return self.movielens.explicit_feedback_scipy_csr(file)

    @property
    def val_explicit(self):
        if file := self.hparams["datamodule_config"].get("val_explicit_file"):
            return self.movielens.explicit_feedback_scipy_csr(file)

    @property
    def test_explicit(self):
        if file := self.hparams["datamodule_config"].get("test_explicit_file"):
            return self.movielens.explicit_feedback_scipy_csr(file)


class MovieLensNonGradientRecommender(
    NonGradientRecommenderMixin, MovieLensRecommender
):
    @property
    def module_candidates(self):
        return super().module_candidates + [als, baseline, bpmf, movielens_callbacks]


class MovieLensPMFRecommender(PMFRecommender, MovieLensRecommender):
    pass


class MovieLensSLIMRecommender(SLIMRecommender, MovieLensRecommender):
    pass


class MovieLensDispatcher(ConfigConstructorBase, abc.ABC):
    def __init__(self, config):
        # For some reason with some configuration it is necessary to manually init cuda.
        torch.cuda.init()

        if "callbacks" not in config:
            config["callbacks"] = {}
        config["callbacks"].update(
            RecommendingIMDBCallback=dict(
                path_to_imdb_ratings_csv="local/my_imdb_ratings.csv",
                path_to_movielens_folder="local/ml-100k",
                n_recommendations=10,
            ),
            RecommendingMetricsCallback=dict(
                directory="local/ml-100k",
                k=100,
            ),
        )
        super().__init__(config)

    @property
    def class_candidates(self):
        return super().class_candidates + [
            MovieLensNonGradientRecommender,
            MovieLensPMFRecommender,
            MovieLensSLIMRecommender,
        ]

    @property
    def module_candidates(self):
        return super().module_candidates + [callbacks, movielens_callbacks, metrics]

    def build_lightning_module(self):
        lightning_module = self.build_class(
            datamodule_config=self.config["datamodule"],
            model_config=self.config["model"],
            loss_config=self.config.get("loss"),
            optimizer_config=self.config.get("optimizer"),
            **self.config["lightning_module"],
        )
        return lightning_module

    def main(self):
        lightning_module = self.build_lightning_module()
        trainer = self.build_trainer()
        trainer.fit(lightning_module)
        trainer.test(lightning_module)

    def update_tune_data(self):
        self.config["datamodule"].update(
            dict(
                train_explicit_file="u1.base",
                val_explicit_file="u1.base",
                test_explicit_file="u1.test",
            )
        )

    def tune(self):
        self.update_tune_data()
        if wandb.run is None and self.config.get("logger") is not None:
            with wandb.init(project=self.config.get("project"), config=self.config):
                return self.main()
        else:
            return self.main()

    def test_datasets_iter(self):
        for i in [2, 3, 4, 5]:
            self.config["datamodule"].update(
                dict(
                    train_explicit_file=f"u{i}.base",
                    val_explicit_file=f"u{i}.base",
                    test_explicit_file=f"u{i}.test",
                )
            )
            yield

    def test(self):
        with wandb.init(project=self.config["project"], config=self.config):
            for _ in self.test_datasets_iter():
                self.main()

    def dispatch(self):
        if self.config.get("stage") == "test":
            self.test()
        else:
            self.tune()
