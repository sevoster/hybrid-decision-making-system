from core.neural_network.neural_net.neural_level import NeuralLevel


class INeuralNet:
    def get_answer(self, input):
        raise NotImplementedError()


class NeuralNet(INeuralNet):
    def __init__(self):
        self.levels = list()
        self.answer = list()
        self.sensor_level = NeuralLevel()
        self.motor_layer = NeuralLevel()

    def get_answer(self, input):
        self.answer = list()

        for neuron in self.sensor_level:
            neuron.income = 0
            neuron.output = 0

        for neuron in self.motor_layer:
            neuron.income = 0
            neuron.output = 0

        for layer in self.levels:
            for neuron in layer:
                neuron.income = 0
                neuron.output = 0

        # 1. устанавливаем входные значения для нейронов
        for i, neuron in enumerate(self.sensor_level):
            neuron.increase_incoming_value(input[i])

        self.sensor_level.process()

        # 2. для каждого уровня вычисляем output нейронов и передаем его дальше
        for level in self.levels:
            level.process()

        # 3. результат в последнем слое
        for neuron in self.motor_layer:
            self.answer.append(neuron.calculate_output())

        return self.answer

    def print_answer(self):
        str = ''
        for value in self.answer:
            str += value
        print(str)

    def print_net(self):
        str = 'sensor: '
        for neuron in self.sensor_level:
            str += neuron.id + '('
            for link in neuron.links:
                str += '{}-{}; '.format(link.target.id, link.weight)
            str += ').........'
        print(str)

        for level in self.levels:
            str = 'hidden: '
            for neuron in level:
                str += neuron.id + '('
                for link in neuron.links:
                    str += '{}-{}; '.format(link.target.id,link.weight)
                str += ').........'
            print(str)

        str = 'motor: '
        for neuron in self.motor_layer:
            str += neuron.id + '('
            for link in neuron.links:
                str += '{}-{}; '.format(link.target.id, link.weight)
            str += ').........'
        print(str)
        print()