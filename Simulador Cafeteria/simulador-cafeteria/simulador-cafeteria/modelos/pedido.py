"""
Pedido: representa la cuenta de una mesa/cliente que atiende un mozo.

Demuestra:
- ENCAPSULAMIENTO: el total y la propina se calculan mediante métodos; el
  estado se cambia con métodos, no "a mano".
- POLIMORFISMO: recorre sus items llamando precio/descripcion sin importar si
  son productos simples o productos decorados con extras.
- COMPOSICIÓN: un Pedido se compone de líneas (items).
"""

PROPINA_PORCENTAJE = 0.10   # 10% configurable en un solo lugar


class Pedido:
    ABIERTO = "abierto"
    FINALIZADO = "finalizado"

    def __init__(self, numero, mozo_nombre):
        self.numero = numero
        self.mozo_nombre = mozo_nombre
        self._items = []                 # lista de Producto (simples o decorados)
        self._estado = Pedido.ABIERTO

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return list(self._items)         # copia: no se modifica desde afuera

    def agregar_item(self, producto):
        self._items.append(producto)

    def subtotal(self):
        """Suma de los precios de todos los items (polimorfismo)."""
        return sum(item.precio for item in self._items)

    def propina(self):
        return round(self.subtotal() * PROPINA_PORCENTAJE, 2)

    def total(self):
        return round(self.subtotal() + self.propina(), 2)

    def finalizar(self):
        self._estado = Pedido.FINALIZADO

    def esta_vacio(self):
        return len(self._items) == 0

    def ticket(self):
        """Devuelve el texto del ticket para imprimir por consola."""
        lineas = []
        lineas.append("=" * 38)
        lineas.append(f"  PEDIDO #{self.numero}  -  Mozo: {self.mozo_nombre}")
        lineas.append("=" * 38)
        for item in self._items:
            lineas.append(f"  {item.descripcion():<28} ${item.precio:>6.0f}")
        lineas.append("-" * 38)
        lineas.append(f"  {'Subtotal':<28} ${self.subtotal():>6.0f}")
        lineas.append(f"  {'Propina (10%)':<28} ${self.propina():>6.0f}")
        lineas.append(f"  {'TOTAL':<28} ${self.total():>6.0f}")
        lineas.append("=" * 38)
        return "\n".join(lineas)
