"""
Define las categorías del menú mediante un Enum.

Usar un Enum (en lugar de strings sueltos como "bebida") evita errores de
tipeo y centraliza los valores válidos en un único lugar. La categoría indica
a qué grupo del menú pertenece un producto; cada producto tiene UNA categoría.
"""
from enum import Enum


class Categoria(Enum):
    BEBIDA = "Bebida"
    SALADO = "Salado"
    DULCE = "Dulce"

    def __str__(self):
        return self.value
