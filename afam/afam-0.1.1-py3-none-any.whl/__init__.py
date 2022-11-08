"""
  Package to support the analyisation of SR Research .asc-files
"""

from .asc_event import ASC_BUTTON
from .asc_event import ASC_SBLINK
from .asc_event import ASC_SSACC
from .asc_event import ASC_SFIX
from .asc_event import ASC_EBLINK
from .asc_event import ASC_ESACC
from .asc_event import ASC_EFIX

from .asc_event import ASC_MSG

from .asc_sample import ASC_SAMPLE
from .asc_sample import ASC_MONO
from .asc_sample import ASC_BINO

from .asc_dataset import ASC_Dataset
from .asc_dataset import ASC_Parser

__all__ = [
    "ASC_SAMPLE",
    "ASC_MONO",
    "ASC_BINO",
    "ASC_BUTTON",
    "ASC_SBLINK",
    "ASC_SSACC",
    "ASC_SFIX",
    "ASC_EBLINK",
    "ASC_ESACC",
    "ASC_EFIX",
    "ASC_MSG",
    "ASC_Dataset",
]

# ----------------------------------------------------------------------------------------------- #


def read_asc(path, search=None):
    """
    Reads the given ASC file and returns a list with all eye events

    Parameter
    ---------
    `path` : str
        The file path of the ASC file

    Return
    ------
    `event_list` : list
        a list of all eye events
    `search` : list
        a list of all relevant message token
    """
    dataset = ASC_Dataset()
    parser = ASC_Parser(search)
    with open(path, encoding="utf-8") as fp:
        line = fp.readline()
        while line:
            cutted_line = " ".join(line.split()).split(" ")
            token = cutted_line[0]
            if token.isnumeric() and line[0] != " ":
                e = parser.parse("SAMPLE", cutted_line)
            else:
                e = parser.parse(cutted_line.pop(0), cutted_line)
            if e:
                if isinstance(e, ASC_MSG):
                    dataset.msg.append(e)
                elif isinstance(e, ASC_SAMPLE):
                    dataset.sample.append(e)
                else:
                    if token.lower() not in dataset.event:
                        dataset.event.update({token.lower(): []})
                    dataset.event[token.lower()].append(e)
            line = fp.readline()
    return dataset
