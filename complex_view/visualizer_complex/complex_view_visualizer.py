import sys
from core.model.graph import Graph
from core.model.node import Node
from core.model.edge import Edge
from core.services.extendable_visualizer import ExtendableVisualizer


class ComplexViewVisualizer(ExtendableVisualizer):
    
    def name(self) -> str:
        return "Complex view visualizer"

    def identifier(self) -> str:
        return "complex_view_visualizer"

    def bird_view(self, graph: Graph) -> str:
        rendered_template = '''<svg width='100%' height='100%' id='bird_view'></svg>
        <script type='text/javascript'>\n
         var nodes_bird = {'''
        for node in graph.nodes :
           rendered_template = rendered_template + self._generate_node_template_string(node) + ","
        rendered_template = rendered_template + "};\n"
        rendered_template = rendered_template + "var links_bird = ["
        for edge in graph.edges:
            rendered_template = rendered_template + self._generate_edge_template_string(edge) + ","
        rendered_template = rendered_template + "];\n"
        rendered_template = rendered_template + '''links_bird.forEach(function(link)
                                  {link.source = nodes_bird[link.source];
                                  link.target = nodes_bird[link.target];});'''
        rendered_template = rendered_template + '''var force_bird = d3.layout.force()
                                    .size([200, 140])
                                    .nodes(d3.values(nodes_bird))
                                    .links(links_bird)
                                    .linkDistance(20)
                                    .on("tick", tick_bird)
                                    .charge(-23)
                                    .start();'''
        rendered_template = rendered_template + '''var svg_bird=d3.select('#bird_view').append("g").attr('id','bird_view_g');
                                    var link_bird = svg_bird.selectAll('.link')
                                        .data(links_bird)
                                        .enter().append('line')
                                        .attr("stroke", "black")
                                        .attr('class', 'link');

                                    var node_bird = svg_bird.selectAll('.node')
                                        .data(force_bird.nodes()) //add
                                        .enter().append('g')
                                        .attr('class', 'node')
                                        .attr('id', function(d){return d.id+"B";})

                                    node_bird.each(function(d){complexViewBird(d);});
                                        '''

        rendered_template = rendered_template + '''function tick_bird(e) {
                                        node_bird.attr("transform", function(d) {
                                                return "translate(" + d.x + "," + d.y + ")";
                                            });
                                            link_bird.attr('x1', function(d) { return d.source.x; })
                                                .attr('y1', function(d) { return d.source.y; })
                                                .attr('x2', function(d) { return d.target.x; })
                                                .attr('y2', function(d) { return d.target.y; });
                                        }\n'''
        rendered_template += self._generate_bird_node_drawing_function_string()
        rendered_template += "</script>"
        return rendered_template

    def main_view(self, graph: Graph) -> str:
        rendered_template = '''<svg width='100%' height='100%' id='main_view'></svg>
        <script type='text/javascript'>\n
         var nodes = {'''
        for node in graph.nodes :
           rendered_template = rendered_template + self._generate_node_template_string(node) + ","
        rendered_template = rendered_template + "};\n"
        rendered_template = rendered_template + "var links = ["
        for edge in graph.edges:
            rendered_template = rendered_template + self._generate_edge_template_string(edge) + ","
        rendered_template = rendered_template + "];\n"
        rendered_template = rendered_template + '''links.forEach(function(link)
                                  {link.source = nodes[link.source];
                                  link.target = nodes[link.target];});'''
        rendered_template = rendered_template + '''var force = d3.layout.force()
                                    .size([1000, 620])
                                    .nodes(d3.values(nodes))
                                    .links(links)
                                    .on("tick", tick)
                                    .linkDistance(1000)
                                    .charge(-1300)
                                    .start();'''
        rendered_template = rendered_template + '''var svg=d3.select('#main_view')
                                                .call(d3.behavior.zoom().on("zoom", function () {
                                                svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
                                                const bird_view = d3.select('#bird_view_g');
                                                var translate_obj = d3.event.translate;
                                                var scale = d3.event.scale;
                                                translate_obj = [d3.event.translate[0] / 5.1, d3.event.translate[1] / 4.5];
                                                bird_view.attr("transform", "translate(" + translate_obj + ")" + " scale(" + scale + ")");
                                                }))
                                                .append("g");
                                    var link = svg.selectAll('.link')
                                        .data(links)
                                        .enter().append('line')
                                        .attr("stroke", "black")
                                        .attr('class', 'link');

                                    var node = svg.selectAll('.node')
                                        .data(force.nodes()) //add
                                        .enter().append('g')
                                        .attr('class', 'node')
                                        .attr('id', function(d){return d.id;})
                                        .on('click',function(){
                                        nodeClick(this);
                                        });

                                    node.each(function(d){complexView(d);});'''

        rendered_template = rendered_template + '''    function tick(e) {
                                        node.attr("transform", function(d) {
                                                return "translate(" + d.x + "," + d.y + ")";
                                            }).call(force.drag);
                                            link.attr('x1', function(d) { return d.source.x; })
                                                .attr('y1', function(d) { return d.source.y; })
                                                .attr('x2', function(d) { return d.target.x; })
                                                .attr('y2', function(d) { return d.target.y; });
                                        };\n'''
        rendered_template = rendered_template + self._generate_node_click_function_string()
        rendered_template += self._generate_node_drawing_function_string()
        rendered_template += "</script>"
        return rendered_template

    
    def _generate_node_template_string(self, node: Node) -> str:
        result = '''"'''
        result += node.id
        result += '''":{id:"'''
        result += node.id
        result += '''",name:"'''
        result += node.name
        result += '''",values: {value:"'''
        value = node.value.replace("\n"," ")
        value = node.value.replace("\r"," ")
        value = node.value.replace("\t"," ")
        value = node.value.strip()
        if(value == ""):
            result += node.name
        else:
            value = ' '.join(value.split())
            result += value
        result += '''",'''
        for key,val in node.attributes.items():
            result += key
            result +=''':"'''
            result += str(val)
            result += '''",'''
        result += '''} }'''
        return result

    def _generate_edge_template_string(self, edge: Edge) -> str:
        result = "{source:'"
        result += edge.start.id
        result += "',\ntarget:'"
        result += edge.end.id
        result += "'}"
        return result

    def _generate_node_click_function_string(self) -> str:
        result = '''function nodeClick(element){
                        const node_info_elem = document.getElementById('node-info');
                        if(node_info_elem){
                            const id = element.getAttribute('id');
                            const clicked_node = nodes[element.id];
                            var node_info = "name : ";
                            node_info += clicked_node.name;
                            node_info += "<br />";
                            Object.entries(clicked_node.values).forEach(([k,v]) => {
                                node_info += k;
                                node_info += " : "
                                node_info += v;
                                node_info += "<br />";
                            });
                            node_info_elem.innerHTML = node_info;
                        }        
                    }'''
        return result

    def _generate_bird_node_drawing_function_string(self) -> str:
        result = '''function complexViewBird(d){
                        var width=15;
                        var height = 10;
                        var rect = d3.select("g#"+d.id+"B")
                            .append('rect')
                            .attr('x',0)
                            .attr('y',0)
                            .attr('width',width)
                            .attr('height',height)
                            .attr('fill','yellow')
                            .style("stroke", "black")
                            .style("stroke-width", "1px");
                        }'''
        return result

    def _generate_node_drawing_function_string(self) -> str:
        result = '''    var lineNum = 0;
                        function wrap(text, width,break_char) {
                            text.each(function () {
                                var text = d3.select(this),
                                    words = text.text().split(break_char).reverse(),
                                    word,
                                    line = [],
                                    lineNumber = 0,
                                    lineHeight = 1.1, // ems
                                    x = text.attr("x"),
                                    y = text.attr("y"),
                                    dy = 0, //parseFloat(text.attr("dy")),
                                    tspan = text.text(null)
                                                .append("tspan")
                                                .attr("x", x)
                                                .attr("y", y)
                                                .attr("dy", dy + "em");
                                while (word = words.pop()) {
                                    line.push(word);
                                    tspan.text(line.join(" "));
                                    if (tspan.node().getComputedTextLength() > width) {
                                        line.pop();
                                        tspan.text(line.join(" "));
                                        line = [word];
                                        tspan = text.append("tspan")
                                                    .attr("x", x)
                                                    .attr("y", y)
                                                    .attr("dy", ++lineNumber * lineHeight + dy + "em")
                                                    .text(word);
                                        lineNum = lineNumber;
                                    }
                                }
                            });
                        }  
                        var totHeight = 0;

                        function complexView(d){
                        var width=170;
                        var heightMultiplier =  Object.keys(d.values).length;
                        var textSize=15;
                        var height=(heightMultiplier==0)?textSize:heightMultiplier*textSize;
                        height += textSize;

                        var g = d3.select("g#"+d.id)
                        .attr('transform', 'translate(20,' + totHeight + ')');
                        
                        var rect = d3.select("g#"+d.id)
                            .append('rect')
                            .attr('x',0)
                            .attr('y',0)
                            .attr('width',width)
                            .attr('height',1)
                            .attr('fill','yellow')
                            .style("stroke", "black")
                            .style("stroke-width", "2px");

                        d3.select("g#"+d.id)
                            .append('text')
                            .attr('x',width / 2)
                            .attr('y',20)
                            .attr('font-weight',500)
                            .attr('text-anchor','middle')
                            .attr('font-size',textSize)
                            .attr('font-family','sans-serif')
                            .attr('fill','black')
                            .text(d.name.toUpperCase())
                            .call(wrap, width - 10,/\s/g);

                        d3.select("g#"+d.id)
                            .append('line')
                            .attr('x1',0)
                            .attr('y1',30)
                            .attr('x2',width)
                            .attr('y2',30)
                            .attr('stroke','gray')
                            .attr('stroke-width',2);

                            var val = "";
                            var counter = 0;
                            Object.entries(d.values).forEach(([k,v]) => {
                                val = k + " : " + v.toString();
                                d3.select("g#"+d.id)
                                .append('text')
                                .attr('x',10)
                                .attr('y',50 + counter*textSize + 5)
                                .attr('text-anchor','start')
                                .attr('font-size',textSize)
                                .attr('font-family','sans-serif')
                                .attr('fill','black')
                                .text((function(d) { return val; }))
                                .each(function(d,i) {
                                    var thisWidth = this.getComputedTextLength();
                                    counter += Math.ceil(thisWidth / width);
                                })
                                .call(wrap, width - 20,/\s/g);
                            });


                        var new_height = g.node().getBBox().height + 25;
                        totHeight += new_height + 10;
                        rect.attr('height', new_height);
                        }'''
        return result
        
