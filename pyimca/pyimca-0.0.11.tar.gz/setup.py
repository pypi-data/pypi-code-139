# -*- coding: UTF-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='pyimca',  # 包名
      version='0.0.11',  # 版本号
      description='为工程创建一个统一的架构',
      long_description=long_description,
      author='Thrent',
      author_email='eel39@yahoo.com',
      url='https://github.com/Thrent33/IMCA_FRAME.git',
      packages=find_packages(),
      install_requires=[
        "pyyaml <= 5.3.1",
        "fire"
      ],
      entry_points={
        'console_scripts':[
          'imca=imca_frame.ImcaScript:main'
        ]
      },
      license='GNU General Public License v3.0',
      platforms=["Linux"]
      )