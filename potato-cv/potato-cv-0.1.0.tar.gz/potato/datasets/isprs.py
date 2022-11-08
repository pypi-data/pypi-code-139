#!/usr/bin/env python3

from .builder import DATASETS
from .custom import CustomJointDataset, OTFCustomJointDataset

ISPRS_CLASSES = (
    "impervious_surface",
    "building",
    "low_vegetation",
    "tree",
    "car",
    "clutter",
)
ISPRS_PALETTE = [
    [255, 255, 255],
    [0, 0, 255],
    [0, 255, 255],
    [0, 255, 0],
    [255, 255, 0],
    [255, 0, 0],
]
ISPRS_labelIds = [0, 1, 2, 3, 4, 5, 255]
# ISPRS_label2trainId = {
#     1: 0,
#     2: 1,
#     3: 2,
#     4: 3,
#     5: 4,
#     6: 5,
# }
ISPRS_label2trainId = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
}


@DATASETS.register_module()
class JointISPRSDataset(CustomJointDataset):
    """Joint ISPRS dataset.
    In segmentation map annotation for LoveDA, 0 is the ignore index.
    ``reduce_zero_label`` should be set to True. The ``img_suffix`` and
    ``seg_map_suffix`` are both fixed to '.png'.
    """

    CLASSES = ISPRS_CLASSES
    PALETTE = ISPRS_PALETTE

    def __init__(
        self,
        thin=False,
        test_mode=False,
        **kwargs,
    ):

        if test_mode:
            if thin:
                edge_map_suffix = "_thin.png"
            else:
                edge_map_suffix = "_raw.png"
        else:
            edge_map_suffix = ".png"

        super(JointISPRSDataset, self).__init__(
            img_suffix=".png",
            edge_map_suffix=edge_map_suffix,
            seg_map_suffix=".png",
            reduce_zero_label=True,
            inst_sensitive=False,
            **kwargs,
        )


@DATASETS.register_module()
class OTFJointISPRSDataset(OTFCustomJointDataset):
    CLASSES = ISPRS_CLASSES
    PALETTE = ISPRS_PALETTE

    def __init__(self, **kwargs):
        super(OTFJointISPRSDataset, self).__init__(
            img_suffix=".png",
            seg_map_suffix=".png",
            reduce_zero_label=True,
            inst_sensitive=False,
            labelIds=ISPRS_labelIds,
            ignore_indices=[6],  # ignore 255
            label2trainId=ISPRS_label2trainId,
            **kwargs,
        )
