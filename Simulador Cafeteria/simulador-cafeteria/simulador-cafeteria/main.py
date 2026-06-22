"""
Simulador de Pedidos de Cafetería - Punto de entrada (consola).

Este archivo SOLO se ocupa de la interfaz de consola y de orquestar las
llamadas a las clases del dominio. No contiene lógica de negocio: esa vive
en los módulos de `modelos/`. Esta separación (interfaz vs. dominio) hace el
código más claro y testeable.

Ejecutar con:  python main.py
"""
from modelos.cafeteria import Cafeteria
from modelos.extra import EXTRAS_DISPONIBLES
from utils.datos_iniciales import cargar_menu_inicial, cargar_mozos_iniciales


def pausar():
    input("\n  (Enter para continuar...)")


def leer_numero(mensaje, entero=False):
    """
    Lee un número positivo desde consola, reintentando si la entrada es
    inválida. (Patrón de validación robusta tomado del aporte del equipo.)
    """
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor) if entero else float(valor)
            if numero <= 0:
                print("  Debe ser un número positivo.")
                continue
            return numero
        except ValueError:
            print("  Entrada inválida. Ingresá un número.")


def mostrar_menu_productos(cafeteria):
    print("\n  --- MENÚ DISPONIBLE ---")
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


def ofrecer_extras(cafeteria, producto, pedido):
    """Si el producto admite extras, permite agregarlos (patrón Decorator)."""
    if not producto.admite_extras():
        return producto
    while True:
        print("\n  ¿Agregar extra? (el patrón Decorator envuelve el producto)")
        for k, (nombre, _) in EXTRAS_DISPONIBLES.items():
            _, clase = EXTRAS_DISPONIBLES[k]
            print(f"   {k}. {nombre}")
        print("   0. Listo, sin más extras")
        op = input("  Opción: ").strip()
        if op == "0":
            break
        if op in EXTRAS_DISPONIBLES:
            _, clase_extra = EXTRAS_DISPONIBLES[op]
            producto = clase_extra(producto)   # se envuelve con el decorador
            print(f"  Ahora: {producto.descripcion()} (${producto.precio:.0f})")
        else:
            print("  Opción inválida.")
    return producto


def tomar_pedido(cafeteria):
    pedido = cafeteria.nuevo_pedido()
    if pedido is None:
        return
    print(f"\n  Nuevo pedido #{pedido.numero} - Mozo: {pedido.mozo_nombre}")
    while True:
        indice = mostrar_menu_productos(cafeteria)
        print("\n   0. Finalizar y emitir ticket")
        sel = input("  Elegí producto (número): ").strip()
        if sel == "0":
            break
        producto_base = indice.get(sel)
        if producto_base is None:
            print("  Opción inválida.")
            continue
        # Primero se verifica stock y se descuenta sobre el producto base.
        # @verificar_stock frena acá si el producto está agotado.
        agregado = cafeteria.agregar_al_pedido(producto_base, pedido)
        if agregado is False:
            continue  # estaba agotado: no se ofrecen extras ni se agrega item
        # Si hay stock, se ofrecen extras (patrón Decorator) y se guarda como item.
        producto_final = ofrecer_extras(cafeteria, producto_base, pedido)
        pedido.agregar_item(producto_final)

    if pedido.esta_vacio():
        print("\n  El pedido quedó vacío, no se emite ticket.")
        return
    pedido.finalizar()
    print("\n" + pedido.ticket())
    print("\n  Pedido finalizado. La venta se sumó al total del día.")


def administrar_menu(cafeteria):
    while True:
        print("\n  --- ADMINISTRAR MENÚ (Gerente) ---")
        print("   1. Ver inventario y valor total")
        print("   2. Modificar precio de un producto")
        print("   3. Reponer stock")
        print("   4. Ver productos agotados")
        print("   0. Volver")
        op = input("  Opción: ").strip()
        if op == "1":
            mostrar_menu_productos(cafeteria)
            print(f"\n  Valor total del inventario: ${cafeteria.valor_inventario():.0f}")
            pausar()
        elif op == "2":
            nombre = input("  Nombre del producto: ").strip()
            nuevo = leer_numero("  Nuevo precio: ")
            cafeteria.modificar_precio(nombre, nuevo)
        elif op == "3":
            nombre = input("  Nombre del producto: ").strip()
            cant = leer_numero("  Cantidad a reponer: ", entero=True)
            cafeteria.reponer_stock(nombre, cant)
        elif op == "4":
            agotados = cafeteria.productos_agotados()
            if not agotados:
                print("  No hay productos agotados.")
            else:
                for p in agotados:
                    print(f"   - {p.nombre}")
            pausar()
        elif op == "0":
            break
        else:
            print("  Opción inválida.")


def ver_cierre(cafeteria):
    total, detalle = cafeteria.cierre_del_dia()
    print("\n  --- CIERRE DEL DÍA ---")
    for nombre, cantidad, vendido in detalle:
        print(f"   {nombre:<10} {cantidad} pedido(s)   ${vendido:>8.0f}")
    print("  " + "-" * 32)
    print(f"   {'TOTAL DEL DÍA':<14}            ${total:>8.0f}")
    pausar()


def sesion_mozo(cafeteria):
    nombre = input("\n  Nombre del mozo (Carlos / María / José): ").strip()
    clave = input("  Clave: ").strip()
    if not cafeteria.login(nombre, clave):
        print("  [!] Nombre o clave incorrectos.")
        return
    print(f"\n  Sesión iniciada: {cafeteria.mozo_actual.nombre}")
    while True:
        print(f"\n  --- MOZO: {cafeteria.mozo_actual.nombre} ---")
        print("   1. Tomar nuevo pedido")
        print("   2. Cerrar sesión")
        op = input("  Opción: ").strip()
        if op == "1":
            tomar_pedido(cafeteria)
        elif op == "2":
            cafeteria.logout()
            print("  Sesión cerrada.")
            break
        else:
            print("  Opción inválida.")


def main():
    cafeteria = Cafeteria("El Rincón del Café")
    cargar_menu_inicial(cafeteria)
    cargar_mozos_iniciales(cafeteria)

    print("=" * 42)
    print(f"   {cafeteria.nombre} - Simulador de Pedidos")
    print("=" * 42)

    while True:
        print("\n  --- MENÚ PRINCIPAL ---")
        print("   1. Ingresar como Mozo")
        print("   2. Administrar menú (Gerente)")
        print("   3. Ver cierre del día (Gerente)")
        print("   0. Salir")
        op = input("  Opción: ").strip()
        if op == "1":
            sesion_mozo(cafeteria)
        elif op == "2":
            administrar_menu(cafeteria)
        elif op == "3":
            ver_cierre(cafeteria)
        elif op == "0":
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  Opción inválida.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Sesión interrumpida. ¡Hasta luego!\n")
