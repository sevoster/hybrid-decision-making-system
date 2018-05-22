class ILink:
    def get_weight(self):
        raise NotImplementedError()

    def set_weight(self, weight):
        raise NotImplementedError()

    def get_target(self):
        raise NotImplementedError()

    def set_target(self, target):
        raise NotImplementedError()


class Link(ILink):
    def __init__(self, weight=0, target=None):
        self.weight = weight
        self.target = target

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target
