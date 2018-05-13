from core.knowledge.knowledge_base import MongoKnowledgeBase

class DecisionSystem:
    # TODO: temporary here
    settings = {
        "mongo_url": "localhost",
        "mongo_port": 32768
    }

    def __init__(self):
        self.knowledge_base = MongoKnowledgeBase(self.settings['mongo_url'], self.settings['mongo_port'])
        pass

