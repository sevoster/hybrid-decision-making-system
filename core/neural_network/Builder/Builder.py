import json

class IBuilder:
    def build_net(self, building_data):
        raise NotImplementedError()


class Builder(IBuilder):
    def __init__(self, building_strategy):
        self.building_strategy = building_strategy

    def build_net(self, building_data):
        return self.building_strategy.build_net(building_data)

    def parse_json(self, path):
        building_data = {}
        with open('path') as file:
            read_data = file.read()
            building_data = json.loads(read_data)
