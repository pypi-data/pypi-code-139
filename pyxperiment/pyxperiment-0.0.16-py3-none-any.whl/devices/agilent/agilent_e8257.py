"""
    pyxperiment/devices/agilent/agilentE8257.py: Support for Agilent E8257 Generator

    This file is part of the PyXperiment project.

    Copyright (c) 2019 PyXperiment Developers

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from pyxperiment.controller import VisaInstrument

class AgilentE8257(VisaInstrument):
    """
    Support for Agilent E8257 Generator
    """

    @staticmethod
    def driver_name():
        return 'Agilent/Keysight E8257'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' signal generator'

    def get_value(self):
        return self.query('FREQ:CW?')

    def set_value(self, value):
        self.write('FREQ:CW ' + str(value))
        