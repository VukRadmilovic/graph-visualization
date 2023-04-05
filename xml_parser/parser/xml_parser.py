from core.services.data_parser import DataParser
from core.model.graph import Graph
from core.model.node import Node
from core.model.edge import Edge
import xml.etree.ElementTree as et  # et is used to parse the xml data


class XMLParser(DataParser):
    def name(self) -> str:
        return "XML Parser"

    def identifier(self) -> str:
        return "xml_parser"

    def parse(self, xml_string, parent_node=None, graph=None, tag_count=None, original_call=True) -> Graph:
        # Parse the XML file string and create an ElementTree object
        root = et.fromstring(xml_string)

        # Initialize an empty graph if this is the root element/node
        if parent_node is None:
            graph = Graph()
            parent_node = Node(root.tag, root.tag, root.attrib, None, root.text)
            graph.add_node(parent_node)

        # Keep track of the number of nodes with each tag name
        # This is used to create unique node IDs
        if not tag_count:
            tag_count = {}

        # Iterate over the root element's children
        for child_element in root:
            # Update the node count for this tag name
            if child_element.tag in tag_count:
                tag_count[child_element.tag] += 1
            else:
                tag_count[child_element.tag] = 1

            # Generate a unique identifier for the node
            node_id = f"{child_element.tag}_{tag_count[child_element.tag]}"

            # Create a new node
            child_node = Node(node_id, child_element.tag, child_element.attrib,parent_node, child_element.text)
            graph.add_node(child_node)

            # Add an edge between the parent node and the child node
            edge = Edge(parent_node, child_node)
            graph.add_edge(edge)

            # Recursively parse the child element's children
            self.parse(et.tostring(child_element), child_node, graph, tag_count, False)

        # Check for custom references to other nodes, only if this is the original call and not a recursive one.
        if original_call:
            for node in graph.nodes:
                # Check if the node has a "ref" attribute
                if "ref" in node.attributes:
                    ref_id = node.attributes["ref"]
                    ref_node = None

                    # Find the node with the matching "id" attribute
                    for node2 in graph.nodes:
                        if node2.attributes.get("id") == ref_id:
                            ref_node = node2
                            break

                    # If the node was found, add an edge between the two nodes
                    if ref_node is not None:
                        edge = Edge(node, ref_node)
                        graph.add_edge(edge)

        return graph
