#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule, DepthwiseSeparableConvModule, build_activation_layer
from mmseg.ops import resize
from mmseg.models.decode_heads.sep_aspp_head import DepthwiseSeparableASPPModule
from blette.models.utils import LocationAdaptiveLearner

from potato.models.builder import HEADS
from potato.models.utils import maskgrad
from .maskgrad_decode_head import BaseMaskGradManyEdgeHead


@HEADS.register_module()
class TSJSBHead(BaseMaskGradManyEdgeHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        edge_key="fuse",
        log_edge_keys=["fuse"],
        binary_edge_keys=[],
        multilabel_edge_keys=["fuse", "side5"],
        loss_binary_edge=None,
        loss_multilabel_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        mask_grad=True,
        loss_mask_edge=None,
        **kwargs,
    ):
        super(TSJSBHead, self).__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            binary_edge_keys=binary_edge_keys,
            multilabel_edge_keys=multilabel_edge_keys,
            loss_binary_edge=loss_binary_edge,
            loss_multilabel_edge=loss_multilabel_edge,
            mask_grad=mask_grad,
            loss_mask_edge=loss_mask_edge,
            **kwargs,
        )

        # DFF-like side outputs
        self.side_r0 = ConvModule(
            in_channels=self.in_channels[0],
            out_channels=1,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side_r1 = ConvModule(
            in_channels=self.in_channels[1],
            out_channels=1,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side_r2 = ConvModule(
            in_channels=self.in_channels[2],
            out_channels=1,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.side_r4 = ConvModule(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )
        self.weight_r4 = ConvModule(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes * 4,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=None,
        )

        # adaptive weight learner
        self.ada_learner = LocationAdaptiveLearner(
            self.num_classes * 4,
            self.num_classes * 4,
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

        # TODO: which is better?
        # fuse in bottleneck
        # fuse in sep_bottleneck

        # fused bottleneck
        self.bottleneck = ConvModule(
            (len(dilations) + 1) * self.channels,
            self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.sep_bottleneck = nn.Sequential(
            DepthwiseSeparableConvModule(
                in_channels=self.channels + c1_channels + self.num_classes,
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

        self.activate = build_activation_layer(self.act_cfg)

        if mask_grad:
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
        bs, c, h, w = x[-1].shape
        resize_to = (h, w)  # TODO: might be too large

        s0 = resize(  # (B, 1, H, W)
            self.side_r0(x[0]),
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s1 = resize(  # (B, 1, H, W)
            self.side_r1(x[1]),
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s2 = resize(  # (B, 1, H, W)
            self.side_r2(x[2]),
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s4_out = self.side_r4(x[4])
        s4 = resize(  # (B, 19, H, W)
            s4_out,
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        s4_w = resize(  # (B, 19*4, H, W)
            self.weight_r4(x[4]),
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )

        # refine aspp with edge features
        aspp_outs = [
            resize(
                self.image_pool(x[4]),
                size=x[4].size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        # aspp_outs.append(s4)  # add edge feature (s4_out)
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
        s4_out = resize(
            # input=self.activate(s4_out),  # activation here
            input=s4_out,  # activation here
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        # fuse backbone and edge features
        output = torch.cat([output, c1_output, s4_out], dim=1)
        output = self.sep_bottleneck(output)

        # convert output
        output = self.cls_seg(output)

        # semantic edge detection
        # s4_w = self.activate(s4_w)  # NOTE: activation here (reduces metrics)
        ada_weights = self.ada_learner(s4_w)  # (B, 19, 4, H, W)
        slice4 = s4[:, 0:1, :, :]  # (B, 1, H, W)

        fused_edges = torch.cat((slice4, s0, s1, s2), 1)
        for i in range(s4.size(1) - 1):
            slice4 = s4[:, i + 1 : i + 2, :, :]  # (B, 1, H, W)
            fused_edges = torch.cat(
                (fused_edges, slice4, s0, s1, s2), 1
            )  # (B, 19*4, H, W)

        fused_edges = fused_edges.view(  # (B, 19, H, W)
            fused_edges.size(0),
            self.num_classes,
            -1,
            fused_edges.size(2),
            fused_edges.size(3),
        )
        # fused_edges = torch.mul(fused_edges, torch.sigmoid(ada_weights))
        fused_edges = torch.mul(fused_edges, ada_weights)
        fused_edges = torch.sum(fused_edges, 2)  # (B, 19, H, W)

        if self.mask_grad:
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
            return output, dict(fuse=edge, side4=s4), mask_edge
        else:
            return output, dict(fuse=fused_edges, side4=s4)
