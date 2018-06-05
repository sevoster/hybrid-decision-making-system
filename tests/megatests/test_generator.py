from core.neural_network.neural_net.neural_net import NeuralNet
from core.neural_network.builder.builder import Builder
from core.decision_system import DecisionSystem
import parser as p
import json
import random
import sys
import math
import time
import xml.etree.ElementTree as etree
import os

from core.knowledge.knowledge_base import FactType
from PyQt5.QtWidgets import (QWidget, QFileDialog, QPushButton, QApplication, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt


def generate_tests(number_of_tests, filename):
    builder = Builder()
    net = builder.build_net(builder.parse_json(filename))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    tests = []
    for i in range(number_of_tests):
        tests.append(list(zip(rules, [random.uniform(0, 1) for x in range(len(rules))])))

    with open('test.json', 'w') as testfile:
        testfile.write(json.dumps(tests))

    # print(*tests, sep='\n')


def generate_analytic_output(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
        pass

    with open('test.json', 'r') as file:
        inputs = json.loads(file.read())
        pass

    outputs = list()

    decision_system = DecisionSystem()
    decision_system.apply_decision_graph(graph_data)
    input_dict = {}
    decision_system.connect_to_user_interface(lambda id, text, callback: callback(str(id), input_dict[str(id)]),
                                              lambda id, text, value: output.append((str(id), value)))

    start = time.time()
    end = time.time()
    start = time.time()
    for input_data in inputs:
        input_dict = {e[0]: e[1] for e in input_data}
        output = list()

        decision_system.start_output()

        outputs.append(output)
        pass
    end = time.time() - start
    # print(outputs)
    print('ANALYTIC TIME: {}'.format(end))
    with open('analytic_output.json', 'w') as result_file:
        json.dump(outputs, result_file)
    pass


def generate_neural_outputs(filename):
    builder = Builder()
    net = builder.build_net(builder.parse_json(filename))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    inputs = None
    with open('test.json', 'r') as file:
        inputs = json.loads(file.read())

    outputs = list()

    start = time.time()
    for input in inputs:
        neural_input = list()
        for neuron in net.sensor_level:
            for rule, value in input:
                if neuron.rule == rule:
                    neural_input.append(value)

        motor_neurons = net.motor_layer.neurons
        # print(input)

        outputs.append(list(zip([n.id[0:-1] for n in motor_neurons], net.get_answer(neural_input))))

    print('NEURAL TIME: {}'.format(time.time()-start))

    # print(*outputs,sep = '\n')
    with open('neural_output.json', 'w') as file:
        file.write(json.dumps(outputs))


def get_stats(filename):
    builder = Builder()
    net = builder.build_net(builder.parse_json(filename))
    rules = set()
    for neuron in net.sensor_level:
        rules.add(neuron.rule)

    input = []
    neural_answer = []
    analytic_answer = []

    with open('test.json', 'r') as file:
        input = json.loads(file.read())

    with open('neural_output.json', 'r') as file:
        neural_answer = json.loads(file.read())

    with open('analytic_output.json', 'r') as file:
        analytic_answer = json.loads(file.read())

    # print(input,neural_answer,analytic_answer,sep='\n')

    for n_answer, a_answer in zip(neural_answer, analytic_answer):
        max_n = max_a = (-1, -1)
        for c in n_answer:
            if c[1] > max_n[1]:
                max_n = (c[0], c[1])
        for a in a_answer:
            if a[1] > max_a[1]:
                max_a = (a[0], a[1])
        print(
            '{};{};{};{}'.format(max_n, max_a, 'TRUE' if max_n[0] == max_a[0] else 'FALSE', 1- math.fabs(max_n[1]-max_a[1]) if max_n[0] == max_a[0] else ''))


# TODO: should be converter, not parser
class Parser(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = None
        self.__status_label = None
        self.init_ui()

    def init_ui(self):
        self.resize(300, 200)
        btn = QPushButton('Generate JSON', self)
        btn.clicked.connect(self.json_save_dialog)

        self.__layout = QVBoxLayout()
        self.__status_label = QLabel("Ready")
        self.__layout.addWidget(self.__status_label, alignment=Qt.AlignCenter)
        self.__layout.addWidget(btn)

        self.setLayout(self.__layout)
        self.show()

    def parse_xml(self, tree):
        json = {
            "directed": True,
            "multigraph": False,
            "graph": {},
            "nodes": [],
            "links": []
        }
        root = tree.getroot()
        for cell in root.iter('mxCell'):
            if 'source' in cell.attrib:
                json["links"].append({
                    "weight": cell.attrib['value'],
                    "source": cell.attrib['source'],
                    "target": cell.attrib['target']
                })
            elif 'style' in cell.attrib:
                if str(cell.attrib['style']).find('ellipse') != -1:
                    json["nodes"].append({
                        "text": cell.attrib['value'],
                        "type": FactType.Antecedent,
                        "id": cell.attrib['id']
                    })
                elif str(cell.attrib['style']).find('rounded=0') != -1:
                    coef = cell.attrib['value'][cell.attrib['value'].rindex('(') + 1:cell.attrib['value'].rindex(')')]
                    json["nodes"].append({
                        "text": cell.attrib['value'],
                        "type": FactType.Consequent,
                        "id": cell.attrib['id'],
                        "coefficient": coef
                    })

        return json

    def json_save_dialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Choose XML File', filter='*.xml')[0]
        if filename:
            # filename = os.path.basename(filename)
            tree = etree.parse(filename)
            result = json.dumps(self.parse_xml(tree), indent=4, ensure_ascii=False)
            filename = 'test_graph.json'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(result)
            generate_tests(100, filename)
            generate_neural_outputs(filename)
            generate_analytic_output(filename)
            get_stats(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Parser()
    sys.exit(app.exec_())

# get_stats('test_graph.json')
