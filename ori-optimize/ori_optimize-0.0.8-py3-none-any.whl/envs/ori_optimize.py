import gym
import torch
from gym import spaces
import numpy as np
import math
import sys

sys.path.append("../../support/build")
import libSupport


class OriOptimizeEnv(gym.Env):
    """该环境类调用.so文件 libSupport用作计算传入的模型的支撑体积并且记录模型朝向的矩阵，
        类中的模型方向与libSupport中记录的模型方向只做同步，
        环境选择action往哪个方向转，类中先计算旋转后的方向然后将方向同步给libSupport,
        该方法是写个linux系统的，传入文件地址需要按照linux系统的文件地址"""

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, file_path, render_mode=None):
        """初始化函数，只要传入模型初始摆放方向即可"""

        self.env = libSupport.Calculation()  # self.observation_space = 2 or 3
        self.model_object(file_path)

        ori = np.array([1, 0, 0])  # 模型初始方向 np.int64
        self.initial_ori = ori.astype(np.float32)  # 上面的数据类型是np.int64 转换成np.float32 c++那边是32位的 python默认的float64
        self.env.getInitialOri(self.initial_ori[0], self.initial_ori[1], self.initial_ori[2])  # 传入初始方向矩阵
        self._agent_orientation = self.initial_ori

        self.current_support_volume = self.env.runCompute()  # 计算模型的支撑

        self.action_space = spaces.Discrete(2)  # rotate model around TWO axis of the XYZ is enough

        cos = np.array([math.cos(math.pi / 36)])  # 这里说明每次旋转模型，模型绕某个轴旋转 pi/36 = 5°
        cos = cos.astype(np.float32)
        self.cos = cos[0]
        sin = np.array([math.sin(math.pi / 36)])  # 先弄成numpy array 然后将其转化成np.float32 只要通过sin[0]即可调用
        sin = sin.astype(np.float32)
        self.sin = sin[0]
        rotation_x = np.array([[1, 0, 0],
                               [0, self.cos, -self.sin],
                               [0, self.sin, self.cos]])
        rotation_y = np.array([[self.cos, 0, self.sin],
                               [0, 1, 0],
                               [-self.sin, 0, self.cos]])
        self.rotate_with_y = rotation_x.astype(np.float32)
        self.rotate_with_x = rotation_y.astype(np.float32)

        self.observation_space = spaces.Box(0, 255, dtype=np.float32)

        self._action_to_direction = {  # 下面的是旋转矩阵 0: 绕"x" 1: 绕"y"
            0: self.rotate_with_x,
            1: self.rotate_with_y,
        }

        self._target_orientation = np.array([0, 0, 1], dtype=float)
        self.total_reward = 0

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # 目前不知用处，设置为None
        self.window = None
        self.clock = None

    def model_object(self, file_path):
        """在该位置传入模型的地址，导入模型给libSupport， 必须先执行此步骤才能执行其他"""

        # 这个位置传入文件地址，设定模型
        return self.env.getFilePath(file_path)

    def _get_info(self):
        """info信息与观察值不同，info信息是深层次的模型信息，比如模型方向的具体数字"""

        return {"orientation": self._agent_orientation}  # 暂时没什么info需要返回

    def _get_obs(self, img=torch.tensor((227, 227, 3))):
        """获得观察值，即图片，应从OpenGL的程序中得到，目前还没放入接口"""

        new_obs = np.moveaxis(img, 2, 0)  # 一般输入的图片的通道就是227x227x3, 调整227x227x3的通道为3x227x227
        # 这里会获得一个模型当前角度
        # 这里会修改picture,传递当前的模型旋转的图片信息
        return {"observation": new_obs.astype(np.float32)}

    def reset(self, seed=None, return_info=True, options=None):
        """将环境的信息重置，将模型的方向也重置，不重置放进来的模型地址"""

        super().reset(seed=seed)
        self._agent_orientation = self.initial_ori  # 重置环境其实就是将模型的角度摆正，摆回原来的位置
        self.env.getInitialOri(self.initial_ori[0], self.initial_ori[1], self.initial_ori[2])
        self.current_support_volume = self.env.runCompute()
        observation = self._get_obs()
        info = self._get_info()
        print("reset success")
        # if self.render_mode == "human":
        #     self._render_frame()

        if not return_info:
            return observation
        else:
            return observation, info

    def step(self, action):
        angle = self._action_to_direction[action]
        self._agent_orientation = self._agent_orientation.dot(angle)  # 乘上一个旋转矩阵以后就是新的模型朝向方向了

        self.env.getOri(self._agent_orientation)
        support_area = self.env.runCompute()
        reward = (self.current_support_volume - support_area) / self.current_support_volume  # 暂定将奖励设计成减少的体积百分比
        terminated = np.array_equal(self._agent_orientation, self._target_orientation)  # 是否结束
        reward += -0.05 if not terminated else 0  # 如果结束获得奖励，未结束的时候获得的奖励不能为0，应该为负，避免模型停在原地不动

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    def render(self, mode="human"):
        """对目前来说这个函数没有作用"""
        pass
    #     if self.render_mode == "rgb_array":
    #         return self._render_frame()
