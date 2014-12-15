from sys import argv

from examples.connect4.connect4 import Connect4Network


if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == 'connect4':
            Connect4Network().play()
