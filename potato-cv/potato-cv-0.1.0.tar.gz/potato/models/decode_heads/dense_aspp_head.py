#!/usr/bin/env python3

import torch
import torch.nn as nn
import torch.nn.functional as F

from mmcv.cnn.bricks import build_activation_layer, build_norm_layer
from mmseg.models.decode_heads.decode_head import BaseDecodeHead

from ..builder import HEADS


class DenseASPPBlock(nn.Sequential):
    """ConvNet block for building DenseASPP."""

    def __init__(
        self,
        in_channels,
        mid_channels,
        out_channels,
        dilation_rate,
        drop_rate,
        bn_start=True,
        norm_cfg=dict(type="BN"),
        act_cfg=dict(type="ReLU"),
    ):
        super(DenseASPPBlock, self).__init__()

        # force momentum on Norm (Assuming BN or SyncBN)
        norm_cfg.update({"momentum": 0.0003})

        if bn_start:
            self.add_module("norm1", build_norm_layer(norm_cfg, in_channels)[1])

        self.add_module("relu1", build_activation_layer(act_cfg))
        self.add_module(
            "conv1",
            nn.Conv2d(
                in_channels=in_channels, out_channels=mid_channels, kernel_size=1
            ),
        )

        self.add_module("norm2", build_norm_layer(norm_cfg, mid_channels)[1])
        self.add_module("relu2", build_activation_layer(act_cfg))
        self.add_module(
            "conv2",
            nn.Conv2d(
                in_channels=mid_channels,
                out_channels=out_channels,
                kernel_size=3,
                dilation=dilation_rate,
                padding=dilation_rate,
            ),
        )

        self.drop_rate = drop_rate

    def forward(self, input):
        feature = super(DenseASPPBlock, self).forward(input)
        if self.drop_rate > 0:
            feature = F.dropout2d(feature, p=self.drop_rate, training=self.training)
        return feature


class DenseASPP(nn.Module):
    def __init__(
        self,
        in_channels,
        mid_channels,
        out_channels,
        dilation_rates=(3, 6, 12, 18, 24),
        drop_rate=0,
    ):
        super(DenseASPP, self).__init__()

        self.aspps = nn.ModuleList()
        for i, dil in enumerate(dilation_rates):
            self.aspps.append(
                DenseASPPBlock(
                    in_channels=in_channels + out_channels * i,
                    mid_channels=mid_channels,
                    out_channels=out_channels,
                    dilation_rate=dil,
                    drop_rate=drop_rate,
                    bn_start=False if i == 0 else True,
                )
            )

    def forward(self, x):
        for aspp in self.aspps:
            f = aspp(x)
            x = torch.cat((x, f), dim=1)
        return x


@HEADS.register_module()
class DenseASPPHead(BaseDecodeHead):
    """DenseASPP.

    This head is the implementation of
    `DenseASPP <https://ieeexplore.ieee.org/document/8578486>`

    Args:
        in_channels (int): input channels for DenseASPP (refer to the backbone)
        channels (int): output channels for each DenseASPPBlock
        mid_channels (int): output channels for the first conv in DenseASPPBlock
        dilations (tuple(int)): dilation_ratio for each DenseASPPBlock
        aspp_dropout_ratio (float): dropout ratio for DenseASPPBlock
    """

    def __init__(
        self,
        in_channels,
        channels,
        mid_channels,
        dilations=(3, 6, 12, 18, 24),
        aspp_dropout_ratio=0.1,
        **kwargs,
    ):
        # pre-calc output channels for final seg
        final_channels = in_channels + len(dilations) * channels
        super(DenseASPPHead, self).__init__(
            in_channels=in_channels,
            channels=final_channels,
            **kwargs,
        )

        self.dense_aspp = DenseASPP(
            in_channels=self.in_channels,
            mid_channels=mid_channels,
            out_channels=channels,
            dilation_rates=dilations,
            drop_rate=aspp_dropout_ratio,
        )

    def forward(self, inputs):
        x = self._transform_inputs(inputs)
        x = self.dense_aspp(x)
        output = self.cls_seg(x)
        return output
