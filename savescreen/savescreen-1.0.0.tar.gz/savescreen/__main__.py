import os
import sys
import argparse
from srutil import util

from . import __version__, __package__
from .screenshot import Screenshot


def get_argument():
    parser = argparse.ArgumentParser(prog=__package__, usage=util.stringbuilder(__package__, " [options]"))
    parser.add_argument('-v', '--version', action='version', help='show version number and exit', version=__version__)
    group = parser.add_argument_group("to take screenshot")
    group.add_argument("-n", "--name", dest="name", metavar="", help="name to screenshot")
    group.add_argument("-p", "--path", dest="path", default=os.getcwd(), metavar="",
                       help="path to save screenshot (default : %(default)ss)")
    group.add_argument("-f", "--format", dest="format", default="png", choices=["png", "jpg", "jpeg"], metavar="",
                       help="image format to save screenshot (default : %(default)s)")
    group.add_argument("-t", "--timeout", metavar="", default="5", type=int, dest="timeout",
                       help="timeout period before taking screenshot in secs (default : %(default)ss)")
    group.add_argument("-d", "--display", dest="display", default=False, action="store_true",
                       help="to display the screenshot (default : %(default)s)")
    parser.add_argument_group(group)
    options = parser.parse_args()
    return options


def take_screenshot(name: str, img_format, path: str, timeout: int, display: bool = False) -> bool:
    screenshot = Screenshot(path=path, name=name, img_format=img_format).take(timeout)
    is_saved = screenshot.save()
    if display:
        screenshot.display()
    ss_path = screenshot.get_screenshot_path()
    print(util.stringbuilder("\n", "Screenshot saved in '", ss_path, "'."))
    return is_saved


def main():
    options = get_argument()
    take_screenshot(options.name, options.format, options.path, options.timeout, options.display)


if __name__ == "__main__":
    sys.exit(main())
