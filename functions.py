from itertools import product
import pandas as pd


valid_operations = ["!", "|", "&", ">", "=", "(", ")"]
true_false = ["0", "1"]
operations_indexes_list = []
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
            operations_indexes_list.append(operation.index(letter))
            continue
    return len(letter_values.keys())


def assign_values(n):
    # TODO No usar itertools
    valores_posibles = list(product([0, 1], repeat=n))

    for valores in valores_posibles:
        for i in range(n):
            letter_values[list(letter_values.keys())[i]].append(valores[i])

    return None

def assign_true_false_values(operation):
    n = len(letter_values.keys())
    if "0" in operation:
        letter_values["0"] = [0] * (2**n)
    if "1" in operation:
        letter_values["1"] = [1] * (2**n)

def calculate_results(operation_string, partial_operation_results=None, num=0):
    if len(operation_string) == 1 or len(operation_string) == 2:
        return partial_operation_results
    else:
        new_partial_operation_results = []
        operation_index = operations_indexes_list[0]

        proposition1_values = letter_values[operation_string[operation_index - 1]]
        proposition2_values = letter_values[operation_string[operation_index + 1]]

        if not partial_operation_results is None:
            if num == 1:
                proposition1_values = partial_operation_results
            else:
                proposition2_values = partial_operation_results

        new_partial_operation_results = evaluate_operators(operation_string, operation_index, proposition1_values,
                                                           proposition2_values, new_partial_operation_results)
        operations_indexes_list.remove(operation_index)

        # TODO recursive function

        partial_operation = "A"
        partial_operation = partial_operation + operation_string[operation_index + 2:]
        partial_operation = operation_string[:operation_index - 1] + partial_operation
        return calculate_results(partial_operation, new_partial_operation_results, 1)

def evaluate_operators(operation, operation_index, proposition1_values, proposition2_values, partial_values):
    if operation[operation_index] in valid_operations[1:]:
        if operation[operation_index] == "&":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 and proposition2_values[i] == 1:
                    partial_values.append(1)
                else:
                    partial_values.append(0)

        elif operation[operation_index] == "|":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 or proposition2_values[i] == 1:
                    partial_values.append(1)
                else:
                    partial_values.append(0)

        elif operation[operation_index] == ">":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 and proposition2_values[i] == 0:
                    partial_values.append(0)
                else:
                    partial_values.append(1)

        elif operation[operation_index] == "=":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == proposition2_values[i]:
                    partial_values.append(1)
                else:
                    partial_values.append(0)
    return partial_values


def create_dataframe(operation, partial_result):
    df = pd.DataFrame(letter_values)
    if len(operation) > 1:
        df[operation] = None

        for i in range(len(partial_result)):
            df.loc[i, operation] = partial_result[i]

    return df


def delete_values():
    letter_values.clear()
    operations_indexes_list.clear()
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
