from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject


class BFSOutputMechanism(QObject):
    """
    Represents core logic for analytic output
    """
    new_question = pyqtSignal(str)

    def __init__(self, working_memory, knowledge):
        super().__init__()
        self.fact_queue = Queue()
        self.used = list()
        self.working_memory = working_memory
        self.knowledge = knowledge
        pass

    def start(self):
        for fact in self.working_memory.memory:
            self.new_question.emit(self.knowledge.get_text_description(fact.id))
        pass

    def on_answer(self, id, value):
        print("Get answer for {}: {}".format(id, value))
        pass
