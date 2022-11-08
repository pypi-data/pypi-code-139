from fractions import Fraction
import numpy as np

def get_row(row):
    return tuple(Fraction(col) for col in row.split(','))

def get_table(table):
    return tuple(get_row(row) for row in table.split(';'))

def calc(array, values, axis):
    P = np.sum(array, axis=axis)
    E = np.sum(values * P)
    D = np.sum(P * (values-E)**2)
    return P, E, D

def table(e, n, p):
    p = p.replace('x', '-1')
    e = np.array(get_row(e))
    n = np.array(get_row(n))
    p = np.array(get_table(p))
    x = -np.sum(p)
    p[p == -1] += x + 1
    Pe, Ee, De = calc(p, e, 0)
    Pn, En, Dn = calc(p, n, 1)
    cov = np.sum(p*e*n.reshape(-1, 1)) - Ee*En
    rho = cov / (De*Dn) ** 0.5
    return f'x: {x}, E: {Ee}, D: {De}, E: {En}, D: {Dn}, cov: {cov}, rho: {rho:.3f}'
