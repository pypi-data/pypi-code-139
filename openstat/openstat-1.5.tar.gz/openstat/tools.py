from fractions import Fraction
import math

def C(k, n):
    assert k <= n
    return math.factorial(n) // math.factorial(k) // math.factorial(n-k)

def B(n, p, f, t=0):
    p = Fraction(p)
    t = t or f
    q = 1 - p
    return float(sum(C(i, n) * p**i * q**(n-i) for i in range(f, t+1)))

def P(n, p, f, t=0):
    p = Fraction(p)
    t = t or f
    l = n * p
    s = sum(l**i / math.factorial(i) for i in range(f, t+1))
    return float(s / Fraction(math.e)**l)

def L(n, p, f, t=0, d=1000):
    p = float(p)
    t = t or f
    t -= d > 1
    q = 1 - p
    result = 0
    np = n*p
    sqrtnpq = math.sqrt(n*p*q)
    for i in range(f, t+1):
        for j in range(d):
            x = (i+j/d - np) / sqrtnpq
            result += math.exp(-(x**2) / 2) / d
    return result / math.sqrt(n*p*q*2*math.pi)

def Pe(n, p, *args, **kwargs):
    p = float(p)
    return min(p, n*p**2)

def Le(n, p, *args, **kwargs):
    p = float(p)
    q = 1 - p
    return 1 / (p*q*math.sqrt(n))
