from queue import Queue
from PyQt5.QtCore import pyqtSignal, QObject

from core.knowledge.knowledge_base import FactType


class BFSOutputMechanism(QObject):
    """
    Represents core logic for analytic output
    """
    MAX_COEFFICIENT_DIFF = 0.6
    ACCURACY = 0.001

    new_question = pyqtSignal(int, str, 'PyQt_PyObject')
    result_found = pyqtSignal(int, str, float)

    def __init__(self, working_memory, knowledge):
        super().__init__()
        self.fact_queue = Queue()
        self.triggered_rules = list()
        self.pushed = list()
        self.working_memory = working_memory
        self.knowledge = knowledge
        self.cycle_flag = False
        self.user_to_expert_min_diff = {}
        pass

    def __push_new_question(self, fact_id):
        if fact_id in self.pushed:
            return
        self.pushed.append(fact_id)
        text = self.knowledge.get_text_description(fact_id)
        self.new_question.emit(int(fact_id), text, self.process_answer)
        pass

    def __push_result(self, fact_id, value):
        if fact_id in self.pushed:
            return
        self.pushed.append(fact_id)
        print("RESULT:", self.knowledge.get_text_description(fact_id))
        self.result_found.emit(int(fact_id), self.knowledge.get_text_description(fact_id), value)
        pass

    def __clean(self):
        self.pushed = list()
        self.fact_queue = Queue()
        self.triggered_rules = list()
        pass

    def start(self):
        self.__clean()
        for root in self.knowledge.root_facts:
            self.__push_new_question(root)
            pass
        pass

    def __request_missing_values(self, predecessors):
        have_missing = False
        for predecessor in predecessors:
            if not self.working_memory.is_inited(predecessor.id):
                have_missing = True
                self.__push_new_question(predecessor.id)
            pass
        return have_missing

    def __count_fact_coefficient(self, fact_id, expert_value):
        user_value = self.working_memory.get_value_by_id(fact_id)
        return abs(expert_value - user_value)

    def main_cycle(self):
        if self.cycle_flag:
            return

        self.cycle_flag = True
        while not self.fact_queue.empty():
            next_fact_id = self.fact_queue.get()
            # print("Next fact:", self.knowledge.get_text_description(next_fact_id))
            rules = self.knowledge.get_rules_with_predecessor(next_fact_id)
            rules = [rule for rule in rules if rule.id not in self.triggered_rules]

            for rule in rules:
                # print("Look:{}".format(rule.successor.id), self.knowledge.get_text_description(rule.successor.id))
                if self.__request_missing_values(rule.predecessors):
                    continue

                satisfied = self.__is_satisfied(rule.predecessors)
                if not satisfied:
                    continue
                self.triggered_rules.append(rule.id)

                consequent = rule.successor.id
                is_intermediate = self.__is_intermediate_consequent(consequent)
                if is_intermediate:
                    self.fact_queue.put(consequent)
                    self.working_memory.set_value_by_id(consequent, self.__get_conclusion_value(rule))
                    self.user_to_expert_min_diff[consequent] = 0
                else:
                    self.__push_result(consequent, self.__get_conclusion_value(rule))
            pass
        self.cycle_flag = False
        pass

    def __get_conclusion_value(self, rule):
        conclusion_value = rule.successor.coefficient
        for predecessor in rule.predecessors:
            if self.knowledge.get_type(predecessor.id) == FactType.Antecedent:
                conclusion_value *= 1 - self.user_to_expert_min_diff[predecessor.id]
            else:
                conclusion_value *= self.working_memory.get_value_by_id(predecessor.id)
            pass
        return conclusion_value

    def __is_satisfied(self, predecessors):
        for predecessor in predecessors:
            fact_id = predecessor.id
            if self.knowledge.get_type(fact_id) == FactType.IntermediateConsequent:
                continue
            coefficient = predecessor.coefficient
            diff = abs(coefficient - self.working_memory.get_value_by_id(fact_id))
            if diff > self.user_to_expert_min_diff[fact_id] + self.ACCURACY or diff > self.MAX_COEFFICIENT_DIFF:
                return False
        return True

    def __is_intermediate_consequent(self, consequent_id):
        return self.knowledge.get_type(consequent_id) == FactType.IntermediateConsequent

    def process_answer(self, fact_id, value):
        print("Get answer for {}: {}. {}".format(fact_id, value, self.knowledge.get_text_description(fact_id)))
        self.working_memory.set_value_by_id(fact_id, value)
        rules = self.knowledge.get_rules_with_predecessor(fact_id)
        min_diff = 1
        for rule in rules:
            diff = self.__count_fact_coefficient(fact_id, rule.get_predecessor_coefficient(fact_id))
            if diff < min_diff:
                min_diff = diff
            pass
        self.user_to_expert_min_diff[fact_id] = min_diff

        self.fact_queue.put(fact_id)
        self.pushed.remove(fact_id)
        self.main_cycle()
        pass
