# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ssg']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.1.3,<9.0.0',
 'debugpy>=1.5.0,<2.0.0',
 'markdown2>=2.4.1,<3.0.0',
 'pytest>=7.2.0,<8.0.0']

entry_points = \
{'console_scripts': ['my_package_cli = src.ssg.app:run']}

setup_kwargs = {
    'name': 'myssg',
    'version': '0.1.2',
    'description': '',
    'long_description': "# This is a small tool to render personal blog\n\n![Blog generator tool](https://github.com/tvph/ssg/actions/workflows/python-app.yml/badge.svg)\n\n## Prerequisite\n\n1. `make`\n2. `python`\n3. `poetry`\n\n## Usage\n\n* I've created a [tool](https://github.com/tvph/ssg) to render from markdown file to static site by `Python` for my self.\n* To use this template, you need to clone the repo first. The project should have this structure:\n\n```\n    |_ prototypes/       # contains .md file, you will write your posts in here.\n    |_ posts/            # contains all html posts file after run ./render\n    |_ tags/             # contains all html tags file after run ./render\n    |_ templates/        # contains jinja templates for constructing posts, tags html files\n    |_ static/           # contains static file like styles or script for your pages\n    |_ index.html        # home page of blog\n    |_ app.py            # blog generator tool\n    |_ test_app.py       # test all functions of blog generator tool\n    |_ Makefile          # command for render html files\n    |_ requirements.txt  # for create environment for github actions\n    |_ poetry.lock\n    |_ pyproject.toml\n\n```\n\n* Firstly, if this is the first time you use this tool:\n    * You need to `fork` this repo to your, then change the name of repo following this format: `<your_github_username>.github.io`. And cloning it to your local machine: `git clone https://github.com/...`.\n    * Then you need to create `prototypes`, `tags` and `posts` folder by run: `make init`.\n\n* Secondly, you need to install environment to render blog. Run: `make install`.\n\n* Then go to `prototypes` folder and write the your posts in `.md` format, edit the metadata and push them into `prototypes` folder. Notice that, the metadata of .md file you need to keep following these formats\n\n```\ntitle: ....\ndate: ....\ntags: ....\nname: ....\nsummary: ....\n```\n* After the first time, you only need to write posts and render to html.\n\n* To render blog posts:\n\n\t* Run `make clean` to delete old html files.\n\t* Run `make test` to run test.\n\t* Run `make run` to render all html files to `posts` and `tags` folder.\n\n* Push to your repo, and go to `https://<your_github_username>.github.io/` to see.\n\n* To read more about `github pages`. Read [this guide](https://pages.github.com/)\n\n* In addition, you can add a comment plugin your self call [utterances](https://utteranc.es/?installation_id=19767855&setup_action=install). After that, go to\n`templates/post.html` and replace the script in `{% block script %}{% endblock %}` with your script.\n\n* You can put your information into `config.yml` file\n\n@LICENSE: [MIT](https://github.com/tvph/ssg/blob/master/LICENSE)\n",
    'author': 'Tran Viet Phuoc',
    'author_email': 'phuoc.finn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tranvietphuoc/ssg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
