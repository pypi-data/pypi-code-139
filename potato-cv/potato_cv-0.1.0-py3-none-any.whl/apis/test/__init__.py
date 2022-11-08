#!/usr/bin/env python3

from .seg import multi_gpu_seg_test, single_gpu_seg_test
from .edge import multi_gpu_edge_test, single_gpu_edge_test

__all__ = [
    "multi_gpu_seg_test",
    "single_gpu_seg_test",
    "multi_gpu_edge_test",
    "single_gpu_edge_test",
]
