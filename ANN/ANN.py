from random import uniform


class Neuron:
    def __init__(self, parents=[]):
        self.parents = [{
            'neuron': parent,
            'weight': uniform(-1, 1),
            'slope': uniform(-1, 1),
        } for parent in parents]

    def calculate(self, increment=0):
        self.output = sum([parent['neuron'].output * (parent['weight'] + increment * parent['slope']) for parent in self.parents]) > 0

    def mutate(self, increment):
        for parent in self.parents:
            parent['weight'] += increment * parent['slope']
            parent['slope'] = uniform(-1, 1)


class NeuralNetwork:
    def __init__(self, inputs, outputs, hidden, rows):
        self.bias = Neuron()
        self.neurons = []
        for row in xrange(rows):
            self.neurons.append([])
            if row == 0:
                self.neurons[row] = [Neuron(parents=[]) for input_ in xrange(inputs)]
            elif row == rows - 1:
                self.neurons[row] = [Neuron(parents=self.neurons[row - 1] + [self.bias]) for output in xrange(outputs)]
            else:
                self.neurons[row] = [Neuron(parents=self.neurons[row - 1] + [self.bias]) for column in xrange(hidden)]
        self.bias.output = True

    def calculate(self, inputs, increment=0):
        for i, neuron_row in enumerate(self.neurons):
            for j, neuron in enumerate(neuron_row):
                if i == 0:
                    neuron.output = inputs[j]
                else:
                    neuron.calculate(increment=increment)
        return [neuron.output for neuron in self.neurons[-1]]

    def mutate(self, increment):
        for neuron_row in self.neurons:
            for neuron in neuron_row:
                neuron.mutate(increment=increment)
