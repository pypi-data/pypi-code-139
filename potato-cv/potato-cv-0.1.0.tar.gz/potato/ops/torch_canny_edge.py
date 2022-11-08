#!/usr/bin/env python3

"""Canny Edge

- Implement pytorch version of the algorithm
- [Canny Edge Pytorch](https://github.com/DCurro/CannyEdgePytorch)
- Already implemented by kornia, but non-differentiable, and very slow
"""

import math
from typing import Tuple

import torch
import torch.nn.functional as F

from kornia.color import rgb_to_grayscale
from kornia.filters import canny
from kornia.filters.gaussian import gaussian_blur2d
from kornia.filters.kernels import get_canny_nms_kernel  # , get_hysteresis_kernel
from kornia.filters.sobel import spatial_gradient

from .transforms import UnNormalize

__all__ = [
    "canny",
    "soft_canny",
    "TorchUnNormalizedCanny",
    "TorchUnNormalizedSoftCanny",
]


def soft_canny(
    input,
    sharpness: float = 1.0,
    low_threshold: float = 0.1,
    high_threshold: float = 0.2,
    kernel_size: Tuple[int, int] = (5, 5),
    sigma: Tuple[float, float] = (1, 1),
    hysteresis: bool = True,
    eps: float = 1e-6,
):
    if not isinstance(input, torch.Tensor):
        raise TypeError(f"Input type is not a torch.Tensor. Got {type(input)}")

    if not len(input.shape) == 4:
        raise ValueError(f"Invalid input shape, we expect BxCxHxW. Got: {input.shape}")

    if low_threshold > high_threshold:
        raise ValueError(
            "Invalid input thresholds. low_threshold should be smaller than the high_threshold. Got: {}>{}".format(
                low_threshold, high_threshold
            )
        )

    # TODO: add warnings for hysteresis

    if low_threshold < 0 and low_threshold > 1:
        raise ValueError(
            f"Invalid input threshold. low_threshold should be in range (0,1). Got: {low_threshold}"
        )

    if high_threshold < 0 and high_threshold > 1:
        raise ValueError(
            f"Invalid input threshold. high_threshold should be in range (0,1). Got: {high_threshold}"
        )

    device: torch.device = input.device
    dtype: torch.dtype = input.dtype

    # To Grayscale
    if input.shape[1] == 3:
        input = rgb_to_grayscale(input)

    # Gaussian filter
    blurred: torch.Tensor = gaussian_blur2d(input, kernel_size, sigma)

    # Compute the gradients
    gradients: torch.Tensor = spatial_gradient(blurred, normalized=False)

    # Unpack the edges
    gx: torch.Tensor = gradients[:, :, 0]
    gy: torch.Tensor = gradients[:, :, 1]

    # Compute gradient magnitude and angle
    magnitude: torch.Tensor = torch.sqrt(gx * gx + gy * gy + eps)
    angle: torch.Tensor = torch.atan2(gy, gx)

    # Radians to Degrees
    angle = 180.0 * angle / math.pi

    # Round angle to the nearest 45 degree
    angle = torch.round(angle / 45) * 45

    # Non-maximal suppression
    nms_kernels: torch.Tensor = get_canny_nms_kernel(device, dtype)
    nms_magnitude: torch.Tensor = F.conv2d(
        magnitude, nms_kernels, padding=nms_kernels.shape[-1] // 2
    )

    # Get the indices for both directions
    positive_idx: torch.Tensor = (angle / 45) % 8
    positive_idx = positive_idx.long()

    negative_idx: torch.Tensor = ((angle / 45) + 4) % 8
    negative_idx = negative_idx.long()

    # Apply the non-maximum suppresion to the different directions
    channel_select_filtered_positive: torch.Tensor = torch.gather(
        nms_magnitude, 1, positive_idx
    )
    channel_select_filtered_negative: torch.Tensor = torch.gather(
        nms_magnitude, 1, negative_idx
    )

    channel_select_filtered: torch.Tensor = torch.stack(
        [channel_select_filtered_positive, channel_select_filtered_negative], 1
    )

    # is_max: torch.Tensor = channel_select_filtered.min(dim=1)[0] > 0.0
    # relaxed thresholding
    is_max: torch.Tensor = torch.sigmoid(channel_select_filtered.min(dim=1)[0])

    magnitude = magnitude * is_max

    # Threshold
    edges: torch.Tensor = F.threshold(magnitude, low_threshold, 0.0)

    # low: torch.Tensor = magnitude > low_threshold
    # high: torch.Tensor = magnitude > high_threshold
    # relax thresholding
    low = torch.sigmoid(sharpness * (magnitude - low_threshold))
    high = torch.sigmoid(sharpness * (magnitude - high_threshold))

    edges = low * 0.5 + high * 0.5
    edges = edges.to(dtype)

    # non-differentiable
    # if hysteresis:
    #     edges_old: torch.Tensor = -torch.ones(edges.shape, device=edges.device, dtype=dtype)
    #     hysteresis_kernels: torch.Tensor = get_hysteresis_kernel(device, dtype)

    #     while ((edges_old - edges).abs() != 0).any():
    #         weak: torch.Tensor = (edges == 0.5).float()
    #         strong: torch.Tensor = (edges == 1).float()

    #         hysteresis_magnitude: torch.Tensor = F.conv2d(
    #             edges, hysteresis_kernels, padding=hysteresis_kernels.shape[-1] // 2
    #         )
    #         hysteresis_magnitude = (hysteresis_magnitude == 1).any(1, keepdim=True).to(dtype)
    #         hysteresis_magnitude = hysteresis_magnitude * weak + strong

    #         edges_old = edges.clone()
    #         edges = hysteresis_magnitude + (hysteresis_magnitude == 0) * weak * 0.5

    #     edges = hysteresis_magnitude

    return edges


