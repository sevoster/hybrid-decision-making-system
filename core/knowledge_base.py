from pymongo import MongoClient


class KnowledgeBase:

    def __init__(self):
        # TODO: move hardcode to config
        self.client = MongoClient('192.168.31.100', 27017)
        self.db = self.client.test_db
        self.rules = self.db.rules
        pass

    def add_new_rules(self, rules):
        self.rules.insert_many(rules)
        pass
