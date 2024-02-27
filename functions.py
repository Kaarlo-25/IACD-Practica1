import copy

import pandas as pd

valid_operations = ["!", "|", "&", ">", "="]
true_false = ["0", "1"]
operations_indexes_list = []
valid_letters = "bcdfghjklmnñpqrstvwxyz"
multiple_negated_letters = []
letter_values = {}
parentheses_indexes_list = []


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
    global operations_indexes_list
    operations_indexes_list.clear()
    negations = []
    dis_conjuctions = []
    implications_bi = []
    for letter in operation:
        if letter in valid_operations:
            if letter == "!" and operation[operation.index(letter) + 1] not in valid_letters:
                negations.append(operation.index(letter))
            elif letter == "&" or letter == "|":
                dis_conjuctions.append(operation.index(letter))
            else:
                implications_bi.append(operation.index(letter))
    indexes_list = negations + dis_conjuctions + implications_bi
    operations_indexes_list = copy.deepcopy(indexes_list)

    return None


def generate_combinations(n):
    if n == 0:
        return [[]]
    else:
        smaller_combinations = generate_combinations(n - 1)
        return [combo + [bit] for combo in smaller_combinations for bit in [0, 1]]


def assign_values(n):
    valores_posibles = generate_combinations(n)

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
        if not operation_string.isnumeric():
            return partial_operation_results
        else:
            return letter_values[operation_string]

    else:
        new_partial_operation_results = []
        prepare_indexes_list(operation_string)
        print(f'Lista de indices desde calculate_results: {operations_indexes_list}, operation: {operation_string}')

        operation_index = operations_indexes_list[0]

        proposition1_values = letter_values[operation_string[operation_index - 1]]
        proposition2_values = letter_values[operation_string[operation_index + 1]]

        new_partial_operation_results = evaluate_operators(operation_string, operation_index, proposition1_values,
                                                           proposition2_values, new_partial_operation_results)

        partial_operation = str(particial_operation_id)
        letter_values[partial_operation] = new_partial_operation_results
        print(f'Letter_values desde calculate_results: {letter_values}')

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
                if int(key) != 0 and int(key) != 1:
                    del letter_values[key]
        except ValueError:
            continue


def change_negated_propositions_keys():
    for key in list(letter_values.keys()):
        try:
            if key.isupper():
                value = letter_values[key]
                del letter_values[key]
                letter_values["!" + key.lower()] = value
        except:
            continue


def create_dataframe(operation, partial_result):
    eliminates_unnecessary_keys()
    change_negated_propositions_keys()
    df = pd.DataFrame(letter_values)
    if len(operation) > 2 and partial_result is not None:
        df[operation] = None

        for i in range(len(partial_result)):
            df.loc[i, operation] = partial_result[i]

    return df


def delete_values():
    letter_values.clear()
    operations_indexes_list.clear()
    multiple_negated_letters.clear()
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


def negate_values(values):
    for i in range(len(values)):
        if values[i] == 0:
            values[i] = 1
        else:
            values[i] = 0
    return values


def rewrite_propositions_negations(operation):
    new_operation = operation

    i = 0
    while i < len(new_operation):
        if new_operation[i] == "!" and i + 1 < len(new_operation) and new_operation[i + 1] != "!" and new_operation[
            i + 1] != "(":
            multiple_negated_letters.append(new_operation.index(new_operation[i + 1]))
            values = copy.deepcopy(letter_values[new_operation[i + 1]])
            letter_values[new_operation[i + 1].capitalize()] = negate_values(values)
            new_operation = new_operation[:i] + new_operation[i + 1].capitalize() + new_operation[i + 2:]
            prepare_indexes_list(new_operation)

        if new_operation[i] == "!" and new_operation[i + 1] == "!":
            print("Double negation")
            new_operation = new_operation[:i] + new_operation[i + 2:]
            print(new_operation)
        i += 1

    return new_operation


def evaluates_parenthesis(operation):
    global parentheses_indexes_list
    i = -1
    particial_operation_id = 2
    if len(parentheses_indexes_list) == 0:
        return operation, particial_operation_id
    while len(parentheses_indexes_list) != 0:
        i += 1
        if parentheses_indexes_list[i][2]:
            continue
        elif not parentheses_indexes_list[i][2]:
            start = parentheses_indexes_list[i][0]
            end = parentheses_indexes_list[i][1]
            prepare_indexes_list(operation[start + 1: end])
            print(
                f'lista de índices: {operations_indexes_list}, operacion: {operation[start + 1: end]} (Antes de calculate_results)')
            calculate_results(operation[start + 1: end], particial_operation_id - 1)

            partial_operation = str(particial_operation_id)

            partial_operation = partial_operation + operation[end + 1:]
            partial_operation = operation[:start] + partial_operation

            if parentheses_indexes_list[i][3]:
                print(f'Letter values antes de negar: {letter_values}')
                print(partial_operation)
                letter_values[str(particial_operation_id)] = negate_values(letter_values[str(particial_operation_id)])
                print(f'Letter values negado: {letter_values}')
                partial_operation = partial_operation[:partial_operation.index(str(particial_operation_id)) - 1] + \
                                    partial_operation[partial_operation.index(str(particial_operation_id)):]

            particial_operation_id += 1
            if i > 1:
                parentheses_indexes_list[i][2] = False
            parentheses_indexes_list.remove(parentheses_indexes_list[i])
            preapre_parentheses_indexes(partial_operation)
            prepare_indexes_list(partial_operation)
            print(f'Operacion sin parentesis: {partial_operation}')
            print(f'Lista de parentesis despues de calcular: {parentheses_indexes_list}')
            operation = partial_operation
            i = -1
    return partial_operation, particial_operation_id


def preapre_parentheses_indexes(operation: str):
    global parentheses_indexes_list
    stack = []
    result = []

    for i, char in enumerate(operation):
        if char == '(':
            stack.append(i)
        elif char == ')' and stack:
            start = stack.pop()
            inner_parentheses = '(' in operation[start + 1:i]
            preceded_by_not = start > 0 and operation[start - 1] == '!'
            result.append([start, i, inner_parentheses, preceded_by_not])

    parentheses_indexes_list = copy.deepcopy(sorted(result, key=lambda x: x[0]))
    print(f'Lista de parentesis: {parentheses_indexes_list}')
