#!/usr/bin/env python3

from pathlib import Path
from . import __app_name__

app_dir = Path.home() / f'.{__app_name__}'
default_log_csv = app_dir / 'log.csv'
default_supposed_file = app_dir / 'supposed'
csv_headers = ['timestamp', 'supposed', 'event', 'focused']

# default_csv_viewer = 'cat'

# cSpell:disable
alfred_workflow_dir = '/Users/tscp/gui/Alfred.alfredpreferences/workflows/user.workflow.6268652E-A1CC-428D-BB4A-542B2A4F5DA5'
# cSpell:enable
