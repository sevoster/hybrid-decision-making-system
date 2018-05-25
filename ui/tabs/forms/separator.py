from PyQt5.QtWidgets import QFrame


class LineSeparator(QFrame):
    def __init__(self, parent=None):
        super(QFrame, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        pass
