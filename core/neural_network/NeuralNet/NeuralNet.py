class INeuralNet:

    def get_answer(self, input):
        raise NotImplementedError()

    def get_levels(self):
        raise NotImplementedError()


class NeuralNet(INeuralNet):

    def __init__(self):
        self.levels = list()
        self.answer = list()

    def get_answer(self, input):
        self.answer = list()

        # 1. устанавливаем входные значения для нейронов
        for i in range(len(input)):
            level = self.levels[0]
            neuron = level.get_neuron(i)
            neuron.increase_incoming_value(input[i])

        # 2. для каждого уровня вычисляем output нейронов и передаем его дальше
        for level in self.levels:
            level.process()

        # 3. результат в последнем слое
        for neuron in self.levels[len(self.levels) - 1]:
            self.answer.append(neuron.calculate_output())

        return self.answer

    def get_levels(self):
        return self.levels

    def print_answer(self):
        str = ''
        for value in self.answer:
            str += value
        print(str)
