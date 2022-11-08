#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule
from mmcv.runner import force_fp32
from mmseg.ops import resize

from potato.models.builder import HEADS, build_edge_loss
from potato.models.utils import maskgrad
from .manyedge_decode_head import BaseManyEdgeDecodeHead


class PatchContext(nn.Module):
    """PatchContext Module

    Input image ->
        make pyramid patches (avgpool)s ->
        conv ->
        sum ->
        element wise sum on original feature


    Original Paper:
    - I don't think they added any bn or activations
    """

    def __init__(self, channels, patch_sizes=(1, 3, 5, 7), **kwargs):
        super().__init__()
        assert isinstance(patch_sizes, (list, tuple))
        assert len(patch_sizes) > 0

        self.patch_sizes = patch_sizes

        modules = []
        for patch in patch_sizes:
            if isinstance(patch, int):
                patch = (patch, patch)
            assert isinstance(patch, (list, tuple))
            assert len(patch) == 2
            modules.append(
                nn.Sequential(
                    nn.AdaptiveAvgPool2d(patch),
                    ConvModule(
                        in_channels=channels,
                        out_channels=channels,
                        kernel_size=patch,
                        **kwargs,
                    ),
                )
            )
        self.patch_convs = nn.ModuleList(modules)

    def forward(self, x):
        b, c, h, w = x.shape
        ps = []
        for pconv in self.patch_convs:
            xi = pconv(x)  # (b, c, 1, 1)
            ps.append(xi)

        ps = torch.stack(ps, dim=0).sum(dim=0)
        return x + ps.repeat(1, 1, h, w)


