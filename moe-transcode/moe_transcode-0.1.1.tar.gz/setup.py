# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moe_transcode']

package_data = \
{'': ['*']}

install_requires = \
['moe>=1.5.1,<2.0.0']

entry_points = \
{'moe.plugins': ['transcode = moe_transcode']}

setup_kwargs = {
    'name': 'moe-transcode',
    'version': '0.1.1',
    'description': 'Plugin for Moe to transcode music.',
    'long_description': "#########\nTranscode\n#########\nPlugin for Moe that transcodes music.\n\nCurrently only flac -> mp3 [v0, v2, 320] is supported.\n\n************\nInstallation\n************\n1. Install via pip\n\n   .. code-block:: bash\n\n       $ pip install moe_transcode\n\n2. `Install ffmpeg <https://ffmpeg.org/download.html>`_\n\n   .. important::\n\n      Ensure ``ffmpeg`` is in your respective OS's path environment variable.\n\n*************\nConfiguration\n*************\nAdd ``transcode`` to the ``enabled_plugins`` configuration option.\n",
    'author': 'Jacob Pavlock',
    'author_email': 'jtpavlock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
