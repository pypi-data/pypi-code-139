import numpy as np

def potenciar(base, potencia):
    result = []
    for i in range(potencia):
        result.append(base)
    return np.prod(result)
