from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxZoomTool, ResetTool, OpenURL
from bokeh.plotting import figure, from_networkx, show
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxZoomTool, ResetTool, OpenURL, ColumnDataSource, LabelSet, Arrow, NormalHead, StaticLayoutProvider
from bokeh.palettes import Spectral4
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with URL attributes
G.add_node(0, URL='https://github.com/arne-cl/discoursegraphs')
G.add_node(1, URL='http://example.com/B')
G.add_node(2, URL='http://example.com/C')

# Add edges
G.add_edge(0, 1)
G.add_edge(0, 2)
# G.add_edge('C', 'A')

# Create a Bokeh plot with the graph
plot = Plot(width=400, height=400, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Clickable Graph"

pos = nx.circular_layout(G)
# Create a Bokeh graph from the NetworkX graph
graph_renderer = from_networkx(G, pos)
graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=pos)

# Add URL and index attributes to the node renderer's data source
graph_renderer.node_renderer.data_source.data['URL'] = [G.nodes[node]['URL'] for node in G.nodes]
graph_renderer.node_renderer.data_source.data['index'] = list(G.nodes)

# Style the nodes and edges
graph_renderer.node_renderer.glyph = Circle(size=15, fill_color='skyblue')
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)

# Add node labels
x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
# node_labels = list(G.nodes())
node_labels = list("ABC")
source = ColumnDataSource({'x': x, 'y': y, 'node_labels': node_labels})
labels = LabelSet(x='x', y='y', text='node_labels', source=source,
                  background_fill_color='white', text_align='center', text_baseline='middle')

# Add arrow heads to the edges to indicate direction
for start, end in G.edges:
    print (start, end)
    start_point = graph_renderer.layout_provider.graph_layout[start]
    end_point = graph_renderer.layout_provider.graph_layout[end]
    # start_point = pos[start]
    # end_point = pos[end]
    arrow = Arrow(end=NormalHead(fill_color="black", size=15), x_start=start_point[0], y_start=start_point[1], x_end=end_point[0], y_end=end_point[1])
    plot.add_layout(arrow)

# Add the graph renderer to the plot
plot.renderers.append(graph_renderer)
plot.add_layout(labels)

# Create a hover tool
hover_tool = HoverTool(tooltips=[
    ("Node", "@index"),
    ("URL", "@URL")
])

# Add the hover tool to the plot
plot.add_tools(hover_tool)

# Show the plot
show(plot)