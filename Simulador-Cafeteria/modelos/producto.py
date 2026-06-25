"""
Jerarquia de productos del menu.

Demuestra:
- ABSTRACCION: Producto es una clase abstracta (ABC).
- HERENCIA: Bebida y Comida heredan de Producto.
- POLIMORFISMO: cada subclase resuelve descripcion() a su manera.
- ENCAPSULAMIENTO: precio con getter y setter via @property.

Tipos de bebida disponibles:
  TIPO_CAFE          -> Cafe: variantes corto/largo/cortado/lagrima.
                        Sabores por variante (ver extra.py). Sin Grande
                        para corto/largo (ya definen tamano).
  TIPO_CAPUCHINO     -> Sin variantes. Crema + ddl. Admite Grande.
  TIPO_CHOCOLATADA   -> Sin variantes. Crema + ddl. Admite Grande.
  TIPO_INFUSION      -> Sin variantes. Solo leche. Admite Grande.
  TIPO_JUGO          -> Sin variantes. Sin sabores. Solo Grande.
  TIPO_PERSONALIZADO -> Bebida creada por el gerente. El comportamiento
                        se define via extras_config al momento de crearla.
"""
from abc import ABC, abstractmethod
from utils.categorias import Categoria


class Producto(ABC):
    def __init__(self, nombre, precio, categoria, stock=0,
                 sin_tacc=False, vegetariano=False):
        self.nombre = nombre
        self._precio = precio
        self.categoria = categoria
        self.stock = stock
        self.sin_tacc = sin_tacc
        self.vegetariano = vegetariano

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        self._precio = valor

    @abstractmethod
    def descripcion(self):
        ...

    def admite_extras(self):
        return False

    def descontar_stock(self, cantidad=1):
        self.stock -= cantidad

    def reponer_stock(self, cantidad):
        self.stock += cantidad

    def _etiquetas(self):
        etiquetas = []
        if self.sin_tacc:
            etiquetas.append("sin TACC")
        if self.vegetariano:
            etiquetas.append("vegetariano")
        return f" [{', '.join(etiquetas)}]" if etiquetas else ""


class Bebida(Producto):
    """Producto liquido que admite extras."""

    TIPO_CAFE          = "cafe"
    TIPO_CAPUCHINO     = "capuchino"
    TIPO_CHOCOLATADA   = "chocolatada"
    TIPO_INFUSION      = "infusion"
    TIPO_JUGO          = "jugo"
    TIPO_PERSONALIZADO = "personalizado"   # bebidas creadas por el gerente

    def __init__(self, nombre, precio, stock=0, tipo=None,
                 sin_tacc=False, vegetariano=False, extras_config=None):
        super().__init__(nombre, precio, Categoria.BEBIDA, stock,
                         sin_tacc, vegetariano)
        self.tipo_bebida   = tipo if tipo is not None else Bebida.TIPO_CAFE
        # None = usa defaults del tipo; dict = config personalizada del gerente
        self.extras_config = extras_config

    def admite_extras(self):
        return True

    def descripcion(self):
        return self.nombre



class Comida(Producto):
    """Producto solido (salado o dulce). No admite extras."""

    def __init__(self, nombre, precio, categoria, stock=0,
                 sin_tacc=False, vegetariano=False):
        super().__init__(nombre, precio, categoria, stock,
                         sin_tacc, vegetariano)

    def descripcion(self):
        return self.nombre
