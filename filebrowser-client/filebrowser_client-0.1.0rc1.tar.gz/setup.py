# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filebrowser_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.3,<4.0.0']

entry_points = \
{'console_scripts': ['filebrowser-client = filebrowser_client:main']}

setup_kwargs = {
    'name': 'filebrowser-client',
    'version': '0.1.0rc1',
    'description': 'A simple CLI client for filebrowser',
    'long_description': '# Overview\n\nThe `filebrowser-client` is an async client library for the [Filebrowser](https://github.com/filebrowser/filebrowser) API.\nIt provides a cli client and a library to interact with the API.\n\n## Installation\n\nThe easiest way to install the `filebrowser-client` is to use `pip`:\n\n```bash\n    pip3 install filebrowser-client\n```\n\n## Features\n\n-   [x] Download a file or a directory\n-   [x] Upload a file or a directory\n-   [x] Delete a file or a directory\n\n## Usage\n\nThe `filebrowser-client` provides a cli client and a library to interact with the `Filebrowser` API.\n\n### CLI\n\nRun `filebrowser-client --help` to see the available commands.\n\n```bash\n    $ filebrowser-client --help\n    usage: filebrowser-client [-h] [--version] --host HOST [--username USERNAME] [--password PASSWORD] [--recaptcha RECAPTCHA] [--insecure]\n                            [--concurrent CONCURRENT] [--override] [--source SOURCE] [--destination DESTINATION]\n                            {upload,download,delete}\n\n    Filebrowser async client CLI\n\n    positional arguments:\n    {upload,download,delete}\n                            Command to execute\n\n    optional arguments:\n    -h, --help            show this help message and exit\n    --version             show program\'s version number and exit\n    --host HOST           Filebrowser host\n    --username USERNAME   Filebrowser username\n    --password PASSWORD   Filebrowser password\n    --recaptcha RECAPTCHA\n                            Filebrowser recaptcha\n    --insecure            Disable SSL verification\n    --concurrent CONCURRENT\n                            Number of concurrent requests\n    --override            Override existing files\n    --source SOURCE       Source file or directory\n    --destination DESTINATION\n                            Destination file or directory\n\n```\n\n### Library\n\n```python\n    import asyncio\n    from filebrowser_client import FilebrowserClient\n\n    client = FilebrowserClient("http://localhost:8080", "admin", "admin")\n    asyncion.run(client.connect())\n\n    asyncio.run(client.download("/path/to/file", "/path/to/destination"))\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n## Development\n\nThe `filebrowser-client` is developed using `poetry`, `pre-commit` and `Pylint`.\n### Prerequisites\n\n-   [Python 3.8+](https://www.python.org/downloads/)\n-   [Poetry](https://python-poetry.org/docs/#installation)\n-   [Pre-commit](https://pre-commit.com/#install)\n-   [Pylint](https://www.pylint.org/#install)\n\n## Build\n\n```bash\n    poetry build\n```\n',
    'author': 'Mohamed Cherkaoui',
    'author_email': 'chermed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
