class DTObject:
    def __init__(self):
        self.description = str()
        self.pos_x = 0
        self.pos_y = 0

    def draw(self, x,y):
        raise NotImplementedError()

    def set_description(self, description):
        raise NotImplementedError()


class DTRectangle(DTObject):
    def draw(self, x, y):
        raise NotImplementedError()

    def set_description(self, description):
        raise NotImplementedError()