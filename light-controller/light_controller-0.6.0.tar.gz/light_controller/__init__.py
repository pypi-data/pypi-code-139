"""Top-level package for Light Controller."""

__author__ = """Tristan Cotte"""
__email__ = 'tristan.cotte@sgs.com'
__version__ = '0.1.0'

import time
from typing import List

import serial
from serial import SerialException

from .transformations import declist_to_binlist, bin_to_hex
from .utils_uart import split, compute_checksum, compute_command


class LightManager(serial.Serial):
    def __init__(self, port: str, baudrate: int, list_channels: List[int]):
        """
        Class which enables to handle the 8 lights channels thanks to the "FG-PDV400W-24-8T" controller
        :param port: communication port used by the computer to reach the controller. Ex : "COM1"
        :param baudrate: communication frequency used to communicate with the controller
        :param list_channels: list of channels used by the controller to handle lights
        """
        super().__init__(port, baudrate, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
        self.port = port
        self.baudrate = baudrate
        self.list_channels = list_channels

        self.initialization()

    def initialization(self) -> None:
        """
        Steady mode on all the channels -> command Hx.1 for all channels named x
        8 is the parameter of the mode
        """
        for i in self.list_channels:
            chain = "$8" + str(i) + "000"
            chain_list = split(chain)
            list_bin = declist_to_binlist(chain_list)

            checksum = compute_checksum(list_bin)
            checksum_hex = bin_to_hex(checksum)
            command = chain + checksum_hex
            self.write(command.encode())

    def switch_off(self) -> None:
        """
        Switch off all lights in the platform
        """
        for c in self.list_channels:
            command = compute_command(intensity=0, channel=c)
            self.write(command.encode())

    def switch_on(self, intensities, channels=None) -> None:
        """
        Switch on one or several lights sending several commands of intensity for the lights
        :param channels: channels of the lights which change value
        :param intensities: list of the light's intensity with index respective to the channel list
        """
        if channels is None:
            channels = self.list_channels

        if isinstance(channels, list):
            for c, i in zip(channels, intensities):
                command = compute_command(intensity=i, channel=c)
                self.write(command.encode())

        elif isinstance(channels, int):
            command = compute_command(intensity=intensities, channel=channels)
            self.write(command.encode())

