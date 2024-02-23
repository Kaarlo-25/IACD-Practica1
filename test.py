""""""
import functions


def rewrite(operation):
    new_operation = operation

    i = 0
    while i < len(new_operation):
        if new_operation[i] == "!" and i + 1 < len(new_operation):
            negated_letters.append(operation.index(operation[i + 1]))
            values = copy.deepcopy(letter_values[operation[i + 1]])
            letter_values[operation[i + 1].capitalize()] = negate_values(values)
            new_operation = new_operation[:i] + new_operation[i + 1].capitalize() + new_operation[i + 2:]
            prepare_indexes_list(new_operation)
            i += 1
        i += 1

    return new_operation

print(rewrite("p&q&q>t=!z"))