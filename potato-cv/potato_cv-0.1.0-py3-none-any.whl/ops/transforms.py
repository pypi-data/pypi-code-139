#!/usr/bin/env python3

import torch


class UnNormalize(object):
    def __init__(
        self,
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        inplace=True,
    ):
        self.mean = mean
        self.std = std
        self.inplace = inplace

    def __call__(self, tensor):
        """
        Args:
            tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
                Supports batched tensor.
        Returns:
            Tensor: Normalized image.
        """

        if tensor.ndim == 4:
            tensor = torch.permute(tensor, (1, 0, 2, 3)).contiguous()
        assert tensor.shape[0] == len(self.mean) == len(self.std)

        if self.inplace:
            for t, m, s in zip(tensor, self.mean, self.std):
                t.mul_(s).add_(m)
                # The normalize code -> t.sub_(m).div_(s)

            if tensor.ndim == 4:
                tensor = torch.permute(tensor, (1, 0, 2, 3)).contiguous()

            return tensor
        else:
            dtype = tensor.dtype
            device = tensor.device
            mean = torch.as_tensor(self.mean, dtype=dtype, device=device)
            std = torch.as_tensor(self.std, dtype=dtype, device=device)

            out = torch.zeros_like(tensor)
            for i, (t, m, s) in enumerate(zip(tensor, mean, std)):
                out[i] = t * s + m

            if out.ndim == 4:
                out = torch.permute(out, (1, 0, 2, 3)).contiguous()

            return out
