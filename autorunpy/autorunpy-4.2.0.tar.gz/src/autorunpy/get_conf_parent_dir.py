"""

    """

import sys
from pathlib import Path


if __name__ == '__main__' :
    conf_fp = sys.argv[1]
    conf_fp = Path(conf_fp)
    conf_dir = conf_fp.parent
    print(conf_dir)
