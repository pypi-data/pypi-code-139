# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
    name="report_client",  # 发布的包的名称
    version="1.0.0",  # 发布包的版本序号
    description="test",  # 发布包的描述信息
    py_modules=['__init__', 'report_client']  # 发布包中的模块文件列表
)
