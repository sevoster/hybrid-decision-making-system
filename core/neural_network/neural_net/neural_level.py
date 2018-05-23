class INeuralLevel:
    def add_neuron(self, neuron):
        raise NotImplementedError()

    def remove_neuron(self, index):
        raise NotImplementedError()

    def process(self):
        raise NotImplementedError()


class NeuralLevel(INeuralLevel):
    def __init__(self):
        self.index = int()
        self.neurons = list()

    def __getitem__(self, item):
        return self.neurons[item]

    def __iter__(self):
        return self.neurons.__iter__()

    def add_neuron(self, neuron):
        self.neurons.append(neuron)
        return neuron

    def process(self):
        for neuron in self.neurons:
            neuron.calculate_output()
            neuron.push_values_to_next_level()

    def remove_neuron(self, index):
        self.neurons.remove(self.neurons[index])