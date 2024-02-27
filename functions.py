import copy
import pandas as pd

valid_operators = ["!", "|", "&", ">", "="]
constants = ["0", "1"]
operators_indexes_list = []
valid_proposition_letters = "bcdfghjklmnñpqrstvwxyz"
valid_characters = valid_proposition_letters + "!|&>=()01" + " "
multiple_negated_propositions = []
proposition_values = {}


def is_valid(operation_string):
    if operation_string[-1] in valid_operators or operation_string[0] in valid_operators[1:]:  # q|p! and &p|q
        print("Invalid operators.")
        return False
    if not parentheses_validation(operation_string):
        print("Invalid parenthesis.")
        return False
    for i in range(len(operation_string)):
        if operation_string[i] not in valid_characters:  # accepts only valid letters and operators
            print("Invalid ]character detected.\n")
            return False
        if i > 0:
            if (operation_string[i] in valid_proposition_letters and
                    operation_string[i - 1] in valid_proposition_letters):  # solving case: pq
                print("Invalid operation.\n")
                return False
            if operation_string[i] in valid_operators and operation_string[i - 1] in valid_operators:
                if operation_string[i] in valid_operators[1:] and operation_string[i - 1] != "!":  # p!&k
                    print("Invalid operators.")
                    return False
                if operation_string[i] in valid_operators[1:] and operation_string[i - 1] in valid_operators[1:]:
                    # p&|k
                    print("Invalid operators.")
                    return False
    print("Valid operators.\n")
    return True


def parentheses_validation(operation_string):
    stack = []
    mapping = {")": "("}
    for i in range(len(operation_string)):
        if operation_string[i] == ")":
            if stack:
                if i - stack[-1][1] == 1 or i - stack[-1][1] == 2:
                    print("Error at:", stack[-1][1])
                    return False
                if ((operation_string[stack[-1][1] - 1] not in valid_operators) or
                        (stack[-1][1] == 0) or
                        (operation_string[stack[-1][1] + 1] not in valid_characters[:23])):
                    print("Error at:", stack[-1][1])
                    return False
                else:
                    top_element = stack.pop()
            else:
                return False
            if mapping[operation_string[i]] != top_element[0]:
                print("Error at:", stack[-1][1])
                return False
        if operation_string[i] == "(":
            stack.append((operation_string[i], i))
    return not stack


def prepare_dict(operation_string):
    for letter in operation_string:
        if letter in valid_proposition_letters:
            proposition_values[letter] = []
            continue
    prepare_operators_indexes_list(operation_string)
    return len(proposition_values.keys())


def prepare_operators_indexes_list(operation_string):
    global operators_indexes_list
    operators_indexes_list.clear()
    negations = []
    dis_conjunctions = []
    implications_bi = []
    for char in operation_string:
        if char in valid_operators:
            if char == "!" and operation_string[operation_string.index(char) + 1] not in valid_proposition_letters:
                negations.append(operation_string.index(char))
            elif char == "&" or char == "|":
                dis_conjunctions.append(operation_string.index(char))
            else:
                implications_bi.append(operation_string.index(char))
    indexes_list = negations + dis_conjunctions + implications_bi
    operators_indexes_list = copy.deepcopy(indexes_list)


def generate_combinations(n):
    if n == 0:
        return [[]]
    else:
        smaller_combinations = generate_combinations(n - 1)
        return [combo + [bit] for combo in smaller_combinations for bit in [0, 1]]


def assign_values(n):
    possible_values = generate_combinations(n)
    for values in possible_values:
        for i in range(n):
            proposition_values[list(proposition_values.keys())[i]].append(values[i])


def assign_constants_values(operation_string):
    n = len(proposition_values.keys())
    if "0" in operation_string:
        proposition_values["0"] = [0] * (2 ** n)
    if "1" in operation_string:
        proposition_values["1"] = [1] * (2 ** n)


def calculate_results(operation_string, partial_operation_id=1, partial_operation_results=None):
    partial_operation_id += 1
    if len(operation_string) == 1 or len(operation_string) == 2:
        if not operation_string.isnumeric():
            return partial_operation_results
        else:
            return proposition_values[operation_string]

    else:
        new_partial_operation_results = []
        prepare_operators_indexes_list(operation_string)
        print(f'Lista de indices desde calculate_results: {operators_indexes_list}, operation: {operation_string}')

        operation_index = operators_indexes_list[0]

        proposition1_values = proposition_values[operation_string[operation_index - 1]]
        proposition2_values = proposition_values[operation_string[operation_index + 1]]

        new_partial_operation_results = evaluate_operators(operation_string, operation_index, proposition1_values,
                                                           proposition2_values, new_partial_operation_results)

        partial_operation = str(partial_operation_id)
        proposition_values[partial_operation] = new_partial_operation_results
        print(f'Letter_values desde calculate_results: {proposition_values}')

        partial_operation = partial_operation + operation_string[operation_index + 2:]
        partial_operation = operation_string[:operation_index - 1] + partial_operation

        prepare_operators_indexes_list(partial_operation)
        return calculate_results(partial_operation, partial_operation_id, new_partial_operation_results)


