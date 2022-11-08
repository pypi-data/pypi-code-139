def triangle_area(base,altura):
    area = (base * altura)/2
    return area

def rectangle_area(base,altura):
    area = base * altura
    return area

def square_area(lado):
    area = lado * lado
    return area

def circle_area(raio):
    area = 3.14 * (raio * raio)
    return area

def trapezoid_area(Base_maior, base_menor, altura):
    area = ((Base_maior + base_menor) * altura)/2
    return area

def rhombus_area(Diagonal_maior, diagonal_menor):
    area = (Diagonal_maior * diagonal_menor)/2
    return area