#!/usr/bin/env python3

from mmcv.runner import force_fp32
from mmseg.ops import resize

from potato.models.builder import build_edge_loss
from .multitask_decode_head import BaseMultiTaskDecodeHead
from .manyedge_decode_head import BaseManyEdgeDecodeHead


class BaseMaskGradMultiTaskHead(BaseMultiTaskDecodeHead):
    def __init__(
        self,
        mask_grad=False,
        loss_mask_edge=dict(type="DualityLoss", loss_weight=1.0),
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.mask_grad = mask_grad
        if self.mask_grad:
            assert isinstance(loss_mask_edge, dict)
            self.mask_edge_loss = build_edge_loss(loss_mask_edge)

    @force_fp32(apply_to=("edge_logit", "maskgrad_prob"))
    def maskgrad_losses(self, edge_logit, maskgrad_prob):
        """Compute maskgrad loss."""
        edge_logit = resize(
            input=edge_logit,
            size=maskgrad_prob.shape[2:],  # (b, 19, h, w)
            mode="bilinear",
            align_corners=self.align_corners,
        )
        return {
            self.mask_edge_loss.loss_name: self.mask_edge_loss(
                edge_logit=edge_logit,
                maskgrad=maskgrad_prob,
            )
        }

    def forward_train(
        self, inputs, img_metas, gt_semantic_seg, gt_semantic_edge, train_cfg
    ):
        if self.mask_grad:
            seg_logit, edge_logit, maskgrad_edge = self(inputs)
        else:
            seg_logit, edge_logit = self(inputs)

        # assume that there are always seg_losses
        losses = self.seg_losses(
            seg_logit=seg_logit,
            seg_label=gt_semantic_seg,
        )
        if self.loss_edge is not None:
            losses.update(
                self.loss_edge(
                    edge_logit=edge_logit,
                    maskgrad_prob=maskgrad_edge,
                )
            )
        if self.loss_joint is not None:
            # FIXME: multilabel edges are not supported (buggy)
            losses.update(
                self.joint_losses(
                    seg_logit=seg_logit,
                    edge_logit=edge_logit,
                    seg_label=gt_semantic_seg,
                    edge_label=gt_semantic_edge,
                )
            )

        # compute losses for mask edge
        if self.mask_grad:
            if self.mask_edge_loss is not None:
                losses.update(
                    self.maskgrad_losses(
                        edge_logit=edge_logit,
                        maskgrad_prob=maskgrad_edge,
                    )
                )

        return losses

    def forward_test(self, inputs, img_metas, test_cfg, return_edge=False, **kwargs):
        if self.mask_grad:
            seg, edge, _ = self(inputs)
        else:
            seg, edge = self(inputs)
        if return_edge:
            return dict(seg=seg, edge=edge)
        else:
            return dict(seg=seg)


class BaseMaskGradManyEdgeHead(BaseManyEdgeDecodeHead):
    def __init__(
        self,
        mask_grad=False,
        loss_mask_edge=dict(type="DualityLoss", loss_weight=1.0),
        loss_mask_edge_key=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.mask_grad = mask_grad
        if self.mask_grad:
            assert loss_mask_edge_key is not None
            assert loss_mask_edge_key in self.multilabel_edge_keys
            assert isinstance(loss_mask_edge, dict)
            self.mask_edge_loss = build_edge_loss(loss_mask_edge)
            self.loss_mask_edge_key = loss_mask_edge_key

    @force_fp32(apply_to=("edge_logit", "maskgrad_prob"))
    def maskgrad_losses(self, edge_logit, maskgrad_prob):
        """Compute maskgrad loss."""
        edge_logit = resize(
            input=edge_logit,
            size=maskgrad_prob.shape[2:],  # (b, 19, h, w)
            mode="bilinear",
            align_corners=self.align_corners,
        )
        return {
            self.mask_edge_loss.loss_name: self.mask_edge_loss(
                edge_logit=edge_logit,
                maskgrad=maskgrad_prob,
            )
        }

    def forward_train(
        self, inputs, img_metas, gt_semantic_seg, gt_semantic_edge, train_cfg
    ):
        if self.mask_grad:
            seg_logits, binary_edge_logits, semantic_edge_logits, mask_edge = self(
                inputs
            )
        else:
            seg_logits, binary_edge_logits, semantic_edge_logits = self(inputs)

        # assume that there are always seg_losses
        losses = self.seg_losses(
            seg_logit=seg_logits,
            seg_label=gt_semantic_seg,
        )
        if self.loss_binary_edge is not None:
            losses.update(
                self.binary_edge_losses(
                    edge_logit=binary_edge_logits,
                    edge_label=gt_semantic_edge,
                )
            )
        if self.loss_multilabel_edge is not None:
            losses.update(
                self.multilabel_edge_losses(
                    edge_logit=semantic_edge_logits,
                    edge_label=gt_semantic_edge,
                )
            )
        if self.loss_joint is not None:
            edge_logit = semantic_edge_logits.get(self.loss_joint_edge_key, None)
            if edge_logit is None:
                edge_logit = binary_edge_logits.get(self.loss_joint_edge_key, None)
            assert edge_logit is not None
            losses.update(
                self.joint_losses(
                    seg_logit=seg_logits,
                    edge_logit=edge_logit,
                    seg_label=gt_semantic_seg,
                    edge_label=gt_semantic_edge,
                )
            )

        # compute losses for mask edge
        if self.mask_grad:
            edge_logit = semantic_edge_logits[self.loss_mask_edge_key]
            losses.update(
                self.maskgrad_losses(
                    edge_logit=edge_logit,
                    maskgrad_prob=mask_edge,
                )
            )

        return losses

    def forward_test(self, inputs, img_metas, test_cfg, return_edge=False, **kwargs):
        if self.mask_grad:
            seg, binary_edge, semantic_edge, _ = self(inputs)
        else:
            seg, binary_edge, semantic_edge = self(inputs)
        if return_edge:
            edge = None
            if isinstance(binary_edge, dict):
                edge = binary_edge.get(self.edge_key, None)
            if isinstance(semantic_edge, dict):
                edge = semantic_edge.get(self.edge_key, None)
            assert edge is not None, f"could not find {self.edge_key}"
            return dict(seg=seg, edge=edge)
        else:
            return dict(seg=seg)
