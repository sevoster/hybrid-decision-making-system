import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QAction, QFileDialog, QLabel,
                             QPushButton, QDesktopWidget, QApplication, QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtGui import QPixmap, QDrag, QFont
from PyQt5.QtCore import Qt, QMimeData

import core.neural_network.Sandbox.utils as utils

class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)


    def mouse_move_event(self, e):

        print(e.pos())
        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.label = Label(self)
        self.initUI()

    def initUI(self):
        utils.center_window(self)
        self.setAcceptDrops(True)
        self.resize(1024, 768)
        self.setWindowTitle('Drawer')

        self.create_json_button()

        self.label.setPixmap(QPixmap("res/ellips.png").scaled(400,200))
        self.label.move(100,100)
        self.show()

    def dragEnterEvent(self, e):
        print('drag')
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.label.move(position)
        print('drop',position)
        e.setDropAction(Qt.MoveAction)
        e.accept()

    def json_save_dialog(self):
        return QFileDialog.getSaveFileName(self, 'Open file', 'C:/')[0]


    def create_json_button(self):
        btn = QPushButton('Generate JSON', self)
        btn.clicked.connect(self.json_save_dialog)
        btn.resize(btn.sizeHint())
        return btn


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())
