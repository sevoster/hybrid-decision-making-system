from core.knowledge.knowledge_base import MongoKnowledgeBase


class DecisionSystem:
	"""
	Represents the main core component which aggregates others
	"""

	# TODO: temporary here
	settings = {
		"mongo_url":  "localhost",
		"mongo_port": 32768,
		"database":   "develop"
	}

	def __init__(self):
		self.knowledge_base = MongoKnowledgeBase(self.settings['database'], self.settings['mongo_url'], self.settings['mongo_port'])
		pass

	def apply_decision_graph(self, decision_graph):
		self.knowledge_base.set_decision_graph(decision_graph)
		pass
