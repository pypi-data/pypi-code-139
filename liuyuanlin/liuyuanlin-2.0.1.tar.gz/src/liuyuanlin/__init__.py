import numpy as np
import cv2
from math import sin, cos, pi, log, fabs  # 内置库 数学计算库
import random

'''
总的来说渲染这样一个跳动的爱心需要构造一个渲染管线


point使用np.array类型：
例如：
point = np.array([1, 2])
x = 1, y = 2.

笛卡尔坐标系下
    每一帧图像：
        缩放爱心函数获得边沿
        扩散
        

变换坐标系为图像坐标
图像->显示
'''


class HeartData:
    def __init__(self):
        self.edge_points = set()
        self.inside_diffusion_points = set()
        self.outside_diffusion_points = set()
        self.init_scale = 1
        self.outside_diffusion_points_sample = []

    def clear(self):
        self.edge_points = set()
        self.inside_diffusion_points = set()
        self.outside_diffusion_points = set()
        self.init_scale = 1
        self.outside_diffusion_points_sample = []


def 变化曲线(t: float):
    '''
    :param t: 时间 0-2π.
    :return:
    '''
    return fabs(2 * (2 * sin(4 * t)) / (2 * pi))


def 心形函数(t: float, radius: float) -> tuple:
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x = x * radius
    y = y * radius
    return (int(x), int(y))


def 向内部扩散(point: tuple, beta: float) -> tuple:
    """
    随机内部扩散,这里假定中心坐标是原点。
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    # 这里ratio总是正值，这样总能够让边沿粒子向原点扩散。
    dx = point[0] * ratio_x
    dy = point[1] * ratio_y

    return (point[0] - dx, point[1] - dy)


def 向外部扩散(point: tuple, beta: float) -> tuple:
    """
    随机内部扩散,这里假定中心坐标是原点。
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    # 这里ratio总是正值，这样总能够让边沿粒子向原点扩散。
    dx = point[0] * ratio_x
    dy = point[1] * ratio_y

    return (point[0] + dx, point[1] + dy)


def 向内向外部随机扩散(point: tuple, beta: float) -> tuple:
    """
    随机内部扩散,这里假定中心坐标是原点。
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    # 这里ratio总是正值，这样总能够让边沿粒子向原点扩散。
    dx = point[0] * ratio_x
    dy = point[1] * ratio_y
    if (random.random() > 0.1):

        return (point[0] - dx, point[1] - dy)
    else:
        return (point[0] + dx / 2, point[1] + dy / 2)


def 在图像上画一个方形粒子(center: tuple, img, color=(0, 0, 0xff)):
    b, g, r = color  # 颜色范围 (95, 47, 180) ~ (203, 169, 254)
    # 可以更具粒子位置变化颜色

    center = (int(center[0]), int(center[1]))
    color = (b + random.randint(0, 60), g + random.randint(0, 60), r + random.randint(0, 120))

    size = 5
    cv2.rectangle(img, center, (center[0] + size, center[1] + size), color, -1)
    color = (b + random.randint(60, 120), g + random.randint(60, 120), r + random.randint(80, 180))
    size = 3
    cv2.rectangle(img, center, (center[0] + size, center[1] + size), color, -1)


heart = HeartData()


def 渲染初始图像(t: float, height, width):
    '''
    :param t: 时间刻度，用来实现粒子变化,时间指的是0-2π。
    :return: 图像。
    '''
    height *= 3
    width *= 3

    heart.clear()
    # 获取本次缩放比例
    heart.init_scale = 变化曲线(t) * 8 + 38

    # 中间点聚集问题
    middle_error = 1

    # 渲染爱心轮廓点
    times = 2000  # 本次渲染次数
    for i in range(1, times):
        t_ = 2 * pi * i / times
        point = 心形函数(t_, heart.init_scale)
        point = 向内部扩散(point, 0.05)
        if (fabs(point[0]) > middle_error):
            heart.edge_points.add(point)
        point = 向内部扩散(point, 0.06)
        if (fabs(point[0]) > middle_error):
            heart.edge_points.add(point)
        point = 向内部扩散(point, 0.07)
        if (fabs(point[0]) > middle_error):
            heart.edge_points.add(point)

    # 光环
    heart.outside_diffusion_points = set()
    halo_number = int(5000 + 4000 * abs(变化曲线(t / 10 * pi) ** 2))
    # 光环
    for _ in range(halo_number):
        t = random.uniform(0, 2 * pi)  # 随机不到的地方造成爱心有缺口

        point = 心形函数(t, radius=40.6)
        point = 向内向外部随机扩散(point, 0.08)
        if (fabs(point[0]) > middle_error):
            heart.outside_diffusion_points.add(point)

    heart.outside_diffusion_points = list(heart.outside_diffusion_points)


def 渲染图像帧(t: float, height, width):
    height *= 3
    width *= 3

    # 获取本次缩放比例
    scale = 变化曲线(t) * 8 + 40
    scale_rate = heart.init_scale / scale

    # 构建一张三通道的图像
    img = np.zeros((height, width, 3), np.uint8)
    all_point = heart.edge_points

    # 变化坐标为OpenCV Mat图像坐标
    # 由点集渲染为图像
    center = np.array([width // 2, height // 2], dtype=np.int32)
    all_point = list(all_point)
    for i in range(len(all_point)):
        all_point[i] = np.array(all_point[i]) * scale_rate + center
        在图像上画一个方形粒子(all_point[i], img)

    heart.outside_diffusion_points_sample = random.sample(heart.outside_diffusion_points,
                                                          len(heart.outside_diffusion_points) // 2)
    for i in range(len(heart.outside_diffusion_points_sample)):
        point = heart.outside_diffusion_points_sample[i]
        point = np.array(point) + center
        在图像上画一个方形粒子(point, img, (0x28, 0x28, 0xff))

    img = cv2.resize(img, (width // 3, height // 3))
    return img


def liuyuanlin():
    time = 0
    渲染初始图像(time, 480, 640)
    while True:
        time += 0.03
        img = 渲染图像帧(time, 480, 640)
        cv2.imshow('HEART BY LIUYUANLIN', img)
        if cv2.waitKey(1000 // 60) in (' ', 27, 13):  # 按下空格、ESC、回车则退出程序
            exit(0)
