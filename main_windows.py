import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.resize(800, 600)
        # TODO: remove
        self.statusBar().showMessage('Hello World!')

        self.setWindowTitle("Decision Maker")
        self.show()


if __name__ == '__main__':

    app = QApplication([])
    main_window = MainWindow()
    sys.exit(app.exec_())
