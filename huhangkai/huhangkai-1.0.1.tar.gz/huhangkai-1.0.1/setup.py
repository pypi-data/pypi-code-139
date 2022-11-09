from setuptools  import setup, find_packages

setup(
    name='huhangkai',  # 对外模块的名字
    version='1.0.1',  # 版本号
    description='接口自动化',  # 描述
    author='胡杭凯',  # 作者
    author_email='3173825608@qq.com',
    package_dir={"": "commen"},
    python_requires=">=3.7",
    install_requires=[
        "faker",
        "requests"
    ],
)