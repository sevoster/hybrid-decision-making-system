import copy

from networkx.readwrite import json_graph
from networkx import algorithms
from pymongo import MongoClient


class MongoKnowledgeBase:
    """
    Use Mongo Database to store and manage knowledge data
    """

    # Constants
    FACTS_COLLECTION_NAME = "facts"
    RULES_COLLECTION_NAME = "rules"

    # TODO: error handling
    def __init__(self, db_name, mongo_url='localhost', mongo_port=27017):
        self.__client = MongoClient(mongo_url, mongo_port)

        # TODO: temporary solution. Always from scratch
        if db_name in self.__client.database_names():
            self.__client.drop_database(db_name)
            pass

        self.__data_base = self.__client[db_name]
        self.__facts = self.__data_base.facts
        self.__rules = self.__data_base.rules
        pass

    def __clean_collections(self):
        if self.__data_base is None:
            return

        self.__data_base.drop_collection(self.FACTS_COLLECTION_NAME)
        self.__data_base.drop_collection(self.RULES_COLLECTION_NAME)
        pass

    def facts_count(self):
        return self.__facts.count()

    def rules_count(self):
        return self.__rules.count()

    def set_decision_graph(self, decision_graph_data):
        self.__clean_collections()
        self.__facts.insert_many(copy.deepcopy(decision_graph_data['nodes']))
        self.transform_to_production_rules(decision_graph_data)
        pass

    # TODO: handle intermediate consequents
    # TODO: add types and classes for facts (ant, con, incon)
    def find_antecedents(self):
        return self.__facts.distinct('id', {'type': {"$in": ['a', 'ic']}})

    def get_fact_by_id(self, fact_id):
        return self.__facts.find_one({"id": fact_id}, {"_id": 0})

    def transform_to_production_rules(self, decision_graph, root=0):
        """
        Transform decision graph into production rules and insert in Data Base
        :param decision_graph: Decision graph in json format
        :param root: Id of the root
        :return: Number of inserted rules
        """
        graph = json_graph.node_link_graph(decision_graph)
        counter = 0
        for node in graph:
            if graph.out_degree(node) == 0:  # leaf
                paths = algorithms.all_simple_paths(graph, root, node)
                for path in paths:
                    consequent_id = path[-1]
                    antecedent_ids = path[:-1]
                    rule = {
                        "predecessors": antecedent_ids,
                        "successor": consequent_id
                    }
                    self.__rules.insert_one(rule)
                    counter += 1
                    pass
                pass
            pass
        return counter
