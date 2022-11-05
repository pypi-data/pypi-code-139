"""
Module for python helper methods
"""

from functools import wraps


def run_n_times(n):
    """Returns a decorator to run decorated function n number of times

    Parameters
    ----------
    n : int : Number of times to run function
        

    Returns
    -------

    """
    def decorator(func):
        """

        Parameters
        ----------
        func : function:
            

        Returns
        -------

        """
        def wrapper(*args, **kwargs):
            """

            Parameters
            ----------
            *args : Arguments of wrapped function
                
            **kwargs : Keyword arguments of wrapped function
                

            Returns
            -------
            None
            """
            for i in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator


def memoize(func):
    """Store the results of the decorated function for fast lookup

    Parameters
    ----------
    func : Function:
        

    Returns
    -------

    """

    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        """

        Parameters
        ----------
        *args : Arguments of wrapped function
            
        **kwargs : Keyword arguments of wrapped function
            

        Returns
        -------
        Output: output of internal function or cache
        """
        # If these arguments haven't been seen before,
        if (args, str(kwargs)) not in cache.keys():
            print('not in cache')
            print(cache)
            # Call func() and store the result.
            cache[(args, str(kwargs))] = func(*args, **kwargs)
        return cache[(args, str(kwargs))]
    return wrapper


# if __name__ == '__main__':
    # @memoize
    # def testfunc(num1, num2, name, age):
    #     time.sleep(3)
    #     print(f'Running operations for {name}')
    #     return num1*num2+age
    #
    # res = testfunc(1, 2, name='levent', age=39)
    # print(res)
    # res = testfunc(1, 3, name='elif', age=39)
    # print(res)
    # res = testfunc(1, 2, name='levent', age=39)
    # print(res)
    # res = testfunc(1, 3, name='elif', age=39)
    # print(res)
    # res = testfunc(1, 3, name='fatma', age=39)
    # print(res)
    # res = testfunc(1, 2, name='levent', age=39)
    # print(res)

    # @timer
    # def wait(name):
    #     time.sleep(1.5)
    #     print(f'Hello {name}')
    # wait('Levent')
    #
    # @return_type
    # def return_func(num1, num2):
    #     return num1*30
    #
    # print(return_func(1, 3))

    # @run_n_times(3)
    # def greet(name):
    #     print(f'Hello {name}')
    #
    # greet('Levent')
