#  __,              __
# /  |   |  |  |   /
# \_/|/   \/ \/    \___/
#   /|
#   \|

from __future__ import absolute_import

import gddriver.providers as providers
import gddriver.transmission as transmission
from pbr.version import VersionInfo

__title__ = 'gwc'
__version__ = VersionInfo(__title__).version_string()
__author__ = 'Wu Yarong'
__description__ = 'GeneDock command-line workflow client for interacting with GeneDock platform'
__url__ = 'https://www.genedock.com'
