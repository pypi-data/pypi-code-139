values = (
    {
        'T': 'E',
        'M': lambda m=1: m,
        'G': lambda p: 1/p,
        'P': lambda l: l,
        'U': lambda a, b: (a+b)/2,
        'E': lambda l: 1/l,
        'N': lambda a, o2: a,
        'C': lambda c: c,
    },
    {
        'T': 'D',
        'M': lambda m=1: m**2,
        'G': lambda p: (1-p)/p**2,
        'P': lambda l: l,
        'U': lambda a, b: (b-a)**2/12,
        'E': lambda l: 1/l**2,
        'N': lambda a, o2: o2,
        'C': lambda c: 0,
    }
)

import re
def basic(expr):
    expr = re.sub('([\\d-]+)?([A-Z])([\\d,]+)?', '+L[\'M\'](\\1)*L[\'\\2\'](\\3)', expr)
    return {L['T']: eval(expr) for L in values}
