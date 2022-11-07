import wandb

from ..entrypoint import fit


def cross_validate(config):
    for i in [1, 2, 3, 4, 5]:
        config["datamodule"].update(
            dict(
                train_explicit_file=f"u{i}.base",
                val_explicit_file=f"u{i}.test",
                test_explicit_file=f"u{i}.test",
            )
        )
        wandb.config.update(config)
        fit(config)
