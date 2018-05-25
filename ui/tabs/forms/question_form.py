from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QFrame, QButtonGroup, \
    QAbstractButton, QTextEdit, QSizePolicy

from ui.tabs.forms.separator import LineSeparator


class QuestionFormFixed(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, fact_id, text, answers, calllback=None, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = QVBoxLayout()
        self.fact_id = fact_id
        self.text = text
        self.callback = calllback

        text_label = QLabel(text)
        text_label.setFont(QFont('Times', 12))
        text_label.setWordWrap(True)

        button_group = QButtonGroup(self)
        button_group.buttonClicked['QAbstractButton *'].connect(self.on_clicked)

        self.__layout.addWidget(LineSeparator(self))
        self.__layout.addWidget(text_label, alignment=Qt.AlignCenter)

        for answer in answers:
            button = QPushButton(str(answer))
            button_group.addButton(button)
            self.__layout.addWidget(button, alignment=Qt.AlignCenter)
            pass
        self.__layout.addWidget(LineSeparator(self))
        self.setLayout(self.__layout)
        pass

    @pyqtSlot(QAbstractButton)
    def on_clicked(self, button):
        if self.callback is not None:
            self.callback(self.fact_id, float(button.text()))
        self.finished.emit(self)
        pass


class QuestionFormSlider(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, fact_id, text, callback=None, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = QVBoxLayout()
        self.fact_id = fact_id
        self.text = text
        self.callback = callback

        question_label = QLabel(text)
        question_label.setFont(QFont('Times', 12))

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10000)
        self.slider.valueChanged.connect(self.slider_position_changed)

        self.value_label = QTextEdit(str(self.slider.value()))
        self.value_label.setMaximumHeight(30)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.on_clicked)

        self.__layout.addWidget(question_label, alignment=Qt.AlignCenter)
        self.__layout.addWidget(self.slider)
        self.__layout.addWidget(self.value_label, alignment=Qt.AlignCenter)
        self.__layout.addWidget(self.send_btn, alignment=Qt.AlignCenter)

        self.setLayout(self.__layout)
        pass

    def on_clicked(self):
        if self.callback is not None:
            self.callback(self.fact_id, self.get_value())
        self.finished.emit(self)
        pass

    def get_value(self):
        return float(self.value_label.toPlainText())

    def get_range(self):
        return self.slider.maximum() - self.slider.minimum()

    def slider_position_changed(self):
        self.value_label.setText(str(self.slider.value() / self.get_range()))
        pass