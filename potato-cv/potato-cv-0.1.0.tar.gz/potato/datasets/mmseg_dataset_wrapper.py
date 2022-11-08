#!/usr/bin/env python3

"""
Wrap mmseg dataset to add additional functions
"""
from collections import OrderedDict

import numpy as np
from prettytable import PrettyTable

from mmcv.utils import print_log
from mmseg.datasets import CityscapesDataset

from potato.core.evaluation.f_boundary import (
    eval_mask_boundary,
    eval_mask_boundary_batch,
    pre_eval_to_boundary,
)
from .builder import DATASETS

FBOUNDARY_EVAL_DATASET_MAPPING = {
    "CityscapesDataset": "WrappedCityscapesDataset",
}


@DATASETS.register_module()
class WrappedCityscapesDataset(CityscapesDataset):
    def pre_boundary_fscore_eval(self, preds, indices, bound_th, num_proc=1):
        """Collect eval result from each iteration for boundaries

        Args:
            preds (list[torch.Tensor] | torch.Tensor): the segmentation logit
                after argmax, shape (N, H, W).
            indices (list[int] | int): the prediction related ground truth
                indices.

        Returns:
            list[torch.Tensor]: (area_intersect, area_union, area_prediction,
                area_ground_truth).
        """
        # In order to compat with batch inference
        if not isinstance(indices, list):
            indices = [indices]
        if not isinstance(preds, list):
            preds = [preds]

        pre_eval_results = []

        if num_proc > 1:
            preds = np.asarray(preds)
            seg_maps = np.asarray([self.get_gt_seg_map_by_idx(i) for i in indices])
            Fpc, Fc = eval_mask_boundary_batch(
                preds,
                seg_maps,
                num_classes=len(self.CLASSES),
                num_proc=num_proc,
                bound_th=bound_th,
            )
            pre_eval_results.append((Fpc, Fc))
        else:
            for pred, index in zip(preds, indices):
                seg_map = self.get_gt_seg_map_by_idx(index)
                Fpc, Fc = eval_mask_boundary(
                    pred,  # already numpy
                    seg_map,  # already numpy
                    num_classes=len(self.CLASSES),
                    bound_th=bound_th,
                )
                pre_eval_results.append((Fpc, Fc))

        return pre_eval_results

    def evaluate_boundary_fscore(self, results, logger=None, **kwargs):

        fscores = pre_eval_to_boundary(results)

        class_names = self.CLASSES

        # summary table
        fscore_summary = OrderedDict({"fscore": np.round(np.nanmean(fscores) * 100, 2)})

        # each class table
        fscore_class = OrderedDict({"fscore": np.round(fscores * 100, 2)})
        fscore_class.update({"Class": class_names})
        fscore_class.move_to_end("Class", last=False)

        # for logger
        class_table_data = PrettyTable()
        for key, val in fscore_class.items():
            class_table_data.add_column(key, val)

        summary_table_data = PrettyTable()
        for key, val in fscore_summary.items():
            if key == "aAcc":
                summary_table_data.add_column(key, [val])
            else:
                summary_table_data.add_column("m" + key, [val])

        print_log("per class results:", logger)
        print_log("\n" + class_table_data.get_string(), logger=logger)
        print_log("Summary:", logger)
        print_log("\n" + summary_table_data.get_string(), logger=logger)

        # each metric dict
        eval_results = {}
        for key, value in fscore_summary.items():
            eval_results["m" + key] = value / 100.0

        fscore_class.pop("Class", None)
        for key, value in fscore_class.items():
            eval_results.update(
                {
                    key + "." + str(name): value[idx] / 100.0
                    for idx, name in enumerate(class_names)
                }
            )

        return eval_results
