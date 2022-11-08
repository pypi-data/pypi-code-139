"""
    This module provides a class to handle .asc-files in python
"""

import os
import pandas as pd
import numpy as np
from scipy.io import savemat

from .asc_event import ASC_BUTTON
from .asc_event import ASC_MSG
from .asc_event import ASC_SSACC
from .asc_event import ASC_SFIX
from .asc_event import ASC_EBLINK
from .asc_event import ASC_EFIX
from .asc_event import ASC_ESACC
from .asc_event import ASC_INPUT
from .asc_event import ASC_SBLINK
from .asc_event import ASC_START
from .asc_sample import ASC_MONO
from .asc_sample import ASC_BINO


class ASC_Dataset:
    """
    TODO:

    Attributes
    ----------
    `event` :
        ...
    `msg` :
        ...
    `sample` :
        ...
    """

    def __init__(self):
        self.event = {}
        self.msg = []
        self.sample = []

    # -------------------------------------------------------------------------------------------- #

    def to_mat(self, file_name):
        """
        Save a ASC_Dataset into a MATLAB-style .mat file.

        Parameters
        ----------
        `file_name` : str
            name of the .mat file
        """
        message = pd.DataFrame(self.msg)
        mdic = {}
        message = message.fillna(value=np.nan)
        for col in message.columns:
            mdic.update({col: list(message[col])})

        sample = pd.DataFrame(self.sample)
        sdic = {}
        sample = sample.fillna(value=np.nan)
        for col in sample.columns:
            sdic.update({col: list(sample[col])})

        edic = {}
        for item in self.event.items():
            events = pd.DataFrame(item[1])

            dic = {}
            events = events.fillna(value=np.nan)
            for col in events.columns:
                dic.update({col: list(events[col])})

            edic.update({item[0]: dic})

        savemat(file_name, {"event": edic, "message": mdic, "sample": sdic})

# -------------------------------------------------------------------------------------------- #

    def to_ascDS(self, folder_name):
        """
        Save a ASC_Dataset into the folder structure ascDS

        Parameters
        ----------
        `folder_name` : str
            name of the folder
        """
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        message = pd.DataFrame(self.msg)
        message = message.fillna("n/a")
        message.to_csv(f"{folder_name}{os.sep}message.tsv", index=False, sep="\t")
        sample = pd.DataFrame(self.sample)
        sample = sample.fillna("n/a")
        sample.to_csv(f"{folder_name}{os.sep}sample.tsv", index=False, sep="\t")
        for item in self.event.items():
            events = pd.DataFrame(item[1])
            events = events.fillna("n/a")
            events.to_csv(f"{folder_name}{os.sep}{item[0]}.tsv", index=False, sep="\t")


# -------------------------------------------------------------------------------------------- #


