#!/usr/bin/env python3

import fxcg


def main() -> int:
    for i in range(2, 7, 2):
        PrintXY(i, i, "Hi")
        GetKey()
