def move(x: int, y: int):
    """
    移动终端光标\n
    坐标系原点为左上角(1,1), 无负坐标
    :param x: 横坐标
    :param y: 纵坐标
    """
    ...


def draw(x: int, y: int, text, color="WHITE", back=False):
    """
    在终端指定坐标打印\n
    :param x: 横坐标
    :param y: 纵坐标
    :param text: 输出
    :param color: 颜色
    :param back: 打印后是否返回原始位置
    """
    ...


def say(x: int, y: int, text, color="WHITE", back=False):
    """
    此方法与draw()完全一致\n
    :param x: 横坐标
    :param y: 纵坐标
    :param text: 输出
    :param color: 颜色
    :param back: 输出后返回原始位置
    """
    ...
