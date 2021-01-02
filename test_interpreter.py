from unittest import TestCase

from interpreter import (
    tokenize, parse_to_tree, evaluate, assign_variable, get_variable, valid_variable_name,
    InputError, ParsingError, VariableNotDefinedError
)


class Test_Interpreter(TestCase):

    def test_tokenize_emptystring(self):
        self.assertEqual(tokenize('  \t\n '), [])

    def test_tokenize_nonempty(self):
        self.assertEqual(tokenize('123 + orange +  5 / 6'), [123, '+', 'orange', '+', 5, '/', 6])

    def test_parse_to_tree(self):
        self.assertEqual(
            parse_to_tree([5, '*', 6, '+', 4, '/', 8, '-', 1]),
            {
                'op': '+',
                'left': {
                    'op': '*',
                    'left': 5,
                    'right': 6,
                },
                'right': {
                    'op': '-',
                    'left': {
                        'op': '/',
                        'left': 4,
                        'right': 8,
                    },
                    'right': 1,
                }
            }
        )

    def test_evaluate_numeric_value(self):
        self.assertEqual(
            evaluate(5, {}),
            5
        )

    def test_evaluate_variableName(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        self.assertEqual(
            evaluate('app', variables_tree),
            123
        )

    def test_evaluate_variableNameNotDefined(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        with self.assertRaises(VariableNotDefinedError):
            evaluate('ap', variables_tree)

    def test_evaluate_expression(self):
        self.assertEqual(
            evaluate(
                {
                    "op": "+",
                    "left": {
                        "op": "*",
                        "left": 10,
                        "right": 2
                    },
                    "right": 5
                },
                {}
            ),
            25
        )

    def test_evaluate_float_result(self):
        self.assertEqual(
            evaluate(
                {
                    "op": "+",
                    "left": {
                        "op": "/",
                        "left": 9,
                        "right": 2
                    },
                    "right": 3
                },
                {}
            ),
            7.5
        )

    def test_evaluate_expressionWithVariableName(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        self.assertEqual(
            evaluate(
                {
                    "op": "+",
                    "left": {
                        "op": "/",
                        "left": 'app',
                        "right": 2
                    },
                    "right": 3
                },
                variables_tree
            ),
            64.5
        )

    def test_evaluate_expressionWithVariableNameNotDefined(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        with self.assertRaises(VariableNotDefinedError):
            evaluate(
                {
                    "op": "+",
                    "left": {
                        "op": "/",
                        "left": 'abc',
                        "right": 2
                    },
                    "right": 3
                },
                variables_tree
            )

    def test_evaluate_assignVariable(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        self.assertEqual(
            evaluate(
                {
                    "op": "=",
                    "left": "abc",
                    "right": {
                        "op": "/",
                        "left": "app",
                        "right": 2,
                    }
                },
                variables_tree
            ),
            61.5
        )
        self.assertEqual(
            variables_tree, 
            {'a': {
                'p': {'p': {'\n': 123}},
                'b': {'c': {'\n': 61.5}}
            }}
        )

    def test_evaluate_reassignVariable(self):
        variables_tree = {'a': {'p': {'p': {'\n': 123}}}}
        self.assertEqual(
            evaluate(
                {
                    "op": "=",
                    "left": "app",
                    "right": {
                        "op": "+",
                        "left": "app",
                        "right": 1,
                    }
                },
                variables_tree
            ),
            124
        )
        self.assertEqual(
            variables_tree, 
            {'a': {'p': {'p': {'\n': 124}}}}
        )


    def test_assign_variable(self):
        variables_tree = {}

        # Assign variable
        assign_variable(variables_tree, 'app', 123)

        self.assertEqual(
            variables_tree,
            {'a': {'p': {'p': {'\n': 123}}}}
        )

        # Overwrite existing variable
        assign_variable(variables_tree, 'app', 100)

        self.assertEqual(
            variables_tree,
            {'a': {'p': {'p': {'\n': 100}}}}
        )

        # Assign overlapping variable
        assign_variable(variables_tree, 'apps', 5)

        self.assertEqual(
            variables_tree,
            {'a': {'p': {'p': {'\n': 100, 's': {'\n': 5}}}}}
        )

        # Assign overlapping variable
        assign_variable(variables_tree, 'ap', 23)

        self.assertEqual(
            variables_tree,
            {'a': {'p': {'\n': 23, 'p': {'\n': 100, 's': {'\n': 5}}}}}
        )

        # Assign non-overlpping variable

        assign_variable(variables_tree, 'bee', 8)

        self.assertEqual(
            variables_tree,
            {
                'a': {'p': {'\n': 23, 'p': {'\n': 100, 's': {'\n': 5}}}},
                'b': {'e': {'e': {'\n': 8}}}
            }
        )

    def test_get_variable(self):
        variables_tree = {
            'a': {'p': {'\n': 23, 'p': {'\n': 100, 's': {'\n': 5}}}},
            'b': {'e': {'e': {'\n': 8}}}
        }

        self.assertEqual(get_variable(variables_tree, 'app'), 100)

        self.assertEqual(get_variable(variables_tree, 'apps'), 5)

        self.assertEqual(get_variable(variables_tree, 'ap'), 23)

        self.assertEqual(get_variable(variables_tree, 'bee'), 8)

        self.assertEqual(get_variable(variables_tree, 'a'), None)

        self.assertEqual(get_variable(variables_tree, 'bees'), None)

        self.assertEqual(get_variable(variables_tree, 'ps'), None)

    def test_valid_variable_name(self):
        self.assertTrue(valid_variable_name('aBc123z'))

        self.assertFalse(valid_variable_name(''))

        self.assertFalse(valid_variable_name('1abc'))

        self.assertFalse(valid_variable_name('abc#'))

        self.assertFalse(valid_variable_name('abc d'))
