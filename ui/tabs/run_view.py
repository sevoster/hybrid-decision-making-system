from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QScrollArea, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


class QuestionForm(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, text, callback=None, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = QVBoxLayout()
        self.text = text
        self.callback = callback

        question_label = QLabel(text)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10000)
        self.slider.valueChanged.connect(self.slider_position_changed)

        self.value_label = QLabel(str(self.slider.value()))

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
            self.callback(self.slider.value())
        self.finished.emit(self)
        pass

    def slider_position_changed(self):
        self.value_label.setText(str(self.slider.value() / (self.slider.maximum() - self.slider.minimum())))
        pass


class LineSeparator(QFrame):
    def __init__(self, parent=None):
        super(QFrame, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        pass


class RunView(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        # TODO: implement
        self.__layout = QVBoxLayout()

        self.__run_button = QPushButton("Run")

        self.__question_list = QVBoxLayout()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_widget = QWidget(scroll_area)
        scroll_widget.setLayout(self.__question_list)
        scroll_area.setWidget(scroll_widget)

        self.__layout.addWidget(self.__run_button, alignment=Qt.AlignCenter)
        self.__layout.addWidget(scroll_area)

        self.setLayout(self.__layout)
        pass

    def connect_run_button(self, callback):
        self.__run_button.clicked.connect(callback)
        pass

    @pyqtSlot(QWidget)
    def remove_question(self, widget):
        self.__question_list.removeWidget(widget)
        widget.deleteLater()
        pass

    def add_question(self, text, callback=None):
        new_form = QuestionForm(text, callback)
        new_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(new_form)
        pass
