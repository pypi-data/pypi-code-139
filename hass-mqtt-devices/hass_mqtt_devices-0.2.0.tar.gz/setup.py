# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hass_mqtt_devices', 'hass_mqtt_devices.cli']

package_data = \
{'': ['*']}

install_requires = \
['gitlike-commands>=0.2.1,<0.3.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pyaml>=21.10.1,<22.0.0',
 'thelogrus>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hmd = hass_mqtt_devices.cli.main_driver:hmd_driver',
                     'hmd-create-binary-sensor = '
                     'hass_mqtt_devices.cli.sensors:create_binary_sensor',
                     'hmd-create-device = '
                     'hass_mqtt_devices.cli.device_driver:create_device']}

setup_kwargs = {
    'name': 'hass-mqtt-devices',
    'version': '0.2.0',
    'description': '',
    'long_description': '<!-- START doctoc generated TOC please keep comment here to allow auto update -->\n<!-- DON\'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->\n## Table of Contents\n\n- [hass-mqtt-devices](#hass-mqtt-devices)\n  - [Supported Types](#supported-types)\n    - [Binary Sensors](#binary-sensors)\n      - [Usage](#usage)\n    - [Devices](#devices)\n      - [Usage](#usage-1)\n  - [Scripts Provided](#scripts-provided)\n    - [`hmd`](#hmd)\n    - [`hmd create binary sensor`](#hmd-create-binary-sensor)\n    - [`hmd create device`](#hmd-create-device)\n\n<!-- END doctoc generated TOC please keep comment here to allow auto update -->\n\n# hass-mqtt-devices\n\nA python 3 module that takes advantage of HA(Home Assistant(\'s MQTT discovery protocol to create sensors without having to define anything on the HA side.\n\nUsing MQTT discoverable devices lets us add new sensors and devices to HA without having to restart HA. This module includes scripts to make it easy to create discoverable devices from the command line if you don\'t want to bother writing python.\n\n## Supported Types\n\n### Binary Sensors\n\n#### Usage\n\n```py\nfrom hass_mqtt_devices.sensors import BinarySensor\n\n# Create a settings dictionary\n#\n# Mandatory Keys:\n#  mqtt_server\n#  mqtt_user\n#  mqtt_password\n#  device_id\n#  device_name\n#  device_class\n#\n# Optional Keys:\n#  mqtt_prefix - defaults to homeassistant\n#  payload_off\n#  payload_on\n#  unique_id\n\nconfigd = {\n    "mqtt_server": "mqtt.example.com",\n    "mqtt_prefix": "homeassistant",\n    "mqtt_user": "mqtt_user",\n    "mqtt_password": "mqtt_password",\n    "device_id": "device_id",\n    "device_name":"MySensor",\n    "device_class":"motion",\n}\n\nmysensor = BinarySensor(settings=configd)\nmysensor.on()\nmysensor.off()\n\n```\n\n### Devices\n\n#### Usage\n\n```py\nfrom hass_mqtt_devices.device import Device\n\n# Create a settings dictionary\n#\n# Mandatory Keys:\n#  mqtt_server\n#  mqtt_user\n#  mqtt_password\n#  device_id\n#  device_name\n#  device_class\n#  unique_id\n#\n# Optional Keys:\n#  client_name\n#  manufacturer\n#  model\n#  mqtt_prefix - defaults to homeassistant\n\nconfigd = {\n    "mqtt_server": "mqtt.example.com",\n    "mqtt_prefix": "homeassistant",\n    "mqtt_user": "mqtt_user",\n    "mqtt_password": "mqtt_password",\n    "device_id": "device_id",\n    "device_name":"MySensor",\n    "device_class":"motion",\n    "manufacturer":"Acme Products",\n    "model": "Rocket Skates",\n}\n\nsensor = Device(settings=configd)\nsensor.add_metric(\n    name="Left skate thrust",\n    value=33,\n    configuration={"name": f"Left Skate Thrust"},\n)\nsensor.add_metric(\n    name="Right skate thrust",\n    value=33,\n    configuration={"name": f"Right Skate Thrust"},\n)\n```\n\n## Scripts Provided\n\nhass_mqtt_devices creates the following helper scripts you can use in your own shell scripts.\n\n### `hmd`\n\nA gitlike command, you can `hmd create binary sensor` and it\'ll find and run `hmd-create-binary-sensor` and pass it all the command line options.\n\n### `hmd create binary sensor`\n\nCreate/Update a binary sensor and set its state.\n\nUsage: `hmd create binary sensor --device-name mfsmaster --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --client-name inquisition --mqtt-server mqtt.unixorn.net --metric-name tamper --device-class motion --state off`\n\n### `hmd create device`\n\nCreate/Update a device and set the state of multiple metrics on it.\n\nUsage: `hmd create device --device-name coyote --device-id 8675309 --mqtt-user HASS_MQTT_USER --mqtt-password HASS_MQTT_PASSWORD --mqtt-server mqtt.example.com --model \'Rocket Skates\' --manufacturer \'Acme Products\' --metric-data \'{"name":"Left Rocket Skate","value":93}\' --metric-data \'{"name":"Right Rocket Skate","value":155}\' --unique-id \'hmd-26536\'`',
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
