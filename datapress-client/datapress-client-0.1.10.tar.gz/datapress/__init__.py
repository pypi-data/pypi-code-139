"""
datapress_client

DataPress API client and utilities.
"""

from .__version__ import __version__ as version
print('Loading datapress_client version: ' + version)

from .geo import *
from .extract import *
from .nomis import *
from .script import *
