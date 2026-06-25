"""
Excepciones personalizadas del sistema.

Crear excepciones propias (en lugar de usar siempre ValueError genérico) hace
que los errores sean más claros: el nombre de la excepción ya dice qué pasó.
Es un elemento opcional valorado por el TPI.

Todas heredan de CafeteriaError, así quien quiera puede atrapar "cualquier
error del sistema" con un solo except, o uno específico si le interesa el caso.
"""


class CafeteriaError(Exception):
    """Excepción base de todo el sistema de cafetería."""
    pass


class ProductoDuplicadoError(CafeteriaError):
    """Se intenta cargar un producto que ya existe (mismo nombre y categoría)."""
    pass


class ProductoNoEncontradoError(CafeteriaError):
    """Se busca un producto que no está en el menú."""
    pass


class PrecioInvalidoError(CafeteriaError):
    """Se intenta asignar un precio que no es positivo."""
    pass


class SinStockError(CafeteriaError):
    """Se intenta vender un producto sin stock disponible."""
    pass

class CantidadInvalidaError(CafeteriaError):
    """Se intenta usar una cantidad que no es un entero positivo."""
    pass
