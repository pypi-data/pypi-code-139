#!/usr/bin/env python3

"""TSJSB with different semantic edge models"""

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule, DepthwiseSeparableConvModule
from mmseg.ops import resize
from mmseg.models.decode_heads.sep_aspp_head import DepthwiseSeparableASPPModule
from blette.models.utils import (
    LocationAdaptiveLearner,
    GroupedConvFuse,
    BasicBlockSideConv,
    SideConv,
)

from potato.models.builder import HEADS
from potato.models.utils import maskgrad
from .maskgrad_decode_head import BaseMaskGradManyEdgeHead


@HEADS.register_module()
class DDSTSJSBHead(BaseMaskGradManyEdgeHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        num_side_blocks=2,
        return_block_feat=False,
        edge_key="fuse",
        log_edge_keys=("fuse", "side1", "side2", "side3", "side4", "side5"),
        binary_edge_keys=("side1", "side2", "side3", "side4"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_joint_edge_key="side3",
        loss_binary_edge=dict(type="BinaryEdgeLoss", loss_weight=1.0),
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        mask_grad=True,
        loss_mask_edge=dict(type="DualityLoss", loss_weight=1.0),
        loss_mask_edge_key="side5",
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            binary_edge_keys=binary_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_joint_edge_key=loss_joint_edge_key,
            loss_binary_edge=loss_binary_edge,
            loss_multilabel_edge=loss_multilabel_edge,
            mask_grad=mask_grad,
            loss_mask_edge=loss_mask_edge,
            loss_mask_edge_key=loss_mask_edge_key,
            **kwargs,
        )

        # changes which feature to `resize_to`
        self.feature_resize_index = feature_resize_index
        self.return_block_feat = return_block_feat

        _interp = "bilinear"
        _bias = True

        # 1. Multi-label edge stream
        self.side1 = BasicBlockSideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            num_blocks=num_side_blocks,
            return_block_output=return_block_feat,
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
            return_block_output=return_block_feat,
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
            return_block_output=return_block_feat,
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
            return_block_output=return_block_feat,
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
            return_block_output=return_block_feat,
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

        if return_block_feat:
            self.aspp_edge_conv = ConvModule(
                in_channels=self.in_channels[4],
                out_channels=self.channels,
                kernel_size=1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )
            self.c1_edge_conv = ConvModule(
                in_channels=c1_in_channels,
                out_channels=c1_channels,
                kernel_size=1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )
        else:
            self.c1_edge_conv = None
            self.aspp_edge_conv = ConvModule(
                in_channels=self.num_classes,
                out_channels=self.channels,
                kernel_size=1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            )

        self.image_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            ConvModule(
                self.in_channels[4],
                self.channels,
                1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )
        self.aspp_modules = DepthwiseSeparableASPPModule(
            in_channels=self.in_channels[4],
            channels=self.channels,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.c1_bottleneck = ConvModule(
            in_channels=c1_in_channels,
            out_channels=c1_channels,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        # fused bottleneck
        self.bottleneck = ConvModule(
            (len(dilations) + 2) * self.channels,
            self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        if self.c1_edge_conv:
            in_channels = self.channels + c1_channels * 2
        else:
            in_channels = self.channels + c1_channels
        self.sep_bottleneck = nn.Sequential(
            DepthwiseSeparableConvModule(
                in_channels=in_channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
            DepthwiseSeparableConvModule(
                in_channels=self.channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )

        self.grouped_edge_conv = nn.Conv2d(
            in_channels=self.num_classes * 2,
            out_channels=self.num_classes,
            kernel_size=1,
            groups=self.num_classes,
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
        if self.return_block_feat:
            side1, _ = self.side1(x[0], resize_to)  # (B, 1, H, W)
            side2, b2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
            side3, _ = self.side3(x[2], resize_to)  # (B, 1, H, W)
            side4, _ = self.side4(x[3], resize_to)  # (B, 1, H, W)
            side5, b5 = self.side5(x[4], resize_to)  # (B, 19, H, W)
            aspp_edge_feat = self.aspp_edge_conv(b5)
        else:
            side1 = self.side1(x[0], resize_to)  # (B, 1, H, W)
            side2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
            side3 = self.side3(x[2], resize_to)  # (B, 1, H, W)
            side4 = self.side4(x[3], resize_to)  # (B, 1, H, W)
            side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)

        fused_edges = self.fuse([side1, side2, side3, side4, side5])

        if not self.return_block_feat:
            aspp_edge_feat = self.aspp_edge_conv(fused_edges)

        # refine aspp with edge features
        aspp_outs = [
            resize(
                self.image_pool(x[4]),
                size=x[4].size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        edge_feat = resize(
            aspp_edge_feat,
            size=x[4].size()[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        aspp_outs.append(edge_feat)
        aspp_outs.extend(self.aspp_modules(x[4]))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)
        c1_output = self.c1_bottleneck(x[1])
        output = resize(
            input=output,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        if self.c1_edge_conv:
            b2 = self.c1_edge_conv(b2)
            # fuse backbone and edge features
            output = torch.cat([output, c1_output, b2], dim=1)
        else:
            output = torch.cat([output, c1_output], dim=1)

        output = self.sep_bottleneck(output)

        # convert output
        output = self.cls_seg(output)

        # calculate mask gradient
        seg_out = resize(
            output,  # we want logits
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        mask_edge = maskgrad(
            seg_map=seg_out,
            sensitivity=100,
        )

        # sliced concatenation and k-grouped convolution
        hold = []
        for c in range(fused_edges.size(1)):
            hold.append(fused_edges[:, c, ...].unsqueeze(1))
            hold.append(mask_edge[:, c, ...].unsqueeze(1))
        edge = torch.cat(hold, dim=1)
        edge = self.grouped_edge_conv(edge)  # logits

        if self.mask_grad:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3, side4=side4),
                # dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
                mask_edge,
            )
        else:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3, side4=side4),
                # dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
            )


@HEADS.register_module()
class CASENetTSJSBHead(BaseMaskGradManyEdgeHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_joint_edge_key="side3",
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        mask_grad=True,
        loss_mask_edge=dict(type="DualityLoss", loss_weight=1.0),
        loss_mask_edge_key="side5",
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_joint_edge_key=loss_joint_edge_key,
            loss_multilabel_edge=loss_multilabel_edge,
            mask_grad=mask_grad,
            loss_mask_edge=loss_mask_edge,
            loss_mask_edge_key=loss_mask_edge_key,
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
        self.aspp_edge_conv = ConvModule(
            in_channels=self.num_classes,
            out_channels=self.channels,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        self.image_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            ConvModule(
                self.in_channels[4],
                self.channels,
                1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )
        self.aspp_modules = DepthwiseSeparableASPPModule(
            in_channels=self.in_channels[4],
            channels=self.channels,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.c1_bottleneck = ConvModule(
            in_channels=c1_in_channels,
            out_channels=c1_channels,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        # fused bottleneck
        self.bottleneck = ConvModule(
            (len(dilations) + 2) * self.channels,
            self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        self.sep_bottleneck = nn.Sequential(
            DepthwiseSeparableConvModule(
                in_channels=self.channels + c1_channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
            DepthwiseSeparableConvModule(
                in_channels=self.channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )

        self.grouped_edge_conv = nn.Conv2d(
            in_channels=self.num_classes * 2,
            out_channels=self.num_classes,
            kernel_size=1,
            groups=self.num_classes,
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
        fused_edges = self.fuse([side1, side2, side3, side5])
        aspp_edge_feat = self.aspp_edge_conv(fused_edges)

        # refine aspp with edge features
        aspp_outs = [
            resize(
                self.image_pool(x[4]),
                size=x[4].size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        edge_feat = resize(
            aspp_edge_feat,
            size=x[4].size()[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        aspp_outs.append(edge_feat)
        aspp_outs.extend(self.aspp_modules(x[4]))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)
        c1_output = self.c1_bottleneck(x[1])
        output = resize(
            input=output,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        output = torch.cat([output, c1_output], dim=1)
        output = self.sep_bottleneck(output)

        # convert output
        output = self.cls_seg(output)

        # calculate mask gradient
        seg_out = resize(
            output,  # we want logits
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        mask_edge = maskgrad(
            seg_map=seg_out,
            sensitivity=100,
        )

        # sliced concatenation and k-grouped convolution
        hold = []
        for c in range(fused_edges.size(1)):
            hold.append(fused_edges[:, c, ...].unsqueeze(1))
            hold.append(mask_edge[:, c, ...].unsqueeze(1))
        edge = torch.cat(hold, dim=1)
        edge = self.grouped_edge_conv(edge)  # logits

        if self.mask_grad:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
                mask_edge,
            )
        else:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
            )


@HEADS.register_module()
class DFFTSJSBHead(BaseMaskGradManyEdgeHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        multilabel_edge_keys=("fuse", "side5"),
        loss_joint_edge_key="side3",
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        mask_grad=True,
        loss_mask_edge=dict(type="DualityLoss", loss_weight=1.0),
        loss_mask_edge_key="side5",
        feature_resize_index=-1,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_joint_edge_key=loss_joint_edge_key,
            loss_multilabel_edge=loss_multilabel_edge,
            mask_grad=mask_grad,
            loss_mask_edge=loss_mask_edge,
            loss_mask_edge_key=loss_mask_edge_key,
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
        self.aspp_edge_conv = ConvModule(
            in_channels=self.num_classes,
            out_channels=self.channels,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        self.image_pool = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            ConvModule(
                self.in_channels[4],
                self.channels,
                1,
                conv_cfg=self.conv_cfg,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )
        self.aspp_modules = DepthwiseSeparableASPPModule(
            in_channels=self.in_channels[4],
            channels=self.channels,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.c1_bottleneck = ConvModule(
            in_channels=c1_in_channels,
            out_channels=c1_channels,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        # fused bottleneck
        self.bottleneck = ConvModule(
            (len(dilations) + 2) * self.channels,
            self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        self.sep_bottleneck = nn.Sequential(
            DepthwiseSeparableConvModule(
                in_channels=self.channels + c1_channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
            DepthwiseSeparableConvModule(
                in_channels=self.channels,
                out_channels=self.channels,
                kernel_size=3,
                padding=1,
                norm_cfg=self.norm_cfg,
                act_cfg=self.act_cfg,
            ),
        )

        self.grouped_edge_conv = nn.Conv2d(
            in_channels=self.num_classes * 2,
            out_channels=self.num_classes,
            kernel_size=1,
            groups=self.num_classes,
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
        aspp_edge_feat = self.aspp_edge_conv(fused_edges)

        # refine aspp with edge features
        aspp_outs = [
            resize(
                self.image_pool(x[4]),
                size=x[4].size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        edge_feat = resize(
            aspp_edge_feat,
            size=x[4].size()[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        aspp_outs.append(edge_feat)
        aspp_outs.extend(self.aspp_modules(x[4]))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)
        c1_output = self.c1_bottleneck(x[1])
        output = resize(
            input=output,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        output = torch.cat([output, c1_output], dim=1)
        output = self.sep_bottleneck(output)

        # convert output
        output = self.cls_seg(output)

        # calculate mask gradient
        seg_out = resize(
            output,  # we want logits
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        mask_edge = maskgrad(
            seg_map=seg_out,
            sensitivity=100,
        )

        # sliced concatenation and k-grouped convolution
        hold = []
        for c in range(fused_edges.size(1)):
            hold.append(fused_edges[:, c, ...].unsqueeze(1))
            hold.append(mask_edge[:, c, ...].unsqueeze(1))
        edge = torch.cat(hold, dim=1)
        edge = self.grouped_edge_conv(edge)  # logits

        if self.mask_grad:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
                mask_edge,
            )
        else:
            return (
                output,
                dict(side1=side1, side2=side2, side3=side3),
                dict(fuse=edge, side5=side5),
            )
