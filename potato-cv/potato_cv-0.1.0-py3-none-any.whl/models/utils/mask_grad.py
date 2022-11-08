#!/usr/bin/env python3

import torch
import torch.nn.functional as F


def maskgrad(
    seg_map: torch.Tensor,
    sensitivity: int = 100,
) -> torch.Tensor:
    """Calculate Mask Gradients."""
    # convert to probability
    seg_probs = F.softmax(sensitivity * seg_map, dim=1)
    # average or maxpooling?
    seg_pool = F.avg_pool2d(seg_probs, kernel_size=3, stride=1, padding=1)
    mask_edge = torch.abs(seg_probs - seg_pool)  # (b, class, h, w)
    return mask_edge
