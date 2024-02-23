from itertools import product
import pandas as pd
import copy

import functions

valid_operations = ["!", "|", "&", ">", "=", "(", ")"]
true_false = ["0", "1"]
operations_indexes_list = []
valid_letters = "bcdfghjklmnñpqrstvwxyz"
negated_letters = []
letter_values = {}


def is_valid(operation):
    return True


def prepare_dict(operation):
    for letter in operation:
        if letter in valid_letters:
            letter_values[letter] = []
            continue
    prepare_indexes_list(operation)
    return len(letter_values.keys())


def prepare_indexes_list(operation):
    operations_indexes_list.clear()
    negations = []
    dis_conjuctions = []
    implications_bi = []
    for letter in operation:
        if letter in valid_operations:
            if letter == "!":
                negations.append(operation.index(letter))
            elif letter == "&" or letter == "|":
                dis_conjuctions.append(operation.index(letter))
            else:
                implications_bi.append(operation.index(letter))
    indexes_list = negations + dis_conjuctions + implications_bi
    functions.operations_indexes_list = copy.deepcopy(indexes_list)

    return None


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
        letter_values["0"] = [0] * (2 ** n)
    if "1" in operation:
        letter_values["1"] = [1] * (2 ** n)


def calculate_results(operation_string, particial_operation_id=1, partial_operation_results=None):
    particial_operation_id += 1
    if len(operation_string) == 1 or len(operation_string) == 2:
        return partial_operation_results
    else:
        new_partial_operation_results = []
        operation_index = operations_indexes_list[0]

        proposition1_values = letter_values[operation_string[operation_index - 1]]
        proposition2_values = letter_values[operation_string[operation_index + 1]]

        new_partial_operation_results = evaluate_operators(operation_string, operation_index, proposition1_values,
                                                           proposition2_values, new_partial_operation_results)

        # TODO recursive function

        partial_operation = str(particial_operation_id)
        letter_values[partial_operation] = new_partial_operation_results

        partial_operation = partial_operation + operation_string[operation_index + 2:]
        partial_operation = operation_string[:operation_index - 1] + partial_operation

        prepare_indexes_list(partial_operation)
        return calculate_results(partial_operation, particial_operation_id, new_partial_operation_results)


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


def eliminates_unnecessary_keys():
    for key in list(letter_values.keys()):
        try:
            if int(key).is_integer():
                if int(key) != 0 or int(key) != 1:
                    del letter_values[key]
        except ValueError:
            continue


def create_dataframe(operation, partial_result):
    eliminates_unnecessary_keys()
    df = pd.DataFrame(letter_values)
    if len(operation) > 2:
        df[operation] = None

        for i in range(len(partial_result)):
            df.loc[i, operation] = partial_result[i]

    return df


def delete_values():
    letter_values.clear()
    operations_indexes_list.clear()
    negated_letters.clear()
    return None


def kind_of_true_table(df_last_column):
    tautologia = all(valor == 1 for valor in df_last_column)
    contradiccion = all(valor == 0 for valor in df_last_column)
    if tautologia:
        return "Tautologia"
    if contradiccion:
        return "Contradiccion"
    else:
        return "Contingencia"
