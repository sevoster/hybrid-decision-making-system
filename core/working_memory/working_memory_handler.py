class WorkingMemoryHandler:
    """
    Handler for working memory
    """

    class MemoryInstance:
        def __init__(self, fact_id, value=None):
            self.__id = fact_id
            self.__value = value
            pass

        @property
        def id(self):
            return self.__id

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, new_value):
            self.__value = min(1, max(0, new_value))
            pass

        def is_inited(self):
            return self.value is not None

    def __init__(self, knowledge_base):
        self.memory = dict()
        self.knowledge_base = knowledge_base
        pass

    def init_from_base(self):
        if self.knowledge_base is None:
            print("Knowledge base is None")
            return
        self.set_fact_ids(self.knowledge_base.find_antecedents())
        pass

    def set_fact_ids(self, fact_ids):
        for fact_id in fact_ids:
            self.memory[fact_id] = self.MemoryInstance(fact_id)
            pass
        pass

    def set_value_by_id(self, fact_id, value):
        if fact_id not in self.memory:
            print("Unknown fact id:", fact_id)
            return
        self.memory[fact_id].value = value
        pass

    def get_value_by_id(self, fact_id):
        if fact_id not in self.memory:
            print("Unknown fact id:", fact_id)
            return None
        return self.memory[fact_id].value

    def is_inited(self, fact_id):
        return self.memory[fact_id].is_inited()
