import copy
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np

from skplan.space import ConfigurationSpace
from skplan.trajectory import Trajectory


@dataclass
class RRTConfig:
    eps: float = 0.05
    n_max_iter: int = 30000
    goal_margin: float = 0.05


class ExtensionResult(Enum):
    REACHED = 0
    ADVANCED = 1
    TRAPPED = 2


class RRT:
    cspace: ConfigurationSpace
    goal: Optional[np.ndarray]
    sample_count: int
    config: RRTConfig
    _samples: np.ndarray
    _parent_indices: np.ndarray
    is_terminated: bool

    def __init__(
        self,
        start: np.ndarray,
        goal: Optional[np.ndarray],
        cspace: ConfigurationSpace,
        config: Optional[RRTConfig] = None,
    ):
        if config is None:
            config = RRTConfig()
        self.config = config

        assert np.all(cspace.is_valid(np.expand_dims(start, axis=0)))
        if goal is not None:
            assert np.all(cspace.is_valid(np.expand_dims(goal, axis=0)))

        # reserve memory to avoid dynamic allocation in each iteration
        n_dof = len(start)
        self.cspace = cspace
        self._samples = np.zeros((config.n_max_iter, n_dof))
        self._parent_indices = np.zeros(config.n_max_iter, dtype=int)
        self._samples[0] = start
        self.sample_count = 1
        self.goal = goal
        self.is_terminated = False

    @property
    def samples(self) -> np.ndarray:
        return self._samples[: self.sample_count]

    @property
    def parent_indices(self) -> np.ndarray:
        return self._parent_indices[: self.sample_count]

    @staticmethod
    def normalize(vec: np.ndarray) -> np.ndarray:
        return vec / np.linalg.norm(vec)

    def extend(self, state_target: np.ndarray) -> ExtensionResult:
        assert not self.is_terminated
        dists = np.sqrt(np.sum((self.samples - state_target) ** 2, axis=1))
        idx_nearest = np.argmin(dists)
        state_nearest = self.samples[idx_nearest]

        # extend
        unit_vec = self.normalize(state_target - state_nearest)
        is_reached = dists[idx_nearest] < self.config.eps
        state_new = state_nearest + min(dists[idx_nearest], self.config.eps) * unit_vec

        # update tree
        is_valid = self.cspace.is_valid(np.expand_dims(state_new, axis=0)).item()
        if not is_valid:
            return ExtensionResult.TRAPPED

        idx_new = self.sample_count
        self._samples[idx_new] = state_new
        self._parent_indices[idx_new] = idx_nearest
        self.sample_count += 1
        if is_reached:
            return ExtensionResult.REACHED
        else:
            return ExtensionResult.ADVANCED

    def connect(self, state_target: np.ndarray) -> ExtensionResult:
        while True:
            result = self.extend(state_target)
            if result != ExtensionResult.ADVANCED:
                return result

    def get_solution(self) -> Trajectory:
        assert self.goal is not None
        idx = self.sample_count - 1
        points = self._backward_search(idx) + [self.goal]
        return Trajectory(points)

    def _backward_search(self, idx: int) -> List[np.ndarray]:
        points = [self.samples[idx]]
        while idx != 0:
            idx = self.parent_indices[idx]
            points.append(self.samples[idx])
        points.reverse()
        return points

    def solve(self) -> Optional[Trajectory]:
        count = 0
        while count < self.config.n_max_iter:
            print(count)
            state_rand = self.cspace.sample(1).flatten()
            res = self.extend(state_rand)
            if res != ExtensionResult.TRAPPED:
                state_new = self.samples[-1]
                if np.linalg.norm(self.goal - state_new) < self.config.goal_margin:
                    self.is_terminated = True
                    return self.get_solution()
            count += 1
        return None

    def visualize(self, fax=None):
        if fax is None:
            fax = plt.subplots()
        fig, ax = fax

        # visualize nodes
        ax.scatter(self.samples[:, 0], self.samples[:, 1], c="black", s=5)

        # visualize edge
        for idx, state in enumerate(self.samples):
            idx_parent = self.parent_indices[idx]
            parent = self.samples[idx_parent]
            arr = np.stack([state, parent])
            ax.plot(arr[:, 0], arr[:, 1], color="red", linewidth=0.5)

        # visualize solution
        if self.is_terminated:
            trajectory = self.get_solution()
            arr = np.array(trajectory)
            ax.plot(arr[:, 0], arr[:, 1], color="blue", linewidth=1.0)


class BidirectionalRRT:
    rrt_start: RRT
    rrt_goal: RRT
    cspace: ConfigurationSpace
    config: RRTConfig
    is_terminated: bool

    def __init__(
        self,
        start: np.ndarray,
        goal: np.ndarray,
        cspace: ConfigurationSpace,
        config: Optional[RRTConfig] = None,
    ):
        if config is None:
            config = RRTConfig()

        assert start.shape == (cspace.dim,)
        assert goal.shape == (cspace.dim,)

        config_each = copy.deepcopy(config)
        config_each.n_max_iter = config.n_max_iter * 30
        rrt_start = RRT(start, None, cspace, config_each)
        rrt_goal = RRT(goal, None, cspace, config_each)
        self.rrt_start = rrt_start
        self.rrt_goal = rrt_goal
        self.cspace = cspace
        self.config = config
        self.is_terminated = False

    def solve(self) -> Optional[Trajectory]:
        count = 0
        rrt_a = self.rrt_start
        rrt_b = self.rrt_goal
        while count < self.config.n_max_iter:
            state_rand = self.cspace.sample(1).flatten()
            if rrt_a.extend(state_rand) != ExtensionResult.TRAPPED:
                state_new = rrt_a.samples[-1]
                result = rrt_b.connect(state_new)
                if result == ExtensionResult.REACHED:
                    self.is_terminated = True
                    return self.get_solution()

            rrt_a, rrt_b = rrt_b, rrt_a
            count += 1
        return None

    def get_solution(self) -> Trajectory:
        pts_from_start = self.rrt_start._backward_search(self.rrt_start.sample_count - 1)
        pts_from_goal = self.rrt_goal._backward_search(self.rrt_goal.sample_count - 1)
        pts_from_goal.reverse()
        pts = pts_from_start + pts_from_goal
        return Trajectory(pts)

    def visualize(self, fax=None):
        if fax is None:
            fax = plt.subplots()
        fig, ax = fax
        self.rrt_start.visualize(fax)
        self.rrt_goal.visualize(fax)

        # visualize solution
        if self.is_terminated:
            trajectory = self.get_solution()
            arr = np.array(trajectory)
            ax.plot(arr[:, 0], arr[:, 1], color="blue", linewidth=1.0)
