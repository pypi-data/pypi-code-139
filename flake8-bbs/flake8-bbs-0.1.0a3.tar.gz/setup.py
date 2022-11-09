# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_bbs']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.0']

entry_points = \
{'flake8.extension': ['BBS = flake8_bbs:StatementChecker']}

setup_kwargs = {
    'name': 'flake8-bbs',
    'version': '0.1.0a3',
    'description': 'A flake8 extension that checks blank lines before statements',
    'long_description': "# Flake8 - check for blank lines before statements\n\n![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)\n![License](https://img.shields.io/badge/License-MIT-blue)\n![codecov](https://codecov.io/gh/ts-mk/flake8-bbs/branch/initial/graph/badge.svg?token=PI2I083V09)]\n![CI](https://github.com/ts-mk/flake8-bbs/actions/workflows/tests.yml/badge.svg)\n\n\n## Introduction\n\nPEP 8 recommends to use blank lines only to separate logical sections:\n\n> Extra blank lines may be used (sparingly) to separate groups of related functions. Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations).\n>\n> Use blank lines in functions, sparingly, to indicate logical sections.\n\nHowever, some people believe that adding blank lines also before (compound) statements improves code readability which is otherwise hindered despite syntax highlighting that modern code editors provide, as demonstrated in the following example:\n\n```python\nimport os\n\na = 3\nif a == 1:\n    print(a)\nwith os.open('filename.txt') as f:\n    content = f.read_lines()\nif a == 2:\n    print(a)\n```\n\nThis Flake8 plugin therefore checks for a blank line before each statement as long as it's **not the first line of code within a module** and **not the first statement within another statement**.\n\n\n## Requirements\n\n* Python >= 3.8\n* flake8 >= 3.8.0\n\n\n## Use in production\n\nUntil version 1.0.0 is reached, this plugin is considered as **NOT ready for production**.\n\n\n## Statements and their error codes\n\nThe statements are split into different categories based on whether they are [simple statements](https://docs.python.org/3.11/reference/simple_stmts.html) or [compound statements](https://docs.python.org/3.11/reference/compound_stmts.html) and whether the error occurs between two statements of the same type or not. This allows you to filter entire groups using `BBS` and the first digit, e.g. `BBS3`.\n\n### BBS1xx: Simple statements\n\nSimple statements, excluding [expression statements](https://docs.python.org/3.11/reference/simple_stmts.html#expression-statements) and [assignment statements](https://docs.python.org/3.11/reference/simple_stmts.html#assignment-statements).\n\n| Statement     | Error  |\n|:--------------|:-------|\n| `assert`      | BBS101 |\n| `break`       | BBS102 |\n| `continue`    | BBS103 |\n| `del`         | BBS104 |\n| `global`      | BBS105 |\n| `import`      | BBS106 |\n| `import from` | BBS107 |\n| `nonlocal`    | BBS108 |\n| `pass`        | BBS109 |\n| `raise`       | BBS110 |\n| `return`      | BBS111 |\n| `yield`       | BBS112 |\n| `yield from`  | BBS113 |\n\n\n### BBS2xx: Simple statements of the same type\n\nTwo or more consecutive simple statements, e.g. `del`. Some of these errors shouldn't occur (e.g. `return` followed by another `return`) because having consecutive siblings of those types does not make sense but the plugin would raise those errors anyway.\n\n| Statement     | Error  |\n|:--------------|:-------|\n| `assert`      | BBS201 |\n| `break`       | BBS202 |\n| `continue`    | BBS203 |\n| `del`         | BBS204 |\n| `global`      | BBS205 |\n| `import`      | BBS206 |\n| `import from` | BBS207 |\n| `nonlocal`    | BBS208 |\n| `pass`        | BBS209 |\n| `raise`       | BBS210 |\n| `return`      | BBS211 |\n| `yield`       | BBS212 |\n| `yield from`  | BBS213 |\n\n### BBS3xx: Compound statements\n\n| Statement    | Error  |\n|:-------------|:-------|\n| `async def`  | BBS301 |\n| `async for`  | BBS302 |\n| `async with` | BBS303 |\n| `class`      | BBS304 |\n| `def`        | BBS305 |\n| `for`        | BBS306 |\n| `if`         | BBS307 |\n| `match`      | BBS308 |\n| `try`        | BBS309 |\n| `while`      | BBS310 |\n| `with`       | BBS311 |\n\n### BBS4xx: Compound statements of the same type\n\nTwo or more consecutive compound statements, e.g. `for`.\n\n| Statement    | Error  |\n|:-------------|:-------|\n| `async def`  | BBS401 |\n| `async for`  | BBS402 |\n| `async with` | BBS403 |\n| `class`      | BBS404 |\n| `def`        | BBS405 |\n| `for`        | BBS406 |\n| `if`         | BBS407 |\n| `match`      | BBS408 |\n| `try`        | BBS409 |\n| `while`      | BBS410 |\n| `with`       | BBS411 |\n\n\n## Configuration\n\nThe plugin checks for a blank line before **every statement**. There are no custom configuration options. Instead, you could simply ignore some errors. This system has benefits as well as drawbacks.\n\nThe benefit is that you could take advantage of Flake8's `ignore` and `per-file-ignores` (flake8>=3.7.0) config options and have a different behaviour for a different set of files:\n\n```ini\n[flake8]\nignore = BBS2\nper-file-ignores =\n    app/*: BBS101, BBS102, BBS103, BBS104, BBS105, BBS106, BBS107, BBS109, BBS110\n    tests/*: BBS1\n```\n\nThe drawback is that with more than 40 different errors, there is quite a bit to exclude... and it's certain that you would need to exclude some because the same or conflicting checks might already be applied by another plugin (e.g. checks by [flake8-import-order](https://github.com/PyCQA/flake8-import-order)) or should be handled by other formatting tools (e.g. [black](https://github.com/psf/black)).\n\n### Recommended exclusions\n\nA custom set of what makes sense to the author.\n\n```ini\n[flake8]\nignore = BBS101, BBS102, BBS103, BBS104, BBS105, BBS106, BBS107, BBS109, BBS110, BBS2\n```\n\n### All simple statements excluded\n\n...so only compound statements would raise errors.\n\n```ini\n[flake8]\nignore = BBS1, BBS2\n```\n",
    'author': 'Tomas Mrozek',
    'author_email': 'tm@nohup.run',
    'maintainer': 'Tomas Mrozek',
    'maintainer_email': 'tm@nohup.run',
    'url': 'https://github.com/ts-mk/flake8-bbs/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
