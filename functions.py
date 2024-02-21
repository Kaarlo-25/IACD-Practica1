from itertools import product
import pandas as pd


valid_operations = ["!", "|", "&", ">", "=", "(", ")"]
operations_indexs = []
valid_letters = "bcdfghjklmnñpqrstvwxyz"
letter_values = {}


def is_valid(operation):
    return True


def prepare_string(operation):
    for letter in operation:
        if letter in valid_letters:
            letter_values[letter] = []
            continue
        if letter in valid_operations:
            operations_indexs.append(operation.index(letter))
            continue
    return len(letter_values.keys())


def assign_values(n):
    # TODO No usar itertools
    valores_posibles = list(product([0, 1], repeat=n))

    for valores in valores_posibles:
        for i in range(n):
            letter_values[list(letter_values.keys())[i]].append(valores[i])

    return None


def calculate_results(operation, partial_value = None, num = 0):
    if len(operation) == 1 or len(operation) == 2:
        return None
    else:
        partial_values = []
        operation_index = operations_indexs[0]

        values1 = letter_values[operation[operation_index - 1]]
        values2 = letter_values[operation[operation_index + 1]]

        if not partial_value is None:
            if num == 1:
                values1 = partial_value
            else:
                values2 = partial_value

        if operation[operation_index] in valid_operations[1:]:
            if operation[operation_index] == "&":
                for i in range(len(values1)):
                    if values1[i] == 1 and values2[i] == 1:
                        partial_values.append(1)
                    else:
                        partial_values.append(0)

            elif operation[operation_index] == "|":
                for i in range(len(values1)):
                    if values1[i] == 1 or values2[i] == 1:
                        partial_values.append(1)
                    else:
                        partial_values.append(0)

            elif operation[operation_index] == ">":
                for i in range(len(values1)):
                    if values1[i] == 1 and values2[i] == 0:
                        partial_values.append(0)
                    else:
                        partial_values.append(1)

            elif operation[operation_index] == "=":
                for i in range(len(values1)):
                    if values1[i] == values2[i]:
                        partial_values.append(1)
                    else:
                        partial_values.append(0)

            operations_indexs.remove(operation_index)

            partial_operation = 'a'
            partial_operation = partial_operation + operation[operation_index + 2:]
            partial_operation = operation[:operation_index - 1] + partial_operation
        return partial_values
#calculate_results(partial_operation, partial_values, 0)

def create_dataframe(operation, partial_result):
    df = pd.DataFrame(letter_values)
    if len(operation) > 1:
        df[operation] = None

        for i in range(len(partial_result)):
            df.loc[i, operation] = partial_result[i]

    return df


def delete_values():
    letter_values.clear()
    operations_indexs.clear()
    return None


def kind_of_true_table(df):
    tautologia = all(valor == 1 for valor in df)
    contradiccion = all(valor == 0 for valor in df)
    if tautologia:
        return "Tautologia"
    if contradiccion:
        return "Contradiccion"
    else:
        return "Contingencia"
