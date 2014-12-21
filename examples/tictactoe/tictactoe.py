class TicTacToe(object):
    def __init__(self, anns=[None, None], increments=[0, 0]):
        self.pieces = [None for _ in xrange(9)]
        self.anns = anns
        self.increments = increments
        self.turn = 0

    def check(self, position):
        if len(set(self.pieces[3*(position/3):3*(position/3 + 1)])) == 1:
            return self.pieces[position]
        if len(set(self.pieces[position % 3::3])) == 1:
            return self.pieces[position]
        if not position % 4:
            if len(set(self.pieces[0::4])) == 1:
                return self.pieces[position]
        if position == 4 or position % 4 == 2:
            if len(set(self.pieces[2::2][0:3])) == 1:
                return self.pieces[position]
        if set(self.pieces) == set([0, 1]):
            return 0.5

    def move(self, position):
        for i in xrange(position, position + 9):
            if self.pieces[i % 9] is None:
                self.pieces[i % 9] = self.turn
                self.turn = 1 - self.turn
                return self.check(i % 9)

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
