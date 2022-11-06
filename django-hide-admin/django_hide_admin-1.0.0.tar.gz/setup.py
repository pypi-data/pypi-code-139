# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hide_admin']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-hide-admin',
    'version': '1.0.0',
    'description': 'Hides Django admin from unauthorized users',
    'long_description': '# django-hide-admin\n\nHides Django admin from users without staff level access. Anonymous users or users without staff level access will see `404 Not found` error if they try to open the Django admin login page or any other admin pages.\n\nSince the Django admin login page is not available, your project should have a login page for users and staff. Once staff are logged in, they can open `/admin/` (by default) to access admin interface.\n\n# Installation\n\n```\npip install django-hide-admin\n```\n\n# Usage\n\nReplace `django.contrib.admin` with `hide_admin.apps.HideAdminConfig` in `INSTALLED_APPS`.\n',
    'author': 'Evgeniy Krysanov',
    'author_email': 'evgeniy.krysanov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/catcombo/django-hide-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
