# interpreter

Simple interpreter program for evaluating numeric expressions (following rules of operator precedence).

Integer variables are accepted. (Variable names must contain start with a letter and contain only alphanumeric characters.)

The following operators are supported: `=`, `*`, `/`, `+`, `-`

## Interpreter steps

Consider the example input string `4 * a + 2`, where a=5

### 1) Tokenization
The input string is parsed and split into values, operators and variable names.

e.g. The string `4 * a + 2` tokenizes to `[4, '*', 'a', '+', 2]`

### 2) Tree parsing

The expression is represented as a tree (following operator precedence).

e.g. The example above is represented as

```
    +
   / \
  *   2
 / \ 
4   a
```

### 3) Evaluation

The parsed tree is evaluated and the result is returned.

e.g. The example above evaluates to 22

## Sample use

```shell
$ python3 interpreter.py
This is a simple interpreter program
Enter 'q' to exit input loop
>>
>> a = 5
INPUT STRING a = 5
TOKENIZED INPUT ['a', '=', 5]
PARSED INPUT TREE {
    "op": "=",
    "left": "a",
    "right": 5
}
RESULT 5
>>
>> 5 * a + 2
INPUT STRING 5 * a + 2
TOKENIZED INPUT [5, '*', 'a', '+', 2]
PARSED INPUT TREE {
    "op": "+",
    "left": {
        "op": "*",
        "left": 5,
        "right": "a"
    },
    "right": 2
}
RESULT 27
>>
>> q
Exiting
```
