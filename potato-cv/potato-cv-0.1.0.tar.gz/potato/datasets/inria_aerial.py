#!/usr/bin/env python3

"""Inria Aerial Image Labeling Dataset

https://project.inria.fr/aerialimagelabeling/
"""

from .builder import DATASETS
from .custom import CustomJointDataset, OTFCustomBinaryJointDataset

INRIA_CLASSES = ("background", "building")
INRIA_PALETTE = [[0, 0, 0], [255, 255, 255]]
INRIA_labelIds = [0, 1]


@DATASETS.register_module()
class INRIAAerialDataset(CustomJointDataset):

    CLASSES = INRIA_CLASSES
    PALETTE = INRIA_PALETTE

    def __init__(
        self,
        img_suffix=".png",
        seg_map_suffix=".png",
        edge_map_suffix=".png",
        gt_edge_loader_cfg=dict(binary=True),
        **kwargs,
    ):
        super().__init__(
            img_suffix=img_suffix,
            seg_map_suffix=seg_map_suffix,
            edge_map_suffix=edge_map_suffix,
            inst_sensitive=False,
            gt_edge_loader_cfg=gt_edge_loader_cfg,
            reduce_zero_label=False,  # zero is background!
            **kwargs,
        )


@DATASETS.register_module()
class OTFINRIAAerialDataset(OTFCustomBinaryJointDataset):

    CLASSES = INRIA_CLASSES
    PALETTE = INRIA_PALETTE
    IDS = [0, 1]

    def __init__(
        self,
        img_suffix=".png",
        seg_map_suffix=".png",
        reduce_zero_label=False,
        ignore_indices=[],
        labelIds=INRIA_labelIds,
        label2trainId=None,
        radius=1,
        selected_label=1,
        **kwargs,
    ):
        super().__init__(
            img_suffix=img_suffix,
            seg_map_suffix=seg_map_suffix,
            reduce_zero_label=reduce_zero_label,
            ignore_indices=ignore_indices,
            labelIds=labelIds,
            label2trainId=label2trainId,
            radius=radius,
            selected_label=selected_label,
            **kwargs,
        )
