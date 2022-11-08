import importlib.resources
from importlib.metadata import version
import sys

def main_program():
    if sys.argv[1] == 'dump-schema':
        with importlib.resources.path('adisinglecell', 'schema.sql') as path:
            contents = open(path, 'rt').read()
        print('-- schema version %s\n%s\n' % (version('adisinglecell'), contents))