def evaluate_operators(operation_string, operator_index, proposition1_values, proposition2_values, partial_values):
    if operation_string[operator_index] in valid_operators[1:]:
        if operation_string[operator_index] == "&":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 and proposition2_values[i] == 1:
                    partial_values.append(1)
                else:
                    partial_values.append(0)

        elif operation_string[operator_index] == "|":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 or proposition2_values[i] == 1:
                    partial_values.append(1)
                else:
                    partial_values.append(0)

        elif operation_string[operator_index] == ">":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == 1 and proposition2_values[i] == 0:
                    partial_values.append(0)
                else:
                    partial_values.append(1)

        elif operation_string[operator_index] == "=":
            for i in range(len(proposition1_values)):
                if proposition1_values[i] == proposition2_values[i]:
                    partial_values.append(1)
                else:
                    partial_values.append(0)
    return partial_values


def eliminates_unnecessary_keys():
    for key in list(proposition_values.keys()):
        try:
            if int(key).is_integer():
                if int(key) != 0 and int(key) != 1:
                    del proposition_values[key]
        except ValueError:
            continue


def change_negated_propositions_keys():
    for key in list(proposition_values.keys()):
        try:
            if key.isupper():
                value = proposition_values[key]
                del proposition_values[key]
                proposition_values["!" + key.lower()] = value
        except:
            continue


def create_dataframe(operation_string, partial_result):
    eliminates_unnecessary_keys()
    change_negated_propositions_keys()
    df = pd.DataFrame(proposition_values)
    if len(operation_string) > 2 and partial_result is not None:
        df[operation_string] = None

        for i in range(len(partial_result)):
            df.loc[i, operation_string] = partial_result[i]

    return df


def delete_values():
    proposition_values.clear()
    operators_indexes_list.clear()
    multiple_negated_propositions.clear()


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


def rewrite_propositions_negations(operation_string):
    new_operation = operation_string
    i = 0

    while i < len(new_operation):
        if (new_operation[i] == "!" and i + 1 < len(new_operation) and
                new_operation[i + 1] != "!" and new_operation[i + 1] != "("):
            multiple_negated_propositions.append(new_operation.index(new_operation[i + 1]))
            values = copy.deepcopy(proposition_values[new_operation[i + 1]])
            proposition_values[new_operation[i + 1].capitalize()] = negate_values(values)
            new_operation = new_operation[:i] + new_operation[i + 1].capitalize() + new_operation[i + 2:]
            prepare_operators_indexes_list(new_operation)

        if new_operation[i] == "!" and new_operation[i + 1] == "!":
            print("Double negation")
            new_operation = new_operation[:i] + new_operation[i + 2:]
            print(new_operation)
        i += 1

    return new_operation


def evaluates_parenthesis(operation_string):
    global parentheses_indexes_list
    i = -1
    partial_operation_id = 2
    if len(parentheses_indexes_list) == 0:
        return operation_string, partial_operation_id
    while len(parentheses_indexes_list) != 0:
        i += 1
        if parentheses_indexes_list[i][2]:
            continue
        elif not parentheses_indexes_list[i][2]:
            start = parentheses_indexes_list[i][0]
            end = parentheses_indexes_list[i][1]
            prepare_operators_indexes_list(operation_string[start + 1: end])
            print(
                f'lista de índices: {operators_indexes_list}, '
                f'operacion: {operation_string[start + 1: end]} (Antes de calculate_results)')
            calculate_results(operation_string[start + 1: end], partial_operation_id - 1)

            partial_operation = str(partial_operation_id)

            partial_operation = partial_operation + operation_string[end + 1:]
            partial_operation = operation_string[:start] + partial_operation

            if parentheses_indexes_list[i][3]:
                print(f'Letter values antes de negar: {proposition_values}')
                print(partial_operation)
                proposition_values[str(partial_operation_id)] = negate_values(
                    proposition_values[str(partial_operation_id)])
                print(f'Letter values negado: {proposition_values}')
                partial_operation = partial_operation[:partial_operation.index(str(partial_operation_id)) - 1] + \
                                    partial_operation[partial_operation.index(str(partial_operation_id)):]

            partial_operation_id += 1
            if i > 1:
                parentheses_indexes_list[i][2] = False
            parentheses_indexes_list.remove(parentheses_indexes_list[i])
            prepare_parentheses_indexes(partial_operation)
            prepare_operators_indexes_list(partial_operation)
            print(f'Operacion sin parentesis: {partial_operation}')
            print(f'Lista de parentesis despues de calcular: {parentheses_indexes_list}')
            operation_string = partial_operation
            i = -1
    return partial_operation, partial_operation_id


def prepare_parentheses_indexes(operation: str):
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
