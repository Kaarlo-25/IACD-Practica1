
"""
    1.- conseguir input
    3.- comprobar validez
    2.- preparar string
    3.- dividir substrings
    4.- asignar valores
    5.- crear data frame
    6.- calcular los resultados
    7.- detectar tautología, contradicción o contingencia

Trabajo de 10:
    - que funcione
    - comentar el codigo
    - Hacer una memoria con las incidencias del desarrollo(2 paj max)
    - Hacer trabajo opcional
    - Responder con soltura
"""
import functions
while True:
    operation = input("\nInsert your operation: \n")
    if functions.is_valid(operation):
        num_proposicions = functions.prepare_string(operation)
        functions.assign_values(num_proposicions)
        functions.calculate_results(operation)
        functions.delete_values()
    else:
        print("Invalid operation")
        continue
