from dataclasses import dataclass, fields
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
from scipy.linalg import block_diag
from scipy.optimize import Bounds, OptimizeResult, minimize

from skplan.kinematics import ArticulatedEndEffectorKinematicsMap
from skplan.space import ConfigurationSpace
from skplan.trajectory import Trajectory


def scipinize(fun: Callable) -> Tuple[Callable, Callable]:
    closure_member = {"jac_cache": None}

    def fun_scipinized(x):
        f, jac = fun(x)
        closure_member["jac_cache"] = jac
        return f

    def fun_scipinized_jac(x):
        return closure_member["jac_cache"]

    return fun_scipinized, fun_scipinized_jac


@dataclass(frozen=True)
class PlannerConfig:
    n_waypoint: int = 10
    clearance: float = 0.02
    ftol: float = 1e-4
    disp: bool = True
    maxiter: int = 100


@dataclass(frozen=True)
class PlanningResult:
    traj_solution: Trajectory
    success: bool
    status: int
    message: str
    fun: np.ndarray
    jac: np.ndarray
    nit: int
    progress_cache: Optional[List[Trajectory]] = None

    @classmethod
    def from_optimize_result(
        cls, res: OptimizeResult, dim: int, progress_cache: Optional[List[Trajectory]] = None
    ) -> "PlanningResult":
        kwargs = {}
        for field in fields(cls):
            key = field.name
            if key == "traj_solution":
                points = res.x.reshape(-1, dim)
                value = Trajectory(list(points))
            elif key in res:
                value = res[key]
            kwargs[key] = value
        kwargs["progress_cache"] = progress_cache  # type: ignore
        return cls(**kwargs)  # type: ignore


