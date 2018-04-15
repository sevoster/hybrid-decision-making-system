import os.path
from enum import Enum

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QFileDialog, QMessageBox

from core.decision_system import DecisionSystem


class MainWindow(QMainWindow):
    class MessageType(Enum):
        Error = 1,
        Warning = 2,
        Info = 3

    def __init__(self):
        super().__init__()

        self.decision_system = DecisionSystem()

        self.setup_ui()

        pass

    def setup_ui(self):
        self.resize(800, 600)
        self.init_menu()
        # TODO: remove
        self.statusBar().showMessage('Hello World!')

        self.setWindowTitle("Decision Maker")
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

    def show_message(self, content, type):
        if type == self.MessageType.Error:
            QMessageBox.critical(self, 'Error', content)
        pass

    def import_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Import decision tree file', filter="JSON files (*.json)")[0]
        if not file_name:
            return

        if not os.path.isfile(file_name):
            self.show_message('File does not exist: ' + file_name, self.MessageType.Error)
            return

        # TODO: apply new rules from file into decision system

        pass
