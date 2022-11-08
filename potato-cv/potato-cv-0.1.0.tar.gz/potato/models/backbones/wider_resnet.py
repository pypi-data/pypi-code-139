#!/usr/bin/env python3

"""Wider ResNet Backbone

Reference:
https://github.com/haruishi43/GSCNN/blob/master/sseg/network/wider_resnet.py
"""

from collections import OrderedDict
from functools import partial

import torch.nn as nn
import torch

from mmcv.cnn import build_activation_layer, build_norm_layer
from mmcv.runner import BaseModule

from ..builder import BACKBONES


def bnrelu(
    channels,
    norm_cfg=dict(type="BN", requires_grad=True),
    act_cfg=dict(type="ReLU", inplace=True),
):
    return nn.Sequential(
        build_norm_layer(norm_cfg, channels)[1],
        build_activation_layer(act_cfg),
    )


class GlobalAvgPool2d(nn.Module):
    def __init__(self):
        """Global average pooling over the input's spatial dimensions"""
        super().__init__()

    def forward(self, inputs):
        in_size = inputs.size()
        return inputs.view((in_size[0], in_size[1], -1)).mean(dim=2)


class IdentityResidualBlock(nn.Module):
    def __init__(
        self,
        in_channels,
        channels,
        stride=1,
        dilation=1,
        groups=1,
        norm_cfg=dict(type="BN", requires_grad=True),
        act_cfg=dict(type="ReLU", inplace=True),
        dropout=None,
        dist_bn=False,
    ):
        """Configurable identity-mapping residual block
        Parameters
        ----------
        in_channels : int
            Number of input channels.
        channels : list of int
            Number of channels in the internal feature maps.
            Can either have two or three elements: if three construct
            a residual block with two `3 x 3` convolutions,
            otherwise construct a bottleneck block with `1 x 1`, then
            `3 x 3` then `1 x 1` convolutions.
        stride : int
            Stride of the first `3 x 3` convolution
        dilation : int
            Dilation to apply to the `3 x 3` convolutions.
        groups : int
            Number of convolution groups.
            This is used to create ResNeXt-style blocks and is only compatible with
            bottleneck blocks.
        norm_cfg : dict
        act_cfg : dict
        dropout: callable
            Function to create Dropout Module.
        dist_bn: Boolean
            A variable to enable or disable use of distributed BN
        """
        super().__init__()
        self.dist_bn = dist_bn

        # Check parameters for inconsistencies
        if len(channels) != 2 and len(channels) != 3:
            raise ValueError("channels must contain either two or three values")
        if len(channels) == 2 and groups != 1:
            raise ValueError("groups > 1 are only valid if len(channels) == 3")

        is_bottleneck = len(channels) == 3
        need_proj_conv = stride != 1 or in_channels != channels[-1]

        self.bn1 = bnrelu(in_channels, norm_cfg=norm_cfg, act_cfg=act_cfg)
        if not is_bottleneck:
            layers = [
                (
                    "conv1",
                    nn.Conv2d(
                        in_channels,
                        channels[0],
                        3,
                        stride=stride,
                        padding=dilation,
                        bias=False,
                        dilation=dilation,
                    ),
                ),
                ("bn2", bnrelu(channels[0], norm_cfg=norm_cfg, act_cfg=act_cfg)),
                (
                    "conv2",
                    nn.Conv2d(
                        channels[0],
                        channels[1],
                        3,
                        stride=1,
                        padding=dilation,
                        bias=False,
                        dilation=dilation,
                    ),
                ),
            ]
            if dropout is not None:
                layers = layers[0:2] + [("dropout", dropout())] + layers[2:]
        else:
            layers = [
                (
                    "conv1",
                    nn.Conv2d(
                        in_channels,
                        channels[0],
                        1,
                        stride=stride,
                        padding=0,
                        bias=False,
                    ),
                ),
                ("bn2", bnrelu(channels[0], norm_cfg=norm_cfg, act_cfg=act_cfg)),
                (
                    "conv2",
                    nn.Conv2d(
                        channels[0],
                        channels[1],
                        3,
                        stride=1,
                        padding=dilation,
                        bias=False,
                        groups=groups,
                        dilation=dilation,
                    ),
                ),
                ("bn3", bnrelu(channels[1], norm_cfg=norm_cfg, act_cfg=act_cfg)),
                (
                    "conv3",
                    nn.Conv2d(
                        channels[1], channels[2], 1, stride=1, padding=0, bias=False
                    ),
                ),
            ]
            if dropout is not None:
                layers = layers[0:4] + [("dropout", dropout())] + layers[4:]
        self.convs = nn.Sequential(OrderedDict(layers))

        if need_proj_conv:
            self.proj_conv = nn.Conv2d(
                in_channels, channels[-1], 1, stride=stride, padding=0, bias=False
            )

    def forward(self, x):
        """
        This is the standard forward function for non-distributed batch norm
        """
        if hasattr(self, "proj_conv"):
            bn1 = self.bn1(x)
            shortcut = self.proj_conv(bn1)
        else:
            shortcut = x.clone()
            bn1 = self.bn1(x)

        out = self.convs(bn1)
        out = out + shortcut
        return out


