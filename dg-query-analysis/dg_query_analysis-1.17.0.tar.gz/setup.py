from setuptools import setup, find_packages

__version__ = '1.17.0' # 版本号
requirements = open('requirements.txt').readlines() # 依赖文件
setup(
    name='dg_query_analysis', # 在pip中显示的项目名称
    version=__version__,
    author='zhouyu',
    author_email='zhouyu@datagrand.com',
    url='https://pypi.org/project/dg_query_analysis',
    description='version',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6.0',
    install_requires=requirements # 安装依赖
)