#!/usr/bin/env python
"""
This module is used configurate the hierarchy of the directories of the project so the
scripts inside a specific directory can use the ones located at the parent directory as
packages.
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Victor Vinci Fantucci"
__email__ = "victor.v.fantucci@gmail.com"
__date__ = "2022/10/30"
__deprecated__ = False
__license__ = "GPLv3"
__maintainer__ = "VictorFantucci"

import os
import inspect
import logging

def function_logger(file_mode: str = "w",
                    file_level: int = logging.INFO,
                    console_level: int = None) -> logging.Logger:
    """
    Creates a logger object specific to the function in which it's called.

    Args:
        file_mode (str): A string that define which mode you want to open the log file.
        Defaults to "w" - Write - Opens a file for writing, creates the file if it does not exist.
        file_level (int): Logging level that will be written in the log file.
        Defaults to logging.INFO.
        console_level (int, optional): Logging level that will be displayed at the console.
        Defaults to None.

    Returns:
        logging.Logger: Logger object of the specific function in which this
        function is called.
    """
    create_logs_folder()
    script_name = os.path.basename(__file__).removesuffix(".py")
    create_script_logs_folder(script_name)

    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)

    # Check if handlers are already present and if so, clear them before adding new handlers.
    if (logger.hasHandlers()):
        logger.handlers.clear()

    # By default, logs all messages.
    logger.setLevel(logging.DEBUG)

    if console_level != None:
        # StreamHandler logs to console.
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch_format = logging.Formatter("%(levelname)-8s - %(message)s")
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    # FileHandler logs to file.
    fh = logging.FileHandler(r"logs/{0}/{1}.log".\
        format(script_name, function_name), mode = file_mode)
    fh.setLevel(file_level)
    fh_format = logging.\
        Formatter("%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s")
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger

def create_logs_folder() -> None:
    """
    Check if there's a logs folder (/logs) in the current directory,
    if there isn't, create it.
    """
    project_directory = os.getcwd()
    logs_directory = os.path.join(project_directory, "logs")
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

def create_script_logs_folder(script_name: str) -> None:
    """
    Check if there's a log folder for the script that is running
    in the project directory (/logs/script_name), if there isn't, create it.

    Args:
        script_name (str): The name of the script that's calling the function
        function_logger.
    """
    project_directory = os.getcwd()
    script_logs_directory = project_directory + "/logs"
    final_directory = os.path.join(script_logs_directory, script_name)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
