#!/usr/bin/env python3

"""Formatting

- use `DefaultFormatBundle` for segmentation only tasks
- use `JointFormatBundle` for joint segmentation and edge detection
"""

import numpy as np
from mmcv.parallel import DataContainer as DC
from mmseg.datasets.pipelines.formatting import to_tensor
from blette.datasets.pipelines import FormatImage

from potato.datasets.builder import PIPELINES


@PIPELINES.register_module()
class FormatJoint(object):
    """Format multilabel edge and segmentation"""

    def __call__(self, results):
        # non-otf
        if "gt_semantic_edge" in results:
            edge = results["gt_semantic_edge"]

            # HACK: decode RGB to 24bit array
            # it's only possible to encode 24 classes
            edge = np.unpackbits(
                edge,
                axis=2,
            )[:, :, -1 : -(results["num_classes"] + 1) : -1]
            edge = np.ascontiguousarray(edge.transpose(2, 0, 1))

            # convert to long
            results["gt_semantic_edge"] = DC(
                to_tensor(edge.astype(np.int64)),
                stack=True,
            )

            # convert segmentation mask as well
            if "gt_semantic_seg" in results:
                # convert to long
                results["gt_semantic_seg"] = DC(
                    to_tensor(results["gt_semantic_seg"][None, ...].astype(np.int64)),
                    stack=True,
                )

        elif "gt_semantic_seg" in results:
            mask2edge = results.get("mask2edge", None)
            assert mask2edge, "ERR: no mask2edge inside `results`"

            if results["inst_sensitive"]:
                inst_map = results.get("gt_inst_seg", None)
                assert inst_map is not None, "ERR: instance map is not available"
                out = mask2edge(
                    mask=results["gt_semantic_seg"],
                    inst_mask=inst_map,
                )
                # remove it from memory?
                del results["gt_inst_seg"]
            else:
                out = mask2edge(mask=results["gt_semantic_seg"])

            # out is a dict('mask'=..., 'edge'=...)
            results["gt_semantic_seg"] = DC(
                to_tensor(out["mask"][None, ...].astype(np.int64)),
                stack=True,
            )
            results["gt_semantic_edge"] = DC(
                to_tensor(out["edge"].astype(np.int64)),
                stack=True,
            )

        return results


@PIPELINES.register_module()
class FormatJointBinaryEdge:
    """Format binary edge and segmentation"""

    def __init__(
        self,
        selected_label=None,
    ):
        """
        Args:
            select_label Optional(int): if multilabel edges are given,
                the label set with this argument will be used
                (assuming that the edge is indexed from 0)
        """
        self._label = selected_label
        if self._label is not None:
            assert isinstance(self._label, int)

    def __call__(self, results):
        # non-otf
        if "gt_semantic_edge" in results:
            edge = results["gt_semantic_edge"]

            if edge.ndim == 3:
                assert self._label is not None
                # ordered (h, w, trainId)
                edge = edge[:, :, self._label]

            assert edge.ndim == 2
            # No need for hacks to convert dataset
            results["gt_semantic_edge"] = DC(
                to_tensor(edge[None, ...].astype(np.int64)),
                stack=True,
            )

            # convert segmentation mask as well
            if "gt_semantic_seg" in results:
                # convert to long
                results["gt_semantic_seg"] = DC(
                    to_tensor(results["gt_semantic_seg"][None, ...].astype(np.int64)),
                    stack=True,
                )
        elif "gt_semantic_seg" in results:
            mask2edge = results.get("mask2edge", None)
            assert mask2edge, "ERR: no mask2edge inside `results`"

            if results.get("inst_sensitive", False):
                inst_map = results.get("gt_inst_seg", None)
                assert inst_map is not None, "ERR: instance map is not available"
                out = mask2edge(
                    mask=results["gt_semantic_seg"],
                    inst_mask=inst_map,
                )
                # remove it from memory?
                del results["gt_inst_seg"]
            else:
                out = mask2edge(mask=results["gt_semantic_seg"])

            edge = out["edge"]

            if edge.ndim == 3:
                assert self._label is not None
                # ordered (trainId, h, w)
                edge = edge[self._label]

            assert edge.ndim == 2

            results["gt_semantic_edge"] = DC(
                to_tensor(edge[None, ...].astype(np.int64)),
                stack=True,
            )
            results["gt_semantic_seg"] = DC(
                to_tensor(out["mask"][None, ...].astype(np.int64)),
                stack=True,
            )

        return results


@PIPELINES.register_module()
class JointFormatBundle(object):
    def __init__(self):
        self.format_image = FormatImage()
        self.format_joint = FormatJoint()

    def __call__(self, results):
        results = self.format_image(results)
        results = self.format_joint(results)
        return results

    def __repr__(self):
        return self.__class__.__name__


@PIPELINES.register_module()
class JointBinaryFormatBundle(object):
    def __init__(self, selected_label=None):
        self.format_image = FormatImage()
        self.format_joint = FormatJointBinaryEdge(selected_label=selected_label)

    def __call__(self, results):
        results = self.format_image(results)
        results = self.format_joint(results)
        return results

    def __repr__(self):
        return self.__class__.__name__
