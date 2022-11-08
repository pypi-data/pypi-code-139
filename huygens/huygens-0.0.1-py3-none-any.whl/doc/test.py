#!/usr/bin/env python3

from huygens import *

cvs = canvas.canvas()

cvs.fill(path.circle(0, 0, 0.5))

cvs.clip(path.rect(-2, -10, 15, 15))

cvs.image("images/Christiaan_Huygens.png", 0.5, 0.5)

cvs.writePDFfile("huy.pdf")
cvs.writeSVGfile("huy.svg")


