import unittest

from core.knowledge.knowledge_base import MongoKnowledgeBase

test_settings = {
	"mongo_url":  "localhost",
	"mongo_port": 32768,
	"database":   "test"
}

test_graph = {
	"nodes": [
		{
			"text": "test_text_1",
			"type": "a",
			"id":   0
		},
		{
			"text":        "test_text_2",
			"type":        "c",
			"coefficient": 1,
			"id":          1
		},
		{
			"text": "test_text_3",
			"type": "a",
			"id":   2
		},
		{
			"text":        "test_text_4",
			"type":        "c",
			"coefficient": 1,
			"id":          3
		}
	],
	"links": [
		{
			'source': 0,
			'target': 1,
			'weight': 0
		},
		{
			'source': 0,
			'target': 2,
			'weight': 1
		},
		{
			'source': 2,
			'target': 3,
			'weight': 0.5
		}
	]
}


class MongoKnowledgeBaseTestCase(unittest.TestCase):
	def setUp(self):
		super().setUp()
		self.mongo = MongoKnowledgeBase(test_settings['database'], test_settings['mongo_url'], test_settings['mongo_port'])
		self.nodes_count = len(test_graph['nodes'])
		self.links_count = len(test_graph['links'])
		pass

	def is_mongo_data_equals(self, json_graph):
		nodes_count = len(json_graph['nodes'])
		links_count = len(json_graph['links'])
		if self.mongo.nodes.count() != nodes_count:
			return False
		if self.mongo.links.count() != links_count:
			return False

		source_nodes = []
		for node in self.mongo.nodes.find():
			node.pop('_id', None)
			source_nodes.append(node)
			pass

		if source_nodes != json_graph['nodes']:
			return False

		source_links = []
		for link in self.mongo.links.find():
			link.pop('_id', None)
			source_links.append(link)
			pass

		if source_links != json_graph['links']:
			return False
		return True

	def test_helper_equal_method(self):
		right_graph = {"nodes": [{"test": 0}], "links": [{"test1": 1}]}
		wrong_graph = {"nodes": [{"test": 1}], "links": [{"t": "est"}]}
		self.mongo.set_decision_graph(right_graph)
		self.assertTrue(self.is_mongo_data_equals(right_graph))
		self.assertFalse(self.is_mongo_data_equals(wrong_graph))
		pass

	def test_set_graph_count(self):
		self.mongo.set_decision_graph(test_graph)
		self.assertTrue(self.is_mongo_data_equals(test_graph))
		pass

	def test_repeated_set_graph(self):
		self.mongo.set_decision_graph(test_graph)
		self.mongo.set_decision_graph(test_graph)
		self.assertTrue(self.is_mongo_data_equals(test_graph))
		pass


if __name__ == '__main__':
	unittest.main()
