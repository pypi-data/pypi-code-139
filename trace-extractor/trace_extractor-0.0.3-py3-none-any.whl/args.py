#  Copyright (C) 2022  Pierre Wendling
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Argument parsing and validation"""


import argparse
import dataclasses
import pathlib
import logging


@dataclasses.dataclass
class Arguments:
    """Represents the program's arguments"""
    input_file: pathlib.Path
    output_file: pathlib.Path
    ffprobe_executable: pathlib.Path
    verbose_logging: bool = False


def _add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-i", "--input",
                        action="store",
                        dest="input_file",
                        type=pathlib.Path,
                        required=True,
                        help="The video file to process",
                        metavar="input.mp4")
    parser.add_argument("-o", "--output",
                        action="store",
                        dest="output_file",
                        type=pathlib.Path,
                        required=True,
                        help="Path to the output file",
                        metavar="output.ns-3-vtrace")
    parser.add_argument("--ffprobe-path",
                        action="store",
                        dest="ffprobe_path",
                        default="",
                        type=pathlib.Path,
                        required=False,
                        help="Path to the ffprobe binary")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        dest="verbose_logging",
                        required=False,
                        default=False,
                        help="Enables verbose output")


def parse_args() -> Arguments:
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m trace_extractor",
        description="MPEG-4 video trace extractor for ns-3.")

    _add_arguments(parser)

    args = parser.parse_args()
    return Arguments(input_file=args.input_file,
                     output_file=args.output_file,
                     ffprobe_executable=args.ffprobe_path,
                     verbose_logging=args.verbose_logging)


def _validate_input_file(input_file: pathlib.Path) -> bool:
    if not input_file.exists():
        logging.error(
            "The input file '%s' does not exist.",
            input_file)
        return False

    if not input_file.is_file():
        logging.error(
            "The input '%s' is not a file.",
            input_file)
        return False

    if input_file.suffix != ".mp4":
        logging.error(
            "The input file '%s' does not end in '.mp4'.",
            input_file)
        return False
    return True


def _validate_output_file(output_file: pathlib.Path) -> bool:
    if output_file.exists():
        logging.error(
            "The output file '%s' already exists.",
            output_file)
        return False
    return True


def _validate_ffprobe_exe(ffprobe_executable: pathlib.Path) -> bool:
    if ffprobe_executable == pathlib.Path():
        logging.info("Skipping ffprobe check.")
        return True

    if not ffprobe_executable.exists():
        logging.error(
            "The ffprobe executable '%s' does not exist.",
            ffprobe_executable)
        return False

    if not ffprobe_executable.is_file():
        logging.error(
            "The ffprobe executable '%s' is not a file.",
            ffprobe_executable)
        return False

    return True


def validate_args(args: Arguments) -> bool:
    """Validate the given arguments."""
    if not _validate_input_file(args.input_file):
        return False
    if not _validate_output_file(args.output_file):
        return False
    if not _validate_ffprobe_exe(args.ffprobe_executable):
        return False
    return True
