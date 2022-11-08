class Probability:

    def __init__(self, p):
        self.p = p

    def __and__(self, other):
        return Probability(self.p * other.p)

    def __or__(self, other):
        return Probability(self.p + other.p - self.p * other.p)

    def __invert__(self):
        return Probability(1 - self.p)

import re
def logic(expr, values, factor=1):
    expr = re.sub('(\\d)+', 'P[\\1]', expr)
    P = [Probability(v*factor) for v in values]
    return f'{eval(expr).p:.3f}'