class ASC_Parser:
    """
    A class used to handle the parsing of an ASC file.

    Attributes
    ----------
    `info` : str
        the current cutted line of the ASC file
    `search` : list
        a list of all relevant message token
    """

    def __init__(self, search=None, info=None, mode="mono"):
        self.info = info
        self.search = search
        self.mode = mode

    # -------------------------------------------------------------------------------------------- #

    def case_BUTTON(self):
        """
        Returns a created BUTTON event object

        Return
        ------
        object
            a BUTTON event object
        """
        try:
            return ASC_BUTTON(
                t=int(self.info[0]), b=int(self.info[1]), s=int(self.info[2])
            )
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: BUTTON {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_INPUT(self):
        """
        Returns a created input event object

        Return
        ------
        object
            a INPUT event object
        """
        try:
            return ASC_INPUT(t=int(self.info[0]), p=int(self.info[1]))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: INPUT {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_SBLINK(self):
        """
        Returns a created SBLINK event object

        Return
        ------
        object
            a SBLINK event object
        """
        try:
            return ASC_SBLINK(eye=self.info[0], st=int(self.info[1]))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: SBLINK {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_SSACC(self):
        """
        Returns a created SSACC event object

        Return
        ------
        object
            a SSACC event object
        """
        try:
            return ASC_SSACC(eye=self.info[0], st=int(self.info[1]))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: SSACC {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_SFIX(self):
        """
        Returns a created SFIX event object

        Return
        ------
        object
            a SFIX event object
        """
        try:
            return ASC_SFIX(eye=self.info[0], st=int(self.info[1]))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: SFIX {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_EBLINK(self):
        """
        Returns a created EBLINK event object

        Return
        ------
        object
            a EBLINK event object
        """
        try:
            return ASC_EBLINK(
                eye=self.info[0],
                st=int(self.info[1]),
                et=int(self.info[2]),
                d=int(self.info[3]),
            )
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: EBLINK {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_ESACC(self):
        """
        Returns a created ESACC event object

        Return
        ------
        object
            a ESACC event object
        """
        try:
            return ASC_ESACC(
                eye=self.info[0],
                st=int(self.info[1]),
                et=int(self.info[2]),
                d=int(self.info[3]),
                sx=float(self.info[4]),
                sy=float(self.info[5]),
                ex=float(self.info[6]),
                ey=float(self.info[7]),
                ampl=float(self.info[8]),
                pvel=float(self.info[9]),
                resx=None,  # TODO: resx
                resy=None,
            )  # TODO: resy
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: ESACC {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_EFIX(self):
        """
        Returns a created EFIX event object

        Return
        ------
        object
            a EFIX event object
        """
        try:
            return ASC_EFIX(
                eye=self.info[0],
                st=int(self.info[1]),
                et=int(self.info[2]),
                d=int(self.info[3]),
                x=float(self.info[4]),
                y=float(self.info[5]),
                resx=None,  # TODO: resx
                resy=None,
            )  # TODO: resy
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: EFIX {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_MSG(self):
        """
        Returns a created MSG event object

        Return
        ------
        object
            a MSG event object
        """
        try:
            st = int(self.info.pop(0))
            if self.info[0] == "TRIALID":
                return ASC_MSG(t=self.info.pop(0), st=st, data=" ".join(self.info))
            if self.info[0] == "TRIAL_RESULT":
                msg = ASC_MSG(t=self.info.pop(0), st=st, data=" ".join(self.info))
                return msg
            if (self.search is not None) and (self.info[0] in self.search):
                return ASC_MSG(t=self.info.pop(0), st=st, data=" ".join(self.info))
            return ASC_MSG(t=None, st=st, data=" ".join(self.info))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: MSG {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_START(self):
        """
        Returns a created START event object

        Return
        ------
        object
            a START event object
        """
        try:
            if ("LEFT" in self.info) and ("RIGHT" in self.info):
                self.mode = "bino"
            else:
                self.mode = "mono"
            return ASC_START(st=int(self.info.pop(0)), data=" ".join(self.info))
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: START {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def case_SAMPLE(self):
        """
        Returns a created sample object

        Return
        ------
        object
            a sample object
        """
        try:
            if self.mode == "bino":
                return ASC_BINO(
                    t=int(self.info[0]),
                    xpl=float(self.info[1]),
                    ypl=float(self.info[2]),
                    psl=float(self.info[3]),
                    xpr=float(self.info[4]),
                    ypr=float(self.info[5]),
                    psr=float(self.info[6]),
                )
            return ASC_MONO(
                t=int(self.info[0]),
                xp=float(self.info[1]),
                yp=float(self.info[2]),
                ps=float(self.info[3]),
            )
        except ValueError:
            print(f"COULD NOT CONVERT TEXTLINE: {' '.join(self.info)}")
            return None

    # -------------------------------------------------------------------------------------------- #

    def parse(self, token, info):
        """
        Parses one line of the ASC file.

        Parameters
        ----------
        `token` : str
            name of a specific event
        `info` : str
            information of a specific event

        Return
        ------
        `x` : object
            an event object with the processed information
        """
        self.info = info
        x = getattr(self, f"case_{token}", lambda: None)()
        return x
