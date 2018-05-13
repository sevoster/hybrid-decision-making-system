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
		self.mongo.set_decision_graph(test_graph)
		pass

	def is_mongo_data_equals(self, json_graph):
		return self.mongo.get_nodes() == json_graph['nodes'] and self.mongo.get_links() == json_graph['links']

	def test_helper_equal_method(self):
		right_graph = {"nodes": [{"test": 0}], "links": [{"test1": 1}]}
		wrong_graph = {"nodes": [{"test": 1}], "links": [{"t": "est"}]}
		self.mongo.set_decision_graph(right_graph)
		self.assertTrue(self.is_mongo_data_equals(right_graph))
		self.assertFalse(self.is_mongo_data_equals(wrong_graph))
		pass

	def test_set_graph(self):
		self.assertTrue(self.is_mongo_data_equals(test_graph))
		pass

	def test_repeated_set_graph(self):
		self.mongo.set_decision_graph(test_graph)
		self.assertTrue(self.is_mongo_data_equals(test_graph))
		pass

	def test_set_bad_graph(self):
		self.assertRaises(Exception, self.mongo.set_decision_graph, {"I'm a big bad graph": "What you say"}, msg="He's gonna huff & puff")
		pass

	def test_find_antecedents(self):
		ants = self.mongo.find_antecedents()
		self.assertGreater(len(ants), 0, "There is no antecedent found in test graph")
		for ant_id in ants:
			fact = self.mongo.get_by_id(ant_id)
			self.assertIsNotNone(fact)
			self.assertEqual(fact['type'], 'a')  # TODO: refactor when types come
		pass


if __name__ == '__main__':
	unittest.main()
