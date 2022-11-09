#!/usr/bin/env python3

from datetime import datetime
from argparse import Namespace
from typing import TYPE_CHECKING
from .config import (
    default_log_csv,
    csv_headers,
    app_dir,
    default_supposed_file,
    alfred_workflow_dir,
)
import csv

from workflow import Workflow3
from workflow.workflow3 import Item3


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
    curr_supposed = get_supposed()
    if curr_supposed == args.supposed:
        print(f'You\'re already supposed to be doing {curr_supposed}')
        return
    set_supposed(args.supposed)
    print(f'Supposed set to "{get_supposed()}"')
    if args.log_start:
        log_event(f'start: {get_supposed()}', focused=True)
        print(f'Logged start of "{get_supposed()}"')
        print(
            f'''\033[32mGood job! You\'re doing what you\'re supposed to be doing, which is "{get_supposed()}"\033[0m'''
        )


def get_rows() -> list[dict]:
    with default_log_csv.open() as f:
        w = csv.DictReader(f)
        rows = list(w)
    return rows


def fill_workflow_items(wf: Workflow3, alfred_filter_string: str | None = None) -> bool:
    query = alfred_filter_string
    # if len(wf.args):
    #     query = wf.args[-1]
    # else:
    #     query = None
    # rows = wf.cached_data('rows', get_rows, max_age=3600)
    rows = get_rows()
    from icecream import ic

    ic(rows, query)
    if not rows:
        wf.add_item('No results found')
        wf.send_feedback()
        return False
    if query:
        rows = [row for row in rows if query in ' '.join(row.values())]
    if not rows:
        wf.add_item('No matching results found')
        wf.send_feedback()
        return False
    for row in rows:
        event = row['event']
        item = Item3(
            title=event,
            subtitle=f'{row["timestamp"]}  |  {row["supposed"]}  |  {"✅" if row["focused"] == "1" else "❌"}',
            arg=event,
            valid=True,
        )
        wf._items.append(item)
    return True


def process_args_logs(args: Namespace):
    if args.alfred:
        wf = Workflow3()
        wf._workflowdir = alfred_workflow_dir
        if fill_workflow_items(wf, alfred_filter_string=args.alfred_filter_string):
            wf.send_feedback()
