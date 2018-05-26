from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont

from ui.tabs.forms.question_form import QuestionFormFixed, QuestionFormSlider
from ui.tabs.forms.result_form import ResultView
from ui.tabs.forms.separator import LineSeparator


class RunView(QWidget):
    explanation_requested = pyqtSignal()

    # TODO: please refactor ASAP
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.__layout = QVBoxLayout()

        self.__run_button = QPushButton("Run")
        self.__run_button.setShortcut("F5")

        self.__explanation_button = QPushButton("Explain")
        self.__explanation_button.setShortcut("F12")
        self.__explanation_button.clicked.connect(self.explanation_requested)

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

        self.__explanation_list = QVBoxLayout()
        self.__explanation_list.setSpacing(10)

        explanation_scroll_area = QScrollArea(self)
        explanation_scroll_area.setWidgetResizable(True)

        explanation_scroll_widget = QWidget(explanation_scroll_area)
        explanation_scroll_widget.setLayout(self.__explanation_list)
        explanation_scroll_area.setWidget(explanation_scroll_widget)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(hbox_layout)
        main_vbox.addWidget(explanation_scroll_area)

        button_group = QHBoxLayout()
        button_group.addWidget(self.__run_button, alignment=Qt.AlignCenter)
        button_group.addWidget(self.__explanation_button, alignment=Qt.AlignCenter)

        self.__layout.addLayout(button_group)
        self.__layout.addWidget(LineSeparator(self))
        self.__layout.addLayout(main_vbox)

        self.setLayout(self.__layout)
        pass

    def connect_run_button(self, callback):
        self.__run_button.clicked.connect(self.clean)
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

    def show_explanation(self, explanation_list):
        self.__clean_vertical_layout(self.__explanation_list)
        for text in explanation_list:
            label = QLabel(text)
            label.setFont(QFont('SanSerif', 11))
            self.__explanation_list.addWidget(label, alignment=Qt.AlignLeft)
        pass

    def __clean_vertical_layout(self, vbox_layout):
        for i in reversed(range(vbox_layout.count())):
            widget = vbox_layout.takeAt(i).widget()
            if widget is not None:
                vbox_layout.removeWidget(widget)
                widget.deleteLater()
            pass
        pass

    def clean(self):
        self.__clean_vertical_layout(self.__result_list)
        self.__clean_vertical_layout(self.__question_list)
        self.__clean_vertical_layout(self.__explanation_list)
        pass
