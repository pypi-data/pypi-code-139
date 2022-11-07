import os

import wandb
import yaml

from my_tools.entrypoints import LightningConfigBuilder, ConfigDispenser

from . import callbacks as movielens_callbacks
from . import lit
from .. import callbacks, metrics

def cross_validate(config):


def update_movielens_config(config, path_to_local_folder="local", dataset_id=1):
    if dataset_id not in range(1, 5):
        raise ValueError(f"Invalid dataset_id {dataset_id}")
    if "callbacks" not in config:
        config["callbacks"] = {}
    config["callbacks"].update(
        RecommendingIMDBCallback=dict(
            path_to_imdb_ratings_csv=os.path.join(
                path_to_data_folder, "my_imdb_ratings.csv"
            )
        )
    )

    config["datamodule"].update(
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
