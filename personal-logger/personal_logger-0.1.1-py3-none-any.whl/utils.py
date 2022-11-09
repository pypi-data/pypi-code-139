#!/usr/bin/env python3

from io import StringIO
from datetime import datetime
from argparse import Namespace
from .config import default_log_csv, csv_headers, app_dir, default_supposed_file
import csv


def init_app() -> None:
    if not app_dir.exists():
        app_dir.mkdir()
    # if csv file doesn't exist, create it
    if not default_log_csv.exists():
        with open(default_log_csv, 'w') as f:
            dw = csv.DictWriter(f, fieldnames=csv_headers)
            dw.writeheader()


def log_event(event: str, timestamp: str | None = None, focused: bool = False) -> None:
    """Log event"""
    with default_log_csv.open('a') as f:
        dw = csv.DictWriter(f, fieldnames=csv_headers)
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        dw.writerow(
            {
                'timestamp': timestamp,
                'supposed': get_supposed(),
                'event': event,
                'focused': int(focused),
            }
        )


def get_supposed() -> str:
    """Get supposed"""
    try:
        with default_supposed_file.open() as f:
            return f.readline().strip()
    except FileNotFoundError:
        return ''


def set_supposed(supposed: str) -> None:
    """Set supposed"""
    with default_supposed_file.open('w') as f:
        f.write(supposed)


def process_args_init(args: Namespace):
    """Process command-line arguments for init"""
    init_app()


def process_args_log(args: Namespace):
    """Process command-line arguments for log"""
    log_event(args.event, focused=args.focused)
    if args.focused:
        # print good job and supposed info in green
        print(
            f'''\033[32mGood job! You\'re doing what you\'re supposed to be doing, which is "{get_supposed()}"\033[0m'''
        )
    else:
        # print supposed info in red
        print(
            f'''\033[31mYou\'re not doing what you\'re supposed to be doing, which is "{get_supposed()}"\033[0m'''
        )


def process_args_supposed_get(args: Namespace):
    """Process command-line arguments for supposed"""
    print(f'You\'re supposed to be doing {get_supposed()}')


def process_args_supposed_set(args: Namespace):
    set_supposed(args.supposed)
    print(f'Supposed set to "{get_supposed()}"')
