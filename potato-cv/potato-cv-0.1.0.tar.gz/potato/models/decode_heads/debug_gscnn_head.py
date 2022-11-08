#!/usr/bin/env python3

"""Debug Multilabel GSCNN

GSCNN that outputs semantic boundaries
"""

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule, DepthwiseSeparableConvModule
from mmseg.ops import resize
from mmseg.models.decode_heads.sep_aspp_head import DepthwiseSeparableASPPModule

from potato.models.builder import HEADS
from potato.models.utils import maskgrad
from potato.ops.canny_edge import UnNormalizedCanny
from potato.ops.torch_canny_edge import TorchUnNormalizedSoftCanny
from .maskgrad_decode_head import BaseMaskGradMultiTaskHead
from ..utils import ResNetGSCNNShapeStream


@HEADS.register_module()
class DebugGSCNNHead(BaseMaskGradMultiTaskHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        loss_edge=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        cv2_canny=False,
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            binary_edge=False,
            loss_edge=loss_edge,
            **kwargs,
        )

        _interp = "bilinear"

        # Shape stream
        self.shape_stream = ResNetGSCNNShapeStream(
            in_channels=self.in_channels,
            num_classes=self.num_classes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )

        self.cw = ConvModule(
            in_channels=self.num_classes + 1,  # shape + canny
            out_channels=self.num_classes,
            kernel_size=1,
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
        self.bottleneck = ConvModule(
            (len(dilations) + 2) * self.channels,  # add edge
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

        if cv2_canny:
            # cv2, fast, non-differentiable
            self.canny = UnNormalizedCanny()
        else:
            # torch, a bit slower, differentiable, no hysteresis
            self.canny = TorchUnNormalizedSoftCanny()

        if self.mask_grad:
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
        assert len(x) == 6

        bs, c, h, w = x[-1].shape
        resize_to = (h, w)  # TODO: might be too large

        edge_out = self.shape_stream(x)
        edge = resize(
            edge_out,  # removed sigmoid here
            size=resize_to,
            mode="bilinear",
            align_corners=self.align_corners,
        )
        canny = self.canny(x[-1])
        edge_cat = torch.cat((edge, canny), dim=1)
        edge_feat = self.cw(edge_cat)
        edge_feat = resize(
            edge_feat,
            size=x[4].size()[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        # aspp
        aspp_outs = [
            resize(
                self.image_pool(x[4]),
                size=x[4].size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        aspp_outs.append(self.aspp_edge_conv(edge_feat))
        aspp_outs.extend(self.aspp_modules(x[4]))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)

        # bottom
        c1_output = self.c1_bottleneck(x[1])
        output = resize(
            input=output,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        output = torch.cat([output, c1_output], dim=1)
        output = self.sep_bottleneck(output)
        output = self.cls_seg(output)

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
            for c in range(edge_out.size(1)):
                hold.append(edge_out[:, c, ...].unsqueeze(1))
                hold.append(mask_edge[:, c, ...].unsqueeze(1))
            edge = torch.cat(hold, dim=1)
            edge = self.grouped_edge_conv(edge)  # logits

            bin_edge = dict()
            sem_edge = dict(edge=edge)
            return output, bin_edge, sem_edge, mask_edge
        else:
            bin_edge = dict()
            sem_edge = dict(edge=edge_out)
            return output, bin_edge, sem_edge
