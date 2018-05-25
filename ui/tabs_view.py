from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from ui.tabs.decision_graph_view import DecisionGraphView
from ui.tabs.run_view import RunView
from ui.tabs.statistics_view import StatisticView


class TabView(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # TODO: split into different classes
        # Init tabs
        self.tabs = QTabWidget()
        self.decision_tree_tab = DecisionGraphView()
        self.run_tab = RunView()
        self.statistics_tab = StatisticView()

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
