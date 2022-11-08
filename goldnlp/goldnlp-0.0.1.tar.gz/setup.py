# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['goldnlp']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2<3.0',
 'MarkupSafe<=2.0.1',
 'Pyphen==0.9.5',
 'blis<=0.7.5',
 'boto3>=1.21.23,<2.0.0',
 'certifi==2017.4.17',
 'dateparser==1.0.0',
 'elasticsearch-dsl==7.3.0',
 'fastapi>=0.67.0,<0.68.0',
 'fastnn>=0.3.0,<0.4.0',
 'fold-to-ascii==1.0.2.post1',
 'ipywidgets>=7.6.3,<8.0.0',
 'jupyterlab>=3.0.0,<4.0.0',
 'langdetect==1.0.7',
 'matplotlib==3.4.2',
 'mmh3>=3.0.0,<4.0.0',
 'nltk>=3.6.2,<4.0.0',
 'numba>=0.55.2,<0.56.0',
 'numpy==1.21.6',
 'openai>=0.15.0,<0.16.0',
 'pandas==1.3.0',
 'pillow>=8.3.1,<9.0.0',
 'probablepeople==0.5.4',
 'psycopg[pool]>=3.0.15,<4.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'pyvis>=0.1.9,<0.2.0',
 'scikit-learn==0.24.2',
 'scipy>=1.7.0,<2.0.0',
 'simhash==1.9.0',
 'spacy>=3.1.0,<3.2.0',
 'textdistance>=4.3.0,<5.0.0',
 'tqdm>=4.63.0,<5.0.0',
 'uvicorn>=0.14.0,<0.15.0',
 'wheel>=0.36.2,<0.37.0']

extras_require = \
{'docs': ['mkdocs-material>=8.1.6,<9.0.0',
          'mkdocstrings>=0.17.0,<0.18.0',
          'mkdocs-render-swagger-plugin>=0.0.3,<0.0.4'],
 'linkprediction': ['networkx>=2.6.3,<3.0.0'],
 'topicmodel': ['top2vec>=1.0.24,<2.0.0', 'gensim>=3.8.3,<4.0.0'],
 'torch': ['torch>=1.0.0,<2.0.0', 'torchvision<1.0.0'],
 'webextract': ['extruct>=0.13.0,<0.14.0',
                'boilerpy3>=1.0.5,<2.0.0',
                'pytidylib>=0.3.2,<0.4.0']}

setup_kwargs = {
    'name': 'goldnlp',
    'version': '0.0.1',
    'description': "Golden's NLP/NLU library focused on state-of-the-art NLP Tasks.",
    'long_description': None,
    'author': 'aychang95',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.10,<3.11',
}


setup(**setup_kwargs)
