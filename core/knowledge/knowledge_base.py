from pymongo import MongoClient


class MongoKnowledgeBase:
    """
    Use Mongo Database to get and store knowledge data
    """

    def __init__(self, db_url='localhost', db_port=27017):
        self.client = MongoClient(db_url, db_port)
        pass

