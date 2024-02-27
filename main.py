from tabulate import tabulate
import functions

initial_message = """
Program starting...

This program calculates all possible well-formed-formulas of propositional logic.

All propositional formulas must be well-formed, which means that only these characters are accepted:
    - Propositions: all consonants in lower case of the spanish alphabet, which includes 'ñ' letter
    - Constants: only the value 1 and 0 are accepted, being 1 = True and 0 = False
    - Operators:
        Negation --> !
        Conjuction --> &
        Disjunction --> |
        Implication --> >
        Bicondicional --> =
    - Other characters: besides the characters already explained, only parentheses are accepted
    - Characters NOT ACCEPTED: punctuation marks(dots, commas, hyphens...)
    
If you want to close the program at any point type \"exit\".
"""

print(initial_message)

while True:
    operation_string = input("\nInsert your operation: \n")
    if operation_string == "exit":
        break
    operation_string = operation_string.replace(" ", "").replace("\n", "").replace("\t", "")
    if functions.is_valid(operation_string):
        num_propositions = functions.prepare_dict(operation_string)
        functions.assign_values(num_propositions)
        functions.assign_constants_values(operation_string)
        operation_with_capital_letters = functions.rewrite_propositions_negations(operation_string)
        functions.prepare_parentheses_indexes(operation_with_capital_letters)
        result_evaluates_parentheses = functions.evaluates_parenthesis(operation_with_capital_letters)
        operation_without_parenthesis = result_evaluates_parentheses[0]
        partial_operation_id = result_evaluates_parentheses[1]
        print(f'Result antes del calculate_results (Main): {operation_without_parenthesis}')

        partial_result = functions.calculate_results(operation_without_parenthesis, partial_operation_id)
        print(f'Result antes del dataframe: {partial_result}')
        df = functions.create_dataframe(operation_string, partial_result)
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))

        print(functions.type_of_truth_table(df[operation_string]) + "\n")
        functions.delete_values()
        continue
    else:
        print("Invalid operation")
        continue
