import unittest
import random
from core.neural_network.neural_net.neuron import Neuron


class NeuronTest(unittest.TestCase):
    def test_zero_calculate_output(self):
        neuron = Neuron(id=random.randint(0, 300000), threshold=0, param_a=1)
        self.assertEqual(neuron.calculate_output(0), 0.5)

    def test_simple_calculate_output(self):
        neuron = Neuron(id=random.randint(0, 300000), threshold=1, param_a=2)
        self.assertEqual(round(neuron.calculate_output(0), 3), 0.119)

    def test_simple_push_values_to_next_level(self):
        neuron_0 = Neuron(id=random.randint(0, 300000), threshold=0, param_a=1)
        neuron_0_a = Neuron(id=random.randint(0, 300000), threshold=0, param_a=1)
        neuron_1 = Neuron(id=random.randint(0, 300000), threshold=1, param_a=2)

        neuron_0.add_link(1, neuron_1)
        neuron_0_a.add_link(1, neuron_1)

        neuron_0.increase_incoming_value(1)
        neuron_0.calculate_output()

        neuron_0_a.increase_incoming_value(1)
        neuron_0_a.calculate_output()

        neuron_0.push_values_to_next_level()
        neuron_0_a.push_values_to_next_level()

        self.assertEqual(round(neuron_1.calculate_output(), 3), 0.716)

    def test_half_link_mult_push_values_to_next_level(self):
        neuron_0 = Neuron(id=random.randint(0, 300000), threshold=0, param_a=1)
        neuron_0_a = Neuron(id=random.randint(0, 300000), threshold=0, param_a=1)
        neuron_1 = Neuron(id=random.randint(0, 300000), threshold=1, param_a=2)

        neuron_0.add_link(0.5, neuron_1)
        neuron_0_a.add_link(0.5, neuron_1)

        neuron_0.increase_incoming_value(1)
        neuron_0.calculate_output()

        neuron_0_a.increase_incoming_value(1)
        neuron_0_a.calculate_output()

        neuron_0.push_values_to_next_level()
        neuron_0_a.push_values_to_next_level()

        self.assertEqual(round(neuron_1.calculate_output(), 3), 0.369)


if __name__ == '__main__':
    unittest.main()
