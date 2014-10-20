from random import random


class Neuron:
    def __init__(self, parents=[]):
        self.parents = parents
        self.weights = [random() for parent in parents]


class NeuronNetwork:
    neurons = []

    def __init__(self, rows, columns):
        self.neurons = []
        for row in xrange(rows):
            self.neurons.append([])
            for column in xrange(columns):
                if row == 0:
                    self.neurons[row].append(Neuron(parents=[]))
                else:
                    self.neurons[row].append(Neuron(parents=self.neurons[row - 1]))
