from moldcast.cli import main
from torxtools.misctools import mainctx
import sys

if __name__ == "__main__":
    with mainctx():
        sys.exit(main())
