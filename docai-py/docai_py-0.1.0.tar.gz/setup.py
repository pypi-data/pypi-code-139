# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docai',
 'docai.annotations',
 'docai.common',
 'docai.generated',
 'docai.generated.api',
 'docai.generated.api.apps',
 'docai.generated.api.auth',
 'docai.generated.api.billing',
 'docai.generated.api.butler_ops',
 'docai.generated.api.create_doc_type_jobs',
 'docai.generated.api.default',
 'docai.generated.api.document_types',
 'docai.generated.api.features',
 'docai.generated.api.incorrect_documents',
 'docai.generated.api.ml_models',
 'docai.generated.api.model_library',
 'docai.generated.api.models',
 'docai.generated.api.queues',
 'docai.generated.api.users',
 'docai.generated.models',
 'docai.predictions',
 'docai.test',
 'docai.training']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.3.0,<23.0.0',
 'evaluate>=0.3.0,<0.4.0',
 'httpx>=0.15.4,<0.24.0',
 'numpy>=1.17.0,<2.0.0',
 'pdf2image>=1.14.0,<2.0.0',
 'pillow>=8.0.0,<10.0.0',
 'python-dateutil>=2.8.1,<2.9.0',
 'seqeval>=1.2.2,<2.0.0',
 'transformers>=4.20.0,<5.0.0',
 'typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'docai-py',
    'version': '0.1.0',
    'description': 'Butler Doc AI',
    'long_description': '# Butler Doc AI\nWelcome to [Butler Doc AI](https://butlerlabs.ai)\n\n## Requirements\nPython >= 3.7\n\n## Installation & Usage\nTo install Doc AI with pip:\n```sh\npip install docai-py\n```\n\n### System Dependencies\n#### Mac\n- Install [poppler](http://macappstore.org/poppler/)\n\n#### Linux\n- Install poppler-utils via your package manager\n\n## Getting Started\nPlease follow the [installation procedure](#installation--usage) and then run the following:\n\n```python\n\nfrom docai import PredictionClient\n\n# Get API Key from https://docs.butlerlabs.ai/reference/uploading-documents-to-the-rest-api#get-your-api-key\napi_key = \'<api-key>\'\n# Get Queue ID from https://docs.butlerlabs.ai/reference/uploading-documents-to-the-rest-api#go-to-the-model-details-page\nqueue_id = \'<queue_id>\'\n# Path to a local JPEG, PNG, or PDF file\nlocal_file_path = \'example.pdf\'\n\nextraction_results = PredictionClient(api_key).extract_document(queue_id, local_file_path)\nprint(extraction_results)\n```\n\n## Maintain\n### Install Packages for Development\nInstall [poetry](https://python-poetry.org/docs/#installation) on your host machine\n```sh\npoetry install\n```\n\n### Butler REST API Codegen\nTo regenerate code updates to REST API:\n```sh\nopenapi-python-client update --url https://app.butlerlabs.ai/api/docs-json --config codegen.yaml\n```\n\n### Running Unit Tests\nTo run unit tests:\n```sh\npoetry run pytest\n```\n\n### Adding a New Dependency\nTo add a new pip package dependency, see [poetry add](https://python-poetry.org/docs/cli/#add).\nFor versioning, it is best to use the minimum version that works, combined with `^`, `~`, or `>=` and `<` checks.\nFor example:\n- `poetry add my-package@^1.2.3` is a shorthand for `>=1.2.3,<2.0.0`\n- `poetry add my-package@~1.2.3` is a shorthand for `>=1.2.3,<1.3.0`\n- `poetry add "my-package>=1.2.3,<4.5.6"`\n\nFor development only dependencies, make sure to include the `--dev` flag.\n\n### Build and Publish\n\n#### Build and Publish Setup\n```sh\n# setup for testpypi\npoetry config repositories.testpypi https://test.pypi.org/legacy/\npoetry config pypi-token.testpypi <testpypi token>\n\n# setup for pypi\npoetry config repositories.pypi https://pypi.org/legacy/\npoetry config pypi-token.pypi <pypi token>\n```\n\n#### Build and Publish Procedure\nUpdate `pyproject.toml` and `docai/__init__.py` to have a new version number\n\n```sh\n# build packages\npoetry build\n\n# upload to test pypi\npoetry publish -r testpypi\n\n# test install from test pypi\npip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple docai-py\n\n# upload to real pypi\npoetry publish -r pypi\n```\n',
    'author': 'Butler Labs',
    'author_email': 'support@butlerlabs.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://butlerlabs.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
