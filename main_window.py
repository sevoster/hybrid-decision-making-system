from PyQt5.QtWidgets import QMainWindow, QAction, qApp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        file_menu.addAction(exit_action)

        pass
