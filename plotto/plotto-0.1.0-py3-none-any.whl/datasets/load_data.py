import os.path
from pathlib import Path

from pandas import read_csv

data_folder = Path(f"{'/'.join(os.path.realpath(__file__).split('/')[:-1])}/csv")


def params():
    """output from the differences pkg"""

    csv_file = data_folder / 'params.csv'

    data = read_csv(csv_file)

    return data
