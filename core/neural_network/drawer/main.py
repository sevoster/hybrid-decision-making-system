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


def create_arrow(empty_link, neuron, link, ids):
    line = copy.deepcopy(empty_link)
    line.attrib['source'] = neuron.id
    line.attrib['target'] = link.target.id
    line.attrib['value'] = str(link.weight)
    line_id = get_random_id(None, ids)
    line.attrib['id'] = line_id
    return line


def create_circle(empty_neuron, neuron, x, y=None):
    circle = copy.deepcopy(empty_neuron)
    circle.attrib['id'] = neuron.id
    circle.attrib['value'] = neuron.text
    geometry = circle.find('mxGeometry')
    geometry.attrib['x'] = str(x)
    if y:
        geometry.attrib['y'] = str(y)
    return circle


def draw_net(neural_net):
    ids = set()

    for neuron in neural_net.sensor_level:
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

    for x, neuron in enumerate(neural_net.sensor_level):
        root.append(create_circle(empty_neuron, neuron, 40 + 440 * x))
        for link in neuron:
            root.append(create_arrow(empty_link, neuron, link, ids))

    y_motor = 1
    for y, layer in enumerate(neural_net.levels):
        for x, neuron in enumerate(layer):
            root.append(create_circle(empty_neuron, neuron, 40 + 360 * x, 440 + 400 * y))
            for link in neuron:
                root.append(create_arrow(empty_link, neuron, link, ids))
        y_motor = y + 1

    for x, neuron in enumerate(neural_net.motor_layer):
        root.append(create_circle(empty_neuron, neuron, 400 * x + x * x * 10, 840 * y_motor))
        for link in neuron:
            root.append(create_arrow(empty_link, neuron, link, ids))

    tree.write('output.xml', encoding='utf-8')
