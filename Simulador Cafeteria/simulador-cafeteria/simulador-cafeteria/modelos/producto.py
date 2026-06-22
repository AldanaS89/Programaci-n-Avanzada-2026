"""
Jerarquía de productos del menú.

Demuestra:
- ABSTRACCIÓN: Producto es una clase abstracta (ABC) que define el contrato
  común (precio, descripcion) sin poder instanciarse directamente.
- HERENCIA: Bebida y Comida heredan de Producto.
- POLIMORFISMO: cada subclase resuelve descripcion() a su manera, y los Extra
  (Decorator) también responden a la misma interfaz.
- ENCAPSULAMIENTO: el precio se guarda como atributo "protegido" y se expone
  mediante @property de solo lectura.

Decisión de diseño:
- La CATEGORÍA del menú (bebida/salado/dulce) es un atributo (Enum), no una
  subclase: un producto pertenece a una sola categoría.
- Las CARACTERÍSTICAS (sin TACC, vegetariano) son banderas booleanas
  independientes, porque se cruzan entre sí y con la categoría.
- Las subclases (Bebida / Comida) existen por COMPORTAMIENTO distinto:
  una bebida admite extras (se la envuelve con el patrón Decorator), una
  comida no.
"""
from abc import ABC, abstractmethod
from utils.categorias import Categoria


class Producto(ABC):
    def __init__(self, nombre, precio, categoria, stock=0,
                 sin_tacc=False, vegetariano=False):
        self.nombre = nombre
        self._precio = precio          # encapsulado: se accede vía @property
        self.categoria = categoria     # instancia de Categoria (Enum)
        self.stock = stock
        self.sin_tacc = sin_tacc
        self.vegetariano = vegetariano

    @property
    def precio(self):
        """Precio de solo lectura (el componente base del patrón Decorator)."""
        return self._precio

    @abstractmethod
    def descripcion(self):
        """Cada producto describe qué es. Método polimórfico."""
        ...

    def admite_extras(self):
        """Por defecto, un producto no admite extras. Las bebidas sí."""
        return False

    def descontar_stock(self, cantidad=1):
        self.stock -= cantidad

    def reponer_stock(self, cantidad):
        self.stock += cantidad

    def _etiquetas(self):
        """Arma el texto de banderas (sin TACC / vegetariano) si aplican."""
        etiquetas = []
        if self.sin_tacc:
            etiquetas.append("sin TACC")
        if self.vegetariano:
            etiquetas.append("vegetariano")
        return f" [{', '.join(etiquetas)}]" if etiquetas else ""


class Bebida(Producto):
    """Producto líquido que SÍ admite extras (leche, crema, etc.)."""

    def __init__(self, nombre, precio, stock=0, sin_tacc=False, vegetariano=False):
        super().__init__(nombre, precio, Categoria.BEBIDA, stock,
                         sin_tacc, vegetariano)

    def admite_extras(self):
        return True

    def descripcion(self):
        return self.nombre


class Comida(Producto):
    """Producto sólido (salado o dulce). No admite extras de café."""

    def __init__(self, nombre, precio, categoria, stock=0,
                 sin_tacc=False, vegetariano=False):
        # La comida puede ser SALADO o DULCE: se pasa la categoría explícita.
        super().__init__(nombre, precio, categoria, stock,
                         sin_tacc, vegetariano)

    def descripcion(self):
        return self.nombre
