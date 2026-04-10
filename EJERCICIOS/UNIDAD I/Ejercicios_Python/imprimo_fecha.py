from datetime import datetime

def imprimo_fecha(dia, mes, año):
    print(f"Hoy es {dia} de {mes} del {año}")

hoy = datetime.now()
meses_nombres = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

dia_string = str(hoy.day)
mes_string = meses_nombres[hoy.month - 1]
año_string = str(hoy.year)

imprimo_fecha(dia_string, mes_string, año_string)