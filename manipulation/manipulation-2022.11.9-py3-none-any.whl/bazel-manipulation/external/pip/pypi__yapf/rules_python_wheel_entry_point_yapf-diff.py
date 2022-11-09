#!/usr/bin/env python3
import sys
from yapf.third_party.yapf_diff.yapf_diff import main
if __name__ == "__main__":
    rc = main()
    sys.exit(main())
