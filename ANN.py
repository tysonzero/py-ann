from random import random


class Neuron:
    output = None

    def __init__(self, parents=[]):
        self.parents = parents
        self.weights = [random() for parent in parents]

    def calculate(self):
        self.output = sum([parent.output * self.weights[i] for i, parent in enumerate(self.parents)]) >= 1


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
