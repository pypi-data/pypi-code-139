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
"""Provides a class to extract frames data from a MPEG-4 video file
using ffprobe.
"""

import json
import subprocess
import pathlib
import logging


class Ffprobe:
    """Wrapper around the ffprobe executable"""

    def __init__(self, ffprobe_executable: pathlib.Path) -> None:
        if ffprobe_executable != pathlib.Path():
            self.__ffprobe_path = str(ffprobe_executable.resolve())
        else:
            self.__ffprobe_path = "ffprobe"

    def get_ffprobe_path(self) -> str:
        """Get the path to the ffprobe executable."""
        return self.__ffprobe_path


class DataExtractor:
    """Extract frame data using ffprobe"""

    def __init__(self, input_filename: pathlib.Path,
                 ffprobe_executable: pathlib.Path) -> None:
        self.__input_file = input_filename
        self.__ffprobe = Ffprobe(ffprobe_executable)

    def __run_ffprobe(self) -> bytes:
        ffprobe_args = [
            self.__ffprobe.get_ffprobe_path(),
            "-select_streams",
            "v:0",
            "-print_format",
            "json=compact=1",
            "-show_frames",
            str(self.__input_file)
        ]
        try:
            proc = subprocess.run(
                ffprobe_args,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as ex:
            logging.error("ffprobe failed with output: %s", ex.output)
            result = b""
        else:
            result = proc.stdout
        return result

    def __try_load_json_data(self, ffprobe_stdout: bytes) -> dict:
        try:
            json_data = json.loads(ffprobe_stdout)
        except json.JSONDecodeError as ex:
            logging.error("Failed to read ffprobe output: %s", ex)
            json_data = {}
        return json_data

    def run(self) -> dict:
        """Calls ffprobe and returns the json data."""
        raw_data = self.__run_ffprobe()
        return self.__try_load_json_data(raw_data)
