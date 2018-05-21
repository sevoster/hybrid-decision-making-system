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

    def __init__(self):
        self.memory = list()
        pass

    def set_fact_ids(self, fact_ids):
        for fact_id in fact_ids:
            self.memory.append(self.MemoryInstance(fact_id))
            pass
        pass

    def get_next_not_inited(self):
        not_inited = [x for x in self.memory if not x.is_inited()]
        return min(not_inited, key=lambda x: x.id)
