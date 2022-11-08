# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakesist']

package_data = \
{'': ['*']}

install_requires = \
['delb[https-loader]>=0.4,<0.5']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata']}

entry_points = \
{'delb': ['snakesist = snakesist.delb_plugins']}

setup_kwargs = {
    'name': 'snakesist',
    'version': '0.3.0',
    'description': 'A Python database interface for eXist-db',
    'long_description': '.. image:: https://i.ibb.co/JsZqM7z/snakesist-logo.png\n    :target: https://snakesist.readthedocs.io\n\nsnakesist\n=========\n\n.. image:: https://badge.fury.io/py/snakesist.svg\n    :target: https://badge.fury.io/py/snakesist\n\n.. image:: https://readthedocs.org/projects/snakesist/badge/?version=latest\n    :target: https://snakesist.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://github.com/delb-xml/snakesist/actions/workflows/tests.yml/badge.svg\n    :target: https://github.com/delb-xml/snakesist/actions/workflows/tests.yml\n\n\n``snakesist`` is a Python database interface for `eXist-db <https://exist-db.org>`_.\nIt supports basic CRUD operations and uses `delb <https://delb.readthedocs.io>`_ for representing the yielded resources.\n\n.. code-block:: shell\n\n    pip install snakesist\n\n``snakesist`` allows you to access individual documents from the database using a ``delb.Document`` object, either by simply passing a URL\n\n.. code-block:: python\n\n    >>> from delb import Document\n\n    >>> manifest = Document("existdb://admin:@localhost:8080/exist/db/manifestos/dada_manifest.xml")\n    >>> [header.full_text for header in manifest.xpath("//head")]\n    ["Hugo Ball", "Das erste dadaistische Manifest"]\n\nor by passing a relative path to the document along with a database client which you can subsequently reuse\n\n.. code-block:: python\n\n    >>> from snakesist import ExistClient\n\n    >>> my_local_db = ExistClient(host="localhost", port=8080, user="admin", password="", root_collection="/db/manifests")\n    >>> dada_manifest = Document("dada_manifest.xml", existdb_client=my_local_db)\n    >>> [header.full_text for header in dada_manifest.xpath("//head")]\n    ["Hugo Ball", "Das erste dadaistische Manifest"]\n    >>> communist_manifest = Document("communist_manifest.xml", existdb_client=my_local_db)\n    >>> communist_manifest.xpath("//head").first.full_text\n    "Manifest der Kommunistischen Partei"\n\n\nand not only for accessing individual documents, but also for querying data across multiple documents\n\n.. code-block:: python\n\n    >>> all_headers = my_local_db.xpath("//*:head")\n    >>> [header.node.full_text for header in all_headers]\n    ["Hugo Ball", "Das erste dadaistische Manifest", "Manifest der Kommunistischen Partei", "I. Bourgeois und Proletarier.", "II. Proletarier und Kommunisten", "III. Sozialistische und kommunistische Literatur", "IV. Stellung der Kommunisten zu den verschiedenen oppositionellen Parteien"]\n\nYou can of course also modify and store documents back into the database or create new ones and store them.\n\n\nYour eXist instance\n-------------------\n\n``snakesist`` leverages the\n`eXist RESTful API <https://www.exist-db.org/exist/apps/doc/devguide_rest.xml>`_\nfor database queries. This means that allowing database queries using\nPOST requests on the RESTful API is a requirement in the used eXist-db\nbackend. eXist allows this by default, so if you haven\'t configured your\ninstance otherwise, don\'t worry about it.\n\nWe aim to directly support all most recent releases from each major branch.\nYet, there\'s no guarantee that releases older than two years will be kept as a\ntarget for tests. Pleaser refer to the values of\n``jobs/tests/matrix/exist-version`` in the `CI\'s configuration file`_ for\nwhat\'s currently considered.\n\n.. _CI\'s configuration file: https://github.com/delb-xml/snakesist/blob/main/.github/workflows/tests.yml\n',
    'author': 'Theodor Costea',
    'author_email': 'theo.costea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/delb-xml/snakesist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
