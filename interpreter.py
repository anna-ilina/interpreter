import json
import operator
import string

"""
Interpreter steps:
    1) Tokenize / lexing
    2) Parsing
    3) Evaluation

Future work:
    - support variables
    - support negative integer inputs
    - support decimal inputs
    - support parantheses
    - support booleans
    - support if statements
"""

OPERATORS = {
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
        if isinstance(tokenized_input[0], (int, float)):
            return tokenized_input[0]
        else:
            raise ParsingError('Invalid input expression')

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


# Evaluate expression encoded by input tree
def evaluate(tree):
    if isinstance(tree, int):
        # Handle case where user enters a value string (e.g. '101'), not an expression
        return tree

    return OPERATORS[tree['op']]['fn'](
        evaluate(tree['left']) if isinstance(tree['left'], dict) else tree['left'],
        evaluate(tree['right']) if isinstance(tree['right'], dict) else tree['right'],
    )


def main():
    # variables = {}

    print("Enter 'q' to exit input loop")
    while True:
        input_string = input('Input here: ')

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
            result = evaluate(parsed_input_tree)
            print("RESULT", result)

        except (InputError, ParsingError) as e:
            print(e.message + ", please try again")


if __name__ == "__main__":
    main()