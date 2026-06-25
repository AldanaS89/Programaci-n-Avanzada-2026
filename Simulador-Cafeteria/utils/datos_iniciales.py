"""
Datos iniciales: menu realista, mozos de ejemplo y clave del gerente.
"""
from modelos.producto import Bebida, Comida
from modelos.mozo import Mozo
from utils.categorias import Categoria


def cargar_menu_inicial(cafeteria):
    productos = [
        # --- BEBIDAS ---
        Bebida("Cafe",            1200, stock=50, tipo=Bebida.TIPO_CAFE,
               vegetariano=True),
        Bebida("Capuchino",       1800, stock=25, tipo=Bebida.TIPO_CAPUCHINO,
               vegetariano=True),
        Bebida("Te",              1100, stock=40, tipo=Bebida.TIPO_INFUSION,
               sin_tacc=True, vegetariano=True),
        Bebida("Mate cocido",     1000, stock=30, tipo=Bebida.TIPO_INFUSION,
               sin_tacc=True, vegetariano=True),
        Bebida("Submarino",       2000, stock=20, tipo=Bebida.TIPO_CHOCOLATADA,
               vegetariano=True),
        Bebida("Jugo de naranja", 1600, stock=15, tipo=Bebida.TIPO_JUGO,
               sin_tacc=True, vegetariano=True),

        # --- SALADO ---
        Comida("Tostado de jamon y queso", 2800, Categoria.SALADO, stock=15),
        Comida("Medialuna de grasa",        700, Categoria.SALADO, stock=40),
        Comida("Fosforitos",                900, Categoria.SALADO, stock=30),
        Comida("Sandwich de miga",         2200, Categoria.SALADO, stock=10,
               vegetariano=True),

        # --- DULCE ---
        Comida("Medialuna de manteca",  800, Categoria.DULCE, stock=40,
               vegetariano=True),
        Comida("Factura rellena",      1000, Categoria.DULCE, stock=25,
               vegetariano=True),
        Comida("Alfajor de maicena",   1200, Categoria.DULCE, stock=20,
               sin_tacc=True, vegetariano=True),
        Comida("Budin de limon",       1400, Categoria.DULCE, stock=12,
               vegetariano=True),
    ]
    for p in productos:
        cafeteria.cargar_producto(p)


def cargar_mozos_iniciales(cafeteria):
    clave_comun = "1234"
    for nombre in ("Carlos", "Maria", "Jose"):
        cafeteria.registrar_mozo(Mozo(nombre, clave_comun))


def registrar_gerente(cafeteria):
    cafeteria.registrar_gerente("gerente1234")
