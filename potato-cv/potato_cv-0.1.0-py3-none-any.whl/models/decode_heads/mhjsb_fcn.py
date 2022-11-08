#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule
from blette.models.utils import (
    GroupedConvFuse,
    LocationAdaptiveLearner,
    BasicBlockSideConv,
    SideConv,
)

from potato.models.builder import HEADS
from .manyedge_decode_head import BaseManyEdgeDecodeHead


@HEADS.register_module()
class DDSFCNMHJSBHead(BaseManyEdgeDecodeHead):
    def __init__(
        self,
        num_convs=2,
        kernel_size=3,
        concat_input=True,
        dilation=1,
        num_side_blocks=2,
        edge_key="fuse",
        log_edge_keys=("fuse", "side1", "side2", "side3", "side4", "side5"),
        binary_edge_keys=("side1", "side2", "side3", "side4"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_binary_edge=dict(type="BinaryEdgeLoss", loss_weight=1.0),
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            binary_edge_keys=binary_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_binary_edge=loss_binary_edge,
            loss_multilabel_edge=loss_multilabel_edge,
            **kwargs,
        )

        # changes which feature to `resize_to`
        self.feature_resize_index = feature_resize_index

        _interp = "bilinear"
        _bias = True

        # 1. Multi-label edge stream
        self.side1 = BasicBlockSideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            num_blocks=num_side_blocks,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side2 = BasicBlockSideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            num_blocks=num_side_blocks,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side3 = BasicBlockSideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            num_blocks=num_side_blocks,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side4 = BasicBlockSideConv(
            in_channels=self.in_channels[3],
            out_channels=1,
            num_blocks=num_side_blocks,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = BasicBlockSideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            num_blocks=num_side_blocks,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.fuse = GroupedConvFuse(
            num_classes=self.num_classes,
            num_sides=5,
            conv_cfg=self.conv_cfg,
        )

        # --> mmseg
        assert num_convs >= 0 and dilation > 0 and isinstance(dilation, int)
        self.num_convs = num_convs
        self.concat_input = concat_input
        self.kernel_size = kernel_size

        fcn_in_channels = self.in_channels[-1]

        if num_convs == 0:
            assert fcn_in_channels == self.channels

        conv_padding = (kernel_size // 2) * dilation
        convs = []
        for i in range(num_convs):
            _in_channels = fcn_in_channels if i == 0 else self.channels
            convs.append(
                ConvModule(
                    _in_channels,
                    self.channels,
                    kernel_size=kernel_size,
                    padding=conv_padding,
                    dilation=dilation,
                    conv_cfg=self.conv_cfg,
                    norm_cfg=self.norm_cfg,
                    act_cfg=self.act_cfg,
                )
            )

        if len(convs) == 0:
            self.convs = nn.Identity()
        else:
            self.convs = nn.Sequential(*convs)
        if self.concat_input:
            self.conv_cat = ConvModule(
                fcn_in_channels + self.channels,
                self.channels,
                kernel_size=kernel_size,
                padding=kernel_size // 2,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )

    def forward(self, inputs):
        """Forward function"""

        # x = self._transform_inputs(inputs)  # out: list
        x = [i for i in inputs]
        # [stem, layer1, layer2, layer3, layer4, input_image]
        # h: 1/2, 1/4, 1/8, 1/8, 1/8, 1

        assert isinstance(x, list)
        bs, c, h, w = x[self.feature_resize_index].shape
        resize_to = (h, w)  # TODO: might be too large

        # Semantic Edge Stream
        side1 = self.side1(x[0], resize_to)  # (B, 1, H, W)
        side2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
        side3 = self.side3(x[2], resize_to)  # (B, 1, H, W)
        side4 = self.side4(x[3], resize_to)  # (B, 1, H, W)
        side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)
        fused_edges = self.fuse([side1, side2, side3, side4, side5])

        # FCN
        fcn_x = x[-2]  # use layer 4
        fcn_feats = self.convs(fcn_x)
        if self.concat_input:
            fcn_feats = self.conv_cat(torch.cat([fcn_x, fcn_feats], dim=1))
        output = self.cls_seg(fcn_feats)

        return (
            output,
            dict(side1=side1, side2=side2, side3=side3, side4=side4),
            # dict(side1=side1, side2=side2, side3=side3),
            dict(fuse=fused_edges, side5=side5),
        )


@HEADS.register_module()
class CASENetFCNMHJSBHead(BaseManyEdgeDecodeHead):
    def __init__(
        self,
        num_convs=2,
        kernel_size=3,
        concat_input=True,
        dilation=1,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_multilabel_edge=loss_multilabel_edge,
            **kwargs,
        )

        # changes which feature to `resize_to`
        self.feature_resize_index = feature_resize_index

        _interp = "bilinear"  # nearest
        _bias = False

        # bias should not be turn on when some of the sides are not supervised

        # Sides 1, 2, 3, 5
        self.side1 = SideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,  # bias instead of bn
            bias=_bias,  # add bias in the last layer
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side2 = SideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,  # bias instead of bn
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side3 = SideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,  # bias instead of bn
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = SideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,  # bias instead of bn
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.fuse = GroupedConvFuse(
            num_classes=self.num_classes,
            num_sides=4,
            conv_cfg=self.conv_cfg,
            bias=_bias,  # originally true
        )

        # --> mmseg
        assert num_convs >= 0 and dilation > 0 and isinstance(dilation, int)
        self.num_convs = num_convs
        self.concat_input = concat_input
        self.kernel_size = kernel_size

        fcn_in_channels = self.in_channels[-1]

        if num_convs == 0:
            assert fcn_in_channels == self.channels

        conv_padding = (kernel_size // 2) * dilation
        convs = []
        for i in range(num_convs):
            _in_channels = fcn_in_channels if i == 0 else self.channels
            convs.append(
                ConvModule(
                    _in_channels,
                    self.channels,
                    kernel_size=kernel_size,
                    padding=conv_padding,
                    dilation=dilation,
                    conv_cfg=self.conv_cfg,
                    norm_cfg=self.norm_cfg,
                    act_cfg=self.act_cfg,
                )
            )

        if len(convs) == 0:
            self.convs = nn.Identity()
        else:
            self.convs = nn.Sequential(*convs)
        if self.concat_input:
            self.conv_cat = ConvModule(
                fcn_in_channels + self.channels,
                self.channels,
                kernel_size=kernel_size,
                padding=kernel_size // 2,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )

    def forward(self, inputs):
        """Forward function"""

        # x = self._transform_inputs(inputs)  # out: list
        x = [i for i in inputs]
        # [stem, layer1, layer2, layer3, layer4, input_image]
        # h: 1/2, 1/4, 1/8, 1/8, 1/8, 1

        assert isinstance(x, list)
        bs, c, h, w = x[self.feature_resize_index].shape
        resize_to = (h, w)  # TODO: might be too large

        # Semantic Edge Stream
        side1 = self.side1(x[0], resize_to)  # (B, 1, H, W)
        side2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
        side3 = self.side3(x[2], resize_to)  # (B, 1, H, W)
        side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)
        fused_edges = self.fuse([side1, side2, side3, side5])

        # FCN
        fcn_x = x[-2]  # use layer 4
        fcn_feats = self.convs(fcn_x)
        if self.concat_input:
            fcn_feats = self.conv_cat(torch.cat([fcn_x, fcn_feats], dim=1))
        output = self.cls_seg(fcn_feats)

        return (
            output,
            dict(side1=side1, side2=side2, side3=side3),
            dict(fuse=fused_edges, side5=side5),
        )


@HEADS.register_module()
class DFFFCNMHJSBHead(BaseManyEdgeDecodeHead):
    def __init__(
        self,
        num_convs=2,
        kernel_size=3,
        concat_input=True,
        dilation=1,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_multilabel_edge=loss_multilabel_edge,
            **kwargs,
        )

        # changes which feature to `resize_to`
        self.feature_resize_index = feature_resize_index

        _interp = "bilinear"  # nearest
        _bias = True  # turn on?

        # Sides 1, 2, 3, 5 and Side 5 Weight
        self.side1 = SideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side2 = SideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side3 = SideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = SideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5_w = SideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes * 4,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,  # might not need?
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.ada_learner = LocationAdaptiveLearner(
            in_channels=self.num_classes * 4,
            out_channels=self.num_classes * 4,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        # --> mmseg
        assert num_convs >= 0 and dilation > 0 and isinstance(dilation, int)
        self.num_convs = num_convs
        self.concat_input = concat_input
        self.kernel_size = kernel_size

        fcn_in_channels = self.in_channels[-1]

        if num_convs == 0:
            assert fcn_in_channels == self.channels

        conv_padding = (kernel_size // 2) * dilation
        convs = []
        for i in range(num_convs):
            _in_channels = fcn_in_channels if i == 0 else self.channels
            convs.append(
                ConvModule(
                    _in_channels,
                    self.channels,
                    kernel_size=kernel_size,
                    padding=conv_padding,
                    dilation=dilation,
                    conv_cfg=self.conv_cfg,
                    norm_cfg=self.norm_cfg,
                    act_cfg=self.act_cfg,
                )
            )

        if len(convs) == 0:
            self.convs = nn.Identity()
        else:
            self.convs = nn.Sequential(*convs)
        if self.concat_input:
            self.conv_cat = ConvModule(
                fcn_in_channels + self.channels,
                self.channels,
                kernel_size=kernel_size,
                padding=kernel_size // 2,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )

    def forward(self, inputs):
        """Forward function"""

        # x = self._transform_inputs(inputs)  # out: list
        x = [i for i in inputs]
        # [stem, layer1, layer2, layer3, layer4, input_image]
        # h: 1/2, 1/4, 1/8, 1/8, 1/8, 1

        assert isinstance(x, list)
        bs, c, h, w = x[self.feature_resize_index].shape
        resize_to = (h, w)  # TODO: might be too large

        # Semantic Edge Side Stream
        side1 = self.side1(x[0], resize_to)  # (B, 1, H, W)
        side2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
        side3 = self.side3(x[2], resize_to)  # (B, 1, H, W)
        side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)
        side5_w = self.side5_w(x[4], resize_to)  # (B, 19*4, H, W)
        fused_edges = self.ada_learner([side1, side2, side3, side5, side5_w])

        # FCN
        fcn_x = x[-2]  # use layer 4
        fcn_feats = self.convs(fcn_x)
        if self.concat_input:
            fcn_feats = self.conv_cat(torch.cat([fcn_x, fcn_feats], dim=1))
        output = self.cls_seg(fcn_feats)

        return (
            output,
            dict(side1=side1, side2=side2, side3=side3),
            dict(fuse=fused_edges, side5=side5),
        )
