import json
from enum import Enum

import os.path
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QFileDialog, QMessageBox

from core.decision_system import DecisionSystem
from ui.tabs_view import TabView


class MainWindow(QMainWindow):
    class MessageType(Enum):
        Error = 1,
        Warning = 2,
        Info = 3

    def __init__(self):
        super().__init__()

        self.decision_system = DecisionSystem()
        self.tab_view = TabView(self)

        self.tab_view.explanation_requested.connect(self.decision_system.get_explanation)
        self.decision_system.explanation_deliver.connect(self.tab_view.show_explanation)

        self.tab_view.run_tab.connect_run_button(self.decision_system.start_output)
        self.decision_system.connect_to_user_interface(self.tab_view.run_tab.add_question_with_answers, self.tab_view.run_tab.show_result)

        self.setup_ui()

        pass

    def setup_ui(self):
        self.resize(800, 600)
        self.init_menu()

        self.statusBar().showMessage('Ready to start')

        self.setWindowTitle("Decision Maker")
        self.setCentralWidget(self.tab_view)
        self.show()
        pass

    def init_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu('&File')

        # Exit menu item
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)

        # Import file menu item
        import_action = QAction('&Import', self)
        import_action.setShortcut('Ctrl+I')
        import_action.setStatusTip('Import file')
        import_action.triggered.connect(self.import_file)

        file_menu.addAction(import_action)
        file_menu.addAction(exit_action)
        pass

    def show_message(self, content, msg_type):
        if msg_type == self.MessageType.Error:
            QMessageBox.critical(self, 'Error', content)
        pass

    def status_bar_message(self, text):
        self.statusBar().showMessage(text)
        pass

    # Only one json format is supported
    # TODO: move logic in parsers
    def import_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Import decision tree file', filter="JSON files (*.json)")[0]
        if not file_name:
            return

        if not os.path.isfile(file_name):
            self.show_message('File does not exist: ' + file_name, self.MessageType.Error)
            return

        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                json_content = json.load(f)
            except json.JSONDecodeError as e:
                self.show_message("Error while parsing JSON: " + e.msg, self.MessageType.Error)
                return

        self.decision_system.apply_decision_graph(json_content)
        self.tab_view.clean()
        self.tab_view.display_expert_knowledge(json_content)

        self.status_bar_message("SUCCESS: Import decision graph")
        pass
