# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['boots']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0', 'numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'boots',
    'version': '0.1.0',
    'description': 'A tiny statistical bootstraping library.',
    'long_description': '# Boots - A Tiny Bootstrapping Library\n\nThis is a tiny library for doing bootstrap sampling and estimating. It pulls together various tricks to make the process as fast and painless as possible. The tricks included are:\n\n- Parallel execution with [`joblib`](https://joblib.readthedocs.io/en/latest/parallel.html) \n- [The Bayesian bootstrap](https://matteocourthoud.github.io/post/bayes_boot/) with two-level sampling.\n- The [Vose method](https://github.com/MaxHalford/vose) for fast weighted sampling with replacement\n\n**Install**\n\n```bash\npip install boots\n```\n\n## Example\n\n```python\nimport numpy as np\n\nx = np.random.pareto(2, 100)\n\nsamples = bootstrap(\n    data=x,\n    statistic=np.median,\n    n_iterations=1000,\n    seed=1234,\n    n_jobs=-1\n)\n\n# bayesian two-level w/ 4 parallel jobs\nsamples = bootstrap(\n    data=x,\n    statistic=np.median, \n    n_iterations=1000, \n    seed=1234, \n    n_jobs=4, \n    bayesian=True\n)\n\n# do something with it\nimport pandas as pd\nposterior = pd.Series(samples)\nposterior.describe(percentiles=[0.025, 0.5, 0.975])\n```\n\n',
    'author': 'Peter Baumgartner',
    'author_email': '5107405+pmbaumgartner@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
