from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

from ui.forms.separator import LineSeparator


class ResultView(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, fact_id, text, value=None, parent=None):
        super(QWidget, self).__init__(parent)

        self.fact_id = fact_id

        self.label = QLabel(text)
        self.label.setFont(QFont('Times', 14))
        if value is not None:
            self.score_label = QLabel("Score: {0:.3f}".format(value))
            self.score_label.setFont(QFont('SanSerif', 11))
            pass
        # self.label.setWordWrap(True)

        self.button = QPushButton("OK")
        self.button.clicked.connect(lambda: self.finished.emit(self))

        main_layout = QVBoxLayout()
        main_layout.addWidget(LineSeparator(self))
        main_layout.addSpacing(10)
        main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        if self.score_label is not None:
            main_layout.addSpacing(10)
            main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)
            main_layout.addSpacing(30)
        else:
            main_layout.addSpacing(50)
        main_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        main_layout.addSpacing(10)
        main_layout.addWidget(LineSeparator(self))

        self.setLayout(main_layout)
        pass
