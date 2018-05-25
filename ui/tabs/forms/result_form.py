from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy

from ui.tabs.forms.separator import LineSeparator


class ResultView(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, fact_id, text, parent=None):
        super(QWidget, self).__init__(parent)

        self.label = QLabel(text)
        self.label.setFont(QFont('Times', 14))
        self.label.setWordWrap(True)

        self.button = QPushButton("OK")
        self.button.clicked.connect(lambda: self.finished.emit(self))

        vbox = QVBoxLayout()
        vbox.addWidget(LineSeparator(self))
        vbox.addWidget(self.label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.button, alignment=Qt.AlignCenter)
        vbox.addWidget(LineSeparator(self))

        self.setLayout(vbox)
        pass
