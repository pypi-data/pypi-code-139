from __future__ import annotations

import _contamxpy

_lib = _contamxpy.lib
_ffi = _contamxpy.ffi

print(f"_contamxpy => \n\t{dir(_contamxpy)}")

def getState():
    return _lib.cxiGetContamState()

def setWindPressureMode(state, mode):
    _lib.cxiSetWindPressureMode(state, mode)

def getVersion(state):
    bufStr = _ffi.new("char[]", 64)
    _lib.cxiGetVersion(state, bufStr)
    return _ffi.string(bufStr).decode('utf-8')
    