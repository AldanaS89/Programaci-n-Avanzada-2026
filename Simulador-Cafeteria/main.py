"""
Simulador de Pedidos de Cafeteria - Punto de entrada (consola).
Solo interfaz: no contiene logica de negocio (esa vive en modelos/).
Ejecutar:  python main.py  (desde la carpeta raiz del proyecto)
"""
from modelos.cafeteria import Cafeteria
from modelos.producto import Bebida, Comida
from modelos.extra import (catalogo_variantes, catalogo_sabores, admite_grande, Grande,
                           catalogo_sabores_cafe, admite_grande_cafe)
from modelos.excepciones import CafeteriaError
from utils.categorias import Categoria
from utils.datos_iniciales import cargar_menu_inicial, cargar_mozos_iniciales, registrar_gerente
from utils.persistencia import guardar_menu, cargar_menu


def pausar():
    input("\n  (Enter para continuar...)")


def leer_numero(mensaje, entero=False):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor) if entero else float(valor)
            if numero <= 0:
                print("  Debe ser un numero positivo.")
                continue
            return numero
        except ValueError:
            print("  Entrada invalida. Ingresa un numero.")


def mostrar_menu_productos(cafeteria):
    print("\n  --- MENU DISPONIBLE ---")
    agrupado = cafeteria.menu_por_categoria()
    indice = {}
    n = 1
    for categoria, productos in agrupado.items():
        if not productos:
            continue
        print(f"\n  {str(categoria).upper()}")
        for p in productos:
            disp = f"stock: {p.stock}" if p.stock > 0 else "AGOTADO"
            print(f"   {n:>2}. {p.nombre:<28} ${p.precio:>6.0f}  ({disp}){p._etiquetas()}")
            indice[str(n)] = p
            n += 1
    return indice


def _seleccionar_variante(producto, catalogo):
    """Elige UNA sola variante de preparacion (o ninguna) y sale inmediatamente.
    Devuelve (producto, variante_key) donde variante_key es None si no se eligio ninguna."""
    if not catalogo:
        return producto, None
    print("\n  Como se prepara? (elegir UNA o 0 para ninguna)")
    for k, (nombre, _) in catalogo.items():
        print(f"   {k}. {nombre}")
    print("   0. Sin variante")
    while True:
        op = input("  Opcion: ").strip()
        if op == "0":
            return producto, None
        if op in catalogo:
            nombre, clase = catalogo[op]
            variante_key = nombre.lower()   # "corto", "largo", "cortado", "lagrima"
            producto = clase(producto)
            print(f"  Elegido: {producto.descripcion()} (${producto.precio:.0f})")
            return producto, variante_key
        print("  Opcion invalida.")


def _agregar_sabores(producto, catalogo):
    """Permite combinar varios sabores (leche, crema, ddl). Loop hasta elegir 0."""
    if not catalogo:
        return producto
    while True:
        print("\n  Agregar sabor? (puede combinar varios, 0 para terminar)")
        for k, (nombre, _) in catalogo.items():
            print(f"   {k}. {nombre}")
        print("   0. Listo")
        op = input("  Opcion: ").strip()
        if op == "0":
            break
        if op in catalogo:
            _, clase = catalogo[op]
            producto = clase(producto)
            print(f"  Ahora: {producto.descripcion()} (${producto.precio:.0f})")
        else:
            print("  Opcion invalida.")
    return producto


def _preguntar_grande(producto):
    """Pregunta si se quiere tamano grande (una sola vez, si/no)."""
    op = input("  Tamano grande? (+$400) [s/n]: ").strip().lower()
    if op == "s":
        producto = Grande(producto)
        print(f"  Ahora: {producto.descripcion()} (${producto.precio:.0f})")
    return producto


