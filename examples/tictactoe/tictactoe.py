class TicTacToe(object):
    def __init__(self):
        self.pieces = [None for _ in xrange(9)]
        self.turn = 0

    def move(self, position):
        for i in xrange(position, position + 9):
            if self.pieces[i % 9] is None:
                self.pieces[i % 9] = self.turn
                self.turn = 1 - self.turn
                return

    def input(self, inputs):
        return self.move(sum(j*2**i for i, j in enumerate(inputs)))

    def output(self):
        return [piece is not None for piece in self.pieces] + [bool(piece) for piece in self.pieces]

    def __str__(self):
        output = ''
        for i, piece in enumerate(self.pieces):
            output += '' if not i else '\n' if not i % 3 else ' '
            output += 'O' if piece else 'X' if piece is not None else str(i)
        return output
