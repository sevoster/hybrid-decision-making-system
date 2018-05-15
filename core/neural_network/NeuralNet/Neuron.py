from core.neural_network.NeuralNet.Link import Link
from math import e


class INeuron:
    def get_links(self):
        raise NotImplementedError()

    def add_links(self, weight, target):
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
    def __init__(self, links=None, threshold=0, param_a=0):
        self.links = links or []
        self.threshold = threshold
        self.param_a = param_a
        self.income = 0
        self.output = 0

    def get_links(self):
        return self.links

    def add_links(self, weight, target):
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

    def calculate_output(self, value=None):
        if value:
            self.output = 1 / (1 + e ** (-self.param_a * (value - self.threshold)))
        else:
            self.output = 1 / (1 + e ** (-self.param_a * (self.income - self.threshold)))
        return self.output

    def push_values_to_next_level(self):
        for link in self.links:
            if link.target:
                link.target.increase_incoming_value(self.output * link.weight)
        self.income = 0
        self.output = 0

    def increase_incoming_value(self, income):
        self.income += income
