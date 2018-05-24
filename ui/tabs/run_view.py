from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QSlider, QScrollArea, QFrame, QTextEdit, \
    QButtonGroup, QAbstractButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot


class ResultView(QWidget):
    finished = pyqtSignal(QWidget)

    def __init__(self, fact_id, text, parent=None):
        super(QWidget, self).__init__(parent)

        self.label = QLabel(text)
        self.label.setFont(QFont('SansSerif', 14))

        self.button = QPushButton("OK")
        self.button.clicked.connect(lambda: self.finished.emit(self))

        vbox = QVBoxLayout()
        vbox.addWidget(self.label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.button, alignment=Qt.AlignCenter)

        self.setLayout(vbox)
        pass


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

        button_group = QButtonGroup(self)
        button_group.buttonClicked['QAbstractButton *'].connect(self.on_clicked)

        self.__layout.addWidget(text_label, alignment=Qt.AlignCenter)

        for answer in answers:
            button = QPushButton(str(answer))
            button_group.addButton(button)
            self.__layout.addWidget(button, alignment=Qt.AlignCenter)
            pass

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

    def add_question(self, fact_id, text, callback=None):
        new_form = QuestionFormSlider(fact_id, text, callback)
        new_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(new_form)
        pass

    def add_question_with_answers(self, fact_id, text, answers, callback=None):
        new_form = QuestionFormFixed(fact_id, text, answers, callback)
        new_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(new_form)
        pass

    def show_result(self, fact_id, text):
        result_form = ResultView(fact_id, text)
        result_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(result_form)
        pass
