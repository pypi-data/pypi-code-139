#!/usr/bin/env python3

from mmcv.utils import Registry
from mmseg.models.builder import (
    MODELS,
    NECKS,
    HEADS,
    LOSSES as SEG_LOSSES,
    SEGMENTORS,
    build_segmentor,
)
from blette.models.builder import (
    BACKBONES,
    LOSSES as EDGE_LOSSES,
)

POTATO_MODELS = Registry("potato_models", parent=MODELS)
JOINT_LOSSES = POTATO_MODELS

__all__ = [
    "BACKBONES",
    "NECKS",
    "HEADS",
    "SEG_LOSSES",
    "EDGE_LOSSES",
    "JOINT_LOSSES",
    "SEGMENTORS",
    "build_backbone",
    "build_neck",
    "build_head",
    "build_seg_loss",
    "build_edge_loss",
    "build_joint_loss",
    "build_segmentor",
]


def build_backbone(cfg):
    """Build backbone."""
    return BACKBONES.build(cfg)


def build_neck(cfg):
    """Build neck."""
    return NECKS.build(cfg)


def build_head(cfg):
    """Build head."""
    return HEADS.build(cfg)


def build_seg_loss(cfg):
    """Build segmentation loss."""
    return SEG_LOSSES.build(cfg)


def build_edge_loss(cfg):
    """Build edge loss."""
    return EDGE_LOSSES.build(cfg)


def build_joint_loss(cfg):
    """Build joint task loss"""
    return JOINT_LOSSES.build(cfg)
