import json
import operator
import string

"""
Interpreter steps:
    1) Tokenize / lexing
    2) Parsing
    3) Evaluation

Future work:
    - support negative integer inputs
    - support decimal inputs
    - support parantheses
    - support booleans
    - support if statements
"""

OPERATORS = {
    '=': {
        'fn': None,  # special operator, handled within evaluate fn
        'precedence': 0,
    },
    '+': {
        'fn': operator.add,
        'precedence': 1,
    },
    '-': {
        'fn': operator.sub,
        'precedence': 1,
    },
    '*': {
        'fn': operator.mul,
        'precedence': 2,
    },
    '/': {
        'fn': operator.truediv,
        'precedence': 2,
    },
}

class BaseError(Exception):
    def __init__(self, message):
        self.message = message


class InputError(BaseError):
    pass


class ParsingError(BaseError):
    pass


class InvalidAssignmentSyntaxError(BaseError):
    pass

class VariableNotDefinedError(BaseError):
    pass

# Convert input string into list of separate tokens
# Token elements can be integers or operator chars
def tokenize(input_string):
    tokens = []

    i = 0
    while i < len(input_string):

        # Ignore whitespace
        if input_string[i] in string.whitespace:
            i += 1

        # Handle integer inputs
        elif input_string[i] in string.digits:
            end_index = i+1
            while end_index < len(input_string) and input_string[end_index] in string.digits:
                end_index += 1
            tokens.append(int(input_string[i:end_index]))
            i = end_index

        # Handle variable name inputs
        elif input_string[i] in string.ascii_letters:
            end_index = i+1
            valid_variable_chars = string.digits + string.ascii_letters
            while end_index < len(input_string) and input_string[end_index] in valid_variable_chars:
                end_index += 1
            tokens.append(input_string[i:end_index])
            i = end_index

        # Handle operator inputs
        elif input_string[i] in OPERATORS.keys():
            tokens.append(input_string[i])
            i += 1

        # Raise exception for unsupported input
        else:
            raise InputError('Unsupported input char: ' + input_string[i])

    return tokens


# Convert list of tokens into nested tree of format
# {'op': <char>, 'left': int or tree dict, 'right': int or tree dict}
# based on operator precedence
# (Or if tokenized input contains only an int value and no operators, return the value)
def parse_to_tree(tokenized_input):
    if len(tokenized_input) == 1:
        if tokenized_input[0] in OPERATORS.keys():
            raise ParsingError('Invalid input expression')
        else:
            return tokenized_input[0]

    lowest_precedence = 3 # Max precedence
    lowest_precedence_op_index = None

    # Find operator with lowest precedence in tokenized_input
    # If multiple operators with same lowest precedence exist, choose first one
    for i, char in enumerate(tokenized_input):
        if char in OPERATORS.keys() and OPERATORS[char]['precedence'] < lowest_precedence:
            lowest_precedence = OPERATORS[char]['precedence']
            lowest_precedence_op_index = i

    if lowest_precedence_op_index is not None:
        return {
            'op': tokenized_input[lowest_precedence_op_index],
            'left': parse_to_tree(tokenized_input[:lowest_precedence_op_index]),
            'right': parse_to_tree(tokenized_input[lowest_precedence_op_index+1:]),
        }
    else:
        raise ParsingError('Invalid input expression')


"""
# Sample structure of variables prefix tree
{
    'a': {
        'p': {
            'p': {
                '\n': 1,
                's': {
                    '\n': 101
                }
            }
        },
        'z': {'\n': 23}
    }
}
"""


# Add variable to variables prefix tree, overwriting previous value
# if it exists
def assign_variable(variables_tree, name, value):
    tree_pointer = variables_tree
    for char in name:
        # Assume variable values are always numeric (cannot be set to None)
        if tree_pointer.get(char) is None:
            tree_pointer[char] = {}

        tree_pointer = tree_pointer[char]

    # Use '\n' as sentinal to mark end of variable
    tree_pointer['\n'] = value


# Walk through variables prefix tree, and return value of variable given by name
# If variable with given name does not exist, return None
def get_variable(variables_tree, name):
    tree_pointer = variables_tree
    for char in name:
        if tree_pointer.get(char) is None:
            return None

        tree_pointer = tree_pointer[char]

    return tree_pointer.get('\n')


# Valid variable names start with a letter
# and contain only alphanumeric characters
def valid_variable_name(name):
    if not isinstance(name, str):
        return False

    if len(name) == 0 or name[0] not in string.ascii_letters:
        return False

    for char in name[1:]:
        if char not in string.ascii_letters and char not in string.digits:
            return False

    return True


# Evaluate expression encoded by input tree
def evaluate(tree, variables):
    # Base case: value is numeric
    if isinstance(tree, (int, float)):
        return tree

    # Base case: value is variable name
    elif isinstance(tree, str):
        value = get_variable(variables, tree)
        if value is not None:
            return value
        else:
            raise VariableNotDefinedError('Variable not exists: ' + tree)

    # Handle variable assignment
    elif tree['op'] == '=':
        if valid_variable_name(tree['left']):
            value = evaluate(tree['right'], variables)
            assign_variable(variables, tree['left'], value)
            return value
        else:
            raise InvalidAssignmentSyntaxError(
                'Left side of assignment expression must be alphanumeric string starting with a letter'
            )

    # Evaluate expression
    else:
        return OPERATORS[tree['op']]['fn'](
            evaluate(tree['left'], variables),
            evaluate(tree['right'], variables),
        )


def main():
    variables = {}

    print("This is a simple interpreter program\nEnter 'q' to exit input loop")
    while True:
        input_string = input('>> ')

        if input_string == 'q':
            print("Exiting")
            return

        
        print("INPUT STRING", input_string)
        try:
            # Tokenize input string
            tokenized_input = tokenize(input_string)
            print("TOKENIZED INPUT", tokenized_input)

            # Parse tokenized input to tree, following operator precendence
            parsed_input_tree = parse_to_tree(tokenized_input)
            print("PARSED INPUT TREE", json.dumps(parsed_input_tree, indent=4))

            # Evaluate expression
            result = evaluate(parsed_input_tree, variables)
            print("RESULT", result)

        except (InputError, ParsingError, VariableNotDefinedError, InvalidAssignmentSyntaxError) as e:
            print(e.message + ", please try again")


if __name__ == "__main__":
    main()