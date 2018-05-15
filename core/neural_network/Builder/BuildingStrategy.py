class IBuildingStrategy:
    def build_net(self, building_data):
        raise NotImplementedError


class CoefsToWeightsBuilding(IBuildingStrategy):
    def build_net(self, building_data):
        param_a = 1
        threshold = 0
        pass