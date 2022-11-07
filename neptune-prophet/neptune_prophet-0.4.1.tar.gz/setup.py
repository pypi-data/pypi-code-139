# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_prophet', 'neptune_prophet.impl']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib<=3.4.3',
 'neptune-client>=0.15.0',
 'numpy',
 'pandas',
 'prophet>=1.0',
 'scipy',
 'statsmodels>=0.13.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1', 'plotly']}

setup_kwargs = {
    'name': 'neptune-prophet',
    'version': '0.4.1',
    'description': 'Neptune.ai Prophet integration library',
    'long_description': '# Neptune + Prophet integration\n\nExperiment tracking, model registry, data versioning, and live model monitoring for Prophet trained models.\n\n## What will you get with this integration?\n\n* Log, display, organize, and compare ML experiments in a single place\n* Version, store, manage, and query trained models and model-building metadata\n* Record and monitor model training, evaluation, or production runs live\n\n## What will be logged to Neptune?\n\n* parameters,\n* forecast data frames,\n* residual diagnostic charts,\n* [other metadata](https://docs.neptune.ai/you-should-know/what-can-you-log-and-display)\n\n![image](https://user-images.githubusercontent.com/97611089/188817349-973a49b2-e0d3-44dd-b51d-7dec670158f9.png)\n*Example dashboard in the Neptune app showing diagnostic charts*\n\n## Resources\n\n* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/model-training/prophet)\n* [Code example on GitHub](https://github.com/neptune-ai/examples/tree/main/integrations-and-supported-tools/prophet/scripts)\n* [Example project in the Neptune app](https://app.neptune.ai/o/common/org/fbprophet-integration/experiments?split=tbl&dash=charts&viewId=standard-view)\n* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/main/integrations-and-supported-tools/prophet/notebooks/Neptune_prophet.ipynb)\n\n## Example\n\n### Before you start\n\n- [Install and set up Neptune](https://docs.neptune.ai/getting-started/installation).\n- Have Prophet installed.\n\n### Installation\n\n```python\npip install neptune-prophet\n```\n\n### Logging example\n\n```python\nimport pandas as pd\nfrom prophet import Prophet\nimport neptune.new as neptune\nimport neptune.new.integrations.prophet as npt_utils\n\n\n# Start a run\nrun = neptune.init_run(project="common/fbprophet-integration", api_token=neptune.ANONYMOUS_API_TOKEN)\n\n\n# Load dataset and fit model\ndataset = pd.read_csv(\'https://raw.githubusercontent.com/facebook/prophet/main/examples/example_wp_log_peyton_manning.csv\'\n)\nmodel = Prophet()\nmodel.fit(dataset)\n\n\n# Log summary metadata (including model, dataset, forecast and charts)\nrun["prophet_summary"] = npt_utils.create_summary(model=model, df=df, fcst=forecast)\n\n\n# Stop the run\nrun.stop()\n```\n\n## Support\n\nIf you got stuck or simply want to talk to us, here are your options:\n\n* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions).\n* You can submit bug reports, feature requests, or contributions directly to the repository.\n* Chat! In the Neptune app, click the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP).\n* You can just shoot us an email at [support@neptune.ai](mailto:support@neptune.ai).\n',
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
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
