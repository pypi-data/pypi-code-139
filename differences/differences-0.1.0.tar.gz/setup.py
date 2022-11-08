# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['differences',
 'differences.attgt',
 'differences.datasets',
 'differences.did',
 'differences.tests',
 'differences.tools',
 'differences.tools.feols',
 'differences.twfe']

package_data = \
{'': ['*']}

install_requires = \
['formulaic>=0.3.4,<0.4.0',
 'joblib>=1.2.0,<2.0.0',
 'linearmodels>=4.27,<5.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.4,<1.5',
 'plotto>=0.1.1,<0.2.0',
 'pyhdfe>=0.1.0,<0.2.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'statsmodels>=0.13,<1.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'differences',
    'version': '0.1.0',
    'description': 'difference-in-differences estimation and inference in Python',
    'long_description': 'difference-in-differences and event study estimation and inference in Python.\n\n\n## Installing\n\nThe latest release can be installed using pip\n\n```bash\npip install differences\n```\n\nsee the [Documentation](https://differences.readthedocs.io/en/latest/) for more details.\n',
    'author': 'Bernardo Dionisi',
    'author_email': 'bernardo.dionisi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bernardodionisi/differences',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
