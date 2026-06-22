"""
Decoradores de función propios.

IMPORTANTE (para la defensa del TPI):
Estos son DECORADORES DE FUNCIÓN de Python (la sintaxis @), una herramienta
del lenguaje. NO confundir con el patrón de diseño Decorator (GoF), que está
implementado con clases en modelos/extra.py.

Un decorador de función envuelve a otra función para agregarle un
comportamiento "alrededor" (validar, controlar acceso, loguear) sin modificar
el cuerpo de la función original.
"""
from functools import wraps


def verificar_stock(funcion):
    """
    Envuelve la acción de agregar un producto a un pedido.

    Antes de ejecutar, comprueba que el producto tenga stock disponible.
    Si no hay stock, avisa y NO ejecuta la función decorada (frena la venta).
    Regla de negocio: "no se puede vender lo que no hay".

    Se asume que la función decorada recibe un `producto` como primer
    argumento posicional (después de self).
    """
    @wraps(funcion)
    def envoltura(self, producto, *args, **kwargs):
        if producto.stock <= 0:
            print(f"  [!] Sin stock: '{producto.nombre}' no está disponible.")
            return False
        return funcion(self, producto, *args, **kwargs)
    return envoltura


def requiere_login(funcion):
    """
    Envuelve acciones que solo puede hacer un mozo con sesión iniciada.

    Si no hay un mozo logueado (self.mozo_actual is None), frena la acción.
    Demuestra el uso de un decorador para control de acceso.
    """
    @wraps(funcion)
    def envoltura(self, *args, **kwargs):
        if getattr(self, "mozo_actual", None) is None:
            print("  [!] Necesitás iniciar sesión para realizar esta acción.")
            return None
        return funcion(self, *args, **kwargs)
    return envoltura
