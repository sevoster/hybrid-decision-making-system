import json
import sys
import xml.etree.ElementTree as etree

from PyQt5.QtWidgets import (QWidget, QFileDialog, QPushButton, QApplication, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt

from core.knowledge.knowledge_base import FactType


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

    def json_save_dialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Choose XML File')[0]
        if filename:
            self.__status_label.setText("Processing...")

            tree = etree.parse(filename)
            result = json.dumps(self.parse(tree), indent=4, ensure_ascii=False)
            saved = QFileDialog.getSaveFileName(self, 'Choose XML File', filter='*.json')[0]
            if saved:
                with open(saved, 'w', encoding='utf-8') as file:
                    file.write(result)
                self.__status_label.setText("Finished")
        pass

    def parse(self, tree):
        json = {
            "directed": True,
            "multigraph": False,
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
                        "type": FactType.Antecedent,
                        "id": cell.attrib['id']
                    })
                elif str(cell.attrib['style']).find('rounded=0') != -1:
                    coef = cell.attrib['value'][0:len(cell.attrib['value']) - 1].partition('(')[2]
                    json["nodes"].append({
                        "text": cell.attrib['value'],
                        "type": FactType.Consequent,
                        "id": cell.attrib['id'],
                        "coefficient": coef
                    })
                elif 'source' in cell.attrib:
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
