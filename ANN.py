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

    def __init__(self, inputs, outputs, rows, columns):
        self.neurons = []
        for row in xrange(rows + 2):
            self.neurons.append([])
            if row == 0:
                for input_ in xrange(inputs):
                    self.neurons[row].append(Neuron(parents=[]))
            elif row == rows + 1:
                for output in xrange(outputs):
                    self.neurons[row].append(Neuron(parents=self.neurons[row - 1]))
            else:
                for column in xrange(columns):
                        self.neurons[row].append(Neuron(parents=self.neurons[row - 1]))
