class NextLink:
    def __init__(self, coef, next_id):
        self.coefficient = coef
        self.next_id = next_id
        pass


class Precedent:

    def __init__(self, precedent_id, text, next_statements):
        self.id = precedent_id
        self.text = text
        self.next_statements = []
        for item in next_statements:
            self.next_statements.append(NextLink(item['coef'], item['id']))
            pass
        pass


class Consequent:

    def __init__(self, consequent_id, text, coef, next_statement):
        self.id = consequent_id
        self.text = text
        self.coefficient = coef
        self.next_statement = NextLink(1, next_statement)
        pass


class KnowledgeBase:

    def __init__(self):
        # TODO: actually it should be graph (I guess)
        self.precedents = []
        self.consequents = []
        pass

    def add_precedent(self, precedent):
        self.precedents.append(precedent)
        pass

    def add_consequent(self, consequent):
        self.consequents.append(consequent)
        pass

    def is_valid(self):
        # TODO: check graph is a connected tree
        pass
