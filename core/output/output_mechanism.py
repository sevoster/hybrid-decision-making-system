from queue import Queue

from PyQt5.QtCore import pyqtSignal, QObject


class BFSOutputMechanism(QObject):
    """
    Represents core logic for analytic output
    """
    new_question = pyqtSignal(int, str, list, 'PyQt_PyObject')
    result_found = pyqtSignal(int, str)

    def __init__(self, working_memory, knowledge):
        super().__init__()
        self.fact_queue = Queue()
        self.used = list()
        self.pushed = list()
        self.working_memory = working_memory
        self.knowledge = knowledge
        pass

    def __push_new_question(self, fact_id):
        if fact_id in self.pushed:
            return
        self.pushed.append(fact_id)
        text = self.knowledge.get_text_description(fact_id)
        answers = self.knowledge.get_fact_by_id(fact_id)['out']
        self.new_question.emit(fact_id, text, answers, self.process_answer)
        pass

    def __push_result(self, fact_id):
        if fact_id in self.pushed:
            return
        self.pushed.append(fact_id)
        self.result_found.emit(fact_id, self.knowledge.get_text_description(fact_id))
        pass

    def __clean(self):
        self.pushed = list()
        self.fact_queue = Queue()
        self.used = list()
        pass

    def start(self):
        self.__clean()
        self.fact_queue.put(self.working_memory.get_next_not_inited())
        self.__push_new_question(self.working_memory.get_next_not_inited())
        pass

    def main_cycle(self):
        next_fact_id = self.fact_queue.get()
        rules = self.knowledge.get_rules_with_predecessor(next_fact_id)
        for rule in rules:
            satisfied = self.__is_satisfied(rule.predecessors)
            if not satisfied:
                continue
            # TODO: array of activated rules id (need id for rules, check Mongo)
            consequent = rule.successor.id
            is_intermediate = self.__is_intermediate_consequent(consequent)
            if not is_intermediate:
                self.__push_result(consequent)
                return
            self.fact_queue.put(consequent)
            self.working_memory.set_value_by_id(consequent, rule.successor.coefficient)
        pass

    def __is_satisfied(self, predecessors):
        for predecessor in predecessors:
            fact_id = predecessor.id
            coefficient = predecessor.coefficient
            if not self.working_memory.is_inited(fact_id):
                self.__push_new_question(fact_id)
                return False
            if abs(coefficient - self.working_memory.get_value_by_id(fact_id)) > 0.001:
                return False
        return True

    def __is_intermediate_consequent(self, consequent_id):
        # TODO: check for it automatically?
        return self.knowledge.get_fact_by_id(consequent_id)['type'] == 'ic'  # hardcoded now, need types!

    def process_answer(self, fact_id, value):
        print("Get answer for {}: {}".format(fact_id, value))
        self.working_memory.set_value_by_id(fact_id, value)
        self.fact_queue.put(fact_id)
        self.main_cycle()
        pass
