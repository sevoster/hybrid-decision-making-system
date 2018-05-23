from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject


class BFSOutputMechanism(QObject):
    """
    Represents core logic for analytic output
    """
    new_question = pyqtSignal(int, str, 'PyQt_PyObject')

    def __init__(self, working_memory, knowledge):
        super().__init__()
        self.fact_queue = Queue()
        self.used = list()
        self.working_memory = working_memory
        self.knowledge = knowledge
        pass

    def __push_new_question(self, fact_id):
        self.new_question.emit(fact_id, self.knowledge.get_text_description(fact_id), self.process_answer)
        pass

    def start(self):
        self.__push_new_question(self.working_memory.get_next_not_inited())
        pass

    def get_facts_to_ask(self, answered):
        rules = self.knowledge.get_rules_with_predecessor(answered)
        return []

    def process_answer(self, fact_id, value):
        print("Get answer for {}: {}".format(fact_id, value))
        self.working_memory.set_by_id(fact_id, value)
        next_facts = self.get_facts_to_ask(fact_id)
        for fact in next_facts:
            self.__push_new_question(fact)
        pass
