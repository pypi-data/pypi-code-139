"""
Module for analysis of python functions
"""

import pandas
import time
from functools import wraps


def timer(func):
    """Calculate and print duration of function

    Parameters
    ----------
    func : Function:
        

    Returns
    -------

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """

        Parameters
        ----------
        *args : Arguments
            
        **kwargs : Keyword Arguments
            

        Returns
        -------
        Output: output of inner function.
        """
        start = pandas.Timestamp('today')
        val = func(*args, **kwargs)
        end = pandas.Timestamp('today')
        delta = end - start
        print(f'Process took: {delta.components.minutes} min, {delta.components.seconds},'
              f'secs {delta.components.milliseconds} ms')
        return val
    return wrapper


def return_type(func):
    """Print the return type of inner function

    Parameters
    ----------
    func : Function:
        

    Returns
    -------

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """

        Parameters
        ----------
        *args : Arguments
            
        **kwargs : Keyword arguments
            

        Returns
        -------
        Output: output of inner function.
        """
        val = func(*args, **kwargs)
        if not val:
            print(f'Process does not return any value - {type(val)}')
        elif len([val]) > 1:
            print([type(n) for n in val])
        else:
            print(type(val))
        return val
    return wrapper


# if __name__ == '__main__':
#
#     @timer
#     def wait(name):
#         time.sleep(2)
#         print(f'Hello {name}')
#
#     wait('Levent')
#     #
#     # @return_type
#     # def return_func(num1, num2):
#     #     return num1*30
#     #
#     # print(return_func(1, 3))
#
#     # @run_n_times(3)
#     # def greet(name):
#     #     print(f'Hello {name}')
#     #
#     # greet('Levent')
