import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow

app = QApplication([])
main_window = MainWindow()
sys.exit(app.exec_())
