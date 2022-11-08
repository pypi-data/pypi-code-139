"""This module provides all supported ASCII sample classes."""

from dataclasses import dataclass


@dataclass
class ASC_SAMPLE:
    """
    A dataclass representing the basic framework of every ASCII sample.

    Attributes
    ----------
    `t` : int
        timestamp in milliseconds
    """

    t: int

    def to_dict(self):
        """
        Convert the ASC_SAMPLE class to a dictionary.

        Return
        ------
        `self.__dict__` : dict
            Dictionary representing all attributes of the ASCII sample

        Example
        -------
        >>> event = ASC_SAMPLE(t=123456)
        >>> event.to_dict()
        {t:123456}
        """
        return self.__dict__


@dataclass
class ASC_MONO(ASC_SAMPLE):
    """
    TODO:

    Attributes
    ----------
    `t` : int
        time of button press
    `xp` : float
        monocular X position data
    `yp` : float
        monocular Y position data
    `ps` : float
        monocular pupil size (area or diameter)
    """

    t: int
    xp: float
    yp: float
    ps: float


@dataclass
class ASC_BINO(ASC_SAMPLE):
    """
    TODO:

    Attributes
    ----------
    `t` : int
        time of button press
    `xpl` : float
        left-eye X position data
    `ypl` : float
        left-eye Y position data
    `psl` : float
        left pupil size (area or diameter)
    `xpr` : float
        right-eye X position data
    `ypr` : float
        right-eye Y position data
    `psr` : float
        right pupil size (area or diameter)
    """

    t: int
    xpl: float
    ypl: float
    psl: float
    xpr: float
    ypr: float
    psr: float
