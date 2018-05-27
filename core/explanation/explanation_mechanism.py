from core.knowledge.knowledge_base import FactType


class ExplanationMechanism:
    def __init__(self, knowledge_base, working_memory):
        self.knowledge_base = knowledge_base
        self.working_memory = working_memory
        pass

    def __convert_to_human_answer(self, value):
        if value >= 0.9:
            return "Yes"
        elif value >= 0.67:
            return "Almost yes"
        elif value >= 0.45:
            return "Don't know"
        elif value >= 0.1:
            return "Almost no"
        else:
            return "No"

    # TODO: concatenate by intermediate consequent
    def get_explanation(self, rule_sequence):
        logic_strings = list()
        for rule_id in rule_sequence:
            logic_string = ""
            rule = self.knowledge_base.get_rule_by_id(rule_id)
            for predecessor in rule.predecessors:
                text = self.knowledge_base.get_text_description(predecessor.id)
                value = self.working_memory.get_value_by_id(predecessor.id)
                fact_type = self.knowledge_base.get_type(predecessor.id)
                if fact_type == FactType.Antecedent:
                    text = "Q: {}; A: {} ({})".format(text, self.__convert_to_human_answer(value), value)
                else:
                    text = "C: {}".format(text)
                logic_string += text + " -> "
                pass
            conclusion_text = self.knowledge_base.get_text_description(rule.successor.id)
            logic_string += conclusion_text
            logic_strings.append(logic_string)
            pass
        return logic_strings
