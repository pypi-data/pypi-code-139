from typing import Optional, Union
from functools import partial
from gym import spaces

from mlagents_envs.base_env import DecisionSteps, TerminalSteps
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import BaseEnv
from mlagents_envs.side_channel.environment_parameters_channel import (
    EnvironmentParametersChannel,
)
import numpy as np
from .gym_unity import UnityToGymWrapper, GymStepResult, logger
from .env_utils import get_exe_path, generate_reorder_mat, process_raycast


def flatten_shape(shp):
    return int(np.prod(shp))


class CanyonRun(UnityToGymWrapper):
    def __init__(
        self,
        # [From UnityToGymWrapper]
        uint8_visual: bool = False,
        flatten_branched: bool = False,
        allow_multiple_obs: bool = True,
        action_space_seed: Optional[int] = None,
        # [From UnityEnvironment]
        file_name: Optional[str] = None,
        worker_id: int = 0,
        base_port: Optional[int] = None,
        seed: int = 0,
        no_graphics: bool = False,
        timeout_wait: int = 60,
        log_folder: Optional[str] = None,
        num_areas: int = 1,
        # [Channel Parameters]
        use_cont_act_space: Optional[bool] = True,
        input_mode: Optional[int] = 3,
        randomize_start_height: Optional[bool] = True,
        fuel_max: Optional[float] = 200.0,
        fuel_default: Optional[float] = 100.0,
        fuel_min: Optional[float] = 0.0,
        fuel_star_increment: Optional[float] = 20.0,
        fuel_tile_increment: Optional[float] = 20.0,
        fuel_burn_rate: Optional[float] = 0.1,
        record: Optional[bool] = False,
        flat_obs=False,
        reward_per_step=1e-3,
        reward_per_end=-1,
    ):
        # Instantiate Unity environment
        if file_name is None:
            file_name = get_exe_path("CanyonRun_0_9_2", "CanyonRun")

        self.channel = EnvironmentParametersChannel()
        unity_env = UnityEnvironment(
            file_name,
            worker_id=worker_id,
            base_port=base_port,
            seed=seed,
            no_graphics=no_graphics,
            side_channels=[self.channel],
            timeout_wait=timeout_wait,
            log_folder=log_folder,
            num_areas=num_areas,
        )

        # Set channel params
        self.channel.set_float_parameter(
            "use_cont_act_space", float(use_cont_act_space)
        )
        self.channel.set_float_parameter("input_mode", input_mode)
        self.channel.set_float_parameter(
            "randomize_start_height", float(randomize_start_height)
        )
        self.channel.set_float_parameter("fuel_max", fuel_max)
        self.channel.set_float_parameter("fuel_default", fuel_default)
        self.channel.set_float_parameter("fuel_min", fuel_min)
        self.channel.set_float_parameter("fuel_star_increment", fuel_star_increment)
        self.channel.set_float_parameter("fuel_tile_increment", fuel_tile_increment)
        self.channel.set_float_parameter("fuel_burn_rate", fuel_burn_rate)
        self.channel.set_float_parameter("record", record)

        # Instantiate gym-unity
        super(CanyonRun, self).__init__(
            unity_env=unity_env,
            uint8_visual=uint8_visual,
            flatten_branched=flatten_branched,
            allow_multiple_obs=allow_multiple_obs,
            action_space_seed=action_space_seed,
        )

        # Observation space
        assert allow_multiple_obs, "`allow_multiple_obs` must be True"
        self._observation_space = self._observation_space[0]

        self._reward_per_step = reward_per_step
        self._reward_per_end = reward_per_end
        self._flat_obs = flat_obs
        self._sensor1_obs_shape = (19, 33, 2)
        self._sensor2_obs_shape = (19, 33, 3)
        self._sensor1_reorder_mat = generate_reorder_mat(self._sensor1_obs_shape[1])
        self._sensor2_reorder_mat = generate_reorder_mat(self._sensor2_obs_shape[1])
        self.process_sensor1_obs = partial(
            process_raycast,
            obs_shape=self._sensor1_obs_shape,
            reorder_mat=self._sensor1_reorder_mat,
        )
        self.process_sensor2_obs = partial(
            process_raycast,
            obs_shape=self._sensor2_obs_shape,
            reorder_mat=self._sensor2_reorder_mat,
        )

        raw_sensor_obs_shape = np.prod(self._sensor1_obs_shape) + np.prod(
            self._sensor2_obs_shape
        )
        raw_vec_obs_shape = 8
        assert self._observation_space.shape[0] == (
            raw_sensor_obs_shape + raw_vec_obs_shape
        )

        if self._flat_obs:
            self._observation_space = spaces.Tuple(
                [
                    spaces.Box(
                        low=np.zeros(
                            flatten_shape(self._sensor1_obs_shape), dtype=np.uint8
                        ),
                        high=np.ones(
                            flatten_shape(self._sensor1_obs_shape), dtype=np.uint8
                        )
                        * 255,
                        dtype=np.uint8,
                    ),
                    spaces.Box(
                        low=np.zeros(
                            flatten_shape(self._sensor2_obs_shape), dtype=np.uint8
                        ),
                        high=np.ones(
                            flatten_shape(self._sensor2_obs_shape), dtype=np.uint8
                        )
                        * 255,
                        dtype=np.uint8,
                    ),
                    spaces.Box(
                        low=self._observation_space.low[-raw_vec_obs_shape:],
                        high=self._observation_space.high[-raw_vec_obs_shape:],
                        dtype=np.float64,
                    ),
                ]
            )

        else:
            self._observation_space = spaces.Tuple(
                [
                    spaces.Box(
                        low=np.zeros(self._sensor1_obs_shape, dtype=np.uint8),
                        high=np.ones(self._sensor1_obs_shape, dtype=np.uint8) * 255,
                        dtype=np.uint8,
                    ),
                    spaces.Box(
                        low=np.zeros(self._sensor2_obs_shape, dtype=np.uint8),
                        high=np.ones(self._sensor2_obs_shape, dtype=np.uint8) * 255,
                        dtype=np.uint8,
                    ),
                    spaces.Box(
                        low=self._observation_space.low[-raw_vec_obs_shape:],
                        high=self._observation_space.high[-raw_vec_obs_shape:],
                        dtype=np.float64,
                    ),
                ]
            )

        # Action space
        if use_cont_act_space:
            self._action_space = self._action_space["continuous"]
        else:
            self._action_space = self._action_space["discrete"]

        assert input_mode == 3, "Only support input_mode = 3 now"

        # Misc
        self.use_cont_act_space = use_cont_act_space

    def step(self, action):
        if self.use_cont_act_space:
            action = {
                "continuous": action,
                "discrete": np.zeros_like(action),
            }
        else:
            action = {
                "discrete": action,
                "continuous": np.zeros_like(action),
            }

        return super().step(action)

    def _single_step(self, info: Union[DecisionSteps, TerminalSteps]) -> GymStepResult:
        (obs, rew, done, _info) = super()._single_step(info)
        obs = obs[0]

        start, end = 0, np.prod(self._sensor1_obs_shape)
        sensor1_obs = self.process_sensor1_obs(obs[start:end])

        start, end = end, end + np.prod(self._sensor2_obs_shape)
        sensor2_obs = self.process_sensor2_obs(obs[start:end])

        vec_obs = obs[end:]

        if self._flat_obs:
            sensor1_obs = sensor1_obs.flatten()
            sensor2_obs = sensor2_obs.flatten()
        obs = [sensor1_obs, sensor2_obs, vec_obs]

        if done:
            rew += self._reward_per_end
        rew += self._reward_per_step
        return obs, rew, done, _info


if __name__ == "__main__":
    env = CanyonRun(no_graphics=True)
    env.reset()

    for _ in range(100):
        act = env.action_space.sample()
        obs, rew, done, _info = env.step(act)

        print(f"obs shape = {[v.shape for v in obs]}")