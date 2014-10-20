class Neuron:
    pass


class NeuronNetwork:
    neurons = []

    def __init__(self, rows, columns):
        self.neurons = []
        for row in xrange(rows):
            self.neurons.append([])
            for column in xrange(columns):
                self.neurons[row].append(Neuron())
