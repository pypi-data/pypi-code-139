"""
Driver for the Thorlabs CLD1010LP. Programming manual here: 
https://www.thorlabs.com/drawings/84b68761fa2c704c-5D5DD69C-9E91-8A48-043C41D5A362BD66/CLD1010LP-ProgrammersReferenceManual.pdf

On linux, you need to grant user access to the usb drivers in order for VISA to detect them.

Add udev rules
$ sudo cp 99-thorlabs-cld1010.rules /etc/udev/rules.d/

Create a user group for the usb device access:
$ sudo groupadd usbtmc

Add any relevant users to the group:
$ usermod -aG usbtmc <user1>

Reboot for the changes to take effect

Copyright (c) 2022, Jacob Feder, Ben Soloway
All rights reserved.
"""
import logging

from pyvisa import ResourceManager
import bs2.config

logger = logging.getLogger(__name__)

class CLD1010:
    def __init__(self, address):
        """
        Args:
            address: PyVISA resource path.
        """
        self.rm = ResourceManager('@py')
        self.address = address
        self.laser = self.rm.open_resource(self.address)
        logger.info(f'Connected to CLD1010 [{self.address}].')

    def idn(self):
        return self.laser.query('*IDN?')

    def get_ld_state(self):
        return int(self.laser.query('OUTP1:STAT?'))

    def set_ld_state(self, value):
        self.laser.write('OUTP1:STAT {}'.format(value))

    def max_current(self):
        return float(self.laser.query('SOUR:CURR:LIM:AMPL?'))

    def meas_current(self):
        return float(self.laser.query('MEAS:CURR?'))

    def get_current_setpoint(self):
        return float(self.laser.query('SOUR:CURR?'))

    def set_current_setpoint(self, value):
        max_current = self.max_current()
        if value <= max_current:
            self.laser.write('SOUR:CURR {:.5f}'.format(value))
        else:
            raise ValueError("Current setpoint: {} is larger than max current {})").format(value, max_current)

    def get_tec_state(self):
        return self.laser.query('OUTP2:STAT?')

    def set_tec_state(self, value):
        self.laser.write('OUTP2:STAT {}'.format(value))

    def temperature(self):
        return self.laser.query('MEAS:TEMP?')

    def on(self):
        if self.get_tec_state():
            self.set_ld_state(1)
        else:
            return("error: temperature controller not on")

    def get_modulation_state(self):
        value = int(self.laser.query('SOUR:AM:STAT?'))
        if value == 0:
            return 'Off'
        elif value == 1:
            return 'On'
        else:
            raise ValueError(f'invalid modulation state {value}')


    def set_modulation_state(self, value):
        if value == 'Off':
            val = 0
        elif value == 'On':
            val = 1
        else:
            raise ValueError(f'invalid modulation state {value}')
        self.laser.write('SOUR:AM:STAT {}'.format(val))

    def off(self):
        self.set_ld_state(0)

    def close(self):
        self.laser.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.off()
        self.close()

if __name__ == '__main__':
    with CLD1010(bs2.config.visa_addresses['cld1010']) as cld1010:
        print("getting ld state")
        print(cld1010.get_ld_state())
        
        print("getting modulation state")
        print(cld1010.get_modulation_state())
        print("setting modulation state on")
        cld1010.set_modulation_state(1)
        print("getting modulation state")
        print(cld1010.get_modulation_state())
        print("setting modulation state off")
        cld1010.set_modulation_state(0)