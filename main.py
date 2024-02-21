
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
from tabulate import tabulate

import functions
while True:
    operation = input("\nInsert your operation: \n")
    if functions.is_valid(operation):
        num_proposicions = functions.prepare_string(operation)
        functions.assign_values(num_proposicions)

        partial_result = functions.calculate_results(operation)
        df = functions.create_dataframe(operation, partial_result)
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

        print(functions.kind_of_true_table(df[operation]) + "\n")
        functions.delete_values()
    else:
        print("Invalid operation")
        continue
