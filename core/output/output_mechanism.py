from queue import Queue


class BFSOutputMechanism:
    """
    Represents core logic for analytic output
    """

    def __init__(self):
        self.fact_queue = Queue()
        self.used = list()
        pass
