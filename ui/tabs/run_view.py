from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QSizePolicy, QSplitter, QAction

from ui.forms.question_form import QuestionFormFixed, QuestionFormSlider
from ui.forms.result_form import ResultView


class RunView(QWidget):

    # TODO: please refactor ASAP!
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.__layout = QVBoxLayout()

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

        hbox_layout = QSplitter()
        qu_widget = QWidget(self)
        qu_widget.setLayout(vbox_question)
        re_widget = QWidget(self)
        re_widget.setLayout(vbox_result)
        hbox_layout.addWidget(qu_widget)
        hbox_layout.addWidget(re_widget)

        self.__explanation_list = QVBoxLayout()
        self.__explanation_list.setSpacing(10)

        self.explanation_scroll_area = QScrollArea(self)
        self.explanation_scroll_area.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.explanation_scroll_area.setWidgetResizable(True)
        self.explanation_scroll_area.setVisible(False)

        explanation_scroll_widget = QWidget(self.explanation_scroll_area)
        explanation_scroll_widget.setLayout(self.__explanation_list)
        self.explanation_scroll_area.setWidget(explanation_scroll_widget)

        main_vbox = QSplitter(Qt.Vertical)
        main_vbox.addWidget(hbox_layout)
        main_vbox.addWidget(self.explanation_scroll_area)

        self.__layout.addWidget(main_vbox)

        self.setLayout(self.__layout)
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
        new_form.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        new_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(new_form, alignment=Qt.AlignTop)
        pass

    def add_question_with_answers(self, fact_id, text, answers, callback=None):
        new_form = QuestionFormFixed(fact_id, text, answers, callback)
        new_form.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        new_form.finished.connect(self.remove_question)
        self.__question_list.addWidget(new_form, alignment=Qt.AlignTop)
        pass

    def show_result(self, fact_id, text):
        result_form = ResultView(fact_id, text)
        result_form.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        result_form.finished.connect(self.remove_result)
        self.__result_list.addWidget(result_form, alignment=Qt.AlignTop)
        pass

    def set_explanation_visible(self, value):
        self.explanation_scroll_area.setVisible(value)
        pass

    def show_explanation(self, explanation_list):
        self.__clean_vertical_layout(self.__explanation_list)
        self.set_explanation_visible(True)
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
        self.set_explanation_visible(False)
        self.__clean_vertical_layout(self.__result_list)
        self.__clean_vertical_layout(self.__question_list)
        self.__clean_vertical_layout(self.__explanation_list)
        pass
