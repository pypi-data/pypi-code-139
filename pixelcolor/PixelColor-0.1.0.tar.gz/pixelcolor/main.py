#!/usr/bin/env python3
##
#     Project: PixelColor
# Description: Get the screen pixel color
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2022 Fabio Castelli
#     License: GPL-3+
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
##

from pixelcolor.command_line_options import CommandLineOptions
from pixelcolor.pixel_color import PixelColor


def main():
    # Get command-line options
    command_line = CommandLineOptions()
    command_line.add_screen_arguments()
    command_line.add_output_arguments()
    options = command_line.parse_options()
    # Get pixel color
    pixelcolor = PixelColor()
    colors = pixelcolor.get_color(display=options.display,
                                  x=options.x - 1,
                                  y=options.y - 1)
    if options.triplets:
        # Return color as triplets (R G B)
        if options.hex:
            # Return triplets as hexadecimal
            print(' '.join(map(hex, colors)).replace('0x', ''))
        else:
            # Return triplets as decimal
            print(' '.join(map(str, colors)))
    else:
        # Return color as decimal
        decimal_color = colors[0] * 256 * 256 + colors[1] * 256 + colors[2]
        if options.hex:
            # Return color as hexadecimal
            print(hex(decimal_color).replace('0x', ''))
        else:
            # Return color as decimal
            print(decimal_color)


if __name__ == '__main__':
    main()
