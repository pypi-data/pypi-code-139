#!/usr/bin/env python3

import os.path as osp
from copy import deepcopy

import numpy as np

import mmcv
from mmcv.runner import HOOKS
from mmcv.runner.dist_utils import master_only
from mmcv.runner.hooks.checkpoint import CheckpointHook

from mmseg.datasets.builder import build_dataloader

from blette.core.hook.basic_wandb_logger import BasicWandbHook
from potato.core.evaluation import (
    EvalHook,
    DistEvalHook,
    EvalSegHook,
    EvalEdgeHook,
    DistEvalSegHook,
    DistEvalEdgeHook,
)
from potato.visualize.vis_edge import beautify_edge


@HOOKS.register_module()
class PotatoWandbHook(BasicWandbHook):
    def __init__(
        self,
        init_kwargs=None,
        interval=50,
        log_checkpoint=False,
        log_checkpoint_metadata=False,
        num_eval_images=50,
        **kwargs,
    ):
        super().__init__(init_kwargs, interval, **kwargs)

        self.log_checkpoint = log_checkpoint
        self.log_checkpoint_metadata = log_checkpoint and log_checkpoint_metadata
        self.num_eval_images = num_eval_images
        self.log_evaluation = num_eval_images > 0
        self.ckpt_hook: CheckpointHook = None

        # NOTE: we're dealing with joint task
        self.eval_seg_hook = None
        self.test_seg_fn = None
        self.eval_edge_hook = None
        self.test_edge_fn = None

        self.num_evals = 0
        self._waited = 0

    @master_only
    def before_run(self, runner):
        super().before_run(runner)

        # Check if EvalHook(s) and CheckpointHook are available.
        # NOTE: use the single-gpu version of evaluatation function instead of multi-gpu
        for hook in runner.hooks:
            if isinstance(hook, CheckpointHook):
                self.ckpt_hook = hook

            # MMSeg EvalHooks
            if isinstance(hook, EvalHook):
                from mmseg.apis import single_gpu_test

                self.eval_seg_hook = hook
                self.test_seg_fn = single_gpu_test
            if isinstance(hook, DistEvalHook):
                from mmseg.apis import single_gpu_test

                self.eval_seg_hook = hook
                self.test_seg_fn = single_gpu_test

            # Potato EvalHooks
            if isinstance(hook, EvalSegHook):
                from potato.apis.test import single_gpu_seg_test

                self.eval_seg_hook = hook
                self.test_seg_fn = single_gpu_seg_test
            if isinstance(hook, DistEvalSegHook):
                from potato.apis.test import single_gpu_seg_test

                self.eval_seg_hook = hook
                self.test_seg_fn = single_gpu_seg_test

            # Potato edge EvalHooks
            if isinstance(hook, EvalEdgeHook):
                from potato.apis.test import single_gpu_edge_test

                self.eval_edge_hook = hook
                self.test_edge_fn = single_gpu_edge_test
            if isinstance(hook, DistEvalEdgeHook):
                from potato.apis.test import single_gpu_edge_test

                self.eval_edge_hook = hook
                self.test_edge_fn = single_gpu_edge_test

        # Check conditions to log checkpoint
        if self.log_checkpoint:
            if self.ckpt_hook is None:
                self.log_checkpoint = False
                self.log_checkpoint_metadata = False
                runner.logger.warning(
                    "To log checkpoint in PotatoWandbHook, `CheckpointHook` is"
                    "required, please check hooks in the runner."
                )
            else:
                self.ckpt_interval = self.ckpt_hook.interval

        # Check conditions to log evaluation
        if self.log_evaluation or self.log_checkpoint_metadata:
            if self.eval_seg_hook is None:
                self.log_evaluation = False
                self.log_checkpoint_metadata = False
                runner.logger.warning(
                    "To log evaluation or checkpoint metadata in "
                    "PotatoWandbHook, `EvalSegHook` or `DistEvalSegHook` in potato "
                    "is required, please check whether the validation "
                    "is enabled."
                )
            else:
                self.eval_interval = self.eval_seg_hook.interval

                # validation datasets are the same for both seg and edge eval hooks
                val_dataset = self.eval_seg_hook.dataloader.dataset

                # Determine the number of samples to be logged.
                if self.num_eval_images > len(val_dataset):
                    self.num_eval_images = len(val_dataset)
                    runner.logger.warning(
                        f"The num_eval_images ({self.num_eval_images}) is "
                        "greater than the total number of validation samples "
                        f"({len(val_dataset)}). The complete validation "
                        "dataset will be logged."
                    )

        # Check conditions to log checkpoint metadata
        if self.log_checkpoint_metadata:
            assert self.ckpt_interval % self.eval_interval == 0, (
                "To log checkpoint metadata in PotatoWandbHook, the interval "
                f"of checkpoint saving ({self.ckpt_interval}) should be "
                "divisible by the interval of evaluation "
                f"({self.eval_interval})."
            )

        if self.eval_seg_hook:
            self.num_evals += 1
        if self.eval_edge_hook:
            self.num_evals += 1

        # Initialize evaluation table
        if self.log_evaluation:
            self._initialize_gts(runner)

    @master_only
    def after_train_iter(self, runner):
        if self.get_mode(runner) == "train":
            # An ugly patch. The iter-based eval hook will call the
            # `after_train_iter` method of all logger hooks before evaluation.
            # Use this trick to skip that call.
            # Don't call super method at first, it will clear the log_buffer
            return super().after_train_iter(runner)
        else:
            super().after_train_iter(runner)

        # Even if `runner.mode` is "train", the mode could be "val"
        # depending on if "time" is in `runner.log_buffer.output`

        if self.by_epoch:
            return

        # HACK: `after_train_iter` gets called after evaluating one of the EvalHooks,
        # so if there are multiple EvalHooks, it will evaluate for every hook
        # need to make sure that it runs after the last iter
        if self._waited > self.num_evals:
            print("something wrong happened")

        self._waited += 1
        if self._waited < self.num_evals:
            # print(f"waiting for more evals (waited {self._waited})")
            return
        self._waited = 0

        # print(f'passed block {self._waited}')

        # Save checkpoint and metadata
        if self.log_checkpoint and (
            self.every_n_iters(runner, self.ckpt_interval)
            or (self.ckpt_hook.save_last and self.is_last_iter(runner))
        ):
            if self.log_checkpoint_metadata and self.eval_seg_hook:
                metadata = {"iter": runner.iter + 1, **self._get_eval_results()}
            else:
                metadata = None
            aliases = [f"iter_{runner.iter+1}", "latest"]
            model_path = osp.join(self.ckpt_hook.out_dir, f"iter_{runner.iter+1}.pth")
            self._log_ckpt_as_artifact(model_path, aliases, metadata)

        # Save seg prediction table
        if self.eval_seg_hook:
            if self.log_evaluation and self.eval_seg_hook._should_evaluate(runner):
                self._log_seg_predictions(runner)

        # Save edge prediction table
        if self.eval_edge_hook:
            if self.log_evaluation and self.eval_edge_hook._should_evaluate(runner):
                self._log_edge_predictions(runner)

    @master_only
    def after_run(self, runner):
        self.wandb.finish()

    def _log_ckpt_as_artifact(self, model_path, aliases, metadata=None):
        """Log model checkpoint as  W&B Artifact.
        Args:
            model_path (str): Path of the checkpoint to log.
            aliases (list): List of the aliases associated with this artifact.
            metadata (dict, optional): Metadata associated with this artifact.
        """
        model_artifact = self.wandb.Artifact(
            f"run_{self.wandb.run.id}_model", type="model", metadata=metadata
        )
        model_artifact.add_file(model_path)
        self.wandb.log_artifact(model_artifact, aliases=aliases)

    def _get_eval_results(self):
        """Get model evaluation results."""
        seg_results = self.eval_seg_hook.latest_results
        val_dataset = self.eval_seg_hook.dataloader.dataset
        eval_seg_results = val_dataset.evaluate(
            seg_results,
            logger="silent",
            **self.eval_seg_hook.eval_kwargs,
        )
        results = dict(seg=eval_seg_results)

        if self.eval_edge_hook:
            edge_results = self.eval_edge_hook.latest_results
            val_dataset = self.eval_edge_hook.dataloader.dataset
            eval_edge_results = val_dataset.evaluate(
                edge_results,
                logger="silent",
                **self.eval_edge_hook.eval_kwargs,
            )
            results.update(edge=eval_edge_results)

        return results

    def _initialize_gts(self, runner):
        # validation datasets are the same for both seg and edge eval hooks
        val_dataset = deepcopy(self.eval_seg_hook.dataloader.dataset)

        # Prune dataset
        eval_image_idx = np.arange(len(val_dataset))
        # Set seed so that same validation set is logged each time.
        np.random.seed(42)
        np.random.shuffle(eval_image_idx)
        eval_image_idx = eval_image_idx[: self.num_eval_images]

        img_infos = val_dataset.img_infos
        new_img_infos = []
        for i in eval_image_idx:
            new_img_infos.append(img_infos[i])
        val_dataset.img_infos = new_img_infos

        self.dataset = val_dataset

        # Setting up a dataloader
        # FIXME: not sure about the arguments being passed
        self.dataloader = build_dataloader(
            dataset=val_dataset,
            samples_per_gpu=1,
            workers_per_gpu=2,
            dist=False,  # `master_only``
            shuffle=False,
        )

        # Get image loading pipeline
        from mmseg.datasets.pipelines import LoadImageFromFile

        img_loader = None
        for t in self.dataset.pipeline.transforms:
            if isinstance(t, LoadImageFromFile):
                img_loader = t

        if img_loader is None:
            self.log_evaluation = False
            runner.logger.warning(
                "LoadImageFromFile is required to add images " "to W&B Tables."
            )
            return

        classes = self.dataset.CLASSES
        self.class_id_to_label = {id: name for id, name in enumerate(classes)}
        self.class_set = self.wandb.Classes(
            [{"id": id, "name": name} for id, name in self.class_id_to_label.items()]
        )

        # Init data table.
        if self.eval_edge_hook is not None:
            columns = ["image_name", "image", "edge"]
        else:
            columns = ["image_name", "image"]
        data_table = self.wandb.Table(columns=columns)

        for idx, img_info in enumerate(self.dataset.img_infos):
            image_name = img_info["filename"]

            # Get image and convert from BGR to RGB
            img_meta = img_loader(
                dict(img_info=img_info, img_prefix=self.dataset.img_dir)
            )
            image = mmcv.bgr2rgb(img_meta["img"])

            # Get segmentation mask
            seg_mask = self.dataset.get_gt_seg_map_by_idx(idx)
            assert (
                seg_mask.ndim == 2
            ), f"ERR: need seg_mask to be 2dim but got {seg_mask.ndim}dim"
            # Dict of masks to be logged.
            wandb_masks = {
                "ground_truth": {
                    "mask_data": seg_mask,
                    "class_labels": self.class_id_to_label,
                }
            }

            if self.eval_edge_hook is not None:
                edge_mask = self.dataset.get_gt_edge_map_by_idx(idx)
                edge = beautify_edge(
                    edge_mask,
                    palette=self.dataset.PALETTE,
                    beautify_threshold=0.7,
                )

                # Log a row to the data table.
                data_table.add_data(
                    image_name,
                    self.wandb.Image(image, masks=wandb_masks, classes=self.class_set),
                    self.wandb.Image(edge),
                )
            else:
                # Log a row to the data table.
                data_table.add_data(
                    image_name,
                    self.wandb.Image(image, masks=wandb_masks, classes=self.class_set),
                )

        """Log the W&B Tables for validation data as artifact and calls
        `use_artifact` on it so that the evaluation table can use the reference
        of already uploaded images.
        This allows the data to be uploaded just once.
        """
        data_artifact = self.wandb.Artifact("val", type="dataset")
        data_artifact.add(data_table, "val_data")
        self.wandb.run.use_artifact(data_artifact)
        data_artifact.wait()  # might take a while...
        self.data_table_ref = data_artifact.get("val_data")

    def _log_seg_predictions(self, runner):
        results = self.test_seg_fn(runner.model, self.dataloader)
        columns = ["image_name", "ground_truth", "prediction"]
        eval_table = self.wandb.Table(columns=columns)
        table_idxs = self.data_table_ref.get_index()
        assert len(table_idxs) == len(self.dataset)
        assert len(results) == len(self.dataset)

        for ndx, pred_mask in enumerate(results):
            assert pred_mask.ndim == 2, f"{pred_mask.ndim}dim is not supported"
            wandb_masks = {
                "prediction": {
                    "mask_data": pred_mask,
                    "class_labels": self.class_id_to_label,
                }
            }

            # Log a row to the data table.
            eval_table.add_data(
                self.data_table_ref.data[ndx][0],
                self.data_table_ref.data[ndx][1],
                self.wandb.Image(
                    self.data_table_ref.data[ndx][1],
                    masks=wandb_masks,
                    classes=self.class_set,
                ),
            )

        pred_artifact = self.wandb.Artifact(
            f"run_{self.wandb.run.id}_pred", type="evaluation"
        )
        pred_artifact.add(eval_table, "eval_data")  # NOTE: naming
        self.wandb.run.log_artifact(pred_artifact)

    def _log_edge_predictions(self, runner):
        results = self.test_edge_fn(runner.model, self.dataloader)
        columns = ["image_name", "ground_truth", "prediction"]
        eval_table = self.wandb.Table(columns=columns)
        table_idxs = self.data_table_ref.get_index()
        assert len(table_idxs) == len(self.dataset)
        assert len(results) == len(self.dataset)

        for ndx, pred_mask in enumerate(results):
            # Convert pred_mask
            if pred_mask.ndim == 3:
                if pred_mask.shape[0] == 1:
                    pred_mask = pred_mask.squeeze(0)
                else:
                    pred_mask = beautify_edge(
                        edges=pred_mask,
                        palette=self.dataset.PALETTE,
                        beautify_threshold=0.7,  # HARD-Coded
                    )
            # Log a row to the data table.
            eval_table.add_data(
                self.data_table_ref.data[ndx][0],
                # self.data_table_ref.data[ndx][1],  # img
                self.data_table_ref.data[ndx][2],  # edge gt
                self.wandb.Image(pred_mask),
            )
        pred_artifact = self.wandb.Artifact(
            f"run_{self.wandb.run.id}_edge_pred", type="evaluation"
        )
        pred_artifact.add(eval_table, "eval_edge_data")
        self.wandb.run.log_artifact(pred_artifact)
