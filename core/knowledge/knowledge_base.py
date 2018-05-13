import copy
from pymongo import MongoClient


class MongoKnowledgeBase:
	"""
	Use Mongo Database to get and store knowledge data
	"""

	# Constants
	NODES_COLLECTION_NAME = "nodes"
	LINKS_COLLECTION_NAME = "links"

	# TODO: error handling
	def __init__(self, db_name, mongo_url='localhost', mongo_port=27017):
		self.client = MongoClient(mongo_url, mongo_port)

		# TODO: temporary solution. Always from scratch
		if db_name in self.client.database_names():
			self.client.drop_database(db_name)
			pass

		self.data_base = self.client[db_name]
		self.nodes = self.data_base.nodes
		self.links = self.data_base.links
		pass

	def _clean_collections(self):
		if self.data_base is None:
			return

		self.data_base.drop_collection(self.NODES_COLLECTION_NAME)
		self.data_base.drop_collection(self.LINKS_COLLECTION_NAME)
		pass

	def set_decision_graph(self, decision_graph_data):
		if self.LINKS_COLLECTION_NAME not in decision_graph_data or self.NODES_COLLECTION_NAME not in decision_graph_data:
			raise Exception("Missing data in decision graph")

		# Mongo adds ObjectId to the documents
		links_docs = copy.deepcopy(decision_graph_data[self.LINKS_COLLECTION_NAME])
		nodes_docs = copy.deepcopy(decision_graph_data[self.NODES_COLLECTION_NAME])

		self._clean_collections()
		self.nodes.insert_many(nodes_docs)
		self.links.insert_many(links_docs)
		pass
