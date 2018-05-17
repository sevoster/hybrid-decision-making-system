from core.neural_network.NeuralNet.NeuralNet import NeuralNet
from core.neural_network.NeuralNet.NeuralLevel import NeuralLevel
from core.neural_network.NeuralNet.Neuron import Neuron
from core.neural_network.NeuralNet.Link import Link


class IBuildingStrategy:
    def build_net(self, building_data):
        raise NotImplementedError


class CoefsToWeightsBuilding(IBuildingStrategy):
    def __init__(self):
        self.nodes = []
        self.arcs = []

    @staticmethod
    def build_node_dictionary(nodes):
        node_dict = {}
        for node in nodes:
            node_dict[node['id']] = {
                'type': node['type'],
                'text': node['text'],
                'id': node['id']
            }
            if 'coefficient' in node:
                node_dict[node['id']]['coefficient'] = node['coefficient']
        return node_dict

    def build_net(self, building_data):
        self.neural_net = NeuralNet()

        self.nodes = self.build_node_dictionary(building_data['nodes'])
        self.arcs = building_data['links']

        # 1. добавляем все эллипсы на сенсорный слой

        for id in self.nodes:
            node = self.nodes[id]
            if node['type'] == 'ellipse':
                for arc in self.arcs:
                    if arc['source'] == id:
                        self.neural_net.sensor_level.add_neuron(
                            Neuron(id=id, sensor_weigth=arc['weight'], text=node['text'] + '|' + arc['weight']))

        for neuron in self.neural_net.sensor_level.get_neurons():
            for arc in self.arcs:
                if arc['source'] == neuron.id and arc['weight'] == neuron.sensor_weight:
                    self.traverse(sender=neuron, node=self.nodes[arc['target']],
                                  index=0, weight=arc['weight'])
        return self.neural_net

    def traverse(self, node, sender, index, weight):
        self.neural_net.print_net()
        if node['type'] == 'rectangle':
            if len(self.neural_net.levels) < index + 1:
                self.neural_net.levels.append(NeuralLevel())

            targets = self.get_targets_ids_by_id(node['id'])

            if len(targets) == 0:
                neuron = self.neural_net.levels[index].get_neuron_by_id(node['id'])
                if neuron:
                    sender.add_link(weight=weight, target=neuron)
                else:
                    m_neuron = self.neural_net.motor_layer.add_neuron(Neuron(id=node['id'] + 'm', text=node['text'],
                                                                             func=lambda x: x))

                    h_neuron = self.neural_net.levels[index].add_neuron(Neuron(id=node['id'], text=node['text']))
                    sender.add_link(weight=weight, target=h_neuron)
                    h_neuron.add_link(weight=node['coefficient'], target=m_neuron)

            else:
                neuron = self.neural_net.levels[index].get_neuron_by_id(node['id'])
                if neuron:
                    sender.add_link(weight=weight, target=neuron)
                else:
                    h_neuron = self.neural_net.levels[index].add_neuron(Neuron(id=node['id'], text=node['text']))
                    sender.add_link(weight=weight, target=h_neuron)
                    for arc in self.arcs:
                        if arc['source'] == h_neuron.id:
                            self.traverse(self.nodes[arc['target']], h_neuron, index + 1, node['coefficient'])
        else:
            for arc in self.arcs:
                if arc['source'] == node['id']:
                    self.traverse(self.nodes[arc['target']], sender, index, weight)

    def get_targets_ids_by_id(self, id):
        target_ids = []
        for arc in self.arcs:
            if arc['source'] == id:
                target_ids.append(id)
        return target_ids
