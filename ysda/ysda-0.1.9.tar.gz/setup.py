# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Doc', 'my_tools', 'my_tools.tests']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=1.1,<2.0',
 'einops>=0.4.1,<0.5.0',
 'gradio>=3.7,<4.0',
 'implicit>=0.6.1,<0.7.0',
 'matplotlib>=3.5.0,<3.6.0',
 'numba>=0.56.2,<0.57.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.4.0,<2.0.0',
 'protobuf==3.19.4',
 'pytest>=7.1.3,<8.0.0',
 'pytorch-lightning>=1.6,<1.7',
 'scipy>=1.7,<2.0',
 'shap>=0.41.0,<0.42.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.11.0,<1.13',
 'wandb>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'ysda',
    'version': '0.1.9',
    'description': '',
    'long_description': '# YSDA\nYandex School of Data Analysis materials \n',
    'author': 'DimaKoshman',
    'author_email': 'koshmandk@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
