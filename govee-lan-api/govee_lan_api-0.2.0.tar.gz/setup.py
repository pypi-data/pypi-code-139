# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['govee_lan_api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'govee-lan-api',
    'version': '0.2.0',
    'description': 'Implementation of the Govee LAN API to control supported Govee products',
    'long_description': '# Govee LAN API Client \n\n[![PyPI version](https://badge.fury.io/py/govee-lan-api.svg)](https://badge.fury.io/py/govee-lan-api) \n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Rhinomcd_govee-lan-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Rhinomcd_govee-lan-client)\n\nA simple API client for [Govee\'s LAN UDP API](https://app-h5.govee.com/user-manual/wlan-guide)\n\nThis was done in a weekend to help support a home assistant plugin for\ncontrolling govee devices over their new(ish) LAN API\n\n\n## Usage \n\n`pip install govee_lan_api`\n\nHere\'s some sample code that I\'m using to test this -- formal API docs and tests coming soon. \n\n```py\nfrom govee_lan_api import GoveeClient\nimport asyncio\nimport logging\n\nLIVING_ROOM_LIGHT = \'18:66:C4:32:38:30:1E:32\'\n\nRED = (255, 0, 0)\nGREEN = (0, 255, 0)\nBLUE = (0, 0, 255)\nPURPLE = (248, 207, 255)\n\n\nasync def main():\n    logging.basicConfig(level=logging.DEBUG)\n    client = GoveeClient()\n    await client.turn_on(LIVING_ROOM_LIGHT)\n    await client.set_brightness(LIVING_ROOM_LIGHT, 100)\n    await client.set_color_by_rgb(LIVING_ROOM_LIGHT, GREEN)\n\n    await client.set_brightness(LIVING_ROOM_LIGHT, 50)\n    await client.set_brightness(LIVING_ROOM_LIGHT, 1)\n    await client.set_brightness(LIVING_ROOM_LIGHT, 100)\n\n    await client.turn_on(LIVING_ROOM_LIGHT)\n    await client.set_color_by_rgb(LIVING_ROOM_LIGHT, RED)\n    await client.set_color_by_rgb(LIVING_ROOM_LIGHT, GREEN)\n    await client.set_color_by_rgb(LIVING_ROOM_LIGHT, BLUE)\n    await client.set_color_by_rgb(LIVING_ROOM_LIGHT, PURPLE)\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```',
    'author': 'Ryan McDonough',
    'author_email': 'Ryan@r2n.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