class PCM(nn.Module):
    """Pyramid Context Module

    Seems like bn+relu in PatchContext stabilizes the training
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        num_inputs,
        patch_sizes=(1, 3, 5, 7),
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
    ):
        super().__init__()

        # lowest -> 4 inputs
        # second -> 3 inputs
        # top -> 2 inputs

        # levels
        # res4 -> l0
        # res2 -> l1
        # res1 -> l2

        # each level will have 3x3 conv (bn + relu)
        self.convs = torch.nn.ModuleList(
            [
                ConvModule(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=3,
                    padding=1,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                    act_cfg=act_cfg,
                )
                for _ in range(num_inputs)
            ]
        )

        if num_inputs > 1:
            pc_kwargs = dict(
                channels=out_channels,
                patch_sizes=patch_sizes,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                bias=False,
                act_cfg=act_cfg,
            )

            # only l0 inputs
            # apply PatchContext to `l0 s-2
            patch_contexts = [PatchContext(**pc_kwargs)]

            if num_inputs == 3:
                # l0 and l1
                # apply PatchContext to `l0 s-1` and `l1 s-2`
                patch_contexts.append(PatchContext(**pc_kwargs))
            elif num_inputs == 4:
                # l0, l1, and l2
                # apply PatchContext to `l0 s-1`, `l1 s-1`, and `l2 s-2`
                patch_contexts.extend(
                    [
                        PatchContext(**pc_kwargs),
                        PatchContext(**pc_kwargs),
                    ]
                )
            self.patch_contexts = nn.ModuleList(patch_contexts)
        else:
            self.patch_contexts = None

    def forward(self, x):
        assert isinstance(x, (list, tuple))

        xs = []
        for xi, conv in zip(x, self.convs):
            xi = conv(xi)
            xs.append(xi)

        if len(xs) == 1:
            return xs[0]

        # assume that `s-2` is the top
        s2 = xs.pop(0)
        _, _, H, W = s2.shape

        outs = []
        for xi, pconv in zip(xs, self.patch_contexts):
            xi = pconv(xi)

            _, _, h, w = xi.shape
            if h < H or w < W:
                xi = resize(xi, (H, W), mode="bilinear", align_corners=False)

            xi = s2 * xi
            outs.append(xi)

        outs = torch.stack(outs, dim=0).sum(dim=0)
        s2 = s2 + outs
        return s2


class Step(nn.Module):
    def __init__(
        self,
        channels,
        patch_sizes,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
    ):
        super().__init__()
        modules = [
            PCM(
                in_channels=channels,
                out_channels=channels,
                num_inputs=i + 2,
                patch_sizes=patch_sizes,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=act_cfg,
            )
            for i in range(3)
        ]
        self.pcms = nn.ModuleList(modules)

    def forward(self, s2, s1):
        # l2 -> l0
        outs = []
        for i, l_s2 in enumerate(reversed(s2)):
            l = 3 - (i + 1)
            inputs = (l_s2, *s1[l:])  # `s-2` is always the first
            outs.append(self.pcms[i](inputs))

        return tuple(reversed(outs))


@HEADS.register_module()
class RPCHead(BaseManyEdgeDecodeHead):
    def __init__(
        self,
        num_steps=4,
        patch_sizes=[1, 3, 5, 7],
        edge_key="edge",
        log_edge_keys=["edge"],
        loss_duality=dict(type="DualityLoss", loss_weight=1.0),
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            multilabel_edge_keys=["edge"],
            no_conv_seg=True,
            **kwargs,
        )

        assert num_steps > 1

        self.side1 = ConvModule(
            in_channels=self.in_channels[0],
            out_channels=self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.side2 = ConvModule(
            in_channels=self.in_channels[1],
            out_channels=self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            act_cfg=self.act_cfg,
        )
        self.side3 = ConvModule(
            in_channels=self.in_channels[2],
            out_channels=self.channels,
            kernel_size=3,
            padding=1,
            conv_cfg=self.conv_cfg,
            act_cfg=self.act_cfg,
        )

        self.s1_l0 = PCM(
            in_channels=self.channels,
            out_channels=self.channels,
            num_inputs=1,
            patch_sizes=patch_sizes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.s1_l1 = PCM(
            in_channels=self.channels,
            out_channels=self.channels,
            num_inputs=2,
            patch_sizes=patch_sizes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.s1_l2 = PCM(
            in_channels=self.channels,
            out_channels=self.channels,
            num_inputs=3,
            patch_sizes=patch_sizes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        if num_steps - 2 > 0:
            self.steps = nn.ModuleList(
                [
                    Step(
                        channels=self.channels,
                        patch_sizes=patch_sizes,
                        conv_cfg=self.conv_cfg,
                        norm_cfg=self.norm_cfg,
                        act_cfg=self.act_cfg,
                    )
                    for _ in range(num_steps - 2)
                ]
            )
        else:
            self.steps = None

        self.last_step = PCM(
            in_channels=self.channels,
            out_channels=self.channels,
            num_inputs=4,
            patch_sizes=patch_sizes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        # self.prob_conv = nn.ModuleList(
        #     nn.Conv2d(self.channels, self.num_classes, kernel_size=1) for _ in range(num_steps)
        # )
        self.edge_prob = nn.Conv2d(self.channels, self.num_classes, kernel_size=1)
        self.seg_prob = nn.Conv2d(self.channels, self.num_classes, kernel_size=1)
        self.grouped_edge_conv = nn.Conv2d(
            self.num_classes * 2,
            self.num_classes,
            kernel_size=1,
            groups=self.num_classes,
        )

        self.dual_loss = build_edge_loss(loss_duality)

    def forward(self, inputs):
        """Forward function"""

        # [layer1, layer2, layer3, layer4]: 1/4, 1/8, 1/16, 1/16
        x1, x2, x3, x4 = [i for i in inputs]

        b1 = self.side1(x1)
        b2 = self.side2(x2)
        b3 = self.side3(x4)

        # run first step
        s2 = (b1, b2, b3)
        s1_l0 = self.s1_l0((b3,))
        s1_l1 = self.s1_l1((b2, b3))
        s1_l2 = self.s1_l2((b1, b2, b3))
        s1 = (s1_l2, s1_l1, s1_l0)
        outs = [s1_l2]

        if self.steps is not None:
            for step in self.steps:
                # unless the tensors of s2 are changed inplace, it should be fine
                b1, b2, b3 = s1
                s1 = step(s2, s1)
                s2 = (b1, b2, b3)
                outs.append(s1[0])

        final = self.last_step((s2[0], *s1))
        outs.append(final)

        segs = []
        edges = []
        # for i, (out, fconv) in enumerate(zip(outs, self.prob_conv)):
        #     if i % 2 == 0:
        #         # even output is for segmentation
        #         segs.append(fconv(out))
        #     else:
        #         # odd output is for edge
        #         edges.append(fconv(out))
        for i, out in enumerate(outs):
            if i % 2 == 0:
                segs.append(out)
            else:
                edges.append(out)

        # TODO: do deep supervision later
        seg = self.seg_prob(segs[-1])
        edge = self.edge_prob(edges[-1])

        mask_edge = maskgrad(
            seg_map=seg,
            sensitivity=100,
        )
        # edge = torch.relu(edge)

        # sliced concatenation and k-grouped convolution
        hold = []
        for c in range(edge.size(1)):
            hold.append(edge[:, c, ...].unsqueeze(1))
            hold.append(mask_edge[:, c, ...].unsqueeze(1))
        edge = torch.cat(hold, dim=1)
        edge = self.grouped_edge_conv(edge)  # logits

        return (seg, dict(edge=edge), mask_edge)

    def forward_train(
        self, inputs, img_metas, gt_semantic_seg, gt_semantic_edge, train_cfg
    ):
        seg_logits, semantic_edge_logits, mask_edge = self(inputs)

        losses = self.seg_losses(
            seg_logit=seg_logits,
            seg_label=gt_semantic_seg,
        )
        losses.update(
            self.multilabel_edge_losses(
                edge_logit=semantic_edge_logits,
                edge_label=gt_semantic_edge,
            )
        )
        losses.update(
            self.compute_dual_loss(
                edge_logit=semantic_edge_logits,
                maskgrad_prob=mask_edge,
            )
        )
        return losses

    def forward_test(self, inputs, img_metas, test_cfg, return_edge=False, **kwargs):
        seg, semantic_edge, mask_edge = self(inputs)
        if return_edge:
            edge = None
            if isinstance(semantic_edge, dict):
                edge = semantic_edge.get(self.edge_key, None)
            assert edge is not None, f"could not find {self.edge_key}"
            return dict(seg=seg, edge=edge)
        else:
            return dict(seg=seg)

    @force_fp32(apply_to=("edge_logit", "maskgrad_prob"))
    def compute_dual_loss(self, edge_logit, maskgrad_prob):
        edge_logit = edge_logit["edge"]
        return {
            self.dual_loss.loss_name: self.dual_loss(
                edge_logit=edge_logit,
                maskgrad=maskgrad_prob,
            )
        }
