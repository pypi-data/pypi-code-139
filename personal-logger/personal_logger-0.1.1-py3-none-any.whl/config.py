#!/usr/bin/env python3

from pathlib import Path
from . import __app_name__

app_dir = Path.home() / f'.{__app_name__}'
default_log_csv = app_dir / 'log.csv'
default_supposed_file = app_dir / 'supposed'
csv_headers = ['timestamp', 'supposed', 'event', 'focused']
