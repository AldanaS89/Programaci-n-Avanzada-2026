import math

def area_circulo(radio):
    area = math.pi * radio ** 2
    return area
print("El área del círculo es:", area_circulo(5), "cm^2")

def area_triangulo(base, altura):
    area = (base * altura) / 2
    return area 
print("El área del triángulo es:", area_triangulo(10, 5), "cm^2")

def area_cuadrado(lado):
    area = lado ** 2
    return area
print("El área del cuadrado es:", area_cuadrado(4), "cm^2")