from core.model.graph import Graph
from core.model.node import Node

class Visualizer:
    def tree_view(self, graph: Graph) -> str:
        parsing_map = {}    #map that will track which nodes are already parsed (shown in tree) -> nested objects in data
        result_template = '''<ul id="parent">'''
        for node in graph.nodes:
            if node in parsing_map.keys() and parsing_map[node] == True : 
                continue
            node_str = ""
            res = self._getNodeTemplateString(node,None,graph,node_str,parsing_map)
            node_str += res
            result_template += node_str
        result_template += '''</ul>
                              <script>
                              var toggler = document.getElementsByClassName("caret");
                              var i;
                              for (i = 0; i < toggler.length; i++) {
                              toggler[i].addEventListener("click", function() {
                                  this.parentElement.querySelector(".nested").classList.toggle("active");
                                  this.classList.toggle("caret-down");
                                });
                               }

                               var references = document.getElementsByClassName("redirect");
                               i = 0;
                               for(i = 0; i < references.length; i++) { 
                                references[i].addEventListener("click", function() {
                                  console.log(this);
                                  const id_redirect = this.getAttribute('id').substring(1);
                                  const elem = document.getElementById(id_redirect);
                                  elem.parentElement.querySelector(".nested").classList.toggle("active");
                                  elem.classList.toggle("caret-down");
                                  elem.scrollIntoView({
                                  behavior: 'smooth',
                                  block: 'nearest',
                                  inline: 'center'
                                  });
                                });
                               }
                               </script>'''
        return result_template
    
    def _getNodeTemplateString(self, node: Node,parent: Node, graph: Graph, node_string: str, parsing_map : map) -> str:
        if node in parsing_map.keys() and parsing_map[node]== True:
            node_string += '''<li class="redirect" id="-'''
            node_string += node.id
            node_string += '''">'''
            node_string += node.id
            node_string += "</li>"
            return node_string
        if not self._checkIfShouldParse(node,parent,graph,parsing_map):
            node_string += '''<li class="redirect" id="-'''
            node_string += node.id
            node_string += '''">'''
            node_string += node.id
            node_string += "</li>"
            return node_string
        node_string += self._getNodeAttributesString(node)
        parsing_map[node] = True
        node_peers= []      #list of nodes that have connection with the referenced node
        for edge in graph.edges:
            if(edge.start.id == node.id):
                node_peers.append(edge.end)


        if(len(node_peers) == 0):
            node_string += "</ul></li>"
            parsing_map[node] = True
            return node_string
        
        node_string += '''<li><span class="caret">Reference</span>\n<ul class="nested">'''

        for peer in node_peers:
            res = self._getNodeTemplateString(peer,node,graph,node_string,parsing_map)
            if res != None:
                node_string = res
        node_string += '''</ul></li></ul></li>'''
        return node_string

    def _getNodeAttributesString(self, node : Node) -> str:
        result_string = '''<li><span class="caret" id="'''
        result_string += node.id
        result_string += '''"></span>'''
        result_string += node.id
        result_string += '''<ul class="nested"><li>value : '''
        result_string += str(node.value)
        result_string += "</li>"
        for key, val in node.attributes.items():
            result_string += '''<li>'''
            result_string += str(key)
            result_string += ''' : '''
            result_string += str(val)
            result_string += '''</li>'''
        return result_string


    def _checkIfShouldParse(self, node: Node,parent : Node, graph : Graph, parsing_map: map) -> bool:
        if(parent == None):
            return True
        if(parent == node.parent):
            return True
        return False