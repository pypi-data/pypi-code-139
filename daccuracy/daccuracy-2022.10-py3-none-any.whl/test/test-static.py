# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Run from project folder with: python -m daccuracy.test.test-static

import os.path as path
import subprocess as prss
from typing import Tuple


MODULE = "daccuracy.daccuracy"
BASE_FOLDER = ()
GT_FOLDER = BASE_FOLDER + ("ground-truth",)
DN_FOLDER = BASE_FOLDER + ("detection",)


def CMP2Path(name: str, components: Tuple[str, ...]) -> str:
    """"""
    return path.join(*(components + (name,)))


csv_vs_correct = (
    f"python -m {MODULE} "
    f"--gt {CMP2Path('ground-truth-1.csv', GT_FOLDER)} "
    f"--dn {CMP2Path('detection-1.png', DN_FOLDER)} "
    f"-s --format csv"
)
csv_vs_wrong = (
    f"python -m {MODULE} "
    f"--gt {CMP2Path('ground-truth-1.csv', GT_FOLDER)} "
    f"--dn {CMP2Path('detection-2.png', DN_FOLDER)} "
    f"--rAcB "
    f"-s --format nev "
)
csv_vs_wrong_w_tol = (
    f"python -m {MODULE} "
    f"--gt {CMP2Path('ground-truth-1.csv', GT_FOLDER)} "
    f"--dn {CMP2Path('detection-2.png', DN_FOLDER)} "
    f"-t 5 "
    f"-s --format nev "
)
png_vs_wrong = (
    f"python -m {MODULE} "
    f"--gt {CMP2Path('ground-truth-1.png', GT_FOLDER)} "
    f"--dn {CMP2Path('detection-2.png', DN_FOLDER)} "
    f"-s --format csv "
)

prss.run(csv_vs_correct.split()), print("")
prss.run(csv_vs_wrong.split()), print("")
prss.run(csv_vs_wrong_w_tol.split()), print("")
prss.run(png_vs_wrong.split())
