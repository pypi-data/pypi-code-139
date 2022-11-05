import copy
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

from skplan.kinematics import CollisionKinmaticsMapProtocol
from skplan.sdf import SDFLike
from skplan.utils.urdf import URDF, JointLimit


@dataclass
class TaskSpace:
    dim: int
    sdf: Optional[SDFLike] = None
    b_min: Optional[np.ndarray] = None
    b_max: Optional[np.ndarray] = None

    def is_colliding(self, points: np.ndarray, margins: Optional[np.ndarray] = None) -> np.ndarray:
        n_points, n_dim = points.shape
        if margins is None:
            margins = np.zeros(n_points)
        assert len(margins) == n_points

        booleans = np.zeros((n_points,), dtype=bool)

        if self.sdf is not None:
            sd = self.sdf(points)
            booleans = np.logical_or(booleans, sd - margins < 0.0)

        if self.b_min is not None:
            tmp = np.any(points - margins[:, None] < self.b_min, axis=1)
            booleans = np.logical_or(booleans, tmp)

        if self.b_max is not None:
            tmp = np.any(points + margins[:, None] > self.b_max, axis=1)
            booleans = np.logical_or(booleans, tmp)

        return booleans


@dataclass
class Bounds:
    b_min: np.ndarray
    b_max: np.ndarray

    def __post_init__(self):
        assert not np.any(np.isinf(self.b_min))
        assert not np.any(np.isinf(self.b_max))

    @property
    def dim(self) -> int:
        return len(self.b_min)

    @classmethod
    def from_urdf(
        cls, urdf_path: Path, joint_names: List[str], base_bounds: Optional["Bounds"] = None
    ):

        urdfpath_str = str(urdf_path.expanduser())
        urdf = URDF.load(urdfpath_str)
        b_min = []
        b_max = []
        for joint_name in joint_names:
            limit: JointLimit = urdf.joint_map[joint_name].limit

            if limit.lower in [-np.inf, np.nan, None]:
                b_min.append(-2 * np.pi)
            else:
                b_min.append(limit.lower)

            if limit.upper in [+np.inf, np.nan, None]:
                b_max.append(2 * np.pi)
            else:
                b_max.append(limit.upper)

        if base_bounds is not None:
            for i in range(3):
                b_min.append(base_bounds.b_min[i])
                b_max.append(base_bounds.b_max[i])

        return cls(np.array(b_min), np.array(b_max))

    def sample(self, n_points: int) -> np.ndarray:
        width = self.b_max - self.b_min
        sample = np.random.rand(n_points, self.dim) * width + self.b_min
        return sample


@dataclass
class ConfigurationSpace:
    tspace: TaskSpace
    col_kinmap: CollisionKinmaticsMapProtocol
    bounds: Bounds

    def __post_init__(self):
        assert self.bounds.dim == self.dim

    @property
    def dim(self) -> int:
        return self.col_kinmap.dim_cspace

    def is_valid(self, points_cspace: np.ndarray, clearance: float = 0.0) -> np.ndarray:
        """check if cspace points are collision free and inside bounds"""
        n_point, dim_cspace = points_cspace.shape
        points_tspace, _ = self.col_kinmap.map(points_cspace)
        points_tspace = points_tspace.reshape(-1, self.tspace.dim)
        margin_radius = np.tile(np.array(self.col_kinmap.radius_list), n_point) + clearance

        is_obstacle_free = np.logical_not(self.tspace.is_colliding(points_tspace, margin_radius))

        is_inside_bound = np.all(
            np.logical_and(points_cspace > self.bounds.b_min, points_cspace < self.bounds.b_max),
            axis=1,
        )
        logicals_per_feature = np.logical_and(is_inside_bound, is_obstacle_free)
        logicals_per_cspace_point = np.all(
            logicals_per_feature.reshape(n_point, self.col_kinmap.n_feature), axis=1
        )
        return logicals_per_cspace_point

    def sample(self, n_points: int) -> np.ndarray:
        return self.bounds.sample(n_points)

    def compute_signed_distance(
        self, points_cspace: np.ndarray, clearance: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """compute signed distance of feature points and its jacobian
        input:
            points_cspace: R^{n_point, dim_cspace}
            clearance: clearance
        output:
            sd_vals_stacked: R^{n_point, n_feature}
            jac_stacked: R^{n_point, n_feature, dim_cspace}
        """
        assert self.tspace.sdf is not None
        dim_tspace = self.tspace.dim
        n_point, dim_cspace = points_cspace.shape
        n_feature = self.col_kinmap.n_feature

        # apply kinematic map
        # points_cspace_stacked: R^{n_point, n_feature * dim_tspace}
        # kin_jac_stacked: R^{n_point, n_feature, dim_tspace, dim_cspace}
        points_cspace_stacked, kin_jac_stacked = self.col_kinmap.map(points_cspace)

        # compute signed sitance and grad along tspace diff
        # points_cspace_stacked_flatten: R^{(n_point * n_feature) * dim_tspace}
        points_cspace_stacked_flatten = points_cspace_stacked.reshape(
            (n_point * n_feature, dim_tspace)
        )
        f0_stacked_flatten = self.tspace.sdf(points_cspace_stacked_flatten)

        eps = 1e-7
        grad_stacked_flatten = np.zeros((n_feature * n_point, dim_tspace))
        for i in range(dim_tspace):
            points_cspace_stacked_flatten_ = copy.deepcopy(points_cspace_stacked_flatten)
            points_cspace_stacked_flatten_[:, i] += eps
            f1_stacked_flatten = self.tspace.sdf(points_cspace_stacked_flatten_)
            grad_stacked_flatten[:, i] = (f1_stacked_flatten - f0_stacked_flatten) / eps
        grad_stacked = grad_stacked_flatten.reshape((n_point, n_feature, dim_tspace))

        # compute jacobian by chain rule
        jac_stacked = np.einsum("ijk,ijkl->ijl", grad_stacked, kin_jac_stacked)

        # compute sd_vals_stacked
        margin_radius = np.tile(np.array(self.col_kinmap.radius_list), n_point) + clearance
        sd_vals_stacked_flatten = f0_stacked_flatten - margin_radius
        sd_vals_stacked = sd_vals_stacked_flatten.reshape(n_point, n_feature)

        return sd_vals_stacked, jac_stacked
