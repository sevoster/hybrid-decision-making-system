from xml.dom import minidom
import xml.etree.ElementTree as etree
import os
import copy
import random


# etree.register_namespace('', 'http://schemas.microsoft.com/sqlserver/reporting/2008/01/reportdefinition')
# etree.register_namespace('rd', 'http://schemas.microsoft.com/SQLServer/reporting/reportdesigner')


# XmlUtils.print_all(nodes.getroot())

def draw_net(neural_net):

    ids = set()

    for neuron in neural_net.sensor_level.get_neurons():
        while neuron.id in ids:
            neuron.id = str(random.randint(2000,300000))
        ids.add(neuron.id)


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

    x = 0
    for neuron in neural_net.sensor_level.get_neurons():
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
            line_id = str(random.randint(2000,500000))
            while line_id in ids:
                line_id = str(random.randint(2000,500000))
            line.attrib['id'] = line_id
            root.append(line)
        x += 1

    y = 1
    for layer in neural_net.levels:
        x = 0
        for neuron in layer.get_neurons():
            circle = copy.deepcopy(empty_neuron)
            circle.attrib['id'] = neuron.id
            circle.attrib['value'] = neuron.text
            geometry = circle.find('mxGeometry')
            geometry.attrib['x'] = str(40 + 360 * x)
            geometry.attrib['y'] = str(40 + 400 * y)
            root.append(circle)
            for link in neuron.get_links():
                line = copy.deepcopy(empty_link)
                line.attrib['source'] = neuron.id
                line.attrib['target'] = link.target.id
                line.attrib['value'] = link.weight
                line_id = str(random.randint(2000, 500000))
                while line_id in ids:
                    line_id = str(random.randint(2000, 500000))
                line.attrib['id'] = line_id
                root.append(line)

            x += 1
        y += 1

    x = 0
    for neuron in neural_net.motor_layer.get_neurons():
        circle = copy.deepcopy(empty_neuron)
        circle.attrib['id'] = neuron.id
        circle.attrib['value'] = neuron.text
        geometry = circle.find('mxGeometry')
        geometry.attrib['x'] = str(40 + 360 * x + x*x*10)
        geometry.attrib['y'] = str(40 + 400 * y)
        root.append(circle)
        for link in neuron.get_links():
            line = copy.deepcopy(empty_link)
            line.attrib['source'] = neuron.id
            line.attrib['target'] = link.target.id
            line.attrib['value'] = link.weight
            line_id = str(random.randint(2000, 500000))
            while line_id in ids:
                line_id = str(random.randint(2000, 500000))
            line.attrib['id'] = line_id
            root.append(line)
        x += 1

    tree.write('output.xml', encoding='utf-8')
