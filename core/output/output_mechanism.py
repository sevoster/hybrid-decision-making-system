from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject


class BFSOutputMechanism(QObject):
    """
    Represents core logic for analytic output
    """
    new_question = pyqtSignal(int, str, 'PyQt_PyObject')
    result_found = pyqtSignal(int, str)

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

    def __push_result(self, fact_id):
        self.result_found.emit(fact_id, self.knowledge.get_text_description(fact_id))
        pass

    def start(self):
        self.__push_new_question(self.working_memory.get_next_not_inited())
        pass

    # TODO: refactor
    def search_for_answer(self, answered):
        answer_value = self.working_memory.get_by_id(answered)
        rules = self.knowledge.get_rules_with_predecessor(answered)
        coeffs = [r.get_predecessor_coefficient(answered) for r in rules]
        diffs = [abs(c - answer_value) for c in coeffs]
        min_value = min(diffs)
        indices = [i for i, x in enumerate(diffs) if x == min_value]
        need_to_ask = set()
        for i in indices:
            rule = rules[i]
            predecessors = rule.predecessors
            for p in predecessors:
                if not self.working_memory.is_inited(p.id):
                    need_to_ask.add(p.id)
                pass
            pass
        if len(need_to_ask) == 0:
            # Try to find a result consequent
            suc_coefs = [rules[i].successor.coefficient for i in indices]
            min_coef = min(suc_coefs)
            result = rules[indices[suc_coefs.index(min_coef)]].successor.id
            self.__push_result(result)
        else:
            for f in need_to_ask:
                self.__push_new_question(f)
        pass

    def process_answer(self, fact_id, value):
        print("Get answer for {}: {}".format(fact_id, value))
        self.working_memory.set_by_id(fact_id, value)
        self.search_for_answer(fact_id)
        pass
