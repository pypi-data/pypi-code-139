# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['max_yaml']
install_requires = \
['maxconsole>=0.4.0,<0.5.0', 'pyaml>=21.10.1,<22.0.0']

entry_points = \
{'console_scripts': ['max_yaml = myaml:main',
                     'setup_files = static.setup_files:main']}

setup_kwargs = {
    'name': 'max-yaml',
    'version': '0.1.0',
    'description': 'Creates dump, dumps, load, and load function for yaml doc based on the json stdlib.',
    'long_description': '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" lang="en">\n<head>\n\t<meta charset="utf-8"/>\n\t<title>README.md</title>\n\t<meta name="path" content="README.md"/>\n\t<meta name="author" content="Max Ludden"/>\n\t<meta name="date" content="2022-10-31 7:28 AM EST"/>\n\t<link type="text/css" rel="stylesheet" href="static/style.css"/>\n\t<meta name="url" content="https://github.com/maxludden/maxsetup/README.html ..."/>\n\t<meta name="viewport" content="width=device-width, initial-scale=1">\n\n</head>\n<body>\n\n<h1><span class="github">maxludden</span>/<span class="repo">max_yaml</span></h1>\n\n<p>This is a wrapper of PyYAML to make it easier to use. It creates functions similar to the stdlib&#8217;s &#8216;json&#8217; module.</p>\n\n<h3 id="installation">Installation</h3>\n\n<p>max_yaml can be installed from PyPi with your favorite package manager.</p>\n\n<h4>pipx<span style="font-size:0.6em;">(recommended)</span></h4>\n\n<pre><code class="bash">pipx install max_yaml\n</code></pre>\n\n<h4 id="pip">pip</h4>\n\n<pre><code class="bash">pip install max_yaml\n</code></pre>\n\n<h4 id="poetry">poetry</h4>\n\n<pre><code class="bash">poetry add max_yaml\n</code></pre>\n\n<h2 id="usage">Usage</h2>\n\n<p>The helper functions are familiar to any developer familiar with the JSON module from the stdlib:</p>\n\n<pre><code class="python">import max_yaml as yaml\n\nyaml.dump(data, file)\n\nyaml.dumps(data)\n\nyaml.load(file)\n\nyaml.loads(string)\n</code></pre>\n\n<p>There are also some helper functions mapped to the Safe Loader and Dumper from the PyYAML library:</p>\n\n<pre><code class="python">import max_yaml as yaml\n\nyaml.safe_dump(data, file)\n\nyaml.safe_dumps(data)\n\nyaml.safe_load(file)\n\nyaml.safe_loads(string)\n</code></pre>\n\n<p>All of the functions are taking advantage of the faster <code>C</code> Loaders and Dumpers if they are available. If not, they will fall back to the slower <code>Python</code> versions.</p>\n\n<h2 id="license">License</h2>\n\n<div class="license">\n    <h4>MIT License</h4>\n    <p>Copyright (c) 2022 Maxwell Owen Ludden</p>\n    <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>\n    <p>copies or substantial portions of the Software.</p>\n    <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>\n</div>\n\n</body>\n</html>\n',
    'author': 'maxludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