class TorchUnNormalizedCanny(object):
    def __init__(
        self,
        low_threshold: float = 0.1,
        high_threshold: float = 0.2,
        kernel_size: Tuple[int, int] = (5, 5),
        sigma: Tuple[float, float] = (1, 1),
        hysteresis: bool = True,
        eps: float = 1e-6,
        mean: Tuple[float, float, float] = [123.675, 116.28, 103.53],
        std: Tuple[float, float, float] = [58.395, 57.12, 57.375],
        inplace: bool = False,  # NOTE: default should be false
    ):
        self._low_threshold = low_threshold
        self._high_threshold = high_threshold
        self._kernel_size = kernel_size
        self._sigma = sigma
        self._hysteresis = hysteresis
        self._eps = eps

        self.unnorm = UnNormalize(
            mean=mean,
            std=std,
            inplace=inplace,
        )

    def __call__(self, tensor):

        non_batch = False
        if tensor.ndim == 3:
            # add batch direction
            non_batch = True
            tensor = tensor.unsqueeze(0)
        assert tensor.ndim == 4

        x = self.unnorm(tensor) / 255.0
        mag, edge = canny(
            input=x,
            low_threshold=self._low_threshold,
            high_threshold=self._high_threshold,
            kernel_size=self._kernel_size,
            sigma=self._sigma,
            hysteresis=self._hysteresis,
            eps=self._eps,
        )

        if non_batch:
            # squeeze on
            edge = edge.squeeze(0)

        return edge


class TorchUnNormalizedSoftCanny(TorchUnNormalizedCanny):
    def __init__(
        self,
        sharpness=50.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._sharpness = sharpness

    def __call__(self, tensor):

        non_batch = False
        if tensor.ndim == 3:
            # add batch direction
            non_batch = True
            tensor = tensor.unsqueeze(0)
        assert tensor.ndim == 4

        x = self.unnorm(tensor) / 255.0
        out = soft_canny(
            input=x,
            sharpness=self._sharpness,
            low_threshold=self._low_threshold,
            high_threshold=self._high_threshold,
            kernel_size=self._kernel_size,
            sigma=self._sigma,
            hysteresis=self._hysteresis,
            eps=self._eps,
        )

        if non_batch:
            # squeeze on
            out = out.squeeze(0)

        return out