@BACKBONES.register_module()
class WiderResNet(BaseModule):

    arch_settings = {
        16: (1, 1, 1, 1, 1, 1),
        20: (1, 1, 1, 3, 1, 1),
        38: (3, 3, 6, 3, 1, 1),
    }

    def __init__(
        self,
        depth,
        out_indices=(0, 2, 3, 6),
        norm_cfg=dict(type="BN", requires_grad=True),
        act_cfg=dict(type="ReLU", inplace=True),
        init_cfg=None,
    ):
        """Wider ResNet with pre-activation (identity mapping) blocks Parameters

        ----------
        structure : list of int
            Number of residual blocks in each of the six modules of the network.
        norm_act : callable
            Function to create normalization / activation Module.
        classes : int
            If not `0` also include global average pooling and \
            a fully-connected layer with `classes` outputs at the end
            of the network.
        """
        super().__init__(init_cfg)
        assert max(out_indices) < 7
        self.out_indices = out_indices

        structure = self.arch_settings[depth]

        # Initial layers
        self.mod1 = nn.Sequential(
            OrderedDict(
                [("conv1", nn.Conv2d(3, 64, 3, stride=1, padding=1, bias=False))]
            )
        )

        # Groups of residual blocks
        in_channels = 64
        channels = [
            (128, 128),
            (256, 256),
            (512, 512),
            (512, 1024),
            (512, 1024, 2048),
            (1024, 2048, 4096),
        ]
        for mod_id, num in enumerate(structure):
            # Create blocks for module
            blocks = []
            for block_id in range(num):
                blocks.append(
                    (
                        "block%d" % (block_id + 1),
                        IdentityResidualBlock(
                            in_channels,
                            channels[mod_id],
                            norm_cfg=norm_cfg,
                            act_cfg=act_cfg,
                        ),
                    )
                )

                # Update channels and p_keep
                in_channels = channels[mod_id][-1]

            # Create module
            if mod_id <= 4:
                self.add_module(
                    "pool%d" % (mod_id + 2), nn.MaxPool2d(3, stride=2, padding=1)
                )
            self.add_module("mod%d" % (mod_id + 2), nn.Sequential(OrderedDict(blocks)))

        # Pooling and predictor
        # self.bn_out = bnrelu(in_channels, norm_cfg=norm_cfg, act_cfg=act_cfg)

    def forward(self, img):
        r1 = self.mod1(img)
        r2 = self.mod2(self.pool2(r1))
        r3 = self.mod3(self.pool3(r2))
        r4 = self.mod4(self.pool4(r3))
        r5 = self.mod5(self.pool5(r4))
        r6 = self.mod6(self.pool6(r5))
        r7 = self.mod7(r6)
        # out = self.bn_out(out)

        outs = [r1, r2, r3, r4, r5, r6, r7]
        outs = [outs[i] for i in self.out_indices]

        return outs


