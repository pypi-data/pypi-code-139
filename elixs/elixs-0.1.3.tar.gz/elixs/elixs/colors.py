from color4console.style import *

def color(text, type = None):
    #Symbols:
    hook = FGCOLOR.NGREEN.value + Symbol.CHECK.value + CEND + TAB
    info = FGCOLOR.NBLUE.value + Symbol.IOTA.value + CEND + TAB
    error = FGCOLOR.NRED.value + Symbol.CHI.value + CEND + TAB

    #Colors:
    red = FGCOLOR.NRED.value
    green = FGCOLOR.NGREEN.value
    yellow = FGCOLOR.NYELLOW.value
    blue = FGCOLOR.NBLUE.value

    if type == "success": style = hook + green
    elif type == "info": style = info + blue
    elif type == "error": style = error + red
    print(style + text + "\033[0m")

def version():
    return 0.1

# This Code is basically just an adapter for the color4console library and is 
# therefore licenced the same way as the color4console library under the MIT Licence.
# All credits go to the original author of the color4console library.

# MIT License

# Copyright (c) 2022 Mahmud Iftekhar Zamil

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.