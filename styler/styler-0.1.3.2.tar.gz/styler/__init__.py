# Made by $udo
# Github repo: https://github.com/sudo001/styler
# Check README.md for more info.

class styler_info:
    version = "0.1.3"

import sys, os, platform
if os.name == "nt":
    try:
        from ctypes import c_int, c_byte, Structure, byref, windll

        class CursorInfo(Structure):
            _fields_ = [("size", c_int),
                        ("visible", c_byte)]

    except:
        raise ModuleNotFoundError("ctypes module not found, some functions may not work.")

if os.name == "posix":
    import distro
    """
    
    No try&except because "distro" is installed automatically on every distribution."""

from time import sleep

class System:
    def PLATFORM():
        return os.uname().sysname
    
    def DISTRO_ID():
        """
        
        Return your distribution id. (For e.g.: pop)"""
        if os.name == "posix":          
            distribution_c = distro.id().capitalize()[0]
            distribution_f = distro.id().removeprefix(distro.id()[0])
            return distribution_c + distribution_f

        """
        
        This just capitalizates the first character to make it look better."""
    
    def DISTRO_NAME():
        """
        
        Returns your distribution name. (For e.g.: Pop!OS)"""
        if os.name == "posix":
            return distro.name()

class Style:
    START = "["

    RED = START+"0;31m"
    LIGHT_RED = START+"1;31m"
    GREEN = START+"0;32m"
    LIGHT_GREEN = START+"1;32m"
    YELLOW = START+"0;33m"
    LIGHT_YELLOW = START+"1;33m"
    BLUE = START+"0;34m"
    LIGHT_BLUE = START+"1;34m"
    PINK = START+"0;35m"
    LIGHT_PINK = START+"1;35m"
    CYAN = START+"0;36m"
    LIGHT_CYAN = START+"1;36m"
    WHITE = START+"0;37m"
    LIGHT_WHITE = START+"1;37m"
    BLACK = START+"0;30m"
    LIGHT_BLACK = START+"1;30m"
    GRAY = START+"0;39m"
    LIGHT_GRAY = START+"1;39m"

    RESET = START+"0m"

class Ascii:
    def COWSAY(text: str):
        output = ""
        output += " " + "_"*int(len(text)+2)
        output += "\n"+f"< {text} >"
        output += "\n " + "-"*int(len(text)+2)
        output += """
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w||
                ||     ||"""
        return output

        finaloutput = ""
        for character in text:
            if character == "\n":
                finaloutput += " "
            else:
                finaloutput += character

class Cursor:

    """
    
    Fuction operate is only used on windows."""

    def operate(visibility: bool):
        cursor_info = CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, byref(cursor_info))
        cursor_info.visible = visibility
        windll.kernel32.SetConsoleCursorInfo(handle, byref(cursor_info))
    
    def HIDE(mode: object=sys.stdout):
        if os.name == "nt":
            Cursor.operate(False)
        else:
            mode.write("\033[?25l")
            mode.flush()

    def SHOW(mode=sys.stdout):
        if os.name == "nt":
            Cursor.operate(True)
        else:
            mode.write("\033[?25h")
            mode.flush()