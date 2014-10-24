from random import uniform


class Neuron:
    def __init__(self, parents=[]):
        self.parents = parents
        self.weights = [uniform(-1, 1) for parent in self.parents]
        self.gradient = [uniform(-1, 1) for parent in self.parents]

    def calculate(self, increment=0):
        self.output = sum([parent.output * (self.weights[i] + increment*self.gradient[i]) for i, parent in enumerate(self.parents)]) > 0


class NeuronNetwork:
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

    def run(self, inputs, increment=0):
        for i, neuron_row in enumerate(self.neurons):
            for j, neuron in enumerate(neuron_row):
                if i == 0:
                    neuron.output = inputs[j]
                else:
                    neuron.calculate(increment=increment)
        return [neuron.output for neuron in self.neurons[len(self.neurons) - 1]]
