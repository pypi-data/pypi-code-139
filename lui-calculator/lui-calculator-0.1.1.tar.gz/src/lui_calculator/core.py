from pathlib import Path

import requests
import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, \
    implicit_multiplication_application, convert_xor, convert_equals_signs

from . import complements
from .utils import exit_after
from .printer import custom_printer

transformations = standard_transformations + (convert_xor, implicit_multiplication_application, convert_equals_signs)

local_dict = {"e": sympy.E, "ℯ": sympy.E, "i": sympy.I, "ⅈ": sympy.I, "π": sympy.pi, "θ": sympy.Heaviside,
              "φ": sympy.GoldenRatio, "ϕ": sympy.GoldenRatio, "⋅": "*"}

replace_dict = {"⋅": "*", "√": "sqrt "}


def parse(expression: str):
    for old, new in replace_dict.items():
        expression = expression.replace(old, new)

    return parse_expr(expression, transformations=transformations, local_dict=local_dict)


def latex_needed(expression, printer=custom_printer) -> bool:
    if expression == sympy.zoo:
        return True
    try:
        return printer(parse(printer(expression))) != printer(expression)
    except SyntaxError:
        return True


def latex2png(latex_str: str, outfile: str | Path = "output.png"):
    response = requests.get(
        r"https://latex.codecogs.com/png.download?\dpi{110}%20\fn_phv%20\huge%20{\color{White}" + latex_str + "}")
    if response.ok:
        with open(outfile, "wb+") as file:
            file.write(response.content)
    else:
        raise ConnectionError("https://latex.codecogs.com/ don't respond correctly")


def calc(expression: str, latex: None | bool = False, output: str | Path = "output.png", max_length: None | int = None)\
        -> str | bool:
    result = parse(expression)

    # TODO: Approximation for solve-set
    if result.is_Equality:
        solve_set = sympy.solveset(result)
        if latex is False:
            return str(custom_printer(solve_set))
        try:
            latex2png(sympy.latex(solve_set))
            return ""
        except ConnectionError as e:
            print(e)
            return str(custom_printer(solve_set))

    if latex is None:
        latex = latex_needed(result)

    if not latex:
        return complements.printer_with_complement(result)
    try:
        latex2png(
            complements.printer_with_complement(result, printer=sympy.latex).replace("≈", r"\approx"),
            outfile=output
        )
        return True
    except ConnectionError as e:
        print(e)
        return complements.printer_with_complement(result)

    #   sign, complement = complements.sign_complement(result)
    #   result = printer(result)
    #   ...
    #   if len(complements.assemble(result, sign, complement)) <= max_length:
    #       return complements.assemble(result, sign, complement)
    #   elif min(len(result), len(complement)) <= max_length:
    #       if len(result) <= len(complement):
    #           return result
    #       else:
    #           return complement
    #   else:
    #       return None


@exit_after(10)
def secure_calc(expression: str, latex: None | bool = None) -> str:
    return calc(expression=expression, latex=latex, max_length=2000)
