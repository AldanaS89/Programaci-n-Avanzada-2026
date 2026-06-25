"""
Patron de diseno DECORATOR (GoF) -- patron estructural.
Implementado con CLASES. No confundir con los decoradores de funcion (@)
de decoradores/validaciones.py.

Modelo de personalizacion por tipo de bebida:

  CAFE        -> variantes: corto / largo / cortado / lagrima (una sola)
                 sabores:   leche / crema / dulce de leche (varios)
                 grande:    NO (corto/largo ya definen el tamano)

  CAPUCHINO   -> variantes: ninguna (ya es una preparacion especifica)
                 sabores:   crema / dulce de leche (varios)
                 grande:    SI

  CHOCOLATADA -> variantes: ninguna
                 sabores:   crema / dulce de leche (varios)
                 grande:    SI

  INFUSION    -> variantes: ninguna
                 sabores:   leche (varios)
                 grande:    SI

  JUGO        -> variantes: ninguna
                 sabores:   ninguno
                 grande:    SI
"""
from modelos.producto import Producto, Bebida


class Extra(Producto):
    """Decorador base. Envuelve un Producto y le agrega precio y descripcion."""

    def __init__(self, producto_envuelto, nombre_extra, precio_extra):
        self._producto = producto_envuelto
        self._nombre_extra = nombre_extra
        self._precio_extra = precio_extra
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
        return self._producto.precio + self._precio_extra

    @precio.setter
    def precio(self, valor):
        self._precio = valor

    def descripcion(self):
        return f"{self._producto.descripcion()} + {self._nombre_extra}"

    def admite_extras(self):
        return self._producto.admite_extras()


# --- VARIANTES DE PREPARACION (solo para cafe) ---

class Corto(Extra):
    def __init__(self, producto):
        super().__init__(producto, "corto", 0)

class Largo(Extra):
    def __init__(self, producto):
        super().__init__(producto, "largo", 100)

class Cortado(Extra):
    def __init__(self, producto):
        super().__init__(producto, "cortado", 150)

class Lagrima(Extra):
    def __init__(self, producto):
        super().__init__(producto, "lagrima", 200)


# --- SABORES (se pueden combinar) ---

class ConLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "leche", 200)

class ConCrema(Extra):
    def __init__(self, producto):
        super().__init__(producto, "crema", 350)

class ConDulceDeLeche(Extra):
    def __init__(self, producto):
        super().__init__(producto, "dulce de leche", 300)


# --- TAMANO (pregunta separada, una sola vez) ---

class Grande(Extra):
    def __init__(self, producto):
        super().__init__(producto, "tamano grande", 400)


# ---------------------------------------------------------------------------
# Catalogos por tipo de bebida
# ---------------------------------------------------------------------------

# Una sola variante de preparacion (o ninguna)
VARIANTES_POR_TIPO = {
    Bebida.TIPO_CAFE:        {"1": ("Corto",   Corto),
                              "2": ("Largo",   Largo),
                              "3": ("Cortado", Cortado),
                              "4": ("Lagrima", Lagrima)},
    Bebida.TIPO_CAPUCHINO:   {},
    Bebida.TIPO_CHOCOLATADA: {},
    Bebida.TIPO_INFUSION:    {},
    Bebida.TIPO_JUGO:        {},
}

# Sabores combinables (sin Grande, que se pregunta aparte)
SABORES_POR_TIPO = {
    Bebida.TIPO_CAFE:        {"1": ("Leche",          ConLeche),
                              "2": ("Crema",          ConCrema),
                              "3": ("Dulce de leche", ConDulceDeLeche)},
    Bebida.TIPO_CAPUCHINO:   {"1": ("Crema",          ConCrema),
                              "2": ("Dulce de leche", ConDulceDeLeche)},
    Bebida.TIPO_CHOCOLATADA: {"1": ("Crema",          ConCrema),
                              "2": ("Dulce de leche", ConDulceDeLeche)},
    Bebida.TIPO_INFUSION:    {"1": ("Leche",          ConLeche)},
    Bebida.TIPO_JUGO:        {},
}

# Tipos que ofrecen la opcion de tamano grande
ADMITE_GRANDE = {
    Bebida.TIPO_CAFE:        False,   # corto/largo ya definen el tamano
    Bebida.TIPO_CAPUCHINO:   True,
    Bebida.TIPO_CHOCOLATADA: True,
    Bebida.TIPO_INFUSION:    True,
    Bebida.TIPO_JUGO:        True,
}


def catalogo_variantes(bebida):
    # Las bebidas personalizadas no tienen variantes de preparacion
    if getattr(bebida, 'extras_config', None) is not None:
        return {}
    return VARIANTES_POR_TIPO.get(bebida.tipo_bebida, {})

def catalogo_sabores(bebida):
    cfg = getattr(bebida, 'extras_config', None)
    if cfg is not None:
        keys = cfg.get('sabores', [])
        return {str(i + 1): MAPA_SABORES[k]
                for i, k in enumerate(keys) if k in MAPA_SABORES}
    return SABORES_POR_TIPO.get(bebida.tipo_bebida, {})

def admite_grande(bebida):
    cfg = getattr(bebida, 'extras_config', None)
    if cfg is not None:
        return cfg.get('grande', False)
    return ADMITE_GRANDE.get(bebida.tipo_bebida, False)


# ---------------------------------------------------------------------------
# Para TIPO_CAFE: sabores y grande segun la variante elegida
# ---------------------------------------------------------------------------
# - "corto"/"largo" definen tamano → no admiten Grande.
# - "cortado"/"lagrima" ya llevan leche implícita → no ofrecen mas leche,
#   pero sí admiten Grande.
# - None (sin variante) → cafe solo, sin extras adicionales.

SABORES_CAFE_POR_VARIANTE = {
    None:      {},                                                     # cafe solo
    "corto":   {"1": ("Leche",          ConLeche),
                "2": ("Crema",          ConCrema),
                "3": ("Dulce de leche", ConDulceDeLeche)},
    "largo":   {"1": ("Leche",          ConLeche),
                "2": ("Crema",          ConCrema),
                "3": ("Dulce de leche", ConDulceDeLeche)},
    "cortado": {"1": ("Crema",          ConCrema),
                "2": ("Dulce de leche", ConDulceDeLeche)},
    "lagrima": {"1": ("Crema",          ConCrema),
                "2": ("Dulce de leche", ConDulceDeLeche)},
}

GRANDE_CAFE_POR_VARIANTE = {
    None:      False,   # cafe solo
    "corto":   False,   # corto ya define tamano
    "largo":   False,   # largo ya define tamano
    "cortado": True,
    "lagrima": True,
}


def catalogo_sabores_cafe(variante_key):
    """Sabores disponibles para cafe segun la variante de preparacion elegida."""
    return SABORES_CAFE_POR_VARIANTE.get(variante_key, {})

def admite_grande_cafe(variante_key):
    """True si la variante de cafe permite pedir tamano grande."""
    return GRANDE_CAFE_POR_VARIANTE.get(variante_key, False)
# ---------------------------------------------------------------------------
# Mapa de sabores por clave string (para bebidas personalizadas del gerente)
# ---------------------------------------------------------------------------
MAPA_SABORES = {
    "leche": ("Leche",          ConLeche),
    "crema": ("Crema",          ConCrema),
    "ddl":   ("Dulce de leche", ConDulceDeLeche),
}