@BACKBONES.register_module()
class WiderResNetA2(BaseModule):

    arch_settings = {
        16: (1, 1, 1, 1, 1, 1),
        20: (1, 1, 1, 3, 1, 1),
        38: (3, 3, 6, 3, 1, 1),
    }

    def __init__(
        self,
        depth,
        out_indices=(0, 2, 3, 6),
        dilation=False,  # GSCNN: True
        dist_bn=False,
        norm_cfg=dict(type="BN", requires_grad=True),
        act_cfg=dict(type="ReLU", inplace=True),
        init_cfg=None,
    ):
        """Wider ResNet with pre-activation (identity mapping) blocks
        This variant uses down-sampling by max-pooling in the first two blocks and
        by strided convolution in the others.

        Parameters
        ----------
        structure : list of int
            Number of residual blocks in each of the six modules of the network.
        norm_cfg : dict
        act_cfg : dict
        classes : int
            If not `0` also include global average pooling and a fully-connected layer
            with `classes` outputs at the end
            of the network.
        dilation : bool
            If `True` apply dilation to the last three modules and change the
            down-sampling factor from 32 to 8.
        """
        super().__init__(init_cfg)

        assert max(out_indices) < 7
        self.out_indices = out_indices
        self.dist_bn = dist_bn

        structure = self.arch_settings[depth]
        self.dilation = dilation

        # Initial layers
        self.mod1 = torch.nn.Sequential(
            OrderedDict(
                [("conv1", nn.Conv2d(3, 64, 3, stride=1, padding=1, bias=False))]
            )
        )

        # Groups of residual blocks
        in_channels = 64
        channels = [
            (128, 128),
            (256, 256),
            (512, 512),
            (512, 1024),
            (512, 1024, 2048),
            (1024, 2048, 4096),
        ]
        for mod_id, num in enumerate(structure):
            # Create blocks for module
            blocks = []
            for block_id in range(num):

                # NOTE: for `a2` we set the number of dilation and strides accordingly

                if not dilation:
                    dil = 1
                    stride = 2 if block_id == 0 and 2 <= mod_id <= 4 else 1
                else:
                    if mod_id == 3:
                        dil = 2
                    elif mod_id > 3:
                        dil = 4
                    else:
                        dil = 1
                    stride = 2 if block_id == 0 and mod_id == 2 else 1

                # NOTE: there are also dropouts
                if mod_id == 4:
                    drop = partial(nn.Dropout2d, p=0.3)
                elif mod_id == 5:
                    drop = partial(nn.Dropout2d, p=0.5)
                else:
                    drop = None

                blocks.append(
                    (
                        "block%d" % (block_id + 1),
                        IdentityResidualBlock(
                            in_channels,
                            channels[mod_id],
                            norm_cfg=norm_cfg,
                            act_cfg=act_cfg,
                            stride=stride,
                            dilation=dil,
                            dropout=drop,
                            dist_bn=self.dist_bn,
                        ),
                    )
                )

                # Update channels and p_keep
                in_channels = channels[mod_id][-1]

            # Create module
            if mod_id < 2:
                self.add_module(
                    "pool%d" % (mod_id + 2), nn.MaxPool2d(3, stride=2, padding=1)
                )
            self.add_module("mod%d" % (mod_id + 2), nn.Sequential(OrderedDict(blocks)))

        # Pooling and predictor
        # self.bn_out = bnrelu(in_channels, norm_cfg=norm_cfg, act_cfg=act_cfg)

    def forward(self, img):
        r1 = self.mod1(img)
        r2 = self.mod2(self.pool2(r1))
        r3 = self.mod3(self.pool3(r2))
        r4 = self.mod4(r3)
        r5 = self.mod5(r4)
        r6 = self.mod6(r5)
        r7 = self.mod7(r6)
        # out = self.bn_out(out)

        outs = [r1, r2, r3, r4, r5, r6, r7]
        outs = [outs[i] for i in self.out_indices]

        return outs
