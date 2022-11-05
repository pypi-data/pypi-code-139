"""

"""

import decimal
from decimal import Decimal
import math
import typing

from .constants import PRECISION


def maclaurin_expansion(func: typing.Callable[[int, Decimal, int], Decimal]) -> typing.Callable:
    """

    :param func:
    :return:
    """

    def wrapper(x: Decimal, *, precision: int = PRECISION) -> typing.Generator[Decimal, None, None]:
        """
        Calculates the :math:`nth` term of the Maclaurin series expansion of ``func``.

        :param x: The value at which to evaluate the Maclaurin series expansion
        :param precision: The number of decimal plays to which the returned value should be rounded
        :return: A generator of terms in the evaluated Maclaurin series expansion
        """
        with decimal.localcontext() as ctx:
            ctx.prec = precision + 2

            n = 0
            while True:
                try:
                    term = func(n, x, precision)
                except decimal.Overflow:
                    return

                # Test for convergence
                if term + Decimal(1) == Decimal(1):
                    return

                yield term

                n += 1

    return wrapper


@maclaurin_expansion
def sine(n: int, x: Decimal, precision: int) -> Decimal:
    r"""
    Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`sin(x)`.

    :math:`a_{n} = \frac{(-1)^{n}}{(2n+1)!} x^{2n+1}`

    :param n: The cardinal position of the term in the Maclaurin series expansion
    :param x: The value at which to evaluate the Maclaurin series expansion
    :param precision: The number of decimal plays to which the returned value should be rounded
    :return: The value of the :math:`nth` term of the evaluated Maclaurin series expansion
    """
    with decimal.localcontext() as ctx:
        ctx.prec = precision + 2

        return Decimal(-1) ** n / Decimal(math.factorial(2 * n + 1)) * (x ** (2 * n + 1))


@maclaurin_expansion
def cosine(n: int, x: Decimal, precision: int) -> Decimal:
    r"""
    Calculates the :math:`mth` term of the Maclaurin series expansion of :math:`cos(x)`.

    :math:`a_{n} = \frac{(-1)^{n}}{(2n)!} x^{2n}`

    :param n: The cardinal position of the term in the Maclaurin series expansion
    :param x: The value at which to evaluate the Maclaurin series expansion
    :param precision: The number of decimal plays to which the returned value should be rounded
    :return: The value of the :math:`nth` term of the evaluated Maclaurin series expansion
    """
    with decimal.localcontext() as ctx:
        ctx.prec = precision + 2

        return Decimal(-1) ** n / Decimal(math.factorial(2 * n)) * (x ** (2 * n))


@maclaurin_expansion
def arcsine(n: int, x: Decimal, precision: int) -> Decimal:
    r"""
    Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`arcsin(x)`.

    :math:`a_{n} = \frac{(2n)!}{4^{n}(n!)^{2}(2n+1)} x^{2n+1}`

    :param n: The cardinal position of the term in the Maclaurin series expansion
    :param x: The value at which to evaluate the Maclaurin series expansion
    :param precision: The number of decimal plays to which the returned value should be rounded
    :return: The value of the :math:`nth` term of the evaluated Maclaurin series expansion
    """
    with decimal.localcontext() as ctx:
        ctx.prec = precision + 2

        return Decimal(
            math.factorial(2 * n)
        ) / (
                Decimal(4 ** n) * Decimal(math.factorial(n)) ** 2 * Decimal(2 * n + 1)
        ) * (x ** (2 * n + 1))


@maclaurin_expansion
def arctangent(n: int, x: Decimal, precision: int) -> Decimal:
    r"""
    Calculates the :math:`nth` term of the Maclaurin series expansion of :math:`arctan(x)`.

    :math:`a_{n} = \frac{(-1)^n}{2n+1} x^{2n+1}`

    :param n: The cardinal position of the term in the Maclaurin series expansion
    :param x: The value at which to evaluate the Maclaurin series expansion
    :param precision: The number of decimal plays to which the returned value should be rounded
    :return: The value of the :math:`nth` term of the evaluated Maclaurin series expansion
    """
    with decimal.localcontext() as ctx:
        ctx.prec = precision + 2

        return Decimal(-1) ** n / Decimal(2 * n + 1) * (x ** (2 * n + 1))
