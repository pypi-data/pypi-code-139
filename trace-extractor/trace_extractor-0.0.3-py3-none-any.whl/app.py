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
"""Entry point of the program"""

import enum
import logging

from .args import Arguments, parse_args, validate_args
from .data_extract import DataExtractor
from .data_transform import DataTransformer


class ReturnValue(enum.IntEnum):
    """Definition of all possible return values"""
    SUCCESS = 0b0000
    INVALID_ARGS = 0b0001
    FFPROBE_ERROR = 0b0010
    TRANSFORM_ERROR = 0b0100
    WRITE_ERROR = 0b1000


class App:
    """Program's entry point."""

    def __init__(self) -> None:
        self.__arguments: Arguments = parse_args()

    def __setup_logging(self) -> None:
        if self.__arguments.verbose_logging:
            logging_level = logging.INFO
        else:
            logging_level = logging.WARNING

        logging.basicConfig(
            format='%(asctime)s %(levelname)s:%(message)s',
            level=logging_level)

    def __write_data(self, transformed_data: str) -> bool:
        try:
            self.__arguments.output_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )
        except OSError as ex:
            logging.error(
                "Failed to create parent directories for output file"
                "'%s': %s",
                self.__arguments.output_file,
                ex)
            return False

        try:
            self.__arguments.output_file.write_text(
                data=transformed_data,
                encoding='utf-8',
                newline='\n')
        except (OSError, ValueError) as ex:
            logging.error(
                "Failed to write to output file '%s': %s",
                self.__arguments.output_file,
                ex)
            return False
        return True

    def run(self) -> int:
        """Starts the program."""
        self.__setup_logging()

        logging.info("Validating arguments...")
        if not validate_args(self.__arguments):
            return ReturnValue.INVALID_ARGS
        logging.info("Done!")

        data_extractor = DataExtractor(
            self.__arguments.input_file,
            self.__arguments.ffprobe_executable)

        logging.info("Extracting data...")
        extracted_data = data_extractor.run()
        if not extracted_data:
            return ReturnValue.FFPROBE_ERROR
        logging.info("Done!")

        logging.info("Tranforming data...")
        transformed_data = DataTransformer(extracted_data).run()
        if not transformed_data:
            return ReturnValue.TRANSFORM_ERROR
        logging.info("Done!")

        logging.info("Writing data...")
        if not self.__write_data(transformed_data):
            return ReturnValue.WRITE_ERROR
        logging.info("Done!")

        return ReturnValue.SUCCESS
