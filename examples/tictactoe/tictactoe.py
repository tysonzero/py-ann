from multiprocessing import Process
from os import mkdir
from pickle import dump, load
from random import randint

from ann.ann import ANN


class TicTacToe(object):
    def __init__(self, anns=None, increments=None):
        self.pieces = [None for _ in xrange(9)]
        self.anns = anns or [None, None]
        self.increments = increments or [0, 0]
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

    def play(self, output=True):
        winner = None
        while winner is None:
            if output:
                print self
            if self.anns[self.turn]:
                winner = self.input(inputs=self.anns[self.turn].calculate(inputs=self.output(), increment=self.increments[self.turn]))
            else:
                winner = self.move(position=input('{0}\'s turn: '.format('O' if self.turn else 'X')))
        if output:
            print self
        if winner == 0.5:
            if output:
                print "It's a tie!"
        else:
            if output:
                print "{0} wins!".format('O' if winner else 'X')
        return winner

    def __str__(self):
        output = ''
        for i, piece in enumerate(self.pieces):
            output += '' if not i else '\n' if not i % 3 else ' '
            output += '\033[92mO\033[0m' if piece else '\033[91mX\033[0m' if piece is not None else str(i)
        return output


class TicTacToeNetwork(object):
    def thread(self, i, output):
        anns = [ANN(inputs=18, outputs=4, hidden=18, rows=4) for _ in xrange(20)]
        for j, ann in enumerate(anns):
            try:
                ann.genome = load(open('examples/tictactoe/genomes/genome{0:02d}.p'.format(j), 'rb'))
            except IOError:
                pass
        scores = []
        for j in xrange(100):
            scores.append(0)
            if i < 10:
                for ann in anns[10:20]:
                    tictactoe = TicTacToe(anns=[anns[i], ann], increments=[j/100.0, 0])
                    winner = tictactoe.play(output=output)
                    scores[-1] += 1 - 2*winner
            else:
                for ann in anns[0:10]:
                    tictactoe = TicTacToe(anns=[ann, anns[i]], increments=[0, j/100.0])
                    winner = tictactoe.play(output=output)
                    scores[-1] += 2*winner - 1
        ann.mutate(increment=scores.index(max(scores))/100.0)
        dump(ann.genome, open('examples/tictactoe/genomes/genome{0:02d}.p'.format(i), 'wb'))

    def play(self):
        try:
            mkdir('examples/tictactoe/genomes')
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
            ann = ANN(inputs=18, outputs=4, hidden=18, rows=4)
            try:
                ann.genome = load(open('examples/tictactoe/genomes/genome{0:02d}.p'.format(roll), 'rb'))
            except IOError:
                pass
            if roll < 10:
                TicTacToe([ann, None]).play()
            else:
                TicTacToe([None, ann]).play()
        elif players == 2:
            TicTacToe().play()
