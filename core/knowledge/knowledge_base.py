import copy
from pymongo import MongoClient


class MongoKnowledgeBase:
	"""
	Use Mongo Database to get and store knowledge data
	"""

	# Constants
	__NODES_COLLECTION_NAME = "nodes"
	__LINKS_COLLECTION_NAME = "links"

	# TODO: error handling
	def __init__(self, db_name, mongo_url='localhost', mongo_port=27017):
		self.__client = MongoClient(mongo_url, mongo_port)

		# TODO: temporary solution. Always from scratch
		if db_name in self.__client.database_names():
			self.__client.drop_database(db_name)
			pass

		self.__data_base = self.__client[db_name]
		self.__nodes = self.__data_base.nodes
		self.__links = self.__data_base.links
		pass

	def __clean_collections(self):
		if self.__data_base is None:
			return

		self.__data_base.drop_collection(self.__NODES_COLLECTION_NAME)
		self.__data_base.drop_collection(self.__LINKS_COLLECTION_NAME)
		pass

	def get_nodes(self):
		nodes = list()
		for node in self.__nodes.find():
			node.pop('_id')
			nodes.append(node)
		return nodes

	def get_links(self):
		links = list()
		for link in self.__links.find():
			link.pop('_id')
			links.append(link)
		return links

	def get_nodes_count(self):
		return self.__nodes.count()

	def get_links_count(self):
		return self.__links.count()

	def set_decision_graph(self, decision_graph_data):
		if self.__LINKS_COLLECTION_NAME not in decision_graph_data or self.__NODES_COLLECTION_NAME not in decision_graph_data:
			raise Exception("Missing data in decision graph")

		# Mongo adds ObjectId to the documents
		links_docs = copy.deepcopy(decision_graph_data[self.__LINKS_COLLECTION_NAME])
		nodes_docs = copy.deepcopy(decision_graph_data[self.__NODES_COLLECTION_NAME])

		self.__clean_collections()
		self.__nodes.insert_many(nodes_docs)
		self.__links.insert_many(links_docs)
		pass

	# TODO: handle intermediate consequents
	# TODO: add types and classes for facts (ant, con, incon)
	def find_antecedents(self):
		results = list()
		ants = self.__nodes.find({'type': 'a'})
		for ant in ants:
			results.append(ant['id'])
		return results

	def get_by_id(self, fact_id):
		fact = self.__nodes.find_one({"id": fact_id})
		if fact is not None:
			fact.pop('_id')
		return fact
