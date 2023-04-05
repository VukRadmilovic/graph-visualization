from core.model.node import Node


class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
