# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_sacred', 'neptune_sacred.impl']

package_data = \
{'': ['*']}

install_requires = \
['flatten-dict', 'neptune-client>=0.16.7', 'sacred']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'neptune-sacred',
    'version': '0.10.1',
    'description': 'Neptune.ai sacred integration library',
    'long_description': '# Neptune + Sacred Integration\n\nNeptune is a tool used for experiment tracking, model registry, data versioning, and live model monitoring. This integration lets you use it as a UI (frontend) for the experiments you track in Sacred.\n\n## What will you get with this integration?\n\n* Log, display, organize, and compare ML experiments in a single place\n* Version, store, manage, and query trained models, and model building metadata\n* Record and monitor model training, evaluation, or production runs live\n\n## What will be logged to Neptune?\n\n* Hyper-parameters\n* Losses & metrics\n* Training code(Python scripts or Jupyter notebooks) and git information\n* Dataset version\n* Model Configuration\n* [Other metadata](https://docs.neptune.ai/you-should-know/what-can-you-log-and-display)\n\n![image](https://user-images.githubusercontent.com/97611089/160633857-48aa87ac-fcab-4225-8172-05aba159feaf.png)\n*Example custom dashboard in the Neptune UI*\n\n\n## Resources\n\n* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/experiment-tracking/sacred)\n* [Code example on GitHub](https://github.com/neptune-ai/examples/tree/main/integrations-and-supported-tools/sacred/scripts)\n* [Example dashboard in the Neptune app](https://app.neptune.ai/o/common/org/sacred-integration/e/SAC-11/dashboard/Sacred-Dashboard-6741ab33-825c-4b25-8ebb-bb95c11ca3f4)\n* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/main/integrations-and-supported-tools/sacred/notebooks/Neptune_Sacred.ipynb)\n\n## Example\n\n```python\n# On the command line:\npip install neptune-client[sacred] sacred torch torchvision\n```\n```python\n# In Python:\nimport neptune.new as neptune\n\n\n# Start a run\nrun = neptune.init(project = "common/sacred-integration",\n                   api_token = "ANONYMOUS")\n\n# Create a sacred experiment\nexperiment = Experiment("image_classification", interactive=True)\n\n# Add NeptuneObserver and run the experiment\nexperiment.observers.append(NeptuneObserver(run=neptune_run))\nexperiment.run()\n```\n\n## Support\n\nIf you got stuck or simply want to talk to us, here are your options:\n\n* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions)\n* You can submit bug reports, feature requests, or contributions directly to the repository.\n* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),\n* You can just shoot us an email at support@neptune.ai\n',
    'author': 'neptune.ai',
    'author_email': 'contact@neptune.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://neptune.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
