#!/usr/bin/env python3

from mmseg.models.losses.accuracy import Accuracy, accuracy
from blette.models.losses.accuracy import calc_metrics as edge_accuracy

__all__ = ["Accuracy", "accuracy", "edge_accuracy"]
