from core.neural_network.NeuralNet.Link import Link
from math import e


class INeuron:
    def get_id(self):
        raise NotImplementedError()

    def get_links(self):
        raise NotImplementedError()

    def add_link(self, weight, target):
        raise NotImplementedError()

    def remove_link(self, target):
        raise NotImplementedError()

    def get_threshold(self):
        raise NotImplementedError()

    def set_threshold(self, threshold):
        raise NotImplementedError()

    def calculate_output(self, value=None):
        raise NotImplementedError()

    def push_values_to_next_level(self):
        raise NotImplementedError()

    def increase_incoming_value(self, income):
        raise NotImplementedError()


class Neuron(INeuron):
    def __init__(self, id, text='', links=None, threshold=0, param_a=1, func=None):
        self.links = links or []
        self.threshold = threshold
        self.param_a = param_a
        self.income = 0
        self.output = 0
        self.id = id
        self.text = text
        self.func = func
        if not self.func:
            self.func = self.sigmoid

    def get_id(self):
        return self.id

    def get_links(self):
        return self.links

    def add_link(self, weight, target):
        self.links.append(Link(weight, target))

    def remove_link(self, target):
        for link in self.links:
            if link.target == target:
                self.links.remove(link)
                return

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

    def sigmoid(self, value):
        return 1 / (1 + e ** (-self.param_a * (value - self.threshold)))

    def calculate_output(self, value=None):
        if value:
            self.output = self.func(value)
        else:
            self.output = self.func(self.income)
        return self.output

    def push_values_to_next_level(self):
        for link in self.links:
            if link.target:
                link.target.increase_incoming_value(self.output * link.weight)
        self.income = 0
        self.output = 0

    def increase_incoming_value(self, income):
        self.income += income

    def get_text(self):
        return self.text