@dataclass
class OptimizationBasedPlanner:
    start: np.ndarray
    goal: np.ndarray
    cspace: ConfigurationSpace
    smooth_mat: Optional[np.ndarray] = None
    config: PlannerConfig = PlannerConfig()

    def __post_init__(self):
        n_dof = self.cspace.dim
        self.smooth_mat = self.construct_smoothcost_fullmat(self.config.n_waypoint, n_dof)

    @staticmethod
    def construct_smoothcost_fullmat(
        n_wp: int, n_dof: int, weights: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Compute A of eq. (17) of IJRR-version (2013) of CHOMP"""

        def construct_smoothcost_mat(n_wp):
            # In CHOMP (2013), squared sum of velocity is computed.
            # In this implementation we compute squared sum of acceralation
            # if you set acc_block * 0.0, vel_block * 1.0, then the trajectory
            # cost is same as the CHOMP one.
            acc_block = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]])
            vel_block = np.array([[1, -1], [-1, 1]])
            A_ = np.zeros((n_wp, n_wp))
            for i in [1 + i for i in range(n_wp - 2)]:
                A_[i - 1 : i + 2, i - 1 : i + 2] += acc_block * 1.0
                A_[i - 1 : i + 1, i - 1 : i + 1] += vel_block * 0.0  # do nothing
            return A_

        if weights is None:
            weights = np.ones(n_dof)

        w_mat = np.diag(weights)
        A_ = construct_smoothcost_mat(n_wp)
        A = np.kron(A_, w_mat**2)
        return A

    def fun_objective(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        assert self.smooth_mat is not None
        f = (0.5 * self.smooth_mat.dot(x).dot(x)).item() / self.config.n_waypoint
        grad = self.smooth_mat.dot(x) / self.config.n_waypoint
        return f, grad

    def fun_eq(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n_dof = self.cspace.dim
        value = np.hstack([self.start - x[:n_dof], self.goal - x[-n_dof:]])
        grad = np.zeros((n_dof * 2, self.config.n_waypoint * n_dof))
        grad[:n_dof, :n_dof] = -np.eye(n_dof)
        grad[-n_dof:, -n_dof:] = -np.eye(n_dof)
        return value, grad

    def fun_ineq(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        n_dof = self.cspace.dim
        points_cspace = x.reshape((self.config.n_waypoint, n_dof))
        vals_stacked, jacs_stacked = self.cspace.compute_signed_distance(points_cspace)

        value = vals_stacked.flatten()
        jac = block_diag(*list(jacs_stacked))
        return value, jac

    def solve(self, init_trajectory: Trajectory, cache_progress: bool = False) -> PlanningResult:

        eq_const_scipy, eq_const_jac_scipy = scipinize(self.fun_eq)
        eq_dict = {"type": "eq", "fun": eq_const_scipy, "jac": eq_const_jac_scipy}

        ineq_const_scipy, ineq_const_jac_scipy = scipinize(self.fun_ineq)
        ineq_dict = {"type": "ineq", "fun": ineq_const_scipy, "jac": ineq_const_jac_scipy}

        if cache_progress:
            progress_cache = []

            def wrap(x: np.ndarray):
                traj = Trajectory(list(x.reshape(-1, 2)))
                progress_cache.append(traj)
                return self.fun_objective(x)

            f, jac = scipinize(wrap)
        else:
            progress_cache = None
            f, jac = scipinize(self.fun_objective)
        lb = np.tile(self.cspace.bounds.b_min + self.config.clearance, self.config.n_waypoint)
        ub = np.tile(self.cspace.bounds.b_max - self.config.clearance, self.config.n_waypoint)
        bounds = Bounds(lb, ub, keep_feasible=True)  # type: ignore

        assert len(init_trajectory) == self.config.n_waypoint
        x_init = init_trajectory.numpy().flatten()

        slsqp_option: Dict = {
            "ftol": self.config.ftol,
            "disp": self.config.disp,
            "maxiter": self.config.maxiter - 1,  # somehome scipy iterate +1 more time
        }

        res = minimize(
            f,
            x_init,
            method="SLSQP",
            jac=jac,
            bounds=bounds,
            constraints=[eq_dict, ineq_dict],
            options=slsqp_option,
        )

        plan_result = PlanningResult.from_optimize_result(res, self.cspace.dim, progress_cache)
        assert plan_result.nit <= self.config.maxiter, "{} must be <= {}".format(
            plan_result.nit, self.config.maxiter
        )
        return plan_result


@dataclass(frozen=True)
class IKConfig:
    clearance: float = 0.005
    ftol: float = 1e-6
    disp: bool = True
    maxiter: int = 200


@dataclass(frozen=True)
class IKResult:
    x: np.ndarray
    success: bool
    status: int
    message: str
    fun: np.ndarray
    jac: np.ndarray
    nit: int

    @classmethod
    def from_optimize_result(cls, res: OptimizeResult) -> "IKResult":
        kwargs = {}
        for field in fields(cls):
            key = field.name
            if key in res:
                value = res[key]
            kwargs[key] = value
        return cls(**kwargs)  # type: ignore


@dataclass
class InverseKinematicsSolver:
    target: List[np.ndarray]
    kinmap: ArticulatedEndEffectorKinematicsMap
    cspace: ConfigurationSpace
    config: IKConfig = IKConfig()

    def __post_init__(self):
        assert self.kinmap.n_feature == len(self.target)

    def fun_objective(self, point_cspace: np.ndarray) -> Tuple[float, np.ndarray]:
        P_tmp, J_tmp = self.kinmap.map(np.expand_dims(point_cspace, axis=0))
        P, J = P_tmp[0].flatten(), np.stack(J_tmp[0])

        diff = P - np.stack(self.target).flatten()
        val = float(np.linalg.norm(diff) ** 2)
        grad = (2 * np.expand_dims(diff, axis=0).dot(J)).flatten()
        return val, grad

    def fun_ineq(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        points_cspace = np.expand_dims(x, axis=0)
        vals_stacked, jacs_stacked = self.cspace.compute_signed_distance(points_cspace)
        value = vals_stacked.flatten() - self.config.clearance
        jac = block_diag(*list(jacs_stacked))
        return value, jac

    def solve(
        self, x_cspace_init: Optional[np.ndarray] = None, avoid_obstacle: bool = False
    ) -> IKResult:

        if x_cspace_init is None:
            x_cspace_init = self.cspace.sample(1)[0]

        f, jac = scipinize(self.fun_objective)

        constraints = []
        if avoid_obstacle:
            assert self.cspace.tspace.sdf is not None
            ineq_const_scipy, ineq_const_jac_scipy = scipinize(self.fun_ineq)
            ineq_dict = {"type": "ineq", "fun": ineq_const_scipy, "jac": ineq_const_jac_scipy}
            constraints.append(ineq_dict)

        slsqp_option: Dict = {
            "ftol": self.config.ftol,
            "disp": self.config.disp,
            "maxiter": self.config.maxiter - 1,  # somehome scipy iterate +1 more time
        }

        lb = self.cspace.bounds.b_min
        ub = self.cspace.bounds.b_max
        bounds = Bounds(lb, ub, keep_feasible=True)  # type: ignore

        res = minimize(
            f,
            x_cspace_init,
            method="SLSQP",
            jac=jac,
            bounds=bounds,
            constraints=constraints,
            options=slsqp_option,
        )

        return IKResult.from_optimize_result(res)
