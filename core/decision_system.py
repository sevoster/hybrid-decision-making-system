from core.knowledge_base import KnowledgeBase, Precedent, Consequent


class DecisionSystem:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        pass

    def apply_decision_tree(self, json_obj):
        for p in json_obj['precedent']:
            self.knowledge_base.add_precedent(Precedent(p['id'], p['text'], p['next']))
            pass
        for c in json_obj['consequent']:
            self.knowledge_base.add_consequent(Consequent(c['id'], c['text'], c['coef'], c['next']))
            pass
        print("SUCCESS: Applied decision tree")
        pass
