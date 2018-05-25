from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont

from ui.tabs.forms.question_form import QuestionFormFixed, QuestionFormSlider
from ui.tabs.forms.result_form import ResultView


class RunView(QWidget):
    # TODO: please refactor
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = QVBoxLayout()

        self.__run_button = QPushButton("Run")
        self.__run_button.setShortcut("F5")

        self.__question_list = QVBoxLayout()
        self.__question_list = QVBoxLayout()
        self.__result_list = QVBoxLayout()

        question_label = QLabel("Questions")
        question_label.setFont(QFont('Veranda', 10))

        question_scroll_area = QScrollArea(self)
        question_scroll_area.setWidgetResizable(True)

        question_scroll_widget = QWidget(question_scroll_area)
        question_scroll_widget.setLayout(self.__question_list)
        question_scroll_area.setWidget(question_scroll_widget)

        vbox_question = QVBoxLayout()
        vbox_question.addWidget(question_label, alignment=Qt.AlignCenter)
        vbox_question.addWidget(question_scroll_area)

        result_label = QLabel("Conclusions")
        result_label.setFont(QFont('Veranda', 10))

        result_scroll_area = QScrollArea(self)
        result_scroll_area.setWidgetResizable(True)

        result_scroll_widget = QWidget(result_scroll_area)
        result_scroll_widget.setLayout(self.__result_list)
        result_scroll_area.setWidget(result_scroll_widget)

        vbox_result = QVBoxLayout()
        vbox_result.addWidget(result_label, alignment=Qt.AlignCenter)
        vbox_result.addWidget(result_scroll_area)

        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(vbox_question)
        hbox_layout.addLayout(vbox_result)
        self.__layout.addWidget(self.__run_button, alignment=Qt.AlignCenter)
        self.__layout.addLayout(hbox_layout)

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

    @pyqtSlot(QWidget)
    def remove_result(self, widget):
        self.__result_list.removeWidget(widget)
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
        result_form.finished.connect(self.remove_result)
        self.__result_list.addWidget(result_form)
        pass
