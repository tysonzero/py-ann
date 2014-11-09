class Connect4(object):
    def __init__(self):
        self.pieces = [[] for i in xrange(7)]

    def move(self, player, row):
        self.pieces[row % 7].append(player)

    def __str__(self):
        output = ''
        for i in xrange(6):
            output += i and '\n ' or ' '
            for piece_column in self.pieces:
                try:
                    output += str(piece_column[5 - i]) + ' '
                except IndexError:
                    output += '  '
        return output


def start():
    pass
