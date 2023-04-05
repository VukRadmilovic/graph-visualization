from core import utils


class Node:
    def __init__(self, id_, name, attributes,parent, value=""):
        self.id = id_
        self.name = name
        self.value = value
        self.parent = parent
        if self.value is None:
            self.value = ""

        self.attributes = {}

        for key, value in attributes.items():
            self.attributes[key] = utils.evaluate(value)