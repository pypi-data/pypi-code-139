# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['game_resolver', 'game_resolver.games', 'game_resolver.util']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'game-resolver',
    'version': '0.2.2',
    'description': '',
    'long_description': '# game_resolver\n\nThis library is internal library for nishino-lab(The University of Tokyo)\n\nhttp://www.css.t.u-tokyo.ac.jp\n\n## Run Sample Game\n\nThis library has three type sample games(prisoner, battle of sex, cournot).\n\n```python\nfrom game_resolver.games.custom_game import Prisoner\nfrom game_resolver.nash_equilibrium import NashEquilibrium\n\nprisoner = Prisoner()\nne = NashEquilibrium()\neq = e.get_equilibrium(g)\nfor i in eq:\n    print(i)\n```\n\n## Run your own game\n\nA Nash equilibrium can be solved by representing the problem to be solved in the Game class.\n\n```python\nfrom game_resolver.games.custom_game import CustomGame\nfrom game_resolver.nash_equilibrium import NashEquilibrium\n\nplayer_num = 2\naction_list = ["Cooperate", "Defect"]\nall_player_action_list = [\n    ("Cooperate", "Cooperate"),\n    ("Cooperate", "Defect"),\n    ("Defect", "Cooperate"),\n    ("Defect", "Defect")\n]\npayoff_list = [\n    [3, 0, 5, 1],\n    [3, 5, 0, 1]\n]\n\nyour_own_game = CustomGame("volunteer_dilenma",\n                            player_num,\n                            action_list,\n                            all_player_action_list,\n                            payoff_list)\ne = NashEquilibrium()\neq = e.get_equilibrium(your_own_game)\nfor i in eq:\n    print(i)\n```\n',
    'author': 'nariaki-nishino',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
