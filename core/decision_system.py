from core.knowledge.knowledge_base import MongoKnowledgeBase
from core.output.output_mechanism import BFSOutputMechanism
from core.working_memory.working_memory_handler import WorkingMemoryHandler


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
		self.output_mechanism = BFSOutputMechanism()
		self.working_memory = WorkingMemoryHandler()
		pass

	def apply_decision_graph(self, decision_graph):
		self.knowledge_base.set_decision_graph(decision_graph)
		self.working_memory.set_fact_ids(self.knowledge_base.find_antecedents())
		pass

	def start_output(self):
		for mem in self.working_memory.memory:
			print(mem.id)
		pass
