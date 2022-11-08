"""
base.py - super class of chamber controller

When you create your child class, overwrite functions "start", "stop", "read_temp", "ramp_conf".
And, use the "Controller" as class name.

Below exception is raised once fail:
    ChamberControllerError(errcode, errmsg)
"""
from ..common.error import ApolloError

__author__ = 'clk'
__version__ = '2.0'


class ChamberControllerError(ApolloError):
    pass


class BaseController(object):

    def __init__(self, connection):
        """
        Initialize Controller
        :param obj connection: the object of chamber connection
        :return:
        """
        self._connection = connection

    def __str__(self):
        return __name__.rsplit('.', 1)[1]

    def start(self, high_limit, low_limit):
        """
        Run the command set to configure/start chamber, this function need to be called before ramp/soak
        :param float high_limit: high limit of temperature alarm
        :param float low_limit: low limit of temperature alarm
        :return: None
        """
        raise NotImplementedError('Function "start" missed in sub-class')

    def stop(self):
        """
        Run the command sets to stop chamber, it is last function call before end of test
        :return: None
        """
        raise NotImplementedError('Function "stop" missed in sub-class')

    def read_temp(self):
        """
        Read temperature
        :return: temperature (float)
        """
        raise NotImplementedError('Function "read_temp" missed in sub-class')

    def read_humi(self):
        """
        Read humidity percentage,
        if don't need to read humidity or no command for this function, leave it as is
        :return: float humidity percentage
        """
        return 0

    def soak_conf(self, temperature, rate, duration, **kwargs):
        """
        Run the command sets for temperature soaking.
        The completed arguments are temperature, rate, duration, margin and humidity called by chamber handler
        If don't need to configure for soaking, leave it as is
        :param number temperature: target temperature
        :param int rate: ramp rate
        :param int duration: the duration time of soaking
        :param dict kwargs: user defined kwargs
        :return: None
        """
        return

    def ramp_conf(self, temperature, rate, duration, **kwargs):
        """
        Run the command sets for temperature ramp
        The completed arguments are temperature, rate, duration, margin and humidity called by chamber handler
        :param number temperature: target temperature
        :param int rate: ramp rate
        :param int duration: runtime from the current to target temperature
        :param dict kwargs: user defined kwargs
        :return: None
        """
        raise NotImplementedError('Function "ramp_conf" missed in sub-class')
