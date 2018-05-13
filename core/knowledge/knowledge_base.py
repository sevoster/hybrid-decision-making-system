from pymongo import MongoClient


class MongoKnowledgeBase:
	"""
	Use Mongo Database to get and store knowledge data
	"""

	# TODO: error handling
	def __init__(self, db_name, mongo_url='localhost', mongo_port=27017):
		self.client = MongoClient(mongo_url, mongo_port)
		self.data_base = self.client[db_name]
		self.current_collection = None
		pass

	def is_collection_chosen(self):
		return self.current_collection is not None

	def choose_collection(self, name):
		self.current_collection = self.data_base[name]
		pass
