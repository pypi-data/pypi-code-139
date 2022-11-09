#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-11-09
Purpose: Personal Logger
"""

import argparse
from argparse import ArgumentParser, Namespace
from pathlib import Path
from .config import default_log_csv
from .utils import (
    process_args_init,
    process_args_log,
    process_args_supposed_get,
    process_args_supposed_set,
    process_args_logs,
)


def get_args() -> tuple[ArgumentParser, Namespace]:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Personal Logger',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    sp = parser.add_subparsers()
    parser_init = sp.add_parser('init', help='Initialize the app')
    parser_init.set_defaults(func=process_args_init)
    parser_log = sp.add_parser(
        'log',
        aliases=['l'],
        help='Log what you\'re doing right now',
    )
    parser_log.add_argument(
        'event',
        metavar='THE THING UR DOING RIGHT NOW',
        help='What you\'re doing right now',
    )
    parser_log.add_argument(
        '-f',
        '--focused',
        action='store_true',
        help='Use this flag if you\'re focused on doing what you\'re supposed to do',
    )
    parser_log.set_defaults(func=process_args_log)
    parser_supposed = sp.add_parser(
        'supposed',
        aliases=['s'],
        help='Getting and setting things that you\'re supposed to do',
    )
    # parser_supposed.set_defaults(func=process_args_supposed)
    sp_supposed = parser_supposed.add_subparsers()
    parser_supposed_get = sp_supposed.add_parser(
        'get', help='Get what you\'re supposed to do'
    )
    parser_supposed_get.set_defaults(func=process_args_supposed_get)
    parser_supposed_set = sp_supposed.add_parser(
        'set', help='Set what you\'re supposed to do'
    )
    parser_supposed_set.add_argument(
        'supposed',
        metavar='THING',
        type=str,
        help='What you\'re supposed to do',
    )
    parser_supposed_set.add_argument(
        '-s',
        '--log-start',
        action='store_true',
        help='Start to do the new thing and log it',
    )
    parser_supposed_set.set_defaults(func=process_args_supposed_set)
    parser_logs = sp.add_parser(
        'logs',
        aliases=['ls'],
        help='Show logs',
    )
    parser_logs.add_argument(
        '--alfred',
        action='store_true',
        help='Output JSON for Alfred workflow script filter',
    )
    parser_logs.add_argument(
        '--alfred-filter-string', type=str, help='Alfred filter string'
    )
    parser_logs.set_defaults(func=process_args_logs)
    return parser, parser.parse_args()


def main():
    """Make a jazz noise here"""

    parser, args = get_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
