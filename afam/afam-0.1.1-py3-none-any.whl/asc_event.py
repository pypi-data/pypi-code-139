"""This module provides all supported ASCII event classes."""

from dataclasses import dataclass


@dataclass
class ASC_EVENT:
    """
    A dataclass representing the basic framework of every ASCII event.
    """

    def to_dict(self):
        """
        Convert the ASC_EVENT class to a dictionary.

        Return
        ------
        `self.__dict__` : dict
            Dictionary representing all attributes of the ASCII event

        Example
        -------
        >>> event = ASC_EVENT()
        >>> event.to_dict()
        {}
        """
        return self.__dict__


@dataclass
class ASC_BUTTON(ASC_EVENT):
    """
    A dataclass used to store the data from a "BUTTON" line.
    This line contains a button press or release event.

    Attributes
    ----------
    `t` : int
        time of button press
    `b` : int
        button number (1-8)
    `s` : int
        button change (1=pressed, 0=released)
    """

    t: int
    b: int
    s: int


@dataclass
class ASC_INPUT(ASC_EVENT):
    """
    A dataclass used to store the data from a "INPUT" line.
    This line contains an input event.

    Attributes
    ----------
    `t` : int
        time of input
    `p` : int
        port number
    """

    t: int
    p: int


@dataclass
class ASC_SBLINK(ASC_EVENT):
    """
    A dataclass used to store the data from a "SBLINK" line.
    This line contains the start of a blink event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    """

    eye: str
    st: int


@dataclass
class ASC_SSACC(ASC_EVENT):
    """
    A dataclass used to store the data from a "SSACC" line.
    This line contains the start of a saccade event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    """

    eye: str
    st: int


@dataclass
class ASC_SFIX(ASC_EVENT):
    """
    A dataclass used to store the data from a "SFIX" line.
    This line contains the start of a fixation event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    """

    eye: str
    st: int


@dataclass
class ASC_EBLINK(ASC_EVENT):
    """
    A dataclass used to store the data from a "EBLINK" line.
    This line contains start and end time (actually the time of the last sample fully within the
    blink), plus summary data of a blink event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    `et` : int
        end time
    `d` : int
        duration
    """

    eye: str
    st: int
    et: int
    d: int


@dataclass
class ASC_ESACC(ASC_EVENT):
    """
    A dataclass used to store the data from a "ESACC" line.
    This line contains start and end time (actually the time of the last sample fully within the
    saccade), plus summary data of a saccade event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    `et` : int
        end time
    `d` : int
        duration
    `sx` : float
        start X position
    `sy` : float
        start Y position
    `ex` : float
        end X position
    `ey` : float
        end Y position
    `ampl` : float
        amplitude in degrees
    `pvel` : float
        peak velocity, degr/sec
    `resx` : float
        resolution (if events_have_resolution==1)
    `resy` : float
        resolution (if events_have_resolution==1)
    """

    eye: str
    st: int
    et: int
    d: int
    sx: float
    sy: float
    ex: float
    ey: float
    ampl: float
    pvel: float
    resx: float
    resy: float


@dataclass
class ASC_EFIX(ASC_EVENT):
    """
    A dataclass used to store the data from a "EFIX" line.
    This line contains start and end time (actually the time of the last sample fully within the
    fixation), plus summary data of a fixation event.

    Attributes
    ----------
    `eye` : str
        eye (L-R)
    `st` : int
        start time
    `et` : int
        end time
    `d` : int
        duration
    `x` : float
        X position
    `y` : float
        Y position
    `resx` : float
        resolution (if events_have_resolution==1)
    `resy` : float
        resolution (if events_have_resolution==1)
    """

    eye: str
    st: int
    et: int
    d: int
    x: float
    y: float
    resx: float
    resy: float


@dataclass
class ASC_MSG(ASC_EVENT):
    """
    A dataclass used to store the data from a "MSG" line.
    This line contains token and start time, plus some summary data.

    Attributes
    ----------
    `t` : str
        token (TRIALID, SYNCTIME, TRIAL_RESULT, INFO, etc.)
    `st` : int
        start time
    `data` : str
        information
    """

    t: str
    st: int
    data: str


@dataclass
class ASC_START(ASC_EVENT):
    """
    A dataclass used to store the data from a "START" line.
    This line contains start time and some summary data.

    Attributes
    ----------
    `st` : int
        start time
    `data` : str
        information
    """

    st: int
    data: str
