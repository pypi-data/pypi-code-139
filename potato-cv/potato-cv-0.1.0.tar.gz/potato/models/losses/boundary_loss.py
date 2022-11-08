#!/usr/bin/env python3

"""Boundary Losses

Alexey Bokhovkin et al., Boundary Loss for Remote Sensing Imagery Semantic Segmentation
https://arxiv.org/abs/1905.07852
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from ..builder import SEG_LOSSES


def one_hot(label, num_classes):
    # FIXME: probably not efficient, but works for now
    # needed to remove ignore label which is usually 255
    onehot = []
    for i in range(num_classes):
        # this operation is probably slow on gpu since it's Long
        onehot.append(label == i)
    return torch.stack(onehot, dim=1).contiguous()


@SEG_LOSSES.register_module()
class BoundaryLoss(nn.Module):
    def __init__(
        self,
        theta0: int = 3,
        theta: int = 5,
        loss_weight=1.0,
        loss_name="loss_boundary_loss",
    ):
        super(BoundaryLoss, self).__init__()
        self.theta0 = theta0
        self.theta = theta
        self.loss_weight = loss_weight
        self._loss_name = loss_name

    def forward(self, cls_score, label, **kwargs):
        """
        Args:
            cls_score: segmentation logits (N, C, H, W)
            label: GT segmentation (N, H, W)
        """

        n, c, _, _ = cls_score.shape

        # softmax so that predicted map can be distributed in [0, 1]
        pred = torch.softmax(cls_score, dim=1)

        # one-hot vector of ground truth
        one_hot_gt = one_hot(label, c).float()
        # one_hot_gt = one_hot_gt.permute(0, 3, 1, 2).float()

        # boundary map
        gt_b = F.max_pool2d(
            1 - one_hot_gt,
            kernel_size=self.theta0,
            stride=1,
            padding=(self.theta0 - 1) // 2,
        )
        gt_b -= 1 - one_hot_gt

        pred_b = F.max_pool2d(
            1 - pred, kernel_size=self.theta0, stride=1, padding=(self.theta0 - 1) // 2
        )
        pred_b -= 1 - pred

        # extended boundary map
        gt_b_ext = F.max_pool2d(
            gt_b, kernel_size=self.theta, stride=1, padding=(self.theta - 1) // 2
        )

        pred_b_ext = F.max_pool2d(
            pred_b, kernel_size=self.theta, stride=1, padding=(self.theta - 1) // 2
        )

        # reshape
        gt_b = gt_b.view(n, c, -1)
        pred_b = pred_b.view(n, c, -1)
        gt_b_ext = gt_b_ext.view(n, c, -1)
        pred_b_ext = pred_b_ext.view(n, c, -1)

        # Precision, Recall
        P = torch.sum(pred_b * gt_b_ext, dim=2) / (torch.sum(pred_b, dim=2) + 1e-7)
        R = torch.sum(pred_b_ext * gt_b, dim=2) / (torch.sum(gt_b, dim=2) + 1e-7)

        # Boundary F1 Score
        BF1 = 2 * P * R / (P + R + 1e-7)

        return self.loss_weight * torch.mean(1 - BF1) / c

    @property
    def loss_name(self):
        return self._loss_name
