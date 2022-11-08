RED = "RED"
YELLOW = "YELLOW"
BLACK = "BLACK"
GREEN = "GREEN"
MAGENTA = "MAGENTA"
CYAN = "CYAN"
WHITE = "WHITE"  # 可用颜色


def echo(something, color=WHITE, end="\n") -> None:
    """
    建议使用的输出\n
    Eg.\n
    echo("标准色",GREEN)\n
    echo("十六进制","f35336")\n
    echo("256色",72)\n
    echo("RGB",(30, 144, 255))\n
    \n
    echo("通过256色设置 前景色，后景色",(23,145))\n
    echo("通过十六进制设置 前景色，后景色",("2add9c","eaff56"))\n
    echo("通过RGB设置 前景色，后景色",((20, 144, 234),(234, 78, 23)))\n
    \n
    echo("混搭",((30, 144, 255),"c93756"))\n
    :param something: 可以为任意类型，如果是字典，列表将输出他们在go中的结构
    :param color: 输出的颜色，可省略，默认为utils.WHITE。
    :param end: 输出的结尾，可省略，默认为换行符
    :return:
    """
    ...


def walk_dir(path: str, recursion=False) -> list:
    """
    遍历文件夹\n
    :param path: 路径
    :param recursion: 递归，可省略，默认false
    :return: 所有文件与文件夹
    """
    ...


def input(prefix=">", color=WHITE, items=dict) -> str:
    """
    带有补全提示的输入\n
    :param prefix: 前缀，可省略，默认为">"
    :param color: 颜色，前缀的颜色，可省略，默认为utils.WHITE
    :param items: 字典，键为提示词，值为描述。e.g.{"hello":"你好"}，可省略，默认空
    :return:
    """
    ...


def center(something, color=WHITE) -> None:
    """
    居中输出，拥有和echo同样的多种颜色格式支持\n
    :param something: 字符串
    :param color: 输出的颜色，可省略，默认为utils.WHITE
    :return:
    """
    ...


def now() -> str:
    """
    返回当前时间字符串\n
    :return:
    """


def col(path) -> str:
    """
    返回collection内路径
    :return:
    """