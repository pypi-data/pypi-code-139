from gym.envs.registration import register

register(
    id="ori_optimize_linux-v0",
    entry_point="ori_optimize_linux.envs.ori_optimize_linux:OriOptimizeEnvLinux",
    max_episode_steps=100,
)