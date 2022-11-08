
from . import wrappers
from . import statistics
from . import fits
from . import schedulers

from . import helpers
from . import IO


def create_wrapper(codestring, execline, optsdict=None):

  if codestring == "TRI3DST":
    return wrappers.TRI3DST.TRI3DST_Wrapper(execline)

  if codestring == "SDTRIMSP":
    return wrappers.SDTRIMSP.SDTRIMSP_Wrapper(execline)

  if codestring == "PARCAS":
    return wrappers.PARCAS.PARCAS_Wrapper(execline)
