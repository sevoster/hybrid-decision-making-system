import xml.etree.ElementTree as etree
import copy
import random


def get_random_id(id, ids):
    result = id
    if not result:
        result = str(random.randint(2000, 300000))
    while result in ids:
        result = str(random.randint(2000, 300000))
    ids.add(result)
    return result


def draw_net(neural_net):
    ids = set()

    for neuron in neural_net.sensor_level.get_neurons():
        neuron.id = get_random_id(neuron.id, ids)

    tree = etree.parse('Empty.xml')
    root = tree.getroot().find('root')
    empty_neuron = None
    empty_link = None
    ec = None
    el = None
    for cell in root.iter('mxCell'):
        if 'style' in cell.attrib:
            if str(cell.attrib['style']).find('ellipse') != -1:
                empty_neuron = copy.deepcopy(cell)
                ec = cell
            elif str(cell.attrib['style']).find('endArrow') != -1:
                empty_link = copy.deepcopy(cell)
                el = cell
    root.remove(ec)
    root.remove(el)

    for x, neuron in enumerate(neural_net.sensor_level.get_neurons()):
        circle = copy.deepcopy(empty_neuron)
        circle.attrib['id'] = neuron.id
        circle.attrib['value'] = neuron.text
        geometry = circle.find('mxGeometry')
        geometry.attrib['x'] = str(40 + 440 * x)
        root.append(circle)

        for link in neuron.get_links():
            line = copy.deepcopy(empty_link)
            line.attrib['source'] = neuron.id
            line.attrib['target'] = link.target.id
            line.attrib['value'] = link.weight
            line_id = get_random_id(None, ids)
            line.attrib['id'] = line_id
            root.append(line)

    y_motor = 1
    for y, layer in enumerate(neural_net.levels):
        for x, neuron in enumerate(layer.get_neurons()):
            circle = copy.deepcopy(empty_neuron)
            circle.attrib['id'] = neuron.id
            circle.attrib['value'] = neuron.text
            geometry = circle.find('mxGeometry')
            geometry.attrib['x'] = str(40 + 360 * x)
            geometry.attrib['y'] = str(440 + 400 * y)
            root.append(circle)
            for link in neuron.get_links():
                line = copy.deepcopy(empty_link)
                line.attrib['source'] = neuron.id
                line.attrib['target'] = link.target.id
                line.attrib['value'] = link.weight
                line_id = get_random_id(None, ids)
                line.attrib['id'] = line_id
                root.append(line)
        y_motor = y + 1

    for x, neuron in enumerate(neural_net.motor_layer.get_neurons()):
        circle = copy.deepcopy(empty_neuron)
        circle.attrib['id'] = neuron.id
        circle.attrib['value'] = neuron.text
        geometry = circle.find('mxGeometry')
        geometry.attrib['x'] = str(40 + 360 * x + x * x * 10)
        geometry.attrib['y'] = str(440 + 400 * y_motor)
        root.append(circle)
        for link in neuron.get_links():
            line = copy.deepcopy(empty_link)
            line.attrib['source'] = neuron.id
            line.attrib['target'] = link.target.id
            line.attrib['value'] = link.weight
            line_id = get_random_id(None, ids)
            line.attrib['id'] = line_id
            root.append(line)

    tree.write('output.xml', encoding='utf-8')
