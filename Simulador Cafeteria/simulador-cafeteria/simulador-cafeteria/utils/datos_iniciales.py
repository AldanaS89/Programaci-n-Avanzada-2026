"""
Datos iniciales para que el sistema arranque con un menú realista y
mozos cargados (útil para la demostración).

Precios de referencia en pesos argentinos (cafetería, mediados de 2026).
Las banderas sin_tacc / vegetariano se marcan donde corresponde.
"""
from modelos.producto import Bebida, Comida
from modelos.mozo import Mozo
from utils.categorias import Categoria


def cargar_menu_inicial(cafeteria):
    productos = [
        # --- BEBIDAS (admiten extras) ---
        Bebida("Café", 1200, stock=30, vegetariano=True),
        Bebida("Café con leche", 1500, stock=25, vegetariano=True),
        Bebida("Capuchino", 1800, stock=20, vegetariano=True),
        Bebida("Submarino", 2000, stock=15, vegetariano=True),
        Bebida("Té", 1100, stock=20, sin_tacc=True, vegetariano=True),
        Bebida("Mate cocido", 1000, stock=18, sin_tacc=True, vegetariano=True),
        Bebida("Jugo de naranja", 1600, stock=12, sin_tacc=True, vegetariano=True),

        # --- SALADO ---
        Comida("Tostado de jamón y queso", 2800, Categoria.SALADO, stock=15),
        Comida("Medialuna de grasa", 700, Categoria.SALADO, stock=40),
        Comida("Fosforitos", 900, Categoria.SALADO, stock=30),
        Comida("Sándwich de miga", 2200, Categoria.SALADO, stock=10,
               vegetariano=True),

        # --- DULCE ---
        Comida("Medialuna de manteca", 800, Categoria.DULCE, stock=40,
               vegetariano=True),
        Comida("Factura rellena", 1000, Categoria.DULCE, stock=25,
               vegetariano=True),
        Comida("Alfajor de maicena", 1200, Categoria.DULCE, stock=20,
               sin_tacc=True, vegetariano=True),
        Comida("Budín de limón", 1400, Categoria.DULCE, stock=12,
               vegetariano=True),
    ]
    for p in productos:
        cafeteria.cargar_producto(p)


def cargar_mozos_iniciales(cafeteria):
    # Clave común y simple para todos los empleados (decisión del local).
    clave_comun = "1234"
    for nombre in ("Carlos", "María", "José"):
        cafeteria.registrar_mozo(Mozo(nombre, clave_comun))
