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


def calculate_results(operation):
    partial_result = []

    for operant_index in operations_indexs:
        if operation[operant_index] in valid_operations[1:]:

            if operation[operant_index] == "&":
                values1 = letter_values[operation[operant_index - 1]]
                values2 = letter_values[operation[operant_index + 1]]
                for i in range(len(values1)):
                    if values1[i] == 1 and values2[i] == 1:
                        partial_result.append(1)
                    else:
                        partial_result.append(0)

            elif operation[operant_index] == ">":
                values1 = letter_values[operation[operant_index - 1]]
                values2 = letter_values[operation[operant_index + 1]]
                for i in range(len(values1)):
                    if values1[i] == 1 and values2[i] == 0:
                        partial_result.append(0)
                    else:
                        partial_result.append(1)

            elif operation[operant_index] == "=":
                values1 = letter_values[operation[operant_index - 1]]
                values2 = letter_values[operation[operant_index + 1]]
                for i in range(len(values1)):
                    if values1[i] == values2[i]:
                        partial_result.append(1)
                    else:
                        partial_result.append(0)

            elif operation[operant_index] == "|":
                values1 = letter_values[operation[operant_index - 1]]
                values2 = letter_values[operation[operant_index + 1]]
                for i in range(len(values1)):
                    if values1[i] == 1 or values2[i] == 1:
                        partial_result.append(1)
                    else:
                        partial_result.append(0)

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
        return 'tautologia'
    if contradiccion:
        return 'contradiccion'
    else:
        return 'contingencia'
