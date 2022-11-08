GET = "GET"
POST = "POST"


class Response:
    def __init__(self):
        """
            http响应
        """
        ...

    def status_code(self) -> int:
        """
        响应包状态码\n(如果为-1则表示请求过程发生错误，详细错误用text()方法查看。\n
        :return:
        """
        ...

    def headers(self) -> dict:
        """
        响应头\n
        存在多个值的响应头以列表储存。\n
        :return:
        """
        ...

    def text(self) -> str:
        """
        获取响应正文\n
        :return:
        """
        ...

    def content(self) -> bytes:
        """
        获取响应正文(bytes)\n
        :return:
        """
        ...
    # ClassTag


def download(url: str, save_path: str, proxy_url: str) -> bool:
    """
    下载文件\n
    :param url: 文件url
    :param save_path: 文件保存路径，如果是文件将会写入文件。可省略，默认当前Icarus工作目录
    :param proxy_url: 代理url，可省略。e.g. http://127.0.0.1:7890 代理到本地clash
    :return: 下载是否成功
    """
    ...


def request(method: str, url: str, params: dict, data: str, headers: dict, verify: bool, proxy: dict,
            timeout=15) -> Response:
    """
    发送http请求\n
    :param method: GET,POST
    :param url: 目标url
    :param params: url参数，可省略
    :param data: post文本，可省略
    :param headers: 请求头,可省略
    :param verify: 是否验证https，可省略，默认为不验证
    :param proxy: 是否使用代理，可省略
    :param timeout: 超时，可省略
    :return: Response
    """
    ...


def ssh(address: str, user: str, passwd_or_private_key_path: str) -> None:
    """
    启动一个交互式的shell\n
    :param address: 目标地址
    :param user: 用户名
    :param passwd_or_private_key_path: 密码或私钥文件路径
    :return:
    """
    ...


def ssh_run(address: str, user: str, passwd_or_private_key_path: str, command: str) -> None:
    """
    通过ssh执行命令并启动交互式\n
    :param address: 目标地址
    :param user: 用户名
    :param passwd_or_private_key_path: 密码或私钥文件路径
    :param command: 需要执行的命令
    :return:
    """
    ...


def ssh_exec(address: str, user: str, passwd_or_private_key_path: str, command: str) -> str:
    """
    通过ssh执行命令并立即断开连接\n
    :param address: 目标地址
    :param user: 用户名
    :param passwd_or_private_key_path: 密码或私钥文件路径
    :param command: 需要执行的命令
    :return: 返回命令执行输出
    """
    ...


class SSH:
    def __init__(self, address: str, user: str, passwd: str):
        """
        ssh连接\n
        :param address: 地址
        :param user: 用户名
        :param passwd: 密码
        """
        ...

    def exec(self, cmd: str):
        """
        执行命令
        """
        ...

    def close(self):
        """
        关闭连接
        """
        ...
    # ClassTag


class SFTP:
    def __init__(self, address: str, user: str, passwd: str):
        """
        sftp连接\n
        :param address: 地址
        :param user: 用户名
        :param passwd: 密码
        """
        ...

    def upload(self, local: str, remote: str):
        """
        上传文件\n
        :param local: 本地路径
        :param remote: 远程路径
        :return:
        """
        ...

    def download(self, remote: str, local: str):
        """
        下载文件\n
        :param remote: 远程路径
        :param local: 本地路径
        :return:
        """
        ...

    def close(self):
        """
        关闭连接
        """
        ...
    # ClassTag


class TCP:
    def __init__(self, address: str):
        """
        建立tcp连接\n
        :param address: 地址
        """
        ...

    def send(self, data: str):
        """
        发送字符串\n
        :param data:
        :return:
        """
        ...

    def send_line(self, data: str):
        """
        发送字符串，但会在末尾加换行符\n
        :param data:
        :return:
        """
        ...

    def send_bytes(self, data: bytes):
        """
        发送字节数组\n
        :param data:
        :return:
        """
        ...

    def send_line_bytes(self, data: bytes):
        """
        发送字节数组，但会在末尾加换行符\n
        :param data:
        :return:
        """
        ...

    def recv(self) -> bytes:
        """
        接收所有数据\n
        :return: 返回字节数组
        """
        ...

    def recv_line(self) -> bytes:
        """
        接收数据到换行符停止\n
        :return: 返回字节数组
        """
        ...

    def interactive(self):
        """
        启用交互式收发数据\n
        :return:
        """
        ...

    def log(self):
        """
        显示收发日志\n
        :return:
        """
        ...

    def close(self):
        """
        关闭连接\n
        :return:
        """
        ...
    # ClassTag


class ProxyRequest:
    def __init__(self):
        """
        代理请求
        """
        ...

    def host(self) -> str:
        """
        获取host
        """
        ...

    def sid(self) -> str:
        """
        获取此次会话id\n
        可以通过sid识别此请求的响应包，同一会话的sid相同。
        """
        ...

    def proto(self) -> str:
        """
        获取协议
        """
        ...

    def remote_addr(self) -> str:
        """
        获取remote addr
        """
        ...

    def params(self) -> str:
        """
        获取请求url参数
        """
        ...

    def url(self) -> str:
        """
        获取url
        """
        ...

    def method(self, method=""):
        """
        获取或更改请求方法
        :param method: 新的方法
        """
        ...

    def headers(self, headers: dict):
        """
        获取或更改请求头
        :param headers:
        """
        ...

    def body(self, body: str):
        """
        获取或更改请求体
        :param body:
        """
        ...

    def release(self):
        """
        释放请求
        """
        ...

    def drop(self):
        """
        丢弃此请求
        """
        ...
    # ClassTag


class ProxyResponse:
    def __init__(self):
        """
        代理响应
        """
        ...

    def sid(self) -> str:
        """
        获取此次会话id\n
        可以通过sid识别此响应包的请求包，同一会话的sid相同。
        """
        ...

    def status_code(self, code: int):
        """
        获取或更改状态码
        :param code:
        """
        ...

    def headers(self, headers: dict) -> dict:
        """
        获取或修改响应头
        """
        ...

    def body(self, body: str) -> str:
        """
        获取或修改响应体
        """
        ...

    def release(self):
        """
        释放此响应
        """
        ...

    def drop(self):
        """
        丢弃此响应
        """
        ...
    # ClassTag


class HttpProxy:
    def __init__(self, addr: str, dump=False, ca_path=""):
        """
        实例化一个Http代理\n
        """
        ...

    def start(self):
        """
        启动代理
        :return:
        """
        ...

    def close(self):
        """
        关闭代理
        :return:
        """
        ...

    def request(self) -> ProxyRequest:
        """
        获取请求
        :return:
        """
        ...

    def response(self) -> ProxyResponse:
        """
        获取响应
        :return:
        """
        ...
    # ClassTag
