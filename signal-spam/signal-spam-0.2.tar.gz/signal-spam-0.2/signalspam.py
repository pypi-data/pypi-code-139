"""Send .eml files to signal-spam.fr."""

from base64 import b64encode
from pathlib import Path
from getpass import getpass
import argparse

import requests

__version__ = "0.2"


CONF = Path("~/.signal-spam").expanduser()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "eml", nargs="+", type=str, help="An email file to report as spam."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        username, password = CONF.read_text(encoding="UTF-8").splitlines()
    except FileNotFoundError:
        username = input("signal spam username: ")
        password = getpass("signal spam password: ")
        CONF.write_text(f"{username}\n{password}\n", encoding="UTF-8")
        CONF.chmod(0o600)
    for eml in args.eml:
        print("Reporting", eml)
        payload = {
            "dossier": 0,
            "message": b64encode(Path(eml).read_text(encoding="UTF-8").encode("UTF-8")),
        }
        response = requests.post(
            "https://www.signal-spam.fr/api/signaler",
            auth=(username, password),
            timeout=10,
            data=payload,
        )
        print(response.text)


if __name__ == "__main__":
    main()
