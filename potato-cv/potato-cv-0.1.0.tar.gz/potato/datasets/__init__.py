#!/usr/bin/env python3

from .builder import (
    DATASETS,
    PIPELINES,
    build_dataloader,
    build_dataset,
)
from .mmseg_dataset_wrapper import FBOUNDARY_EVAL_DATASET_MAPPING
from .pipelines import *  # noqa: F401,F403

from .custom import (
    CustomJointDataset,
    OTFCustomJointDataset,
    OTFCustomBinaryJointDataset,
)
from .cityscapes import JointCityscapesDataset, OTFJointCityscapesDataset
from .isprs import JointISPRSDataset, OTFJointISPRSDataset
from .potsdam import JointPotsdamDataset, OTFJointPotsdamDataset
from .loveda import JointLoveDADataset, OTFJointLoveDADataset
from .inria_aerial import INRIAAerialDataset, OTFINRIAAerialDataset

__all__ = [
    "DATASETS",
    "PIPELINES",
    "FBOUNDARY_EVAL_DATASET_MAPPING",
    "build_dataloader",
    "build_dataset",
    "CustomJointDataset",
    "OTFCustomJointDataset",
    "OTFCustomBinaryJointDataset",
    "JointCityscapesDataset",
    "OTFJointCityscapesDataset",
    "JointISPRSDataset",
    "OTFJointISPRSDataset",
    "JointPotsdamDataset",
    "OTFJointPotsdamDataset",
    "JointLoveDADataset",
    "OTFJointLoveDADataset",
    "INRIAAerialDataset",
    "OTFINRIAAerialDataset",
]
