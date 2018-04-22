from pymongo import MongoClient


class KnowledgeBase:

    def __init__(self):
        # TODO: move hardcode to config
        self.db_client = MongoClient('192.168.31.100', 27017)
        pass
