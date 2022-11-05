# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cacheproxy']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp-client-cache>=0.7.3,<0.8.0',
 'aiohttp[speedups]>=3.8.3,<4.0.0',
 'aiosqlite>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['cacheproxy = cacheproxy.cli:main']}

setup_kwargs = {
    'name': 'cacheproxy',
    'version': '0.1.0',
    'description': 'Simple Python cache/caching proxy for Web development and something else',
    'long_description': '# CacheProxy\n\n[![test](https://github.com/nolze/cacheproxy/actions/workflows/test.yaml/badge.svg)](https://github.com/nolze/cacheproxy/actions/workflows/test.yaml)\n\nA simple Python cache/caching proxy for Web development and something else, built on [aiohttp](https://github.com/aio-libs/aiohttp) and [aiohttp-client-cache](https://github.com/requests-cache/aiohttp-client-cache) (a family project of [requests-cache](https://github.com/requests-cache/requests-cache)).\n\nUseful to avoid unfavorable massive accesses to external APIs during development, with little change, without preparing mocks. Not recommended for production.\n\n## Install\n\n```bash\npip install cacheproxy\n```\n\n## Usage\n\n### 1. Start up proxy\n\n```bash\n$ cacheproxy sqlite -c ./cache --expire-after 1800\nCache database: /Users/nolze/src/cacheproxy/cache.sqlite\n\n======== Running on http://0.0.0.0:8080 ========\n(Press CTRL+C to quit)\n```\n\nOther backends:\n\n```bash\ncacheproxy # in-memory\ncacheproxy memory # in-memory\ncacheproxy file -c ./cache # file-based, saved under ./cache/\ncacheproxy sqlite -c ./cache # sqlite, saved to ./cache.sqlite\n```\n\n### 2. Access through proxy\n\ncURL:\n\n```bash\ncurl http://0.0.0.0:8080/api.github.com/repos/nolze/cacheproxy # This request is cached until the expiration time\n# → {"id":...,"node_id":"...","name":"cacheproxy", ...\n```\n\nPython (requests):\n\n```python\nimport requests\n\nbase_url = "http://0.0.0.0:8080/api.github.com" # Just replace with "https://api.github.com" on production\nresp = requests.get(f"{base_url}/repos/nolze/cacheproxy") # or use urljoin()\nprint(resp.json())\n# → {\'id\': ...., \'node_id\': \'....\', \'name\': \'cacheproxy\', ...\n```\n\nJavaScript/Node:\n\n```javascript\nconst baseURL = "http://0.0.0.0:8080/api.github.com"; // Just replace with "https://api.github.com" on production\nconst resp = await fetch(`${baseURL}/repos/nolze/cacheproxy`);\nconst data = await resp.json();\nconsole.log(data);\n// → Object { id: ..., node_id: "...", name: "cacheproxy", ...\n```\n\n### Interact with or modify cached data\n\nUse [aiohttp-client-cache](https://github.com/requests-cache/aiohttp-client-cache) to load existing databases.\n\nSee also:\n\n- <https://aiohttp-client-cache.readthedocs.io/>\n\n## Todos\n\n- [ ] Better error handling\n- [ ] Write tests\n- [ ] Better logging\n- [ ] Support POST/PUT\n- [ ] Support switching http/https (with --http/--https flags)\n- [ ] Support DynamoDB, MongoDB, and Redis backends\n\n## License\n\nMIT\n',
    'author': 'nolze',
    'author_email': 'nolze@int3.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nolze/cacheproxy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
