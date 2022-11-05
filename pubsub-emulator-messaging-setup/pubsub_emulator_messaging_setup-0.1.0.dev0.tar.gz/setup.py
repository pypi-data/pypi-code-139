# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pubsub_emulator_messaging_setup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0',
 'click>=8.1',
 'google-api-core>=2.10',
 'google-auth>=2.13',
 'google-cloud-pubsub>=2.13',
 'grpcio>=1.50',
 'loguru>=0.6',
 'pydantic>=1.10']

entry_points = \
{'console_scripts': ['pubsub_emu_setup = '
                     'pubsub_emulator_messaging_setup.cli:main']}

setup_kwargs = {
    'name': 'pubsub-emulator-messaging-setup',
    'version': '0.1.0.dev0',
    'description': 'CLI tool to setup topics and subscriptions on a PubSub emulator from a definition in a YAML file',
    'long_description': '# pubsub-emulator-messaging-setup\n\nA small tool to create topics and subscriptions on a PubSub emulator in a simple and quick way.\n\n## Usage\n\nJust create a `pubsub.yml` file with the list of topics and topic\'s subscriptions like this one:\n\n```yaml\ntopics:\n  - name: my_topic\n    subscriptions:\n      - my_subscription_1\n      - my_subscription_2\n```\n\nThen run `pubsub_emu_setup`:\n\n```bash\npubsub_emu_setup\n```\n\nand it will automatically ensure that all the topics and subscriptions are created in the PubSUb emulator.\n\n## Starting a PubSub emulator in Docker\n\nGoogle provides a very convenient image to start a PubSub emulator locally with Docker.\n\nA simple Docker Compose file like the one below is suffice to have a working Pubsub emulator:\n\n```yaml\nversion: "3.8"\n\nservices:\n  pubsub_emulator:\n    image: google/cloud-sdk:emulators\n    ports:\n      - 8085:8085\n    command: |\n      gcloud beta emulators pubsub start --project=test-project --host-port=0.0.0.0:8085\n```\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/expobrain/pubsub-emulator-messaging-setup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
