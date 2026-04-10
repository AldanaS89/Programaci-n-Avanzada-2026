def retorno_mensaje():
    return "Estudiando en la UNAB"
print(retorno_mensaje())

# ¿Cómo hago para mostrar ese mensaje en pantalla? -> Utilizando la función print() y llamando a la función retorno_mensaje() dentro de ella.
# ¿Qué diferencia encuentra con el ejercicio anterior? -> En el ejercicio anterior, la función imprimía directamente el mensaje en pantalla,
#                                                         mientras que en este ejercicio, la función retorna el mensaje como un valor que luego
#                                                         se puede imprimir o utilizar de otras formas.
#Si tuvieras que imprimir mensajes como "Estudiando 
# Matemática I en la UNAB" usando la misma función, 
# ¿cómo la modificarías? -> Podría modificar la función para que acepte un parámetro que especifique la materia,
#                           y luego construir el mensaje utilizando ese parámetro. Por ejemplo:
def retorno_mensaje(materia):
    return f"Estudiando {materia} en la UNAB"
print(retorno_mensaje("Matemática I"))