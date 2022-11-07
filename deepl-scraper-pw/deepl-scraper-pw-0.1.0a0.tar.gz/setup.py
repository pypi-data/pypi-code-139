# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_scraper_pw']

package_data = \
{'': ['*']}

install_requires = \
['about-time>=4.1.0,<5.0.0',
 'get-pwbrowser-sync>=0.1.2,<0.2.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'set-loglevel>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['deepl-scraper-playwright = '
                     'deepl_scraper_pw.__main__:app']}

setup_kwargs = {
    'name': 'deepl-scraper-pw',
    'version': '0.1.0a0',
    'description': 'Scrape deepl using playwright',
    'long_description': '# deepl-scraper-playwright\n[![pytest](https://github.com/ffreemt/deepl-scraper-playwright/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/deepl-scraper-playwright/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl_scraper_pw.svg)](https://badge.fury.io/py/deepl_scraper_pw)\n\nScrape deepl using playwright\n\n## Install it\n\n```shell\npip install deepl-scraper-pw\n\n# pip install git+https://github.com/ffreemt/deepl-scraper-playwright\n# poetry add git+https://github.com/ffreemt/deepl-scraper-playwright\n# git clone https://github.com/ffreemt/deepl-scraper-playwright && cd deepl-scraper-playwright\n```\n\n## Use it\n```python\nfrom pprint import pprint\nfrom deepl_scraper_pw import deepl_tr\n\npprint(deepl_tr("Test me\\n\\nTest him"))\n# \'测试我\\n\\n测试他\'\n\npprint(deepl_tr("Test me\\n\\nTest him", from_lang="en", to_lang="de"))\n# \'Teste mich\\n\\nTesten Sie ihn\'\n```\n## Debug\nShould something go wrong, you can turn on HEADFUL (a firefox browser will show up). Place .env in the current work directory, with the following content:\n```bash\nPWBROWSER_HEADFUL=1\n```\n\nYou can also set DEBUG env variable to turn on detailed debug messages, in Windows:\n```\nset DEBUG=1\n```\nIn Linux and friends\n```\nexport DEBUG=1\n```',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/deepl-scraper-playwright',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
