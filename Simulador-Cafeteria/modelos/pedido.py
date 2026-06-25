"""
Pedido: representa la cuenta de una mesa/cliente que atiende un mozo.

Demuestra:
- ENCAPSULAMIENTO: el total y la propina se calculan mediante métodos; el
  estado se cambia con métodos, no "a mano".
- POLIMORFISMO: recorre sus items llamando precio/descripcion sin importar si
  son productos simples o productos decorados con extras.
- COMPOSICION: un Pedido se compone de lineas (LineaPedido).

Cada linea almacena:
  - producto_final: el producto tal como se pidio (puede tener decoradores).
  - producto_base:  el producto original del menu (usado para restock si se
                    elimina la linea antes de finalizar).
  - cantidad:       unidades pedidas de ese item.
"""
from datetime import datetime

PROPINA_PORCENTAJE = 0.10   # 10% configurable en un solo lugar


class LineaPedido:
    """Representa un renglon del pedido: que se pidio, en que presentacion
    y cuantas unidades."""

    def __init__(self, producto_final, producto_base, cantidad=1):
        self.producto_final = producto_final   # puede ser un Extra (decorado)
        self.producto_base  = producto_base    # Producto original del menu
        self.cantidad       = cantidad

    def subtotal_linea(self):
        return self.producto_final.precio * self.cantidad

    def descripcion_linea(self):
        desc = self.producto_final.descripcion()
        if self.cantidad > 1:
            desc = f"{desc} x{self.cantidad}"
        return desc


class Pedido:
    ABIERTO    = "abierto"
    FINALIZADO = "finalizado"

    def __init__(self, numero, mozo_nombre):
        self.numero      = numero
        self.mozo_nombre = mozo_nombre
        self._items      = []                  # lista de LineaPedido
        self._estado     = Pedido.ABIERTO
        self.fecha_hora  = datetime.now()      # timestamp al crear el pedido

    # ---------- Propiedades ----------

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return list(self._items)   # copia: no se modifica desde afuera

    # ---------- Gestion de items ----------

    def agregar_item(self, producto_final, producto_base, cantidad=1):
        """Agrega una linea al pedido."""
        self._items.append(LineaPedido(producto_final, producto_base, cantidad))

    def eliminar_item(self, indice):
        """Elimina la linea en 'indice' y la devuelve para que el caller
        pueda reponer stock si corresponde."""
        return self._items.pop(indice)

    # ---------- Calculos ----------

    def subtotal(self):
        """Suma de los precios de todas las lineas (polimorfismo)."""
        return sum(linea.subtotal_linea() for linea in self._items)

    def propina(self):
        return round(self.subtotal() * PROPINA_PORCENTAJE, 2)

    def total(self):
        return round(self.subtotal() + self.propina(), 2)

    # ---------- Estado ----------

    def finalizar(self):
        self._estado = Pedido.FINALIZADO

    def esta_vacio(self):
        return len(self._items) == 0

    # ---------- Ticket ----------

    def ticket(self):
        """Devuelve el texto del ticket para imprimir por consola."""
        fecha_str = self.fecha_hora.strftime("%d/%m/%Y  %H:%M")
        lineas = []
        lineas.append("=" * 42)
        lineas.append(f"  PEDIDO #{self.numero:<4}  Mozo: {self.mozo_nombre}")
        lineas.append(f"  Fecha: {fecha_str}")
        lineas.append("=" * 42)
        for linea in self._items:
            desc  = linea.descripcion_linea()
            monto = linea.subtotal_linea()
            lineas.append(f"  {desc:<32} ${monto:>6.0f}")
        lineas.append("-" * 42)
        lineas.append(f"  {'Subtotal':<32} ${self.subtotal():>6.0f}")
        lineas.append(f"  {'Propina (10%)':<32} ${self.propina():>6.0f}")
        lineas.append(f"  {'TOTAL':<32} ${self.total():>6.0f}")
        lineas.append("=" * 42)
        return "\n".join(lineas)
