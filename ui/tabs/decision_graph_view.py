from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5 import QtCore


class DecisionGraphView(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Init with default message
        self.message_label = QLabel("Here will be your graph")
        self.message_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setWidget(self.message_label)

        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        pass

    # temporary
    def set_text(self, text):
        self.message_label.setText(text)
        pass

