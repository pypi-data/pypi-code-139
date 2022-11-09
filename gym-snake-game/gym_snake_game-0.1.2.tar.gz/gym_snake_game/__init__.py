from gym_snake_game.version import VERSION as __version__
from gym.envs.registration import register

import gym

__author__ = "Ming Yu"

register(
    id="Snake-v0",
    entry_point="gym_snake_game.environment:SnakeEnv",
)


def make(name, **kwargs):
    return gym.make(name, **kwargs)
