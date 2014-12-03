from os import mkdir
from pickle import dump, load
from random import randint


from ann.ann import NeuralNetwork


class Connect4(object):
    def __init__(self):
        self.pieces = [[] for i in xrange(7)]
        self.turn = 0

    def check(self, column):
        vectors = ((1, 0), (1, 1), (0, 1), (-1, 1))
        for i in xrange(4):
            row = []
            for j in xrange(-3, 4):
                try:
                    if column + j*vectors[i][0] >= 0 and len(self.pieces[column]) - 1 + j*vectors[i][1] >= 0:
                        row.append(self.pieces[column + j*vectors[i][0]][len(self.pieces[column]) - 1 + j*vectors[i][1]])
                    else:
                        row.append(None)
                except IndexError:
                    row.append(None)
            for j in xrange(4):
                if row[j] == row[j + 1] == row[j + 2] == row[j + 3] is not None:
                    return row[j]
        if sum(len(piece_column) for piece_column in self.pieces) == 42:
            return 2

    def move(self, column):
        for i in xrange(column, column + 7):
            if len(self.pieces[i % 7]) < 6:
                self.pieces[i % 7].append(self.turn)
                self.turn = 1 - self.turn
                return self.check(i % 7)

    def input(self, inputs):
        return self.move(sum(j*2**i for i, j in enumerate(inputs)))

    def output(self):
        return [piece for piece_column in self.pieces for piece in piece_column + [1] + (6 - len(piece_column))*[0]]

    def __str__(self):
        output = ''
        for i in xrange(6):
            output += i and '\n|' or '|'
            for piece_column in self.pieces:
                try:
                    output += piece_column[5 - i] and 'X|' or 'O|'
                except IndexError:
                    output += ' |'
        output += '\n 0 1 2 3 4 5 6 '
        return output


def start():
    try:
        mkdir('examples/connect4/genomes')
    except OSError:
        pass
    players = input('Players: ')
    if players == 0:
        output = input('Output: ')
        anns = [NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5) for i in xrange(20)]
        for i, ann in enumerate(anns):
            try:
                ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(i), 'rb'))
            except IOError:
                pass
        for _ in xrange(input('Iterations: ')):
            for i, ann0 in enumerate(anns[0:10]):
                scores = []
                for j in xrange(100):
                    scores.append(0)
                    for ann1 in anns[10:20]:
                        connect4 = Connect4()
                        winner = None
                        while winner is None:
                            if connect4.turn:
                                winner = connect4.input(inputs=ann1.calculate(inputs=connect4.output()))
                            else:
                                winner = connect4.input(inputs=ann0.calculate(inputs=connect4.output(), increment=j/100.0))
                        if output:
                            print connect4
                        if winner == 2:
                            if output:
                                print "It's a tie!"
                        else:
                            scores[-1] += 1 - 2*winner
                            if output:
                                print "{0} wins!".format(winner and 'X' or 'O')
                ann0.mutate(increment=scores.index(max(scores))/100.0)
                dump(ann0.genome, open('examples/connect4/genomes/genome{0:02d}.p'.format(i), 'wb'))
            for i, ann1 in enumerate(anns[10:20]):
                scores = []
                for j in xrange(100):
                    scores.append(0)
                    for ann0 in anns[0:10]:
                        connect4 = Connect4()
                        winner = None
                        while winner is None:
                            if connect4.turn:
                                winner = connect4.input(inputs=ann1.calculate(inputs=connect4.output(), increment=j/100.0))
                            else:
                                winner = connect4.input(inputs=ann0.calculate(inputs=connect4.output()))
                        if output:
                            print connect4
                        if winner == 2:
                            if output:
                                print "It's a tie!"
                        else:
                            scores[-1] += 2*winner - 1
                            if output:
                                print "{0} wins!".format(winner and 'X' or 'O')
                ann1.mutate(increment=scores.index(max(scores))/100.0)
                dump(ann1.genome, open('examples/connect4/genomes/genome{0:02d}.p'.format(i + 10), 'wb'))
    if players == 1:
        roll = randint(0, 19)
        connect4 = Connect4()
        ann = NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5)
        try:
            ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(roll), 'rb'))
        except IOError:
            pass
        if roll >= 10:
            winner = None
            while winner is None:
                print connect4
                if connect4.turn:
                    winner = connect4.input(inputs=ann.calculate(inputs=connect4.output()))
                else:
                    winner = connect4.move(column=input('{0}\'s turn: '.format(connect4.turn and 'X' or 'O')))
            print connect4
            if winner == 2:
                print "It's a tie!"
            else:
                print "{0} wins!".format(winner and 'X' or 'O')
        else:
            winner = None
            while winner is None:
                print connect4
                if connect4.turn:
                    winner = connect4.move(column=input('{0}\'s turn: '.format(connect4.turn and 'X' or 'O')))
                else:
                    winner = connect4.input(inputs=ann.calculate(inputs=connect4.output()))
            print connect4
            if winner == 2:
                print "It's a tie!"
            else:
                print "{0} wins!".format(winner and 'X' or 'O')
    if players == 2:
        connect4 = Connect4()
        winner = None
        while winner is None:
            print connect4
            winner = connect4.move(column=input('{0}\'s turn: '.format(connect4.turn and 'X' or 'O')))
        print connect4
        if winner == 2:
            print "It's a tie!"
        else:
            print "{0} wins!".format(winner and 'X' or 'O')
