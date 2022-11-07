from functools import cache
from time import perf_counter
import sys

def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False

def isstring(x):
    try:
        str(x)
        return True
    except:
        return False

def isint(x):
    try:
        int(x)
        return True
    except:
        return False

def radice(x):
    return x**.5


def get_time(func):

    def wrapper(*args, **kwargs):
        start_time = perf_counter()

        func(*args, *kwargs)

        end_time = perf_counter()

        total_time = round(end_time - start_time, 5)

        print('Durata:', total_time, 'secondi.')

    return wrapper

@cache
def setup():
    sys.setrecursionlimit(1000000000)
    return "Setup Done."

