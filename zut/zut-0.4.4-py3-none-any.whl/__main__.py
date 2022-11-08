#!/usr/bin/env python3
from zut.env import configure_env
from zut.tools import BaseTools

class Tools(BaseTools):
    pass

def main():
    configure_env()
    Tools().exec()

if __name__ == '__main__':
    main()
