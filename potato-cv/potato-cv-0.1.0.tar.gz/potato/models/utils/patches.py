#!/usr/bin/env python3

import math

import torch
import torch.nn.functional as F


def extract_image_patches(x, patch_size=(3, 3)):
    b, c, h, w = x.shape
    patch_h = math.ceil(h / patch_size[0])
    patch_w = math.ceil(w / patch_size[1])
    pad_h = patch_size[0] * patch_h - h
    pad_w = patch_size[1] * patch_w - w
    # pad: left, right, top, bottom
    x = F.pad(x, (pad_w // 2, pad_w - pad_w // 2, pad_h // 2, pad_h - pad_h // 2))

    # Extract patches
    patches = x.unfold(2, patch_h, patch_h).unfold(3, patch_w, patch_w)
    patches = patches.permute(0, 1, 2, 3, 4, 5).contiguous()

    return patches.view(b, -1, c, patches.shape[-2], patches.shape[-1])


def patch_wise_pool(x, patch_size=(3, 3)):
    b, p, c, h, w = x.shape

    vs = []
    for i in range(p):
        vs.append(
            F.avg_pool2d(x[:, i, ...], (h, w)).unsqueeze(-1).unsqueeze(-1)
        )  # (b, c)

    f = torch.stack(vs, dim=-3)
    f = f.view(b, c, *patch_size)

    return f  # (b, c, p, p)
