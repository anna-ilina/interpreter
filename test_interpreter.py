from unittest import TestCase

from interpreter import tokenize, parse_to_tree, evaluate


class Test_Interpreter(TestCase):

    def test_tokenize_emptystring(self):
        self.assertEqual(tokenize('  \t\n '), [])

    def test_tokenize_nonempty(self):
        self.assertEqual(tokenize('123 +   5 / 6'), [123, '+', 5, '/', 6])

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

    def test_evaluate(self):
        self.assertEqual(
            evaluate({
                "op": "+",
                "left": {
                    "op": "*",
                    "left": 10,
                    "right": 2
                },
                "right": 5
            }),
            25
        )

    def test_evaluate_no_operators(self):
        self.assertEqual(
            evaluate(5),
            5
        )
