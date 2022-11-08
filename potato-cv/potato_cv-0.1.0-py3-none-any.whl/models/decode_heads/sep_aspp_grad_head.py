#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule, DepthwiseSeparableConvModule
from mmseg.ops import resize
from mmseg.models.decode_heads.decode_head import BaseDecodeHead
from mmseg.models.decode_heads.sep_aspp_head import DepthwiseSeparableASPPModule

from potato.models.builder import HEADS
from potato.ops.canny_edge import UnNormalizedCanny
from potato.ops.torch_canny_edge import TorchUnNormalizedSoftCanny


@HEADS.register_module()
class GradASPPHead(BaseDecodeHead):
    def __init__(
        self,
        dilations=(1, 6, 12, 18),
        c1_in_channels=256,
        c1_channels=48,
        cv2_canny=False,
        **kwargs,
    ):
        super().__init__(input_transform="multiple_select", **kwargs)

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
            (len(dilations) + 1) * self.channels + 1,  # add edge
            self.channels,
            3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.sep_bottleneck = nn.Sequential(
            DepthwiseSeparableConvModule(
                in_channels=self.channels + c1_channels + self.channels,
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

        self.cw = ConvModule(
            in_channels=1,
            out_channels=1,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=None,  # using sigmoid
        )
        self.edge_conv = ConvModule(
            in_channels=1,
            out_channels=self.channels,
            kernel_size=1,
            padding=0,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        if cv2_canny:
            # cv2, fast, non-differentiable
            self.canny = UnNormalizedCanny()
        else:
            # torch, a bit slower, differentiable, no hysteresis
            self.canny = TorchUnNormalizedSoftCanny()

    def forward(self, inputs):
        """Forward function"""

        # x = self._transform_inputs(inputs)  # out: list
        x = [i for i in inputs]
        # [stem, layer1, layer2, layer3, layer4, input_image]
        # h: 1/2, 1/4, 1/8, 1/8, 1/8, 1

        inp_bot = x[1]
        inp = x[4]

        # Canny Edge
        # FIXME: change this to image gradient
        canny = self.canny(x[-1])
        canny_feat = torch.sigmoid(self.cw(canny))  # remove sigmoid?
        deep_canny_feat = resize(
            canny_feat,
            size=inp.size()[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )

        aspp_outs = [
            resize(
                self.image_pool(inp),
                size=inp.size()[2:],
                mode="bilinear",
                align_corners=self.align_corners,
            )
        ]
        aspp_outs.append(deep_canny_feat)  # 1. introduce canny features
        aspp_outs.extend(self.aspp_modules(inp))
        aspp_outs = torch.cat(aspp_outs, dim=1)
        output = self.bottleneck(aspp_outs)
        c1_output = self.c1_bottleneck(inp_bot)
        output = resize(
            input=output,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        shallower_canny_feat = resize(
            input=canny_feat,
            size=c1_output.shape[2:],
            mode="bilinear",
            align_corners=self.align_corners,
        )
        sem_edge_feat = self.edge_conv(shallower_canny_feat)
        # 2. introduce canny features into shallower head
        output = torch.cat([output, c1_output, sem_edge_feat], dim=1)
        output = self.sep_bottleneck(output)
        output = self.cls_seg(output)

        return output
