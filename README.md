PY-ANN
======

An Artificial Neural Network

Examples:
---------

    python run.py connect4
    python run.py tictactoe

To use it yourself:
-------------------

    from ann.ann import ANN
    ann = ANN(inputs=4, outputs=4, hidden=4, rows=4)
    print ann.calculate(inputs=[True, False, True, False])
    print ann.calculate(inputs=[True, False, True, False], increment=1)

If the ann does better with the second result you can mutate it:

    ann.mutate(increment=1)
    print ann.calculate(inputs=[True, False, True, False])

This should give you the exact same result as the earlier one with the increment.
