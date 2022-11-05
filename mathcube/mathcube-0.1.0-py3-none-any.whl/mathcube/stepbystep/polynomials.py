from mathcube import Table


class HornerMethod:
    """A step by step implementation of Horner's method to evaluate polynomials."""

    def __init__(self, poly, x0):
        """Initialize Horner method to evaluate polynomial at given point.

        Parameters
        ----------
        poly:  sympy polynomial
            The polynomial to evaluate.
        x0:  number
            The point where to evaluate the polynomial.

        Examples
        --------

        The following example creates the Horner table for the polynomial

            .. math::
                3x^3 + 2x^2 - 4x + 7

        at x = 2.

        >>> from sympy import *
        >>> from sympy.abc import x
        >>> import mathcube.stepbystep as sbs
        >>> p = poly(3*x**3+2*x**2-4*x+7, x)
        >>> horner = sbs.HornerMethod(p, 2)
        >>> horner.step()
        >>> horner.step()
        >>> ...

        """
        self.x0 = x0
        t = Table([poly.all_coeffs()])
        t.insert_column(0)
        t.insert_row()
        t.insert_row()
        t[1, 0] = "x=%d" % x0
        t[1, 1] = 0
        t.style[0, :] = 'border-bottom: 1px solid #000;'
        t.style[:, 0] = 'border-right: 1px solid #000;'
        self.table = t
        self._step_no = 0

    def _repr_html_(self):
        return self.table._repr_html_()

    def step(self):

        t = self.table
        _, ncols = t.shape
        if self._step_no == 2 * ncols - 3:
            return self

        def add_step():
            col = self._step_no // 2 + 1
            t[2, col] = t[0, col] + t[1, col]

        def mul_step():
            col = self._step_no // 2 + 2
            t[1, col] = self.x0 * t[2, col - 1]

        if self._step_no % 2 == 0:
            add_step()
        else:
            mul_step()

        self._step_no += 1

        return self
