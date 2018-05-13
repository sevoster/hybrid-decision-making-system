import json

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea


class DecisionGraphView(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Init with default message
        self.message_label = QLabel("Please import file with decision tree")
        self.message_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.message_label.setFont(QFont("Veranda", 14, QFont.Decorative))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setWidget(self.message_label)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        pass

    def display(self, decision_graph):
        pretty = json.dumps(decision_graph, indent=4)
        self.message_label.setText(pretty)
        pass
