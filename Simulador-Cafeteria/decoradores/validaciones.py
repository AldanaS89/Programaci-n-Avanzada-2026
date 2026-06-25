"""
Decoradores de funcion propios.

IMPORTANTE (para la defensa del TPI):
Estos son DECORADORES DE FUNCION de Python (la sintaxis @), una herramienta
del lenguaje. NO confundir con el patron de diseno Decorator (GoF), que esta
implementado con clases en modelos/extra.py.

Un decorador de funcion envuelve a otra funcion para agregarle un
comportamiento "alrededor" (validar, controlar acceso, loguear) sin modificar
el cuerpo de la funcion original.
"""
from functools import wraps


def verificar_stock(funcion):
    """
    Envuelve la accion de agregar un producto a un pedido.

    Antes de ejecutar, comprueba que haya stock suficiente para la cantidad
    solicitada (kwarg 'cantidad', por defecto 1).
    Si no alcanza, avisa y NO ejecuta la funcion decorada (frena la venta).
    Regla de negocio: no se puede vender lo que no hay.

    Se asume que la funcion decorada recibe un producto como primer
    argumento posicional (despues de self).
    """
    @wraps(funcion)
    def envoltura(self, producto, *args, **kwargs):
        cantidad = kwargs.get("cantidad", 1)
        if producto.stock <= 0:
            print(f"  [!] Sin stock: '{producto.nombre}' no esta disponible.")
            return False
        if producto.stock < cantidad:
            print(
                f"  [!] Stock insuficiente: '{producto.nombre}' "
                f"(pedido: {cantidad}, disponible: {producto.stock})."
            )
            return False
        return funcion(self, producto, *args, **kwargs)
    return envoltura


def requiere_login(funcion):
    """
    Envuelve acciones que solo puede hacer un mozo con sesion iniciada.

    Si no hay un mozo logueado (self.mozo_actual is None), frena la accion.
    Demuestra el uso de un decorador para control de acceso.
    """
    @wraps(funcion)
    def envoltura(self, *args, **kwargs):
        if getattr(self, "mozo_actual", None) is None:
            print("  [!] Necesitas iniciar sesion para realizar esta accion.")
            return None
        return funcion(self, *args, **kwargs)
    return envoltura
