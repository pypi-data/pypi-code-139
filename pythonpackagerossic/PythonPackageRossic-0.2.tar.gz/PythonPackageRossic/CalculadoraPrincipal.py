
from .SumarFile import Sumar

class Calculadora(Sumar):
    def __init__(self,numero1,numero2,operation):
        Sumar.__init__(self, numero1,numero2)
        self.operation = operation

