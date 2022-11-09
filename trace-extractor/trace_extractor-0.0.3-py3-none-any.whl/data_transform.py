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
"""Converts ffprobe's output into a format readable by ns3's UdpTraceClient"""

import math
import logging


class DataTransformer:
    """Transform the raw ffprobe data into a format readable by ns-3:

    `<frame index> <frame type> <frame time (ms, integer)> <frame size>`
    """

    def __init__(self, json_data: dict) -> None:
        self.__json_data = json_data

    def __convert_data(self) -> str:

        transformed_data: list[str] = []

        frames = self.__json_data["frames"]

        for frame in frames:
            frame_number = frame["coded_picture_number"]
            frame_type = frame["pict_type"]
            frame_time_s = frame["pts_time"]
            frame_time_ms = math.trunc(float(frame_time_s) * 1000.0)
            frame_size = frame["pkt_size"]
            transformed_data.append(
                f"{frame_number} {frame_type} {frame_time_ms} {frame_size}"
            )

        return '\n'.join(transformed_data)

    def __try_convert_data(self) -> str:
        """Attempts to convert ffprobe data.

        Returns an empty string on failure.
        """
        try:
            result = self.__convert_data()
        except (ValueError, KeyError) as ex:
            logging.error("Failed to convert data: %s", ex)
            result = ""

        return result

    def run(self) -> str:
        """Returns whether the transformation succeeded."""
        return self.__try_convert_data()
