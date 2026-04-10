def cuantos_dias(nro_mes):

    calendario = [
        ["enero", 31], ["febrero", 28], ["marzo", 31], ["abril", 30],
        ["mayo", 31], ["junio", 30], ["julio", 31], ["agosto", 31],
        ["septiembre", 30], ["octubre", 31], ["noviembre", 30], ["diciembre", 31]
    ]
    
    mes_info = calendario[nro_mes - 1]
    nombre = mes_info[0]
    dias = mes_info[1]
    
    print(f"{nombre.capitalize()} tiene {dias} días.") # Imprime el nombre del mes con la primera letra en mayúscula
    #                                                    y la cantidad de días que tiene.
    
    return dias

cantidad = cuantos_dias(3) 
