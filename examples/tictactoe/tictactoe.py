class TicTacToe(object):
    def __init__(self):
        self.pieces = [None for _ in xrange(9)]
        self.turn = 0
