import json
import core.neural_network.builder.building_strategy as BuildingStrategy
from core.neural_network.drawer.main import draw_net


class IBuilder:
    def build_net(self, building_data):
        raise NotImplementedError()


class Builder(IBuilder):
    def __init__(self, building_strategy=BuildingStrategy.CoefsToWeightsBuilding()):
        self.building_strategy = building_strategy
        self.building_data = {}

    def build_net(self, building_data):
        return self.building_strategy.build_net(building_data)

    def parse_json(self, path='SimpleTest.json' ):
        with open(path, 'r', encoding='utf-8') as file:
            read_data = file.read()
            self.building_data = json.loads(read_data)
        return self.building_data


builder = Builder()
net = builder.build_net(builder.parse_json())
net.print_net()
draw_net(net)