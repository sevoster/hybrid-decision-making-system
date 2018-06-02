from core.neural_network.neural_net.neural_net import NeuralNet
from core.neural_network.builder.builder import Builder
from core.decision_system import DecisionSystem
import json
import random


def generate_tests(number_of_tests):
    builder = Builder()
    net = builder.build_net(builder.parse_json(''))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    tests = []
    for i in range(number_of_tests):
        tests.append(list(zip(rules, [random.uniform(0, 1) for x in range(len(rules))])))

    with open('test', 'w') as testfile:
        testfile.write(json.dumps(tests))

    # print(*tests, sep='\n')


def generate_analytic_output():
    with open('SimpleTest.json', 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
        pass

    with open('test', 'r') as file:
        inputs = json.loads(file.read())
        pass

    outputs = list()

    decision_system = DecisionSystem()
    decision_system.apply_decision_graph(graph_data)
    input_dict = {}
    decision_system.connect_to_user_interface(lambda id, text, callback: callback(str(id), input_dict[str(id)]),
                                              lambda id, text, value: output.append((str(id), value)))

    for input_data in inputs:
        input_dict = {e[0]: e[1] for e in input_data}
        output = list()
        decision_system.start_output()
        outputs.append(output)
        pass
    # print(outputs)
    with open('analytic_output.json', 'w') as result_file:
        json.dump(outputs, result_file)
    pass


def generate_neural_outputs():
    builder = Builder()
    net = builder.build_net(builder.parse_json(''))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    inputs = None
    with open('test', 'r') as file:
        inputs = json.loads(file.read())

    outputs = list()

    for input in inputs:
        neural_input = list()
        for neuron in net.sensor_level:
            for rule, value in input:
                if neuron.rule == rule:
                    neural_input.append(value)

        motor_neurons = net.motor_layer.neurons
        print(input)
        outputs.append(list(zip([n.id[0:-1] for n in motor_neurons], net.get_answer(neural_input))))

    print(*outputs,sep = '\n')
    with open('neural_output','w') as file:
        file.write(json.dumps(outputs))


def generate_test_values(number_of_tests, graph_filename):
    builder = Builder()
    net = builder.build_net(builder.parse_json(''))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    input_values = list(zip(rules, [random.uniform(0, 1) for x in range(len(rules))]))
    print(input_values)
    neural_input = list()
    for rule, value in input_values:
        for neuron in net.sensor_level:
            if neuron.rule == rule:
                neural_input.append(value)

    # print(neural_input)

    motor_neurons = net.motor_layer.neurons
    print(list(zip([n.id[0:-1] for n in motor_neurons], net.get_answer(neural_input))))


# generate_test_values(5, '')

generate_tests(7)
generate_neural_outputs()
generate_analytic_output()
