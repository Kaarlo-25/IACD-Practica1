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
    proposiciones = [f'p{i + 1}' for i in range(n)]
    valores_posibles = list(product([0, 1], repeat=n))
    tabla_verdad = {proposicion: [] for proposicion in proposiciones}

    for valores in valores_posibles:
        for i in range(n):
            tabla_verdad[proposiciones[i]].append(valores[i])
    i = -1
    for _, valores in tabla_verdad.items():
        i += 1
        letter_values[list(letter_values.keys())[i]] = valores
    return None


def create_dataframe():
    df = pd.DataFrame(letter_values)
    return df


def calculate_results(operation):
    return None


def delete_values():
    letter_values.clear()
    return None