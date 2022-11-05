"""Helper functions"""

from __future__ import annotations

from random import randint


def bulk_random_numbers(quantity: int, range_high: int, range_low: int = 1) -> tuple[list[int], int]:
    """
    Generate bulk random numbers within the given range.

    Parameters
    ----------
    quantity
        How many numbers to generate
    range_high
        The highest possible number
    range_low
        The lowest possible number

    Examples
    --------
    >>> bulk_random_numbers(3,1)
    ([1, 1, 1], 3)

    Returns
    -------
    A tuple containing the list of numbers and the sum of all the numbers

    """
    numbers = [randint(range_low, range_high) for _ in range(quantity)]
    return numbers, sum(numbers)
