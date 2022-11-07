from fractions import Fraction
from . tools import B, P, L, Pe, Le

def BPL(*args, **kwargs):
    assert len(args) >= 2 and isinstance(args[1], str) or \
        'p' in kwargs and isinstance(kwargs['p'], str)
    b = B(*args, **kwargs)
    p = P(*args, **kwargs), Pe(*args, **kwargs)
    l = L(*args, **kwargs), Le(*args, **kwargs)
    r = f'B: {b:.3f}, ' \
        f'P: {p[0]:.3f}, Pl: {max(p[0]-p[1], 0):.3f}, Pr: {min(p[0]+p[1], 1):.3f}, ' \
        f'L: {l[0]:.3f}, Ll: {max(l[0]-l[1], 0):.3f}, Lr: {min(l[0]+l[1], 1):.3f}'
    return r
