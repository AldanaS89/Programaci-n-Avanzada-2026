def tabla_multiplicar(numero):
    for i in range(1, 11): # El rango va de 1 a 10, ya que queremos multiplicar el número por los números del 1 al 10.
        resultado = numero * i
        print(f"{numero} x {i} = {resultado}")

tabla_multiplicar(1100)