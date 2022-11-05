from dataclasses import dataclass
from typing import Protocol

import numpy as np
from skrobot.sdf import SignedDistanceFunction


class SDFLike(Protocol):
    def __call__(self, points: np.ndarray) -> np.ndarray:
        ...


@dataclass
class CircleSDF:
    center: np.ndarray
    radius: float

    def __call__(self, points: np.ndarray) -> np.ndarray:
        dists = np.sqrt(np.sum((points - self.center) ** 2, axis=1)) - self.radius
        return dists


@dataclass
class BoxSDF:
    center: np.ndarray
    width: np.ndarray

    def __call__(self, points: np.ndarray) -> np.ndarray:
        points_from_center = points - self.center
        half_extent = self.width * 0.5

        sd_vals_each_axis = np.abs(points_from_center) - half_extent

        positive_dists_each_axis = np.maximum(sd_vals_each_axis, 0.0)
        positive_dists = np.sqrt(np.sum(positive_dists_each_axis**2, axis=1))

        negative_dists_each_axis = np.max(sd_vals_each_axis, axis=1)
        negative_dists = np.minimum(negative_dists_each_axis, 0.0)

        sd_vals = positive_dists + negative_dists
        return sd_vals


@dataclass
class SkrobotSDF:
    skrobot_sdf: SignedDistanceFunction

    @classmethod
    def from_skrobot_sdf(cls, skrobot_sdf: SignedDistanceFunction) -> "SkrobotSDF":
        return cls(skrobot_sdf)

    def __call__(self, points: np.ndarray) -> np.ndarray:
        return self.skrobot_sdf.__call__(points)
        # n_point, n_dim = points.shape

        # x0 = points
        # f0 = self.skrobot_sdf.__call__(x0)
        # if not with_grad:
        #    return f0, None

        # eps = 1e-7
        # grad = np.zeros((n_point, n_dim))
        # for idx in range(n_dim):
        #    x1 = copy.copy(x0)
        #    x1[:, idx] += eps
        #    f1 = self.skrobot_sdf(x1)
        #    grad[:, idx] = (f1 - f0) / eps
        # return f0, grad
