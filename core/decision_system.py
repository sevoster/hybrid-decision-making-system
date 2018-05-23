from os import path, makedirs
import json

from core.knowledge.knowledge_base import MongoKnowledgeBase
from core.output.output_mechanism import BFSOutputMechanism
from core.working_memory.working_memory_handler import WorkingMemoryHandler


class DecisionSystem:
    """
    Represents the main core component which aggregates others
    """

    DEFAULT_SETTINGS = {
        "mongo_url": "localhost",
        "mongo_port": 27017,
        "database": "develop"
    }

    CONFIG_PATH = "./config/settings.json"

    def __init__(self):
        self.settings = self.__read_or_create_config()
        self.knowledge_base = MongoKnowledgeBase()
        self.knowledge_base.connect(self.settings['database'], self.settings['mongo_url'], self.settings['mongo_port'])
        self.working_memory = WorkingMemoryHandler(self.knowledge_base)
        self.output_mechanism = BFSOutputMechanism(self.working_memory, self.knowledge_base)
        pass

    # TODO: Bad architecture is here
    def connect_to_user_interface(self, add_question):
        self.output_mechanism.new_question.connect(add_question)
        pass

    def __read_or_create_config(self):
        """
        Read config file by path $(pwd)/config/settings.json or create one with default parameters.
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
        self.working_memory.init_from_base()
        pass

    def start_output(self):
        self.output_mechanism.start()
        pass
