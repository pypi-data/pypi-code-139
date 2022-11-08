import sys
from src import oisin


def get_file(file_dir_str):
    file_dir = file_dir_str
    try:
        file_dir = sys.argv[1]
    except IndexError:
        pass

    return file_dir


def create_poem(filename):
    oisin.balladize(
        oisin.load(filename),
        meter=oisin.iambic(4, 'aabbccdd'),
        step=50,
        order=3)


create_poem(get_file('~/oisin/input/alices.txt'))  # example dir, change to your absolute one
