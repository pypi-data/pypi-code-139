import sympy as sp

def E(x, f, l, r):
    return sp.integrate(x*f, ('x', l, r))

def D(x, f, l, r):
    # return E((x - E(x, f, l, r))**2, f, l, r)
    return E(x**2, f, l, r) - E(x, f, l, r)**2

def P(f, l, r):
    return lambda a, b: float(sp.integrate(f, ('x', max(l, a), min(r, b))))

def cdist(f, l, r):
    f = sp.sympify(f)
    с, = sp.solve(sp.integrate(f, ('x', l, r))-1)
    f = f.subs('с', с)
    x, = f.free_symbols
    return {'c': с, 'E': E(x, f, l, r), 'D': D(x, f, l, r)}, P(f, l, r)
