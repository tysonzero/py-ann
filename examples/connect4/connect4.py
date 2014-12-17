from multiprocessing import Process
from os import mkdir
from pickle import dump, load
from random import randint


from ann.ann import NeuralNetwork


class Connect4(object):
    def __init__(self, anns=[None, None], increments=[0, 0]):
        self.pieces = [[] for _ in xrange(7)]
        self.anns = anns
        self.increments = increments
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
                if len(set(row[j:j + 4])) == 1:
                    return row[j]
        if sum(len(piece_column) for piece_column in self.pieces) == 42:
            return 0.5

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

    def play(self, output=True):
        winner = None
        while winner is None:
            if output:
                print self
            if self.anns[self.turn]:
                winner = self.input(inputs=self.anns[self.turn].calculate(inputs=self.output(), increment=self.increments[self.turn]))
            else:
                winner = self.move(column=input('{0}\'s turn: '.format('X' if self.turn else 'O')))
        if output:
            print self
        if winner == 0.5:
            if output:
                print "It's a tie!"
        else:
            if output:
                print "{0} wins!".format('X' if winner else 'O')
        return winner

    def __str__(self):
        output = ''
        for i in xrange(6):
            output += '\n|' if i else '|'
            for piece_column in self.pieces:
                try:
                    output += 'X|' if piece_column[5 - i] else 'O|'
                except IndexError:
                    output += ' |'
        output += '\n 0 1 2 3 4 5 6 '
        return output


class Connect4Network(object):
    def thread(self, i, output):
        anns = [NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5) for _ in xrange(20)]
        for j, ann in enumerate(anns):
            try:
                ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(j), 'rb'))
            except IOError:
                pass
        scores = []
        for j in xrange(100):
            scores.append(0)
            if i < 10:
                for ann in anns[10:20]:
                    connect4 = Connect4(anns=[anns[i], ann], increments=[j/100.0, 0])
                    winner = connect4.play(output=output)
                    scores[-1] += 1 - 2*winner
            else:
                for ann in anns[0:10]:
                    connect4 = Connect4(anns=[ann, anns[i]], increments=[0, j/100.0])
                    winner = connect4.play(output=output)
                    scores[-1] += 2*winner - 1
        ann.mutate(increment=scores.index(max(scores))/100.0)
        dump(ann.genome, open('examples/connect4/genomes/genome{0:02d}.p'.format(i), 'wb'))

    def play(self):
        try:
            mkdir('examples/connect4/genomes')
        except OSError:
            pass
        players = input('Players: ')
        if players == 0:
            output = input('Output: ')
            for _ in xrange(input('Iterations: ')):
                processes = []
                for i in xrange(20):
                    processes.append(Process(target=self.thread, kwargs={'i': i, 'output': output}))
                    processes[-1].start()
                for process in processes:
                    process.join()
        elif players == 1:
            roll = randint(0, 19)
            ann = NeuralNetwork(inputs=49, outputs=3, hidden=49, rows=5)
            try:
                ann.genome = load(open('examples/connect4/genomes/genome{0:02d}.p'.format(roll), 'rb'))
            except IOError:
                pass
            if roll < 10:
                Connect4([ann, None]).play()
            else:
                Connect4([None, ann]).play()
        elif players == 2:
            Connect4().play()
