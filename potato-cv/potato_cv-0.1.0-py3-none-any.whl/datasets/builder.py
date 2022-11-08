#!/usr/bin/env python3

"""builder.py

Currently a placeholder for subclassing `mmseg` and `blette`.
"""

# I want to use the original segmentation only datasets
from mmseg.datasets import (
    DATASETS,
    build_dataloader,
    build_dataset,
)

# blette pipeline includes mmseg's pipelines
from blette.datasets import PIPELINES


__all__ = [
    "DATASETS",
    "PIPELINES",
    "build_dataloader",
    "build_dataset",
]
