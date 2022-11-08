# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nalogapi']
install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'nalogapi',
    'version': '0.1.0',
    'description': 'Unofficial synchronous wrapper for lknpd.nalog.ru API written in Python',
    'long_description': '# Неофициальная синхронная обёртка для API сервиса lknpd.nalog.ru на Python.\n\nСлужит для автоматизации отправки информации о доходах самозанятых и получения информации о созданных чеках.\n\nInspired by [https://github.com/alexstep/moy-nalog](https://github.com/alexstep/moy-nalog)\n\n## Использование\nУстановите пакет\n```bash\npip install nalogapi\n```\n\nИнициализаци и авторизация\n```python\nfrom nalogapi import NalogAPI\nNalogAPI.configure("inn", "password") #password that used in lkfl\n```\n\nОтправка информации о доходе\n```python\nNalogAPI.addIncome(datetime.utcnow(), 1.0, "Предоставление информационных услуг #970/2495")\n```\n\nФункция возвращает ссылку на чек вида [https://lknpd.nalog.ru/api/v1/receipt/344111066022/200egltxe8/print](https://lknpd.nalog.ru/api/v1/receipt/344111066022/200egltxe8/print)',
    'author': 'Mike Ovchinnikov',
    'author_email': 'mixao@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
