from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class StatisticView(QWidget):

	def __init__(self, parent=None):
		super(QWidget, self).__init__(parent)

		# TODO: implement
		self.layout = QVBoxLayout(self)

		message_label = QLabel()
		message_label.setText("Here will be statistics charts")
		self.layout.addWidget(message_label)
		self.setLayout(self.layout)
		pass