def ofrecer_extras(producto_base):
    """Flujo de personalizacion de bebida:
    1. Una variante de preparacion (si aplica al tipo)
    2. Sabores combinables (dependen de la variante, para cafe)
    3. Tamano grande (depende de la variante, para cafe)

    Para TIPO_CAFE los sabores disponibles y la opcion Grande cambian
    segun la variante elegida:
      - Sin variante     → cafe solo, sin extras adicionales
      - Corto / Largo    → leche, crema, ddl; sin Grande (tamano ya definido)
      - Cortado / Lagrima → crema, ddl (la leche va incluida); si admiten Grande
    """
    if not producto_base.admite_extras():
        return producto_base
    variantes = catalogo_variantes(producto_base)
    producto, variante_key = _seleccionar_variante(producto_base, variantes)

    if producto_base.tipo_bebida == Bebida.TIPO_CAFE:
        sabores   = catalogo_sabores_cafe(variante_key)
        es_grande = admite_grande_cafe(variante_key)
    else:
        sabores   = catalogo_sabores(producto_base)
        es_grande = admite_grande(producto_base)

    producto = _agregar_sabores(producto, sabores)
    if es_grande:
        producto = _preguntar_grande(producto)
    return producto


def mostrar_items_pedido(pedido):
    items = pedido.items
    if not items:
        return
    print("\n  Items en el pedido:")
    for i, linea in enumerate(items, 1):
        print(f"   {i}. {linea.descripcion_linea():<32} ${linea.subtotal_linea():>6.0f}")
    print(f"  {'-' * 42}")
    print(f"   Subtotal actual: ${pedido.subtotal():.0f}")


def eliminar_item_pedido(cafeteria, pedido):
    items = pedido.items
    if not items:
        print("  El pedido esta vacio, no hay nada que quitar.")
        return
    mostrar_items_pedido(pedido)
    op = input("  Numero de item a quitar (0 para cancelar): ").strip()
    if op == "0":
        return
    try:
        idx = int(op) - 1
        if idx < 0 or idx >= len(items):
            print("  Numero invalido.")
            return
        linea = pedido.eliminar_item(idx)
        linea.producto_base.reponer_stock(linea.cantidad)
        print(f"  '{linea.descripcion_linea()}' quitado del pedido.")
    except (ValueError, IndexError):
        print("  Entrada invalida.")


def tomar_pedido(cafeteria):
    pedido = cafeteria.nuevo_pedido()
    if pedido is None:
        return
    print(f"\n  Nuevo pedido #{pedido.numero} - Mozo: {pedido.mozo_nombre}")
    while True:
        mostrar_items_pedido(pedido)
        indice = mostrar_menu_productos(cafeteria)
        print("\n   Q. Quitar un item del pedido")
        print("   0. Finalizar y emitir ticket")
        sel = input("  Elegi producto (numero): ").strip().upper()

        if sel == "0":
            break
        if sel == "Q":
            eliminar_item_pedido(cafeteria, pedido)
            continue

        producto_base = indice.get(sel)
        if producto_base is None:
            print("  Opcion invalida.")
            continue

        cant_str = input("  Cuantas unidades? [1]: ").strip()
        cantidad = 1
        if cant_str:
            try:
                cantidad = int(cant_str)
                if cantidad <= 0:
                    print("  La cantidad debe ser positiva.")
                    continue
            except ValueError:
                print("  Entrada invalida.")
                continue

        ok = cafeteria.agregar_al_pedido(producto_base, pedido, cantidad=cantidad)
        if ok is False:
            continue

        producto_final = ofrecer_extras(producto_base)
        pedido.agregar_item(producto_final, producto_base, cantidad)

    if pedido.esta_vacio():
        print("\n  El pedido quedo vacio, no se emite ticket.")
        return
    pedido.finalizar()
    print("\n" + pedido.ticket())
    guardar_menu(cafeteria)
    print("\n  Pedido finalizado. La venta se sumo al total del dia.")


# ---------- Seccion Gerente ----------

def sesion_gerente(cafeteria):
    clave = input("\n  Clave del gerente: ").strip()
    if not cafeteria.verificar_gerente(clave):
        print("  [!] Clave incorrecta.")
        return
    print("  Acceso concedido.")
    while True:
        print("\n  --- GERENTE ---")
        print("   1. Administrar menu")
        print("   2. Ver cierre del dia")
        print("   0. Volver")
        op = input("  Opcion: ").strip()
        if op == "1":
            administrar_menu(cafeteria)
        elif op == "2":
            ver_cierre(cafeteria)
        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


