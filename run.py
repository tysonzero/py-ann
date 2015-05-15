from sys import argv

from examples.connect4.connect4 import Connect4Network
from examples.tictactoe.tictactoe import TicTacToeNetwork


if __name__ == '__main__':
    if len(argv) == 1:
        print
        print 'Available Commands:'
        print 'connect4'
        print 'tictactoe'
        print
    elif argv[1] == 'connect4':
        Connect4Network().play()
    elif argv[1] == 'tictactoe':
        TicTacToeNetwork().play()
