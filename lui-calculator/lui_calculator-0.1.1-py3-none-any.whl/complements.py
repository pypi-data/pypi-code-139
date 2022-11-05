from typing import Any

import sympy

from .printer import custom_printer


# TODO: Repeating digit simplify by an over-line
# enum str + bool
class Sign:
    pass


def complement_for_real(real) -> tuple[float | int, str, bool]:
    """
    Return an equality or an approximation of a real number
    :param real: any real number of sympy
    :return: (equality | approximation, sign, is_different)
        equality | approximation:
            1/5 -> 0.2
            1/3 -> 0.3333333333333333
        sign ("=" or "≈"):
            1/5 -> "="
            1/3 -> "≈"
        is_different (True if equality | approximation != real):
            1       -> False
            2.5     -> False
            1/5     -> True
            1/3     -> True
            sqrt(2) -> True
    """

    try:
        if not real.is_real:
            raise ValueError("Only real number is accepted")
    except AttributeError as e:
        raise ValueError("Only real number is accepted") from e

    if real.is_Integer:
        return int(real), "=", False
    if real.is_Float:
        return float(real), "=", False
    if real.is_Rational:
        if sympy.primefactors(real.denominator) in ([2], [5], [2, 5]):
            return float(real), "=", True
        else:
            return float(real), "≈", True
    if real.is_irrational or real.is_irrational is None:
        return float(real), "≈", True
    return real, "=", False


def complement_for_complex(complex_number) -> tuple[tuple[Any, Any], str, bool]:
    """
    Return an equality or an approximation of a complex number
    :param complex_number: any complex number of sympy
    :return: (equality | approximation, sign, is_different)
        equality | approximation (tuple: (real_part, imaginary_part)):
            1/5 + i -> (0.2, 1)
            1/3 + i -> (0.3333333333333333, 1)
        sign ("=" or "≈"):
            1/5 + i -> "="
            1/3 + i -> "≈"
        is_different (True if equality | approximation != argument:real):
            1           -> False
            i           -> False
            1/5 + i     -> True
            1/3 + i     -> True
            sqrt(2) + i -> True
    """

    try:
        if not complex_number.is_complex:
            raise ValueError("Only complex number is accepted")
    except AttributeError as e:
        raise ValueError("Only complex number is accepted") from e

    real, imaginary = complex_number.as_real_imag()

    real, real_sign, real_is_useful = complement_for_real(real)
    imaginary, imaginary_sign, imaginary_is_useful = complement_for_real(imaginary)

    if not real_is_useful and not imaginary_is_useful:
        return (real, imaginary), "=", False

    sign = "=" if real_sign == "=" and imaginary_sign == "=" else "≈"

    return (real, imaginary), sign, True


def printer_with_complement_for_complex(expression, complex_number, sign, is_useful, printer=custom_printer) -> str:
    if not is_useful:
        return str(printer(expression))
    if complex_number[1] == 1:
        complex_number = (complex_number[0], printer(sympy.I))
    else:
        multiply_by_i = printer(sympy.Mul(sympy.Number(2), sympy.I))[1:]
        complex_number = (complex_number[0], str(complex_number[1]) + multiply_by_i)

    if complex_number[0] == 0:
        return f"{printer(expression)} {sign} {complex_number[1]}"
    else:
        return f"{printer(expression)} {sign} {complex_number[0]} + {complex_number[1]}"


def sign_complement(expression, printer=custom_printer) -> tuple[str | None, str | None]:
    pass


def assemble(result, sign, complement) -> str:
    pass


def printer_with_complement(expression, printer=custom_printer) -> str:
    """
    Format an sympy expression with the complement
    :param printer: a sympy printer function
    :param expression: a sympy expression
    :return: the expression with a complement (equality or approximation) if useful
        following examples with default printer:
            1                -> 1
            1/5              -> 1/5 = 0.2
            1/3              -> 1/3 ≈ 0.3333333333333333
            sqrt(2)          -> √2 ≈ 1.4142135623730951
            pi               -> π ≈ 3.141592653589793
            I                -> ⅈ
            3*I              -> 3⋅ⅈ
            1/5+3*I          -> 1/5 + 3⋅ⅈ = 0.2 + 3⋅ⅈ
            Lambda(x, x + 1) -> x ↦ x + 1
            Heaviside(x)     -> θ(x)
    """
    try:
        if expression.is_real:
            if (complement := complement_for_real(expression))[2]:
                return f"{printer(expression)} {complement[1]} {complement[0]}"
            else:
                return str(printer(complement[0]))
        if expression.is_complex:
            complex_number, sign, is_useful = complement_for_complex(expression)
            return printer_with_complement_for_complex(expression, complex_number, sign, is_useful, printer)
        if expression.is_complex is None:
            complex_number = expression.evalf().as_real_imag()
            if complex_number[0].is_number and complex_number[1].is_number:
                sign = "≈"
            else:
                return str(printer(expression))
            is_useful = expression != complex_number[0] + complex_number[1]
            return printer_with_complement_for_complex(expression, complex_number, sign, is_useful, printer)
        else:
            return str(printer(expression))
    except AttributeError:
        return str(printer(expression))
