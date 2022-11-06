#!/usr/bin/env python3

from src.maxhk import op  # a bit hacky but allows running `op` prior to install
import subprocess as sp
import shutil
import os

def main():
    pypi_creds = op.get_item("pypi.org", ["username", "password"])
    shutil.rmtree('dist', ignore_errors=True)
    assert sp.check_call("python3 -m build", shell=True) == 0
    sp.Popen(
        f'python3 -m twine  upload -u "{pypi_creds.username}" -p "{pypi_creds.password}"  dist/*',
        shell=True,
    )


if __name__ == "__main__":
    main()
