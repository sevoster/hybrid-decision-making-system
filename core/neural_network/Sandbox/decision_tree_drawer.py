import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QDesktopWidget, QApplication)
from PyQt5.QtGui import QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.resize(1024, 768)
        self.setWindowTitle('Drawer')
        self.center()
        self.create_buttons()
        self.show()

    def create_buttons(self):
        btn = QPushButton('Generate JSON', self)
        btn.resize(btn.sizeHint())
        btn.move(460,700)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Example()
    sys.exit(app.exec_())