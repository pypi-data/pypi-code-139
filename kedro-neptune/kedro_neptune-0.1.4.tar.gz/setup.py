# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kedro_neptune']

package_data = \
{'': ['*']}

install_requires = \
['kedro>=0.18.0', 'neptune-client>=0.16.7', 'ruamel.yaml>=0.17.0,<0.18.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit',
         'pytest>=5.0',
         'pytest-cov==2.10.1',
         'neptune-optuna',
         'neptune-fastai']}

entry_points = \
{'kedro.hooks': ['neptune_hooks = kedro_neptune:neptune_hooks'],
 'kedro.project_commands': ['neptune = kedro_neptune:commands']}

setup_kwargs = {
    'name': 'kedro-neptune',
    'version': '0.1.4',
    'description': 'Neptune.ai integration with Kedro',
    'long_description': '# Neptune + Kedro Integration\n\nKedro plugin for experiment tracking and metadata management. It lets you browse, filter and sort runs in a nice UI, visualize node/pipeline metadata, and compare pipelines.\n\n## What will you get with this integration?\n\n* **browse, filter, and sort** your model training runs\n* **compare nodes and pipelines** on metrics, visual node outputs, and more\n* **display all pipeline metadata** including learning curves for metrics, plots, and images, rich media like video and audio or interactive visualizations from Plotly, Altair, or Bokeh\n* and do whatever else you would expect from a modern ML metadata store\n\n![image](https://user-images.githubusercontent.com/97611089/160640893-9b95aac1-095e-4869-88a1-99f2cba5a59f.png)\n*Kedro pipeline metadata in custom dashboard in the Neptune UI*\n\nNote: Kedro-Neptune plugin supports distributed pipeline execution and works in Kedro setups that use orchestrators like Airflow or Kubeflow.\n\n## Resources\n\n* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/automation-pipelines/kedro)\n* [Code example on GitHub](https://github.com/neptune-ai/examples/blob/main/integrations-and-supported-tools/kedro/scripts/kedro_neptune_quickstart)\n* [Runs logged in the Neptune app](https://app.neptune.ai/o/common/org/kedro-integration/e/KED-632/dashboard/Basic-pipeline-metadata-42874940-da74-4cdc-94a4-315a7cdfbfa8)\n* How to [Compare Kedro pipelines](https://docs.neptune.ai/integrations-and-supported-tools/automation-pipelines/kedro/compare-kedro-pipelines)\n* How to [Compare results between Kedro nodes](https://docs.neptune.ai/integrations-and-supported-tools/automation-pipelines/kedro/compare-results-between-kedro-nodes)\n* How to [Display Kedro node metadata and outputs](https://docs.neptune.ai/integrations-and-supported-tools/automation-pipelines/kedro/display-kedro-node-metadata-and-outputs)\n\n## Example\n\n```python\n# On the command line:\npip install neptune-client kedro kedro-neptune\nkedro new --starter=pandas-iris\n\n# In your Kedro project directory:\nkedro neptune init\n```\n```python\n# In a pipeline node, in nodes.py:\nimport neptune.new as neptune\n\n# Add a Neptune run handler to the report_accuracy() function\n# and log metrics to neptune_run\ndef report_accuracy(predictions: np.ndarray, test_y: pd.DataFrame,\n                    neptune_run: neptune.run.Handler) -> None:\n    target = np.argmax(test_y.to_numpy(), axis=1)\n    accuracy = np.sum(predictions == target) / target.shape[0]\n\n    neptune_run["nodes/report/accuracy"] = accuracy * 100\n\n# Add the Neptune run handler to the Kedro pipeline\nnode(\n    report_accuracy,\n    ["example_predictions", "example_test_y", "neptune_run"],\n    None,\n    name="report")\n```\n```python\n# On the command line, run the Kedro pipeline\nkedro run\n```\n\n\n\n## Support\n\nIf you got stuck or simply want to talk to us, here are your options:\n\n* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions)\n* You can submit bug reports, feature requests, or contributions directly to the repository.\n* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),\n* You can just shoot us an email at support@neptune.ai\n',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
