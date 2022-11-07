# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantha_streamlit_compare', 'semantha_streamlit_compare.components']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'streamlit>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'semantha-streamlit-compare',
    'version': '0.1.4',
    'description': 'This is the project for a streamlit component which uses semantha semantic compare.',
    'long_description': 'This project gives you an idea of how to use and build applications for streamlit. And all of this using semantha\'s native capabilities to process semantics in text.\n\ntl;dr: using Streamlit, you can employ semantha\'s semantic comparison with just three lines of code (see below).\n\n### Which Components Are Involved?\nStreamlit.io offers easy GUI implementations. semantha.ai is a semantic processing platform which provides a REST/API for many use cases, end systems, etc.\n\n![alt text](img/streamlit-compare-component.jpg "Streamlit Example")\n\n\n## Setup, Secret, and API Key\nTo use semantha, you need to request a secrets.toml file. You can request that at support@thingsthinking.atlassian.net<br />\nThe file is structured as follows:\n```\n[semantha]\nserver_url="URL_TO_SERVER"\napi_key="YOUR_API_KEY_ISSUED"\ndomain="USAGE_DOMAIN_PROVIDED_TO_YOU"\n```\n\n\n## Usage\nUsing the component is simple:\n\n```python\nfrom semantha_streamlit_compare.components.compare import SemanticCompare\n\ncompare = SemanticCompare()\ncompare.build_input(sentences=("First sentence", "Second sentence"))\n```\n',
    'author': 'thingsTHINKING GmbH',
    'author_email': 'github@thingsthinking.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
