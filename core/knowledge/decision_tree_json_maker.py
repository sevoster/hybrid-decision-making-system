import xml.etree.ElementTree as etree
import os
import copy
import json

def parse(tree):
    json = {
        "directed": 'true',
        "multigraph": 'false',
        "graph": {},
        "nodes": [],
        "links": []
    }
    root = tree.getroot()
    for cell in root.iter('mxCell'):
        if 'style' in cell.attrib:
            if str(cell.attrib['style']).find('ellipse') != -1:
                json["nodes"].append({
                    "text": cell.attrib['value'],
                    "type": "ellipse",
                    "id": cell.attrib['id']
                })
            elif str(cell.attrib['style']).find('rounded=0') != -1:
                coef = cell.attrib['value'][0:len(cell.attrib['value'])-1].partition('(')[2]
                json["nodes"].append({
                    "text": cell.attrib['value'],
                    "type": "rectangle",
                    "id": cell.attrib['id'],
                    "coefficient": coef
                })
            elif str(cell.attrib['style']).find('endArrow') != -1:
                json["links"].append({
                    "weight": cell.attrib['value'],
                    "source": cell.attrib['source'],
                    "target": cell.attrib['target']
                })
    return json


filename = 'SimpleTest.xml'
tree = etree.parse(filename)
result = json.dumps(parse(tree), indent=4, ensure_ascii=False)
print(result)
with open('SimpleTest.json', 'w', encoding='utf-8') as file:
    file.write(result)
