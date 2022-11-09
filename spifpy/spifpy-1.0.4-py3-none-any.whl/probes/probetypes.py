"""Probe types module."""

from abc import ABC, abstractmethod
from enum import Enum


class ProbeType(Enum):
    """Enumerate for defining a probe type."""

    Unknown = 0
    TwoDs = 1
    TwoDc = 2
    Hvps = 3
    Cip = 4
    Pip = 5
    Cpi = 6
    Hsi = 7


class SpifProbe(ABC):
    """
    Probe type interface.

    Each probe must inherit this interface.

    Parameters
    ----------
    ABC : abc.ABCMeta
        Metaclass to implement abstract classes in python
    """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, 'CPI', '2DS-V', 'CIP', etc.
        """
        pass

    @classmethod
    def get_name_lower(cls) -> str:
        """
        Get a probe type name in lower case.

        Returns
        -------
        str
            Probe type in lower case, 'cpi', '2ds-v', 'cip', etc.
        """
        return cls.get_name().lower()

    @classmethod
    @abstractmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        pass

    @classmethod
    @abstractmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        By default the smallest particle will have a zero size, therefore
        all particles will be considered as "not small".

        Normally, threshold value would be similar to the probe resolution,
        and sometimes it is 2x or 3x of the resolution. For example, if a
        probe resolution is 5 micron, particles that are about 10 microns
        or even 15 microns may still be considered small.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 0.0

    @classmethod
    @abstractmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Unknown


class CpiProbe(SpifProbe):
    """Cpi probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, 'CPI'
        """
        return "CPI"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 2.3

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 6.25

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Cpi


class TwoDsProbe(SpifProbe):
    """2DS probe class."""

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 10.0

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 11.83

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.TwoDs


class TwoDsVProbe(TwoDsProbe):
    """2DS probe class. Channel V."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, '2DS-V'
        """
        return "2DS-V"


class TwoDsHProbe(TwoDsProbe):
    """2DS probe class. Channel H."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, '2DS-H'
        """
        return "2DS-H"


class HvpsProbe(SpifProbe):
    """HVPS probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, `HVPS`
        """
        return "HVPS"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 150.0

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 200.0

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Hvps


class CipProbe(SpifProbe):
    """CIP probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, `CIP`
        """
        return "CIP"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 25.0

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 35.0

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Cip


class PipProbe(SpifProbe):
    """PIP probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, `PIP`
        """
        return "PIP"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 100.0

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 150.0

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Pip


class TwoDcProbe(SpifProbe):
    """2DC probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, `2DC`
        """
        return "2DC"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 25.0

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 35.0

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.TwoDc


class HsiProbe(SpifProbe):
    """Hsi probe class."""

    @classmethod
    def get_name(cls):
        """
        Get a probe type name.

        Returns
        -------
        str
            Probe type, 'HSI'
        """
        return "HSI"

    @classmethod
    def get_resolution(cls) -> float:
        """
        Get a probe resolution.

        Returns
        -------
        float
            Probe resolution, microns per pixel
        """
        return 2.5

    @classmethod
    def get_small_threshold(cls) -> float:
        """
        Get a size thresold for a "small" particle for the probe.

        Returns
        -------
        float
            Particle size threshold, microns
        """
        return 6.25

    @classmethod
    def get_type(cls) -> ProbeType:
        """
        Get a probe type.

        Returns
        -------
        ProbeType
            Probe type
        """
        return ProbeType.Hsi
