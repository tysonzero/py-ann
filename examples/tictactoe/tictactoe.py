class TicTacToe(object):
    def __init__(self):
        self.pieces = [None for _ in xrange(9)]
        self.turn = 0

    def move(self, position):
        for i in xrange(position, position + 9):
            if self.pieces[i % 9] is None:
                self.pieces[i % 9] = self.turn
