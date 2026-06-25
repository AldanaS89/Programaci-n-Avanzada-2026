"""
Persistencia del estado de la cafeteria entre sesiones.

Guarda y carga el menu completo (precios y stock) en un archivo JSON local.
Esto permite que el stock se mantenga entre ejecuciones del programa y que
los cambios del gerente (precios, altas, bajas) persistan.

El archivo se actualiza automaticamente despues de cada pedido finalizado
y despues de cada operacion del gerente sobre el menu.
"""
import json
import os
from modelos.producto import Bebida, Comida
from utils.categorias import Categoria

ARCHIVO_ESTADO = "estado_cafeteria.json"
_CAT_MAP = {c.value: c for c in Categoria}


def guardar_menu(cafeteria):
    """Serializa el menu completo a JSON."""
    datos = []
    for p in cafeteria.menu:
        item = {
            "nombre":      p.nombre,
            "precio":      p.precio,
            "stock":       p.stock,
            "categoria":   p.categoria.value,
            "sin_tacc":    p.sin_tacc,
            "vegetariano": p.vegetariano,
        }
        if hasattr(p, "tipo_bebida"):
            item["tipo_bebida"] = p.tipo_bebida
        if hasattr(p, "extras_config") and p.extras_config is not None:
            item["extras_config"] = p.extras_config
        datos.append(item)

    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump({"menu": datos}, f, ensure_ascii=False, indent=2)


def cargar_menu(cafeteria):
    """
    Restaura el menu desde el archivo guardado.
    Devuelve True si se cargaron datos, False si no habia archivo.
    """
    if not os.path.exists(ARCHIVO_ESTADO):
        return False

    with open(ARCHIVO_ESTADO, encoding="utf-8") as f:
        datos = json.load(f)

    for item in datos.get("menu", []):
        cat = _CAT_MAP.get(item.get("categoria"))
        if cat is None:
            continue
        nombre      = item["nombre"]
        precio      = item["precio"]
        stock       = item["stock"]
        sin_tacc    = item.get("sin_tacc", False)
        vegetariano = item.get("vegetariano", False)

        if "tipo_bebida" in item:
            p = Bebida(nombre, precio, stock=stock, tipo=item["tipo_bebida"],
                       sin_tacc=sin_tacc, vegetariano=vegetariano,
                       extras_config=item.get("extras_config"))
        else:
            p = Comida(nombre, precio, cat, stock=stock,
                       sin_tacc=sin_tacc, vegetariano=vegetariano)

        try:
            cafeteria.cargar_producto(p)
        except Exception:
            pass  # duplicado: ignorar silenciosamente

    return True
