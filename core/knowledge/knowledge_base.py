from networkx.readwrite import json_graph
from networkx import algorithms
from pymongo import MongoClient


PREDECESSORS_STRING = "predecessors"
SUCCESSOR_STRING = "successor"
ID_STRING = "id"
COEFFICIENT_STRING = "coefficient"


class ProductionRule:
    class Predecessor:
        def __init__(self, predecessor_id, coefficient):
            self.id = predecessor_id
            self.coefficient = coefficient
            pass

    class Successor:
        def __init__(self, successor_id, coefficient):
            self.id = successor_id
            self.coefficient = coefficient
            pass

    def __init__(self, data):
        if PREDECESSORS_STRING not in data or SUCCESSOR_STRING not in data:
            raise Exception("Wrong data format for production rule")
        self.predecessors = [self.Predecessor(predecessor_data[ID_STRING], predecessor_data[COEFFICIENT_STRING])
                             for predecessor_data in data[PREDECESSORS_STRING]]
        self.successor = self.Successor(data[SUCCESSOR_STRING][ID_STRING], data[SUCCESSOR_STRING][COEFFICIENT_STRING])
        pass

    def get_predecessor_coefficient(self, predecessor_id):
        return [x.coefficient for x in self.predecessors if x.id == predecessor_id][0]


class MongoKnowledgeBase:
    """
    Use Mongo Database to store and manage knowledge data
    """

    # Constants
    FACTS_COLLECTION_NAME = "facts"
    RULES_COLLECTION_NAME = "rules"

    def __init__(self):
        self.__client = None
        self.__data_base = None
        self.__facts = None
        self.__rules = None
        self.root_facts = list()
        pass

    # TODO: error handling
    def connect(self, db_name, mongo_url='localhost', mongo_port=27017):
        self.__client = MongoClient(mongo_url, mongo_port)

        # TODO: temporary solution. Always from scratch
        if db_name in self.__client.database_names():
            self.__client.drop_database(db_name)
            pass

        self.__data_base = self.__client[db_name]
        self.__facts = self.__data_base.facts
        self.__rules = self.__data_base.rules
        pass

    def __clean(self):
        if self.__data_base is not None:
            self.__data_base.drop_collection(self.FACTS_COLLECTION_NAME)
            self.__data_base.drop_collection(self.RULES_COLLECTION_NAME)
        self.root_facts = list()
        pass

    def facts_count(self):
        return self.__facts.count()

    def rules_count(self):
        return self.__rules.count()

    def set_decision_graph(self, decision_graph_data):
        self.__clean()

        graph = json_graph.node_link_graph(decision_graph_data)
        consequent_list = list()
        for node in graph:
            if graph.in_degree(node) == 0:  # root
                self.root_facts.append(node)
            if graph.node[node]['type'] == 'c':  # leaf
                consequent_list.append(node)

            self.__facts.insert_one(self.transform_node_to_fact(node, graph))
            pass

        print("Consequents count:", len(consequent_list))
        for rule in self.transform_to_rules(consequent_list, graph):
            self.__rules.insert_one(rule)
            pass
        pass

    # TODO: handle intermediate consequents
    # TODO: add types and classes for facts (ant, con, incon)
    def find_antecedents(self):
        return self.__facts.distinct(ID_STRING, {'type': {"$in": ['a', 'ic']}})

    def get_fact_by_id(self, fact_id):
        return self.__facts.find_one({ID_STRING: fact_id}, {"_id": 0})

    def get_text_description(self, fact_id):
        return self.get_fact_by_id(fact_id)['text']

    def get_rules_with_predecessor(self, fact_id):
        return [ProductionRule(x) for x in self.__rules.find({PREDECESSORS_STRING: {'$elemMatch': {ID_STRING: fact_id}}}, {"_id": 0})]

    def transform_node_to_fact(self, node, graph):
        attributes = graph.node[node]
        out = set()
        for edge in graph.out_edges(node):
            out.add(graph.edges[edge]['weight'])
        fact = {
            "id": node,
            "type": attributes['type'],
            "text": attributes['text'],
            "out": list(out)
        }
        if attributes['type'] == 'c':
            if graph.out_degree(node) != 0:
                fact['type'] = 'ic'
            fact['coefficient'] = attributes['coefficient']
        return fact

    def transform_to_rules(self, consequent_list, graph):
        if len(self.root_facts) == 0:
            print("Can not add rules: No root elements")
            return
        for root in self.root_facts:
            for consequent in consequent_list:
                paths = algorithms.all_simple_paths(graph, root, consequent)

                for path in paths:
                    consequent_id = path[-1]
                    rule = {
                        PREDECESSORS_STRING: [],
                        SUCCESSOR_STRING: {ID_STRING: consequent_id,
                                           COEFFICIENT_STRING: graph.node[consequent_id][COEFFICIENT_STRING]}
                    }

                    for i in range(len(path) - 1):
                        rule[PREDECESSORS_STRING].append({ID_STRING: path[i],
                                                          COEFFICIENT_STRING: graph.get_edge_data(path[i], path[i + 1])[
                                                              'weight']})
                    yield rule
                    pass
                pass
            pass
        pass
