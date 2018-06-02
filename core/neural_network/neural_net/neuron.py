from core.neural_network.neural_net.link import Link
from math import e
import copy


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

    def calculate_output(self, value=None):
        raise NotImplementedError()

    def push_values_to_next_level(self):
        raise NotImplementedError()

    def increase_incoming_value(self, income):
        raise NotImplementedError()


class Neuron(INeuron):
    def __init__(self, id, text='', rule=None, links=None, threshold=0.5, param_a=3, func=None, sensor_weigth=''):
        self.links = links or []
        self.threshold = threshold
        self.param_a = param_a
        self.income = 0
        self.output = 0
        self.id = id
        self.rule = rule
        self.text = text
        self.func = copy.deepcopy(func)
        self.sensor_weight = sensor_weigth
        if not self.func:
            self.func = self.sigmoid

    def __getitem__(self, item):
        return self.links[item]

    def __iter__(self):
        return self.links.__iter__()

    def add_link(self, weight, target):
        self.links.append(Link(weight, target))

    def remove_link(self, target):
        for link in self.links:
            if link.target == target:
                self.links.remove(link)
                return

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
                link.target.increase_incoming_value(self.output * float(link.weight))
        self.income = 0
        self.output = 0

    def increase_incoming_value(self, income):
        self.income += income
