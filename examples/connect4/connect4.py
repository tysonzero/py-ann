class Connect4(object):
    def __init__(self):
        self.pieces = [[] for i in xrange(7)]

    def move(self, player, row):
        self.pieces[row % 7].append(player)


def start():
    pass
