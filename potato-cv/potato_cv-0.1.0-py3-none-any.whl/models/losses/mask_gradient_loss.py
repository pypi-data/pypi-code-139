#!/usr/bin/env python3

"""Mask Gradient Losses

FIXME:
- maybe calculate masks in the loss instead (make it a joint loss)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from ..builder import EDGE_LOSSES


@EDGE_LOSSES.register_module()
class DualityLoss(nn.Module):
    """Mask Gradient L1 Loss for RPCNet"""

    def __init__(
        self,
        loss_weight=1.0,
        loss_name="duality_l1",
        reduction="sum",
    ):
        super().__init__()
        self.loss_weight = loss_weight
        self._loss_name = loss_name
        self._reduction = reduction

    def forward(
        self,
        edge_logit,
        maskgrad,
        **kwargs,
    ):
        edge = torch.sigmoid(edge_logit)
        loss = F.l1_loss(
            input=maskgrad,
            target=edge,
            reduction=self._reduction,
        )
        if self._reduction == "sum":
            loss = loss / edge.numel()
        return self.loss_weight * loss

    @property
    def loss_name(self):
        return self._loss_name


@EDGE_LOSSES.register_module()
class MaskGradientCrossEntropyLoss(nn.Module):
    """FIXME: maskgrads are not logits

    I don't this this loss is working correctly
    """

    def __init__(
        self,
        loss_weight=1.0,
        loss_name="loss_mask_grad_ce",
    ):
        super().__init__()
        self.loss_weight = loss_weight
        self._loss_name = loss_name

    def forward(
        self,
        edge_logit,  # logits
        edge_label,
        weight=None,
        **kwargs,
    ):
        # FIXME: input segmentation instead of edge
        # FIXME: input
        loss_total = 0

        # FIXME: could optimize for batched loss
        for i in range(edge_label.size(0)):  # iterate for batch size
            pred = edge_logit[i]
            target = edge_label[i]

            num_pos = torch.sum(target)  # true positive number
            num_total = target.size(-1) * target.size(-2)  # true total number
            num_neg = num_total - num_pos
            # compute a pos_weight for each image
            pos_weight = (num_neg / num_pos).clamp(min=1, max=num_total)

            max_val = (-pred).clamp_min_(0)
            log_weight = 1 + (pos_weight - 1) * target
            loss = (
                pred
                - pred * target
                + log_weight
                * (
                    max_val
                    + torch.log(torch.exp(-max_val) + torch.exp(-pred - max_val))
                )
            )

            loss = loss.mean()
            loss_total = loss_total + loss

        loss_total = loss_total / edge_label.size(0)
        return self.loss_weight * loss_total

    @property
    def loss_name(self):
        return self._loss_name
