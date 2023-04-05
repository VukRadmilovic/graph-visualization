import pandas as pd
from core.model.node import Node
from core.model.edge import Edge
from core import utils


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def search(self, query):
        # Initialize an empty subgraph
        subgraph = Graph()

        query = query.lower()

        # Iterate over the nodes in the graph
        for node in self.nodes:
            # Check if the node's name or values contain the query
            if query in node.name.lower() or query in node.value.lower():
                subgraph.add_node(node)
            else:
                # Iterate over the node's attributes
                for key, value in node.attributes.items():
                    try:
                        # Check if the attribute's value is a datetime
                        # whose representation with month names contains the query
                        if type(value) == pd.Timestamp and query in value.strftime("%d %B, %Y").lower():
                            subgraph.add_node(node)
                            break
                        # Check if the attribute's key or value contain the query
                        if query == key.lower() or query == str(value).lower() or query in key.lower() or query in str(value).lower():
                            subgraph.add_node(node)
                            break
                    except:
                        continue

        # Iterate over the edges in the graph
        for edge in self.edges:
            # Check if both endpoints of the edge are in the subgraph
            if edge.start in subgraph.nodes and edge.end in subgraph.nodes:
                subgraph.add_edge(edge)

        return subgraph

    def filter(self, query):
        # Split the query into its parts
        attribute_name, relational_operator, attribute_value_str = query.split()

        # Convert the attribute value in the query to the correct type
        attribute_value = utils.evaluate(attribute_value_str)

        # Initialize an empty subgraph
        subgraph = Graph()

        # Iterate over the nodes in the graph
        for node in self.nodes:
            node_attribute_value = node.attributes.get(attribute_name)

            # Check if the node has the attribute
            if not node_attribute_value:
                continue

            # Check that the attribute value in the query is of a compatible type
            if not isinstance(node_attribute_value, type(attribute_value)) and not \
                    ((isinstance(node_attribute_value, int) and
                      isinstance(attribute_value, float)) or
                     (isinstance(node_attribute_value, float) and
                      isinstance(attribute_value, int))):
                raise TypeError("Incompatible attribute value type")

            # Check if the node's attribute value matches the query
            if relational_operator == "==":
                if node.attributes.get(attribute_name) == attribute_value:
                    subgraph.add_node(node)
            elif relational_operator == ">":
                if node.attributes.get(attribute_name) > attribute_value:
                    subgraph.add_node(node)
            elif relational_operator == ">=":
                if node.attributes.get(attribute_name) >= attribute_value:
                    subgraph.add_node(node)
            elif relational_operator == "<":
                if node.attributes.get(attribute_name) < attribute_value:
                    subgraph.add_node(node)
            elif relational_operator == "<=":
                if node.attributes.get(attribute_name) <= attribute_value:
                    subgraph.add_node(node)
            elif relational_operator == "!=":
                if node.attributes.get(attribute_name) != attribute_value:
                    subgraph.add_node(node)

        # Iterate over the edges in the graph
        for edge in self.edges:
            # Check if both endpoints of the edge are in the subgraph
            if edge.start in subgraph.nodes and edge.end in subgraph.nodes:
                subgraph.add_edge(edge)

        # Return the subgraph
        return subgraph
