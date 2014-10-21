from random import random


class Neuron:
    def __init__(self, parents=[]):
        self.parents = parents
        self.weights = [random() for parent in parents]

    def get_output(self):
        return sum([parent.output * self.weights[i] for i, parent in enumerate(self.parents)]) >= 1

    output = property(get_output)


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
