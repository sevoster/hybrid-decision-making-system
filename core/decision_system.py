from os import path, makedirs
import json

from core.knowledge.knowledge_base import MongoKnowledgeBase
from core.output.output_mechanism import BFSOutputMechanism
from core.working_memory.working_memory_handler import WorkingMemoryHandler


class DecisionSystem:
    """
    Represents the main core component which aggregates others
    """

    # TODO: temporary here
    DEFAULT_SETTINGS = {
        "mongo_url": "localhost",
        "mongo_port": 27017,
        "database": "develop"
    }

    CONFIG_PATH = "./config/settings.json"

    def __init__(self):
        self.settings = self.__read_or_create_config()
        self.knowledge_base = MongoKnowledgeBase(self.settings['database'], self.settings['mongo_url'], self.settings['mongo_port'])
        self.output_mechanism = BFSOutputMechanism()
        self.working_memory = WorkingMemoryHandler()
        pass

    def __read_or_create_config(self):
        """
        Read config file by path (pwd)/config/settings.json or create one with default parameters.
        :return: Settings dictionary
        """
        if path.exists(self.CONFIG_PATH):
            print("Read config from:", path.abspath(self.CONFIG_PATH))
            with open(self.CONFIG_PATH, 'r') as config_file:
                settings = json.load(config_file)
            return settings

        print("Created config file with default settings:", path.abspath(self.CONFIG_PATH))
        makedirs(path.dirname(self.CONFIG_PATH), exist_ok=True)
        with open(self.CONFIG_PATH, 'w') as config_file:
            config_file.write(json.dumps(self.DEFAULT_SETTINGS))
        return self.DEFAULT_SETTINGS

    def apply_decision_graph(self, decision_graph):
        self.knowledge_base.set_decision_graph(decision_graph)
        self.working_memory.set_fact_ids(self.knowledge_base.find_antecedents())
        pass

    def start_output(self):
        for mem in self.working_memory.memory:
            print(mem.id)
        pass
