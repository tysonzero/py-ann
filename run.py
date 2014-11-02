from sys import argv

from examples.connect4 import connect4


if __name__ == '__main__':
    if argv[1] == 'connect4':
        connect4.start()
