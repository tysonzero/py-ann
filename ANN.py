from random import uniform


class Neuron:
    def __init__(self, parents=[]):
        self.parents = parents
        self.weights = [uniform(-1, 1) for parent in self.parents]
        self.slopes = [uniform(-1, 1) for parent in self.parents]

    def calculate(self, increment=0):
        self.output = sum([parent.output * (self.weights[i] + increment*self.slopes[i]) for i, parent in enumerate(self.parents)]) > 0

    def mutate(self, increment):
        self.weights = [weight + increment*self.slopes[i] for i, weight in enumerate(self.weights)]
        self.slopes = [uniform(-1, 1) for parent in self.parents]


class NeuronNetwork:
    def __init__(self, inputs, outputs, hidden, rows):
        self.neurons = []
        for row in xrange(rows):
            self.neurons.append([])
            if row == 0:
                for input_ in xrange(inputs):
                    self.neurons[row].append(Neuron(parents=[]))
            elif row == rows - 1:
                for output in xrange(outputs):
                    self.neurons[row].append(Neuron(parents=self.neurons[row - 1]))
            else:
                for column in xrange(hidden):
                    self.neurons[row].append(Neuron(parents=self.neurons[row - 1]))

    def run(self, inputs, increment=0):
        for i, neuron_row in enumerate(self.neurons):
            for j, neuron in enumerate(neuron_row):
                if i == 0:
                    neuron.output = inputs[j]
                else:
                    neuron.calculate(increment=increment)
        return [neuron.output for neuron in self.neurons[len(self.neurons) - 1]]

    def mutate(self, increment):
        for neuron_row in self.neurons:
            for neuron in neuron_row:
                neuron.mutate(increment=increment)
