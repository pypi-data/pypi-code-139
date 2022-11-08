# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splunk_contentctl',
 'splunk_contentctl.actions',
 'splunk_contentctl.detection_testing',
 'splunk_contentctl.detection_testing.modules',
 'splunk_contentctl.enrichments',
 'splunk_contentctl.helper',
 'splunk_contentctl.input',
 'splunk_contentctl.objects',
 'splunk_contentctl.output']

package_data = \
{'': ['*'],
 'splunk_contentctl': ['templates/*', 'templates/detections/*'],
 'splunk_contentctl.output': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'attackcti>=0.3.7,<0.4.0',
 'pycvesearch>=1.2,<2.0',
 'pydantic>=1.10.2,<2.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'xmltodict>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['contentctl = splunk_contentctl.contentctl:main']}

setup_kwargs = {
    'name': 'splunk-contentctl',
    'version': '1.0.1',
    'description': 'Splunk Content Control Tool',
    'long_description': '# contentctl\n\n# TODO\n* take a stab at the .conf file\n* clean up pandentic folder structure and use spec files for the object validation\n* remove app listing and pre-installing them\n* remove github integration\n\n',
    'author': 'STRT',
    'author_email': 'research@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
