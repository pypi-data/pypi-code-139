# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filebrowser_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.3,<4.0.0',
 'colorama>=0.4.6,<0.5.0',
 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['filebrowser-client = filebrowser_client:main']}

setup_kwargs = {
    'name': 'filebrowser-client',
    'version': '0.1.0',
    'description': 'An async CLI client and library for filebrowser API',
    'long_description': '# Overview\n\nThe `filebrowser-client` is an async client CLI and library for the [Filebrowser](https://github.com/filebrowser/filebrowser) API.\n\n## Installation\n\nThe easiest way to install the `filebrowser-client` is to use `pip`:\n\n```bash\n    pip3 install filebrowser-client\n```\n\n## Features\n\n-   [x] Download a remote file or a directory\n-   [x] Upload a file or a directory to a remote location\n-   [x] Delete a file or a directory from a remote location\n\n## Usage\n\nThe `filebrowser-client` provides a cli client and a library to interact with the `Filebrowser` API.\n\n### CLI\n\nRun `filebrowser-client --help` to see the global options and the available commands.\n\n```bash\n    filebrowser-client --help\n    Usage: filebrowser-client [OPTIONS] COMMAND [ARGS]...\n\n    Options:\n    --help  Show this message and exit.\n\n\n    Commands:\n    download  Download a file or a directory from a remote location\n    upload    Upload a file or a directory to a remote location\n    delete    Delete a file or a directory from a remote location\n```\n\n### Library\n\n```python\n    import asyncio\n    from filebrowser_client import FilebrowserClient\n\n    client = FilebrowserClient("http://localhost:8080", "admin", "admin")\n    asyncio.run(client.connect())\n\n    asyncio.run(client.download("/path/to/file", "/path/to/destination"))\n```\n\n## License\n\nThis project is licensed under the MIT License\n\n## Development\n\nThe `filebrowser-client` is developed using `poetry` and `pre-commit`.\n### Prerequisites\n\n-   [Python 3.7+](https://www.python.org/downloads/)\n-   [Poetry](https://python-poetry.org/docs/#installation)\n-   [Pre-commit](https://pre-commit.com/#install)\n\n### Setup\n\n```bash\n    poetry install\n    pre-commit install\n```\n## Build\n\n```bash\n    poetry build\n```\n',
    'author': 'Mohamed CHERKAOUI',
    'author_email': 'chermed@gmail.com',
    'maintainer': 'Mohamed CHERKAOUI',
    'maintainer_email': 'chermed@gmail.com',
    'url': 'https://github.com/chermed/filebrowser-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0',
}


setup(**setup_kwargs)
