#!/usr/bin/env python3

"""Boundary F-score evaluation

NOTE: only single gpu evaluation is supported

TODO: support multi-gpu or distributed
"""

import torch

import mmcv


def single_gpu_boundary_fscore_test(
    model,
    data_loader,
    bound_th=0.008,
    num_proc=16,
):
    model.eval()
    results = []
    dataset = data_loader.dataset
    prog_bar = mmcv.ProgressBar(len(dataset))

    # The pipeline about how the data_loader retrieval samples from dataset:
    # sampler -> batch_sampler -> indices
    # The indices are passed to dataset_fetcher to get data from dataset.
    # data_fetcher -> collate_fn(dataset[index]) -> data_sample
    # we use batch_sampler to get correct data idx
    loader_indices = data_loader.batch_sampler

    for batch_indices, data in zip(loader_indices, data_loader):

        with torch.no_grad():
            result = model(return_loss=False, **data)

        result = dataset.pre_boundary_fscore_eval(
            result,
            indices=batch_indices,
            bound_th=bound_th,
            num_proc=num_proc,
        )
        results.extend(result)

        batch_size = len(result)
        for _ in range(batch_size):
            prog_bar.update()

    return results
