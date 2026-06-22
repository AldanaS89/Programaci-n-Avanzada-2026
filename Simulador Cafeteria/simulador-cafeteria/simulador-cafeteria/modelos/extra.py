"""
Patrón de diseño DECORATOR (GoF) — patrón estructural.

IMPORTANTE (para la defensa del TPI):
Esto es el PATRÓN DE DISEÑO Decorator, implementado con CLASES. No tiene
relación con la sintaxis @ de Python (esos son los decoradores de función,
en decoradores/validaciones.py). Comparten el nombre "decorador" pero son
conceptos distintos.

Idea del patrón:
- Extra hereda de Producto (misma interfaz: precio, descripcion).
- Además, Extra GUARDA ADENTRO otro Producto (el que envuelve).
- Al pedirle precio/descripcion, delega en el producto envuelto y le SUMA lo
  suyo.
- Como un Extra es un Producto, se puede envolver un Extra con otro Extra,
  encadenando: Café -> ConLeche -> Grande.

Ventaja frente a crear subclases (CafeConLecheGrande, CafeConCrema, ...):
se evita la explosión de clases. Los extras se combinan en tiempo de
ejecución.
"""
from modelos.producto import Producto


class Extra(Producto):
    """
    Decorador base. Envuelve un Producto y le agrega precio y descripción.
    """

    def __init__(self, producto_envuelto, nombre_extra, precio_extra):
        self._producto = producto_envuelto       # el objeto que se decora
        self._nombre_extra = nombre_extra
        self._precio_extra = precio_extra
        # Hereda categoría y banderas del producto envuelto.
        super().__init__(
            nombre=producto_envuelto.nombre,
            precio=producto_envuelto.precio,
            categoria=producto_envuelto.categoria,
            stock=producto_envuelto.stock,
            sin_tacc=producto_envuelto.sin_tacc,
            vegetariano=producto_envuelto.vegetariano,
        )

    @property
    def precio(self):
        # Precio del producto envuelto + el del extra (delegación + suma).
        return self._producto.precio + self._precio_extra

    def descripcion(self):
        return f"{self._producto.descripcion()} + {self._nombre_extra}"

    def admite_extras(self):
        # Un producto decorado sigue admitiendo más extras (encadenamiento).
        return self._producto.admite_extras()


# --- Extras concretos: cada uno define su nombre y su precio ---

class ConLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "leche", 200)


class ConCrema(Extra):
    def __init__(self, producto):
        super().__init__(producto, "crema", 350)


class ConDulceDeLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "dulce de leche", 300)


class Grande(Extra):
    def __init__(self, producto):
        super().__init__(producto, "tamaño grande", 400)


# Catálogo de extras disponibles, para ofrecerlos desde el menú de consola.
EXTRAS_DISPONIBLES = {
    "1": ("Leche", ConLeche),
    "2": ("Crema", ConCrema),
    "3": ("Dulce de leche", ConDulceDeLeche),
    "4": ("Tamaño grande", Grande),
}
