#!/usr/bin/env python3

"""
NOTE
- since `reduce_zero_label=True`, we have to be careful about what we pass to Mask2Edge
"""

import os.path as osp

import mmcv
import numpy as np
from PIL import Image

from .builder import DATASETS
from .custom import CustomJointDataset, OTFCustomJointDataset

LOVEDA_CLASSES = (
    "background",
    "building",
    "road",
    "water",
    "barren",
    "forest",
    "agricultural",
)
LOVEDA_PALETTE = [
    [255, 255, 255],
    [255, 0, 0],
    [255, 255, 0],
    [0, 0, 255],
    [159, 129, 183],
    [0, 255, 0],
    [255, 195, 128],
]
LOVEDA_labelIds = [0, 1, 2, 3, 4, 5, 6, 255]
LOVEDA_label2trainId = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}


@DATASETS.register_module()
class JointLoveDADataset(CustomJointDataset):
    """LoveDA dataset.
    In segmentation map annotation for LoveDA, 0 is the ignore index.
    ``reduce_zero_label`` should be set to True. The ``img_suffix`` and
    ``seg_map_suffix`` are both fixed to '.png'.
    """

    CLASSES = LOVEDA_CLASSES
    PALETTE = LOVEDA_PALETTE

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

        super(JointLoveDADataset, self).__init__(
            img_suffix=".png",
            edge_map_suffix=edge_map_suffix,
            seg_map_suffix=".png",
            reduce_zero_label=True,
            inst_sensitive=False,
            **kwargs,
        )

    def results2img(self, results, imgfile_prefix, indices=None):
        """Write the segmentation results to images.
        Args:
            results (list[ndarray]): Testing results of the
                dataset.
            imgfile_prefix (str): The filename prefix of the png files.
                If the prefix is "somepath/xxx",
                the png files will be named "somepath/xxx.png".
            indices (list[int], optional): Indices of input results, if not
                set, all the indices of the dataset will be used.
                Default: None.
        Returns:
            list[str: str]: result txt files which contains corresponding
            semantic segmentation images.
        """

        mmcv.mkdir_or_exist(imgfile_prefix)
        result_files = []
        for result, idx in zip(results, indices):

            filename = self.img_infos[idx]["filename"]
            basename = osp.splitext(osp.basename(filename))[0]

            png_filename = osp.join(imgfile_prefix, f"{basename}.png")

            # The  index range of official requirement is from 0 to 6.
            output = Image.fromarray(result.astype(np.uint8))
            output.save(png_filename)
            result_files.append(png_filename)

        return result_files

    def format_results(self, results, imgfile_prefix, indices=None):
        """Format the results into dir (standard format for LoveDA evaluation).
        Args:
            results (list): Testing results of the dataset.
            imgfile_prefix (str): The prefix of images files. It
                includes the file path and the prefix of filename, e.g.,
                "a/b/prefix".
            indices (list[int], optional): Indices of input results,
                if not set, all the indices of the dataset will be used.
                Default: None.
        Returns:
            tuple: (result_files, tmp_dir), result_files is a list containing
                the image paths, tmp_dir is the temporal directory created
                for saving json/png files when img_prefix is not specified.
        """
        if indices is None:
            indices = list(range(len(self)))

        assert isinstance(results, list), "results must be a list."
        assert isinstance(indices, list), "indices must be a list."

        result_files = self.results2img(results, imgfile_prefix, indices)

        return result_files


@DATASETS.register_module()
class OTFJointLoveDADataset(OTFCustomJointDataset):
    CLASSES = LOVEDA_CLASSES
    PALETTE = LOVEDA_PALETTE

    def __init__(
        self,
        **kwargs,
    ):
        super(OTFJointLoveDADataset, self).__init__(
            img_suffix=".png",
            seg_map_suffix=".png",
            reduce_zero_label=True,
            inst_sensitive=False,
            labelIds=LOVEDA_labelIds,
            ignore_indices=[7],  # ignore 255
            label2trainId=LOVEDA_label2trainId,
            **kwargs,
        )

    def format_results(self, **kwargs):
        raise ValueError("ERR: should not use OTF for testing")
