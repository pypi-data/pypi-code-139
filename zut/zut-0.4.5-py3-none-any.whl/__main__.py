#!/usr/bin/env python3
from zut import configure_env, BaseTools, __version__

class Tools(BaseTools):
    prog = "zut (tools)"
    version = __version__

def main():
    configure_env()
    Tools().exec()

if __name__ == '__main__':
    main()
