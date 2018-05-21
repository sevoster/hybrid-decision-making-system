from unittest import TestCase
from networkx import readwrite, path_graph, DiGraph

from core.knowledge.knowledge_base import MongoKnowledgeBase


class TestMongoKnowledgeBase(TestCase):
    def setUp(self):
        self.mongo = MongoKnowledgeBase()
        pass

    def test_transform_to_production_rules(self):
        test_path_graph = path_graph(5, create_using=DiGraph())
        rules = self.mongo.transform_to_production_rules(readwrite.node_link_data(test_path_graph))
        self.assertEqual(1, len(rules))
        self.assertListEqual(rules[0]['predecessors'], [0, 1, 2, 3])
        self.assertEqual(rules[0]['successor'], 4)
        pass
