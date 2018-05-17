class INeuralLevel:
    def get_neurons(self):
        raise NotImplementedError()

    def get_index(self):
        raise NotImplementedError()

    def get_neuron(self,index):
        raise NotImplementedError()

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

    def get_neurons(self):
        return self.neurons

    def get_neuron_by_id(self, id):
        for neuron in self.neurons:
            if neuron['id'] == id:
                return neuron

    def get_index(self):
        return self.index

    def get_neuron(self,index):
        return self.neurons[index]

    def add_neuron(self, neuron):
        self.neurons.append(neuron)
        return neuron

    def process(self):
        for neuron in self.neurons:
            neuron.calculate_output()
            neuron.push_values_to_next_level()

    def remove_neuron(self, index):
        self.neurons.remove(self.neurons[index])