from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

from ui.tabs.decision_graph_view import DecisionGraphView
from ui.tabs.run_view import RunView
from ui.tabs.statistics_view import StatisticView


class TabView(QWidget):
    explanation_requested = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # TODO: split into different classes
        # Init tabs
        self.tabs = QTabWidget()
        self.decision_tree_tab = DecisionGraphView()
        self.run_tab = RunView()
        self.statistics_tab = StatisticView()

        self.run_tab.explanation_requested.connect(self.explanation_requested)

        # Add tabs
        # self.tabs.addTab(self.decision_tree_tab, "Decision Tree")
        self.tabs.addTab(self.run_tab, "Run")
        self.tabs.addTab(self.statistics_tab, "Statistics")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        pass

    def display_expert_knowledge(self, decision_graph):
        self.decision_tree_tab.display(decision_graph)
        pass

    def show_explanation(self, explanation):
        self.run_tab.show_explanation(explanation)
        pass

    def clean(self):
        self.run_tab.clean()
        pass
