# Copyright (c) OpenMMLab. All rights reserved.
from typing import List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import ConvModule
from torch import Tensor

from mmdet.models.layers import multiclass_nms
from mmdet.models.losses import accuracy
from mmdet.models.task_modules import SamplingResult
from mmdet.models.utils import multi_apply
from mmdet.registry import MODELS, TASK_UTILS
from mmdet.utils.typing import (ConfigDict, ConfigType, InstanceData,
                                InstanceList, OptConfigType, OptMultiConfig)
from .bbox_head import BBoxHead


@MODELS.register_module()
class SABLHead(BBoxHead):
    """Side-Aware Boundary Localization (SABL) for RoI-Head.

    Side-Aware features are extracted by conv layers
    with an attention mechanism.
    Boundary Localization with Bucketing and Bucketing Guided Rescoring
    are implemented in BucketingBBoxCoder.

    Please refer to https://arxiv.org/abs/1912.04260 for more details.

    Args:
        cls_in_channels (int): Input channels of cls RoI feature. \
            Defaults to 256.
        reg_in_channels (int): Input channels of reg RoI feature. \
            Defaults to 256.
        roi_feat_size (int): Size of RoI features. Defaults to 7.
        reg_feat_up_ratio (int): Upsample ratio of reg features. \
            Defaults to 2.
        reg_pre_kernel (int): Kernel of 2D conv layers before \
            attention pooling. Defaults to 3.
        reg_post_kernel (int): Kernel of 1D conv layers after \
            attention pooling. Defaults to 3.
        reg_pre_num (int): Number of pre convs. Defaults to 2.
        reg_post_num (int): Number of post convs. Defaults to 1.
        num_classes (int): Number of classes in dataset. Defaults to 80.
        cls_out_channels (int): Hidden channels in cls fcs. Defaults to 1024.
        reg_offset_out_channels (int): Hidden and output channel \
            of reg offset branch. Defaults to 256.
        reg_cls_out_channels (int): Hidden and output channel \
            of reg cls branch. Defaults to 256.
        num_cls_fcs (int): Number of fcs for cls branch. Defaults to 1.
        num_reg_fcs (int): Number of fcs for reg branch.. Defaults to 0.
        reg_class_agnostic (bool): Class agnostic regression or not. \
            Defaults to True.
        norm_cfg (dict): Config of norm layers. Defaults to None.
        bbox_coder (dict): Config of bbox coder. Defaults 'BucketingBBoxCoder'.
        loss_cls (dict): Config of classification loss.
        loss_bbox_cls (dict): Config of classification loss for bbox branch.
        loss_bbox_reg (dict): Config of regression loss for bbox branch.
        init_cfg (dict or list[dict], optional): Initialization config dict.
            Defaults to None.
    """

    def __init__(self,
                 num_classes: int,
                 cls_in_channels: int = 256,
                 reg_in_channels: int = 256,
                 roi_feat_size: int = 7,
                 reg_feat_up_ratio: int = 2,
                 reg_pre_kernel: int = 3,
                 reg_post_kernel: int = 3,
                 reg_pre_num: int = 2,
                 reg_post_num: int = 1,
                 cls_out_channels: int = 1024,
                 reg_offset_out_channels: int = 256,
                 reg_cls_out_channels: int = 256,
                 num_cls_fcs: int = 1,
                 num_reg_fcs: int = 0,
                 reg_class_agnostic: bool = True,
                 norm_cfg: OptConfigType = None,
                 bbox_coder: ConfigType = dict(
                     type='BucketingBBoxCoder',
                     num_buckets=14,
                     scale_factor=1.7),
                 loss_cls: ConfigType = dict(
                     type='CrossEntropyLoss',
                     use_sigmoid=False,
                     loss_weight=1.0),
                 loss_bbox_cls: ConfigType = dict(
                     type='CrossEntropyLoss',
                     use_sigmoid=True,
                     loss_weight=1.0),
                 loss_bbox_reg: ConfigType = dict(
                     type='SmoothL1Loss', beta=0.1, loss_weight=1.0),
                 init_cfg: OptMultiConfig = None) -> None:
        super(BBoxHead, self).__init__(init_cfg=init_cfg)
        self.cls_in_channels = cls_in_channels
        self.reg_in_channels = reg_in_channels
        self.roi_feat_size = roi_feat_size
        self.reg_feat_up_ratio = int(reg_feat_up_ratio)
        self.num_buckets = bbox_coder['num_buckets']
        assert self.reg_feat_up_ratio // 2 >= 1
        self.up_reg_feat_size = roi_feat_size * self.reg_feat_up_ratio
        assert self.up_reg_feat_size == bbox_coder['num_buckets']
        self.reg_pre_kernel = reg_pre_kernel
        self.reg_post_kernel = reg_post_kernel
        self.reg_pre_num = reg_pre_num
        self.reg_post_num = reg_post_num
        self.num_classes = num_classes
        self.cls_out_channels = cls_out_channels
        self.reg_offset_out_channels = reg_offset_out_channels
        self.reg_cls_out_channels = reg_cls_out_channels
        self.num_cls_fcs = num_cls_fcs
        self.num_reg_fcs = num_reg_fcs
        self.reg_class_agnostic = reg_class_agnostic
        assert self.reg_class_agnostic
        self.norm_cfg = norm_cfg

        self.bbox_coder = TASK_UTILS.build(bbox_coder)
        self.loss_cls = MODELS.build(loss_cls)
        self.loss_bbox_cls = MODELS.build(loss_bbox_cls)
        self.loss_bbox_reg = MODELS.build(loss_bbox_reg)

        self.cls_fcs = self._add_fc_branch(self.num_cls_fcs,
                                           self.cls_in_channels,
                                           self.roi_feat_size,
                                           self.cls_out_channels)

        self.side_num = int(np.ceil(self.num_buckets / 2))

        if self.reg_feat_up_ratio > 1:
            self.upsample_x = nn.ConvTranspose1d(
                reg_in_channels,
                reg_in_channels,
                self.reg_feat_up_ratio,
                stride=self.reg_feat_up_ratio)
            self.upsample_y = nn.ConvTranspose1d(
                reg_in_channels,
                reg_in_channels,
                self.reg_feat_up_ratio,
                stride=self.reg_feat_up_ratio)

        self.reg_pre_convs = nn.ModuleList()
        for i in range(self.reg_pre_num):
            reg_pre_conv = ConvModule(
                reg_in_channels,
                reg_in_channels,
                kernel_size=reg_pre_kernel,
                padding=reg_pre_kernel // 2,
                norm_cfg=norm_cfg,
                act_cfg=dict(type='ReLU'))
            self.reg_pre_convs.append(reg_pre_conv)

        self.reg_post_conv_xs = nn.ModuleList()
        for i in range(self.reg_post_num):
            reg_post_conv_x = ConvModule(
                reg_in_channels,
                reg_in_channels,
                kernel_size=(1, reg_post_kernel),
                padding=(0, reg_post_kernel // 2),
                norm_cfg=norm_cfg,
                act_cfg=dict(type='ReLU'))
            self.reg_post_conv_xs.append(reg_post_conv_x)
        self.reg_post_conv_ys = nn.ModuleList()
        for i in range(self.reg_post_num):
            reg_post_conv_y = ConvModule(
                reg_in_channels,
                reg_in_channels,
                kernel_size=(reg_post_kernel, 1),
                padding=(reg_post_kernel // 2, 0),
                norm_cfg=norm_cfg,
                act_cfg=dict(type='ReLU'))
            self.reg_post_conv_ys.append(reg_post_conv_y)

        self.reg_conv_att_x = nn.Conv2d(reg_in_channels, 1, 1)
        self.reg_conv_att_y = nn.Conv2d(reg_in_channels, 1, 1)

        self.fc_cls = nn.Linear(self.cls_out_channels, self.num_classes + 1)
        self.relu = nn.ReLU(inplace=True)

        self.reg_cls_fcs = self._add_fc_branch(self.num_reg_fcs,
                                               self.reg_in_channels, 1,
                                               self.reg_cls_out_channels)
        self.reg_offset_fcs = self._add_fc_branch(self.num_reg_fcs,
                                                  self.reg_in_channels, 1,
                                                  self.reg_offset_out_channels)
        self.fc_reg_cls = nn.Linear(self.reg_cls_out_channels, 1)
        self.fc_reg_offset = nn.Linear(self.reg_offset_out_channels, 1)

        if init_cfg is None:
            self.init_cfg = [
                dict(
                    type='Xavier',
                    layer='Linear',
                    distribution='uniform',
                    override=[
                        dict(type='Normal', name='reg_conv_att_x', std=0.01),
                        dict(type='Normal', name='reg_conv_att_y', std=0.01),
                        dict(type='Normal', name='fc_reg_cls', std=0.01),
                        dict(type='Normal', name='fc_cls', std=0.01),
                        dict(type='Normal', name='fc_reg_offset', std=0.001)
                    ])
            ]
            if self.reg_feat_up_ratio > 1:
                self.init_cfg += [
                    dict(
                        type='Kaiming',
                        distribution='normal',
                        override=[
                            dict(name='upsample_x'),
                            dict(name='upsample_y')
                        ])
                ]

    def _add_fc_branch(self, num_branch_fcs: int, in_channels: int,
                       roi_feat_size: int,
                       fc_out_channels: int) -> nn.ModuleList:
        """build fc layers."""
        in_channels = in_channels * roi_feat_size * roi_feat_size
        branch_fcs = nn.ModuleList()
        for i in range(num_branch_fcs):
            fc_in_channels = (in_channels if i == 0 else fc_out_channels)
            branch_fcs.append(nn.Linear(fc_in_channels, fc_out_channels))
        return branch_fcs

    def cls_forward(self, cls_x: Tensor) -> Tensor:
        """forward of classification fc layers."""
        cls_x = cls_x.view(cls_x.size(0), -1)
        for fc in self.cls_fcs:
            cls_x = self.relu(fc(cls_x))
        cls_score = self.fc_cls(cls_x)
        return cls_score

    def attention_pool(self, reg_x: Tensor) -> tuple:
        """Extract direction-specific features fx and fy with attention
        methanism."""
        reg_fx = reg_x
        reg_fy = reg_x
        reg_fx_att = self.reg_conv_att_x(reg_fx).sigmoid()
        reg_fy_att = self.reg_conv_att_y(reg_fy).sigmoid()
        reg_fx_att = reg_fx_att / reg_fx_att.sum(dim=2).unsqueeze(2)
        reg_fy_att = reg_fy_att / reg_fy_att.sum(dim=3).unsqueeze(3)
        reg_fx = (reg_fx * reg_fx_att).sum(dim=2)
        reg_fy = (reg_fy * reg_fy_att).sum(dim=3)
        return reg_fx, reg_fy

    def side_aware_feature_extractor(self, reg_x: Tensor) -> tuple:
        """Refine and extract side-aware features without split them."""
        for reg_pre_conv in self.reg_pre_convs:
            reg_x = reg_pre_conv(reg_x)
        reg_fx, reg_fy = self.attention_pool(reg_x)

        if self.reg_post_num > 0:
            reg_fx = reg_fx.unsqueeze(2)
            reg_fy = reg_fy.unsqueeze(3)
            for i in range(self.reg_post_num):
                reg_fx = self.reg_post_conv_xs[i](reg_fx)
                reg_fy = self.reg_post_conv_ys[i](reg_fy)
            reg_fx = reg_fx.squeeze(2)
            reg_fy = reg_fy.squeeze(3)
        if self.reg_feat_up_ratio > 1:
            reg_fx = self.relu(self.upsample_x(reg_fx))
            reg_fy = self.relu(self.upsample_y(reg_fy))
        reg_fx = torch.transpose(reg_fx, 1, 2)
        reg_fy = torch.transpose(reg_fy, 1, 2)
        return reg_fx.contiguous(), reg_fy.contiguous()

    def reg_pred(self, x: Tensor, offset_fcs: nn.ModuleList,
                 cls_fcs: nn.ModuleList) -> tuple:
        """Predict bucketing estimation (cls_pred) and fine regression (offset
        pred) with side-aware features."""
        x_offset = x.view(-1, self.reg_in_channels)
        x_cls = x.view(-1, self.reg_in_channels)

        for fc in offset_fcs:
            x_offset = self.relu(fc(x_offset))
        for fc in cls_fcs:
            x_cls = self.relu(fc(x_cls))
        offset_pred = self.fc_reg_offset(x_offset)
        cls_pred = self.fc_reg_cls(x_cls)

        offset_pred = offset_pred.view(x.size(0), -1)
        cls_pred = cls_pred.view(x.size(0), -1)

        return offset_pred, cls_pred

    def side_aware_split(self, feat: Tensor) -> Tensor:
        """Split side-aware features aligned with orders of bucketing
        targets."""
        l_end = int(np.ceil(self.up_reg_feat_size / 2))
        r_start = int(np.floor(self.up_reg_feat_size / 2))
        feat_fl = feat[:, :l_end]
        feat_fr = feat[:, r_start:].flip(dims=(1, ))
        feat_fl = feat_fl.contiguous()
        feat_fr = feat_fr.contiguous()
        feat = torch.cat([feat_fl, feat_fr], dim=-1)
        return feat

    def bbox_pred_split(self, bbox_pred: tuple,
                        num_proposals_per_img: Sequence[int]) -> tuple:
        """Split batch bbox prediction back to each image."""
        bucket_cls_preds, bucket_offset_preds = bbox_pred
        bucket_cls_preds = bucket_cls_preds.split(num_proposals_per_img, 0)
        bucket_offset_preds = bucket_offset_preds.split(
            num_proposals_per_img, 0)
        bbox_pred = tuple(zip(bucket_cls_preds, bucket_offset_preds))
        return bbox_pred

    def reg_forward(self, reg_x: Tensor) -> tuple:
        """forward of regression branch."""
        outs = self.side_aware_feature_extractor(reg_x)
        edge_offset_preds = []
        edge_cls_preds = []
        reg_fx = outs[0]
        reg_fy = outs[1]
        offset_pred_x, cls_pred_x = self.reg_pred(reg_fx, self.reg_offset_fcs,
                                                  self.reg_cls_fcs)
        offset_pred_y, cls_pred_y = self.reg_pred(reg_fy, self.reg_offset_fcs,
                                                  self.reg_cls_fcs)
        offset_pred_x = self.side_aware_split(offset_pred_x)
        offset_pred_y = self.side_aware_split(offset_pred_y)
        cls_pred_x = self.side_aware_split(cls_pred_x)
        cls_pred_y = self.side_aware_split(cls_pred_y)
        edge_offset_preds = torch.cat([offset_pred_x, offset_pred_y], dim=-1)
        edge_cls_preds = torch.cat([cls_pred_x, cls_pred_y], dim=-1)

        return edge_cls_preds, edge_offset_preds

    def forward(self, x: Tensor) -> tuple:
        """Forward features from the upstream network."""
        bbox_pred = self.reg_forward(x)
        cls_score = self.cls_forward(x)

        return cls_score, bbox_pred

    def get_targets(self,
                    sampling_results: List[SamplingResult],
                    rcnn_train_cfg: ConfigDict,
                    concat: bool = True) -> tuple:
        """Calculate the ground truth for all samples in a batch according to
        the sampling_results."""
        pos_proposals = [res.pos_bboxes for res in sampling_results]
        neg_proposals = [res.neg_bboxes for res in sampling_results]
        pos_gt_bboxes = [res.pos_gt_bboxes for res in sampling_results]
        pos_gt_labels = [res.pos_gt_labels for res in sampling_results]
        cls_reg_targets = self.bucket_target(
            pos_proposals,
            neg_proposals,
            pos_gt_bboxes,
            pos_gt_labels,
            rcnn_train_cfg,
            concat=concat)
        (labels, label_weights, bucket_cls_targets, bucket_cls_weights,
         bucket_offset_targets, bucket_offset_weights) = cls_reg_targets
        return (labels, label_weights, (bucket_cls_targets,
                                        bucket_offset_targets),
                (bucket_cls_weights, bucket_offset_weights))

    def bucket_target(self,
                      pos_proposals_list: list,
                      neg_proposals_list: list,
                      pos_gt_bboxes_list: list,
                      pos_gt_labels_list: list,
                      rcnn_train_cfg: ConfigDict,
                      concat: bool = True) -> tuple:
        """Compute bucketing estimation targets and fine regression targets for
        a batch of images."""
        (labels, label_weights, bucket_cls_targets, bucket_cls_weights,
         bucket_offset_targets, bucket_offset_weights) = multi_apply(
             self._bucket_target_single,
             pos_proposals_list,
             neg_proposals_list,
             pos_gt_bboxes_list,
             pos_gt_labels_list,
             cfg=rcnn_train_cfg)

        if concat:
            labels = torch.cat(labels, 0)
            label_weights = torch.cat(label_weights, 0)
            bucket_cls_targets = torch.cat(bucket_cls_targets, 0)
            bucket_cls_weights = torch.cat(bucket_cls_weights, 0)
            bucket_offset_targets = torch.cat(bucket_offset_targets, 0)
            bucket_offset_weights = torch.cat(bucket_offset_weights, 0)
        return (labels, label_weights, bucket_cls_targets, bucket_cls_weights,
                bucket_offset_targets, bucket_offset_weights)

    def _bucket_target_single(self, pos_proposals: Tensor,
                              neg_proposals: Tensor, pos_gt_bboxes: Tensor,
                              pos_gt_labels: Tensor, cfg: ConfigDict) -> tuple:
        """Compute bucketing estimation targets and fine regression targets for
        a single image.

        Args:
            pos_proposals (Tensor): positive proposals of a single image,
                 Shape (n_pos, 4)
            neg_proposals (Tensor): negative proposals of a single image,
                 Shape (n_neg, 4).
            pos_gt_bboxes (Tensor): gt bboxes assigned to positive proposals
                 of a single image, Shape (n_pos, 4).
            pos_gt_labels (Tensor): gt labels assigned to positive proposals
                 of a single image, Shape (n_pos, ).
            cfg (dict): Config of calculating targets

        Returns:
            tuple:

            - labels (Tensor): Labels in a single image. Shape (n,).
            - label_weights (Tensor): Label weights in a single image.
                Shape (n,)
            - bucket_cls_targets (Tensor): Bucket cls targets in
                a single image. Shape (n, num_buckets*2).
            - bucket_cls_weights (Tensor): Bucket cls weights in
                a single image. Shape (n, num_buckets*2).
            - bucket_offset_targets (Tensor): Bucket offset targets
                in a single image. Shape (n, num_buckets*2).
            - bucket_offset_targets (Tensor): Bucket offset weights
                in a single image. Shape (n, num_buckets*2).
        """
        num_pos = pos_proposals.size(0)
        num_neg = neg_proposals.size(0)
        num_samples = num_pos + num_neg
        labels = pos_gt_bboxes.new_full((num_samples, ),
                                        self.num_classes,
                                        dtype=torch.long)
        label_weights = pos_proposals.new_zeros(num_samples)
        bucket_cls_targets = pos_proposals.new_zeros(num_samples,
                                                     4 * self.side_num)
        bucket_cls_weights = pos_proposals.new_zeros(num_samples,
                                                     4 * self.side_num)
        bucket_offset_targets = pos_proposals.new_zeros(
            num_samples, 4 * self.side_num)
        bucket_offset_weights = pos_proposals.new_zeros(
            num_samples, 4 * self.side_num)
        if num_pos > 0:
            labels[:num_pos] = pos_gt_labels
            label_weights[:num_pos] = 1.0
            (pos_bucket_offset_targets, pos_bucket_offset_weights,
             pos_bucket_cls_targets,
             pos_bucket_cls_weights) = self.bbox_coder.encode(
                 pos_proposals, pos_gt_bboxes)
            bucket_cls_targets[:num_pos, :] = pos_bucket_cls_targets
            bucket_cls_weights[:num_pos, :] = pos_bucket_cls_weights
            bucket_offset_targets[:num_pos, :] = pos_bucket_offset_targets
            bucket_offset_weights[:num_pos, :] = pos_bucket_offset_weights
        if num_neg > 0:
            label_weights[-num_neg:] = 1.0
        return (labels, label_weights, bucket_cls_targets, bucket_cls_weights,
                bucket_offset_targets, bucket_offset_weights)

    def loss(self,
             cls_score: Tensor,
             bbox_pred: Tuple[Tensor, Tensor],
             rois: Tensor,
             labels: Tensor,
             label_weights: Tensor,
             bbox_targets: Tuple[Tensor, Tensor],
             bbox_weights: Tuple[Tensor, Tensor],
             reduction_override: Optional[str] = None) -> dict:
        """Calculate the loss based on the network predictions and targets.

        Args:
            cls_score (Tensor): Classification prediction
                results of all class, has shape
                (batch_size * num_proposals_single_image, num_classes)
            bbox_pred (Tensor): A tuple of regression prediction results
                containing `bucket_cls_preds and` `bucket_offset_preds`.
            rois (Tensor): RoIs with the shape
                (batch_size * num_proposals_single_image, 5) where the first
                column indicates batch id of each RoI.
            labels (Tensor): Gt_labels for all proposals in a batch, has
                shape (batch_size * num_proposals_single_image, ).
            label_weights (Tensor): Labels_weights for all proposals in a
                batch, has shape (batch_size * num_proposals_single_image, ).
            bbox_targets (Tuple[Tensor, Tensor]): A tuple of regression target
                containing `bucket_cls_targets` and `bucket_offset_targets`.
                the last dimension 4 represents [tl_x, tl_y, br_x, br_y].
            bbox_weights (Tuple[Tensor, Tensor]): A tuple of regression
                weights containing `bucket_cls_weights` and
                `bucket_offset_weights`.
            reduction_override (str, optional): The reduction
                method used to override the original reduction
                method of the loss. Options are "none",
                "mean" and "sum". Defaults to None,

        Returns:
            dict: A dictionary of loss.
        """
        losses = dict()
        if cls_score is not None:
            avg_factor = max(torch.sum(label_weights > 0).float().item(), 1.)
            losses['loss_cls'] = self.loss_cls(
                cls_score,
                labels,
                label_weights,
                avg_factor=avg_factor,
                reduction_override=reduction_override)
            losses['acc'] = accuracy(cls_score, labels)

        if bbox_pred is not None:
            bucket_cls_preds, bucket_offset_preds = bbox_pred
            bucket_cls_targets, bucket_offset_targets = bbox_targets
            bucket_cls_weights, bucket_offset_weights = bbox_weights
            # edge cls
            bucket_cls_preds = bucket_cls_preds.view(-1, self.side_num)
            bucket_cls_targets = bucket_cls_targets.view(-1, self.side_num)
            bucket_cls_weights = bucket_cls_weights.view(-1, self.side_num)
            losses['loss_bbox_cls'] = self.loss_bbox_cls(
                bucket_cls_preds,
                bucket_cls_targets,
                bucket_cls_weights,
                avg_factor=bucket_cls_targets.size(0),
                reduction_override=reduction_override)

            losses['loss_bbox_reg'] = self.loss_bbox_reg(
                bucket_offset_preds,
                bucket_offset_targets,
                bucket_offset_weights,
                avg_factor=bucket_offset_targets.size(0),
                reduction_override=reduction_override)

        return losses

    def _predict_by_feat_single(
            self,
            roi: Tensor,
            cls_score: Tensor,
            bbox_pred: Tuple[Tensor, Tensor],
            img_meta: dict,
            rescale: bool = False,
            rcnn_test_cfg: Optional[ConfigDict] = None) -> InstanceData:
        """Transform a single image's features extracted from the head into
        bbox results.

        Args:
            roi (Tensor): Boxes to be transformed. Has shape (num_boxes, 5).
                last dimension 5 arrange as (batch_index, x1, y1, x2, y2).
            cls_score (Tensor): Box scores, has shape
                (num_boxes, num_classes + 1).
            bbox_pred (Tuple[Tensor, Tensor]): Box cls preds and offset preds.
            img_meta (dict): image information.
            rescale (bool): If True, return boxes in original image space.
                Defaults to False.
            rcnn_test_cfg (obj:`ConfigDict`): `test_cfg` of Bbox Head.
                Defaults to None

        Returns:
            :obj:`InstanceData`: Detection results of each image
            Each item usually contains following keys.

            - scores (Tensor): Classification scores, has a shape
              (num_instance, )
            - labels (Tensor): Labels of bboxes, has a shape
              (num_instances, ).
            - bboxes (Tensor): Has a shape (num_instances, 4),
              the last dimension 4 arrange as (x1, y1, x2, y2).
        """
        results = InstanceData()
        if isinstance(cls_score, list):
            cls_score = sum(cls_score) / float(len(cls_score))
        scores = F.softmax(cls_score, dim=1) if cls_score is not None else None
        img_shape = img_meta['img_shape']
        if bbox_pred is not None:
            bboxes, confidences = self.bbox_coder.decode(
                roi[:, 1:], bbox_pred, img_shape)
        else:
            bboxes = roi[:, 1:].clone()
            confidences = None
            if img_shape is not None:
                bboxes[:, [0, 2]].clamp_(min=0, max=img_shape[1] - 1)
                bboxes[:, [1, 3]].clamp_(min=0, max=img_shape[0] - 1)

        if rescale and bboxes.size(0) > 0:
            assert img_meta.get('scale_factor') is not None
            scale_factor = bboxes.new_tensor(img_meta['scale_factor']).repeat(
                (1, 2))
            bboxes = (bboxes.view(bboxes.size(0), -1, 4) / scale_factor).view(
                bboxes.size()[0], -1)

        if rcnn_test_cfg is None:
            results.bboxes = bboxes
            results.scores = scores
        else:
            det_bboxes, det_labels = multiclass_nms(
                bboxes,
                scores,
                rcnn_test_cfg.score_thr,
                rcnn_test_cfg.nms,
                rcnn_test_cfg.max_per_img,
                score_factors=confidences)
            results.bboxes = det_bboxes[:, :4]
            results.scores = det_bboxes[:, -1]
            results.labels = det_labels
        return results

    def refine_bboxes(self, sampling_results: List[SamplingResult],
                      bbox_results: dict,
                      batch_img_metas: List[dict]) -> InstanceList:
        """Refine bboxes during training.

        Args:
            sampling_results (List[:obj:`SamplingResult`]): Sampling results.
            bbox_results (dict): Usually is a dictionary with keys:

                - `cls_score` (Tensor): Classification scores.
                - `bbox_pred` (Tensor): Box energies / deltas.
                - `rois` (Tensor): RoIs with the shape (n, 5) where the first
                  column indicates batch id of each RoI.
                - `bbox_targets` (tuple):  Ground truth for proposals in a
                  single image. Containing the following list of Tensors:
                  (labels, label_weights, bbox_targets, bbox_weights)
            batch_img_metas (List[dict]): List of image information.

        Returns:
            list[:obj:`InstanceData`]: Refined bboxes of each image.
        """
        pos_is_gts = [res.pos_is_gt for res in sampling_results]
        # bbox_targets is a tuple
        labels = bbox_results['bbox_targets'][0]
        cls_scores = bbox_results['cls_score']
        rois = bbox_results['rois']
        bbox_preds = bbox_results['bbox_pred']

        if cls_scores.numel() == 0:
            return None

        labels = torch.where(labels == self.num_classes,
                             cls_scores[:, :-1].argmax(1), labels)

        img_ids = rois[:, 0].long().unique(sorted=True)
        assert img_ids.numel() <= len(batch_img_metas)

        results_list = []
        for i in range(len(batch_img_metas)):
            inds = torch.nonzero(
                rois[:, 0] == i, as_tuple=False).squeeze(dim=1)
            num_rois = inds.numel()

            bboxes_ = rois[inds, 1:]
            label_ = labels[inds]
            edge_cls_preds, edge_offset_preds = bbox_preds
            edge_cls_preds_ = edge_cls_preds[inds]
            edge_offset_preds_ = edge_offset_preds[inds]
            bbox_pred_ = (edge_cls_preds_, edge_offset_preds_)
            img_meta_ = batch_img_metas[i]
            pos_is_gts_ = pos_is_gts[i]

            bboxes = self.regress_by_class(bboxes_, label_, bbox_pred_,
                                           img_meta_)
            # filter gt bboxes
            pos_keep = 1 - pos_is_gts_
            keep_inds = pos_is_gts_.new_ones(num_rois)
            keep_inds[:len(pos_is_gts_)] = pos_keep
            results = InstanceData(bboxes=bboxes[keep_inds.type(torch.bool)])
            results_list.append(results)

        return results_list

    def regress_by_class(self, rois: Tensor, label: Tensor, bbox_pred: tuple,
                         img_meta: dict) -> Tensor:
        """Regress the bbox for the predicted class. Used in Cascade R-CNN.

        Args:
            rois (Tensor): shape (n, 4) or (n, 5)
            label (Tensor): shape (n, )
            bbox_pred (Tuple[Tensor]): shape [(n, num_buckets *2), \
                (n, num_buckets *2)]
            img_meta (dict): Image meta info.

        Returns:
            Tensor: Regressed bboxes, the same shape as input rois.
        """
        assert rois.size(1) == 4 or rois.size(1) == 5

        if rois.size(1) == 4:
            new_rois, _ = self.bbox_coder.decode(rois, bbox_pred,
                                                 img_meta['img_shape'])
        else:
            bboxes, _ = self.bbox_coder.decode(rois[:, 1:], bbox_pred,
                                               img_meta['img_shape'])
            new_rois = torch.cat((rois[:, [0]], bboxes), dim=1)

        return new_rois
