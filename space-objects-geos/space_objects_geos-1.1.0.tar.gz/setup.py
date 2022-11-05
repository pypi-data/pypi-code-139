# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['space_objects_geos']

package_data = \
{'': ['*']}

install_requires = \
['geojson>=2.5.0,<3.0.0',
 'shapely>=1.8.5.post1,<2.0.0',
 'space-objects>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'space-objects-geos',
    'version': '1.1.0',
    'description': 'Provide space_objects output geometry capabilities like shapely geometry and geojson.',
    'long_description': '# space_objects_geos\n\n- ![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)\n\n- ![coverage](coverage-badge.svg)\n\n```bash\npip install space-objects-geos\n```\n\nThis is an extension for [space_objects](https://github.com/larrieu-olivier/space_objects) package.\n\nProvides outputs objects for easily work with shapely geometries from the originals outputs objects.\n\nUsefull for geometries calculations and geojson representation for web display.\n\n### sample\n\n```python\nfrom space_objects.models import SatelliteActive\nfrom space_objects_geos.outputs import OrbitObjectGeos, PositionObjectGeos\n\nyour_position = {\n    "observation_position_longitude": 1.433333,\n    "observation_position_latitude": 43.6,\n}\n\nsatellite_name = "ISS (ZARYA)"\niss_object = SatelliteActive(satellite_name, **your_position)\n\nposition = PositionObjectGeos(iss_object.get_position())\norbit = OrbitObjectGeos(iss_object.get_orbit())\n\nprint(position.geojson)\nprint(orbit.geojson)\n```\n\nposition geojson\n\n![position geojson](assets/images/position_geojson.png)\n\norbit geojson\n\n![orbit geojson](assets/images/orbit_geojson.png)\n',
    'author': 'larrieu olivier',
    'author_email': 'larrieuolivierad@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
