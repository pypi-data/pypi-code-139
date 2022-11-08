import argparse
import os


def init_command():
    config = os.environ.get("CONFIG", "development")
    parser = argparse.ArgumentParser(description="Happy development.")
    parser.add_argument("--config", default=config)
    args = parser.parse_args()

    return args
