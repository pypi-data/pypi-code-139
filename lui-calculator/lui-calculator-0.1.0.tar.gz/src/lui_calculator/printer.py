from sympy.printing.pretty import pretty


def custom_printer(expr, **kwargs):
    return pretty(expr, wrap_line=False, **kwargs)
