#!/usr/bin/env python3

from .builder import DATASETS
from .isprs import JointISPRSDataset, OTFJointISPRSDataset


@DATASETS.register_module()
class JointPotsdamDataset(JointISPRSDataset):
    """Joint ISPRS Potsdam dataset.
    In segmentation map annotation for Potsdam dataset, 0 is the ignore index.
    ``reduce_zero_label`` should be set to True. The ``img_suffix`` and
    ``seg_map_suffix`` are both fixed to '.png'.
    """


@DATASETS.register_module()
class OTFJointPotsdamDataset(OTFJointISPRSDataset):
    """OTF Joint ISPRS Potsdam dataset.
    In segmentation map annotation for Potsdam dataset, 0 is the ignore index.
    ``reduce_zero_label`` should be set to True. The ``img_suffix`` and
    ``seg_map_suffix`` are both fixed to '.png'.
    """
