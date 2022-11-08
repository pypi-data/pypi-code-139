# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperer']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hyperer-cargo = hyperer.cargo:main',
                     'hyperer-rg = hyperer.rg:main']}

setup_kwargs = {
    'name': 'hyperer',
    'version': '0.2.1',
    'description': 'Injects hyperlinks into terminal commands',
    'long_description': "`hyperer` adds [terminal hyperlinks] to the output of other commands.\nFor example, `hyperer-rg` runs [ripgrep] and links to the files it finds.\n\n[terminal hyperlinks]: https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda\n[ripgrep]: https://github.com/BurntSushi/ripgrep\n\n\nInstallation\n============\nInstall Python 3.9 or later and run `pip install hyperer` to install the hyperer commands into your system Python.\nAlternatively, if you're using the [Nix package manager], depend on the flake.nix in this repo.\n\n[Nix package manager]: https://nixos.org/manual/nix/stable/introduction.html\n\nCommands\n========\n* hyperer-rg - wraps [ripgrep] and links to files it finds\n* hyperer-cargo - wraps [cargo] and links to compilation failures, test failures, and backtraces\n\n[cargo]: https://doc.rust-lang.org/cargo/\n\nCredit\n======\nThe basic idea and `hyperer-rg` comes from [kitty].\n[hyperlinked_grep] is kitty's version of `hyperer-rg`.\nIf you only want ripgrep links and you already have kitty installed, you can run `kitty +kitten hyperlinked_grep` and you don't need to install `hyperer`.\nI created this project to have a home for `hyperer-cargo` and to be able to hyperlink ripgrep without installing all of kitty.\n\n[kitty]: https://sw.kovidgoyal.net/kitty/\n[hyperlinked_grep]: https://sw.kovidgoyal.net/kitty/kittens/hyperlinked_grep/\n\nMany thanks to the kitty project!\nConsider [sponsoring its creator][sponsor Kovid] to help move the terminal forward.\n\n[sponsor Kovid]: https://github.com/sponsors/kovidgoyal\n",
    'author': 'Charlie Groves',
    'author_email': 'c@sevorg.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/groves/hyperer',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
