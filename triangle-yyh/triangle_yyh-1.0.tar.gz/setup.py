import setuptools
setuptools.setup(
    name="triangle_yyh",  # 库的名称
    version="1.0",  # 库的版本
    author="yyh",  # 库的作者
    author_email="1807875605@qq.com",  # 作者邮箱
    description="test_pypi",  # 库的简介
    long_description="test_pypi",  # 库的详细说明
    long_description_content_type="text/markdown",  # 库的详细说明的内容形式
    packages=setuptools.find_packages(),  # 在分发包中的所有Python导入包的列表，自动发现所有包和子包
    classifiers=[
        "Programming Language :: Python :: 3",  # 该软件包仅与Python 3兼容
        "License :: OSI Approved :: MIT License",  # 根据MIT许可证进行许可
        "Operating System :: OS Independent",  # 与操作系统无关
    ],
)
