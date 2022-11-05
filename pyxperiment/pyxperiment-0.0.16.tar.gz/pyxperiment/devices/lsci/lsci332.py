"""
    pyxperiment/devices/lsci/lsci332.py:
    Support for Lake Shore Model 332 resistance bridge

    This file is part of the PyXperiment project.

    Copyright (c) 2022 PyXperiment Developers

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
from pyxperiment.controller.device_options import (
    ValueDeviceOption as ValueControl, ListControl
)

class LakeShore332ResBridge(VisaInstrument):
    """
    Lake Shore Model 332 resistance bridge support
    Provides the most simple functionality to read the temperature and
    manually set the heater range/value.
    """

    def __init__(self, rm, resource):
        super().__init__(rm, resource)
        self.write('*CLS')
        self.set_options([
            self.heater_range,
            self.heater_power,
            self.temperature_a,
            self.temperature_b,
            self.sensor_units_a,
            self.sensor_units_b
        ])

    @staticmethod
    def driver_name():
        return 'Lake Shore Model 332 resistance bridge support'

    def device_name(self):
        value = self.query_id().translate({ord(c): None for c in ['\r', '\n']}).split(',')
        return value[0] + ' ' + value[1] + ' resistance bridge'

    def get_temperature(self, channel):
        """
        Get sensor reading in kelvin
        """
        return self.query('KRDG? ' + channel)

    def get_sensor_units(self, channel):
        """
        Get sensor reading in sensor units
        """
        return self.query('SRDG? ' + channel)

    heater_range = [
        'Off', 'Low', 'Medium', 'High'
    ]
    heater_range = ListControl(
        'Heater range',
        values_list=dict(zip(heater_range, map(str, range(len(heater_range))))),
        get_func=lambda instr: instr.query('RANGE?'),
        set_func=lambda instr, val: instr.write('RANGE ' + val),
    )

    heater_power = ValueControl(
        'Heater 1 manual power', '%',
        get_func=lambda instr: instr.query('MOUT? 1'),
        set_func=lambda instr, val: instr.write('MOUT 1,' + str(val)),
    )

    temperature_a = ValueControl(
        'Temperature CH A', 'K', lambda instr: instr.get_temperature('A')
        )
    temperature_b = ValueControl(
        'Temperature CH B', 'K', lambda instr: instr.get_temperature('B')
        )
    sensor_units_a = ValueControl(
        'Sensor units CH A', 'Ohm', lambda instr: instr.get_sensor_units('A')
        )
    sensor_units_b = ValueControl(
        'Sensor units CH B', 'Ohm', lambda instr: instr.get_sensor_units('B')
        )
