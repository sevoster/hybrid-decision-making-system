from core.knowledge.knowledge_base import FactType


class ExplanationMechanism:
    def __init__(self, knowledge_base, working_memory):
        self.knowledge_base = knowledge_base
        self.working_memory = working_memory
        pass

    def __convert_to_human_answer(self, value):
        if value >= 0.9:
            return "Да"
        elif value >= 0.67:
            return "Возможно"
        elif value >= 0.45:
            return "Не знаю"
        elif value >= 0.1:
            return "Скорее нет"
        else:
            return "Нет"

    # TODO: concatenate by intermediate consequent
    def get_explanation(self, rule_sequence):
        logic_strings = list()
        consequent_ids = list()
        for rule_id in rule_sequence:
            logic_string = ""
            rule = self.knowledge_base.get_rule_by_id(rule_id)
            for predecessor in rule.predecessors:
                text = self.knowledge_base.get_text_description(predecessor.id)
                value = self.working_memory.get_value_by_id(predecessor.id)
                fact_type = self.knowledge_base.get_type(predecessor.id)
                if fact_type == FactType.Antecedent:
                    text = "Q: {}; A: {} ({})".format(text, value, self.__convert_to_human_answer(value))
                else:
                    # text = "C: {}".format(text)
                    continue
                logic_string += text + " ->\n"
                pass
            conclusion_text = self.knowledge_base.get_text_description(rule.successor.id)
            logic_string += conclusion_text
            if rule.predecessors[0].id in consequent_ids:
                index = consequent_ids.index(rule.predecessors[0].id)
                logic_strings[index] += " ->\n" + logic_string
            else:
                logic_strings.append(logic_string)
                consequent_ids.append(rule.successor.id)
            pass
        return logic_strings
