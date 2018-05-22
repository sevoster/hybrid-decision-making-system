import xml.etree.ElementTree as etree
import os
import sys
import json
from PyQt5.QtWidgets import (QWidget,QFileDialog, QPushButton, QApplication)


class Parser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 200)
        btn = QPushButton('Generate JSON', self)
        btn.clicked.connect(self.json_save_dialog)
        btn.resize(btn.sizeHint())
        self.show()

    def json_save_dialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Choose XML File')[0]
        if filename:
            tree = etree.parse(filename)
            result = json.dumps(self.parse(tree), indent=4, ensure_ascii=False)
            saved = QFileDialog.getSaveFileName(self, 'Choose XML File',filter = '*.json')[0]
            if saved:
                with open(saved, 'w', encoding='utf-8') as file:
                    file.write(result)

    def parse(self,tree):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Parser()
    sys.exit(app.exec_())

