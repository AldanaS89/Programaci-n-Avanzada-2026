"""
Cafetería: clase central que coordina el sistema (rol del Gerente).

Demuestra:
- AGREGACIÓN: la Cafetería agrupa Mozos y administra el Menú (colección de
  Productos). Mozos y productos existen como entidades propias.
- ENCAPSULAMIENTO: el alta de pedidos pasa por la verificación de stock
  (decorador de función @verificar_stock).

Responsabilidades:
- Administrar el menú: cargar productos, modificar precios, reponer stock.
- Login de mozos.
- Agregar productos a un pedido descontando stock (con @verificar_stock).
- Consolidar el cierre del día (ventas de todos los mozos).
"""
from utils.categorias import Categoria
from modelos.pedido import Pedido
from decoradores.validaciones import verificar_stock, requiere_login


class Cafeteria:
    def __init__(self, nombre):
        self.nombre = nombre
        self._menu = []                  # lista de Producto
        self._mozos = {}                 # nombre -> Mozo
        self.mozo_actual = None          # mozo logueado (para @requiere_login)
        self._contador_pedidos = 0

    # ---------- Administración del menú (Gerente) ----------

    def cargar_producto(self, producto):
        self._menu.append(producto)

    def modificar_precio(self, nombre_producto, nuevo_precio):
        if nuevo_precio <= 0:
            print("  [!] El precio debe ser mayor que cero.")
            return
        producto = self.buscar_producto(nombre_producto)
        if producto:
            producto._precio = nuevo_precio
            print(f"  Precio de '{producto.nombre}' actualizado a ${nuevo_precio:.0f}.")

    def reponer_stock(self, nombre_producto, cantidad):
        if cantidad <= 0:
            print("  [!] La cantidad a reponer debe ser positiva.")
            return
        producto = self.buscar_producto(nombre_producto)
        if producto:
            producto.reponer_stock(cantidad)
            print(f"  Stock de '{producto.nombre}' repuesto. Ahora: {producto.stock}.")

    def buscar_producto(self, nombre):
        for p in self._menu:
            if p.nombre.lower() == nombre.lower():
                return p
        print(f"  [!] Producto '{nombre}' no encontrado.")
        return None

    def menu_por_categoria(self):
        """Devuelve un diccionario {Categoria: [productos]} para listar."""
        agrupado = {cat: [] for cat in Categoria}
        for p in self._menu:
            agrupado[p.categoria].append(p)
        return agrupado

    @property
    def menu(self):
        return list(self._menu)

    def valor_inventario(self):
        """Reporte simple: suma de precio * stock de todo el menú."""
        return round(sum(p.precio * p.stock for p in self._menu), 2)

    def productos_agotados(self):
        return [p for p in self._menu if p.stock <= 0]

    # ---------- Login de mozos ----------

    def registrar_mozo(self, mozo):
        self._mozos[mozo.nombre.lower()] = mozo

    def login(self, nombre, clave):
        mozo = self._mozos.get(nombre.lower())
        if mozo and mozo.verificar_clave(clave):
            self.mozo_actual = mozo
            return True
        return False

    def logout(self):
        self.mozo_actual = None

    # ---------- Operación de pedidos (Mozo) ----------

    @requiere_login
    def nuevo_pedido(self):
        self._contador_pedidos += 1
        pedido = Pedido(self._contador_pedidos, self.mozo_actual.nombre)
        self.mozo_actual.registrar_pedido(pedido)
        return pedido

    @verificar_stock
    def agregar_al_pedido(self, producto, pedido):
        """
        Verifica stock y lo descuenta para un producto del pedido.

        El decorador @verificar_stock se ejecuta ANTES: si el producto está
        agotado, devuelve False y este cuerpo no corre. Si hay stock, descuenta
        una unidad y devuelve True. El item concreto (ya decorado con extras)
        lo agrega quien llama, para no perder los extras.
        """
        producto.descontar_stock(1)
        return True

    # ---------- Cierre del día (Gerente) ----------

    def cierre_del_dia(self):
        """Consolida las ventas finalizadas de todos los mozos."""
        total = 0
        detalle = []
        for mozo in self._mozos.values():
            vendido = mozo.total_vendido()
            cantidad = len(mozo.pedidos_finalizados())
            total += vendido
            detalle.append((mozo.nombre, cantidad, vendido))
        return total, detalle