def administrar_menu(cafeteria):
    while True:
        print("\n  --- ADMINISTRAR MENU (Gerente) ---")
        print("   1. Ver inventario y valor total")
        print("   2. Modificar precio de un producto")
        print("   3. Reponer stock")
        print("   4. Ver productos agotados")
        print("   5. Cargar producto nuevo")
        print("   6. Dar de baja un producto")
        print("   0. Volver")
        op = input("  Opcion: ").strip()
        try:
            if op == "1":
                mostrar_menu_productos(cafeteria)
                print(f"\n  Valor total del inventario: ${cafeteria.valor_inventario():.0f}")
                pausar()
            elif op == "2":
                modificar_precio_por_numero(cafeteria)
            elif op == "3":
                reponer_stock_por_numero(cafeteria)
            elif op == "4":
                agotados = cafeteria.productos_agotados()
                if not agotados:
                    print("  No hay productos agotados.")
                else:
                    for p in agotados:
                        print(f"   - {p.nombre}")
                pausar()
            elif op == "5":
                cargar_producto_nuevo(cafeteria)
                guardar_menu(cafeteria)
            elif op == "6":
                dar_de_baja_producto(cafeteria)
            elif op == "0":
                break
            else:
                print("  Opcion invalida.")
        except CafeteriaError as e:
            print(f"  [!] {e}")


def _configurar_extras_bebida():
    """Pregunta al gerente que extras tendra la nueva bebida.
    Devuelve None si tiene variantes cafe, o extras_config dict si es bebida nueva."""
    print("\n  ¿Tiene variantes de preparacion (corto / largo / cortado / lagrima)? [s/n]")
    if input("  ").strip().lower() == "s":
        # Se comporta como cafe: usa el sistema de variantes ya definido
        return None

    # Bebida nueva: preguntar cada sabor individualmente
    sabores = []
    print("\n  Sabores disponibles:")
    if input("  ¿Admite leche? [s/n]: ").strip().lower() == "s":
        sabores.append("leche")
    if input("  ¿Admite crema? [s/n]: ").strip().lower() == "s":
        sabores.append("crema")
    if input("  ¿Admite dulce de leche? [s/n]: ").strip().lower() == "s":
        sabores.append("ddl")
    grande = input("  ¿Admite tamano grande? (+$400) [s/n]: ").strip().lower() == "s"

    return {"tiene_variantes": False, "sabores": sabores, "grande": grande}


def cargar_producto_nuevo(cafeteria):
    nombre = input("  Nombre del nuevo producto: ").strip()
    if not nombre:
        print("  El nombre no puede estar vacio.")
        return
    print("  Categoria:  1. Bebida   2. Salado   3. Dulce")
    cat_op = input("  Opcion: ").strip()
    mapa = {"1": Categoria.BEBIDA, "2": Categoria.SALADO, "3": Categoria.DULCE}
    if cat_op not in mapa:
        print("  Categoria invalida.")
        return
    categoria = mapa[cat_op]
    precio       = leer_numero("  Precio: ")
    stock        = leer_numero("  Stock inicial: ", entero=True)
    sin_tacc     = input("  ¿Es sin TACC? [s/n]: ").strip().lower() == "s"
    vegetariano  = input("  ¿Es vegetariano? [s/n]: ").strip().lower() == "s"

    if categoria == Categoria.BEBIDA:
        extras_config = _configurar_extras_bebida()
        if extras_config is None:
            # Con variantes → TIPO_CAFE
            tipo = Bebida.TIPO_CAFE
        else:
            tipo = Bebida.TIPO_PERSONALIZADO
        producto = Bebida(nombre, precio, stock=int(stock), tipo=tipo,
                          sin_tacc=sin_tacc, vegetariano=vegetariano,
                          extras_config=extras_config)
    else:
        producto = Comida(nombre, precio, categoria, stock=int(stock),
                          sin_tacc=sin_tacc, vegetariano=vegetariano)

    cafeteria.cargar_producto(producto)
    print(f"  Producto '{nombre}' agregado al menu.")


