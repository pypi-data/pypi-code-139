"""
Module for statistical helper methods.
Power methods are received from DataCamp Customer Analytics and AB Testing Course
"""

from scipy import stats


def get_power(n, p1, p2, cl):
    """Returns the power of our hypothesis test by number of samples,
    probabilities (conversion_rate) and confidence level

    Parameters
    ----------
    n : int : Number of samples
        
    p1 : float: probability for first set
        
    p2 : float: probability for second set
        
    cl : float: confidence level
        

    Returns
    -------
    Power : float:

    """
    alpha = 1 - cl

    qu = stats.norm.ppf(1 - alpha / 2)

    diff = abs(p2 - p1)
    bp = (p1 + p2) / 2

    v1 = p1 * (1 - p1)
    v2 = p2 * (1 - p2)

    bv = bp * (1 - bp)

    power_part_one = stats.norm.cdf((n ** 0.5 * diff - qu * (2 * bv) ** 0.5) / (v1 + v2) ** 0.5)
    power_part_two = 1 - stats.norm.cdf((n ** 0.5 * diff + qu * (2 * bv) ** 0.5) / (v1 + v2) ** 0.5)

    power = power_part_one + power_part_two
    return power


def get_sample_size(power, p1, p2, cl, max_n=1000000):
    """calculates the power for different test size until it reaches the desired power level,
    and returns the test size

    Parameters
    ----------
    power : int:
        
    p1 : float: probability for first set
        
    p2 : float: probability for second set
        
    cl : float: confidence level
        
    max_n : int: maximum number of tests to be run
         (Default value = 1000000)

    Returns
    -------
    n : int: sample size
    """
    n = 1
    while n <= max_n:
        tmp_power = get_power(n, p1, p2, cl)
        if tmp_power >= power:
            return n
        else:
            n = n + 1
