# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dooti']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'pyobjc-core>=7.2,<8.0',
 'pyobjc-framework-UniformTypeIdentifiers>=7.2,<8.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['dooti = dooti.cli:main']}

setup_kwargs = {
    'name': 'dooti',
    'version': '0.2.0',
    'description': 'Manage default file and URI scheme handlers on macOS 12.0+',
    'long_description': '==============\nDooti overview\n==============\n\nManage default handlers for files and URI schemes on MacOS 12.0+.\n\n\nFeatures\n--------\n* Manage handlers by specifying file extension, UTI or URI scheme.\n* Specify handlers by name, bundle ID or absolute path.\n* Check your associations into a dotfiles repository and ensure an idempotent state by simply running ``dooti apply``.\n\n\nInstallation\n------------\nI recommend installing with `pipx <https://pypa.github.io/pipx/>`_, although pip will work fine as well:\n\n.. code-block:: bash\n\n        pipx install dooti\n\n\nQuickstart\n----------\n``dooti`` currently supports three specific subcommands (``ext``, ``scheme``, ``uti``) and a broad one (``apply``).\n\nLookup handlers\n~~~~~~~~~~~~~~~\nSimply pass a list of one specific type to the appropriate command. Example:\n\n.. code-block:: console\n\n    $ dooti ext html xml\n    html: /Applications/Firefox.app\n    xml: /Applications/Sublime Text.app\n\n    $ dooti --format json scheme http https ftp | jq\n    {\n      "http": "/Applications/Firefox.app",\n      "https": "/Applications/Firefox.app",\n      "ftp": "/System/Library/CoreServices/Finder.app"\n    }\n\n    $ dooti uti public.html\n    public.html: /Applications/Firefox.app\n\nSet handlers\n~~~~~~~~~~~~\nChanging the default handler can be requested by adding ``-x <handler_ref>`` to the lookup command. The handler reference can be a name, bundle ID or absolute filesystem path. Example:\n\n.. code-block:: console\n\n    $ dooti ext csv xml -x "Sublime Text"\n    The following extensions are set to be changed:\n    csv: /Applications/Numbers.app -> /Applications/Sublime Text.app\n    xml: /Applications/Firefox.app -> /Applications/Sublime Text.app\n\n    $ dooti scheme ftp -x /Applications/Firefox.app\n    The following scheme is set to be changed:\n    ftp: /System/Library/CoreServices/Finder.app -> /Applications/Firefox.app\n\n    $ dooti -tf json uti public.c-source -x com.sublimetext.4\n    {"changes": {"utis": {"public.c-source": {"from": "/Applications/Notes.app", "to": "/Applications/Sublime Text.app"}}}, "errors": []}\n\n\nEnsure state\n~~~~~~~~~~~~\n``dooti`` can ingest and apply a YAML configuration like this:\n\n.. code-block:: yaml\n\n    ext:\n      jpeg: Preview\n\n    scheme:\n      http: Firefox\n      mailto: Mail\n\n    uti:\n      public.c‑source: Sublime Text\n\n    app:\n      Sublime Text:\n        ext:\n          - py\n          - rst\n          - yml\n          - yaml\n        uti:\n          - public.fortran‑source\n\n      Brave Browser:\n        scheme:\n          - ipfs\n\nBy default, it looks at ``$XDG_CONFIG_HOME/dooti/config.yaml`` (and others, see ``docs/usage.rst``).\n\nLimitations\n-----------\n* The designated handler has to be installed before running the command.\n* Setting some URI scheme handlers (especially for http) might cause a prompt.\n* Setting some file extension handlers might be restricted (especially html seems to fail silently).\n\n\nWhy?\n----\nMost existing tools use `LSSetDefaultRoleHandlerForContentType <https://developer.apple.com/documentation/coreservices/1444955-lssetdefaultrolehandlerforconten>`_ and `LSSetDefaultHandlerForURLScheme <https://developer.apple.com/documentation/coreservices/1447760-lssetdefaulthandlerforurlscheme?language=objc>`_, which are deprecated in macOS 12.0. ``dooti`` uses a more recent API and should work on Monterey (12.0) and above.\n\n\nSimilar tools\n-------------\n* `duti <https://github.com/moretension/duti>`_\n* `openwith <https://github.com/jdek/openwith>`_\n* `defaultbrowser <https://gist.github.com/miketaylr/5969656>`_\n* `SwiftDefaultApps <https://github.com/Lord-Kamina/SwiftDefaultApps>`_\n',
    'author': 'jeanluc',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lkubb/dooti',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