def modificar_precio_por_numero(cafeteria):
    """El gerente ve el menu numerado y elige el producto cuyo precio modificar."""
    indice = mostrar_menu_productos(cafeteria)
    print("\n   0. Cancelar")
    sel = input("  Numero del producto a modificar: ").strip()
    if sel == "0" or not sel:
        print("  Operacion cancelada.")
        return
    producto = indice.get(sel)
    if producto is None:
        print("  Numero invalido.")
        return
    print(f"  Precio actual de '{producto.nombre}': ${producto.precio:.0f}")
    nuevo = leer_numero("  Nuevo precio: ")
    try:
        cafeteria.modificar_precio(producto.nombre, nuevo)
        guardar_menu(cafeteria)
        print(f"  Precio actualizado a ${nuevo:.0f}.")
    except CafeteriaError as e:
        print(f"  [!] {e}")


def reponer_stock_por_numero(cafeteria):
    """El gerente ve el menu numerado y elige el producto a reponer por numero."""
    indice = mostrar_menu_productos(cafeteria)
    print("\n   0. Cancelar")
    sel = input("  Numero del producto a reponer: ").strip()
    if sel == "0" or not sel:
        print("  Operacion cancelada.")
        return
    producto = indice.get(sel)
    if producto is None:
        print("  Numero invalido.")
        return
    cant = leer_numero("  Cantidad a reponer: ", entero=True)
    try:
        cafeteria.reponer_stock(producto.nombre, int(cant))
        guardar_menu(cafeteria)
    except CafeteriaError as e:
        print(f"  [!] {e}")


def dar_de_baja_producto(cafeteria):
    """Permite al gerente eliminar un producto eligiendo por numero."""
    indice = mostrar_menu_productos(cafeteria)
    print("\n   0. Cancelar")
    sel = input("  Numero del producto a dar de baja: ").strip()
    if sel == "0" or not sel:
        print("  Operacion cancelada.")
        return
    producto = indice.get(sel)
    if producto is None:
        print("  Numero invalido.")
        return
    confirmacion = input(f"  Confirmar baja de '{producto.nombre}'? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("  Baja cancelada.")
        return
    try:
        cafeteria.eliminar_producto(producto.nombre)
        guardar_menu(cafeteria)
        print(f"  '{producto.nombre}' eliminado del menu.")
    except CafeteriaError as e:
        print(f"  [!] {e}")


def ver_cierre(cafeteria):
    total, detalle = cafeteria.cierre_del_dia()
    print("\n  --- CIERRE DEL DIA ---")
    for nombre, cantidad, vendido in detalle:
        print(f"   {nombre:<10} {cantidad} pedido(s)   ${vendido:>8.0f}")
    print("  " + "-" * 32)
    print(f"   {'TOTAL DEL DIA':<14}            ${total:>8.0f}")
    pausar()


def sesion_mozo(cafeteria):
    nombre = input("\n  Nombre del mozo (Carlos / Maria / Jose): ").strip()
    clave  = input("  Clave: ").strip()
    if not cafeteria.login(nombre, clave):
        print("  [!] Nombre o clave incorrectos.")
        return
    while True:
        print(f"\n  --- MOZO: {cafeteria.mozo_actual.nombre} ---")
        print("   1. Tomar nuevo pedido")
        print("   2. Cerrar sesion")
        op = input("  Opcion: ").strip()
        if op == "1":
            tomar_pedido(cafeteria)
        elif op == "2":
            cafeteria.logout()
            print("  Sesion cerrada.")
            break
        else:
            print("  Opcion invalida.")


def main():
    cafeteria = Cafeteria("El Rincon del Cafe")
    cargar_mozos_iniciales(cafeteria)
    registrar_gerente(cafeteria)

    if not cargar_menu(cafeteria):
        cargar_menu_inicial(cafeteria)

    print("=" * 42)
    print(f"   {cafeteria.nombre} - Simulador de Pedidos")
    print("=" * 42)

    while True:
        print("\n  --- MENU PRINCIPAL ---")
        print("   1. Ingresar como Mozo")
        print("   2. Ingresar como Gerente")
        print("   0. Salir")
        op = input("  Opcion: ").strip()
        if op == "1":
            sesion_mozo(cafeteria)
        elif op == "2":
            sesion_gerente(cafeteria)
        elif op == "0":
            print("\n  Hasta luego!\n")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Sesion interrumpida. Hasta luego!\n")
