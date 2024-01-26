from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxZoomTool, ResetTool, OpenURL
from bokeh.plotting import figure, from_networkx, show
from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxZoomTool, ResetTool, OpenURL, ColumnDataSource, LabelSet
from bokeh.palettes import Spectral4
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with URL attributes
G.add_node('A', URL='https://github.com/arne-cl/discoursegraphs')
G.add_node('B', URL='http://example.com/B')
G.add_node('C', URL='http://example.com/C')

# Add edges
G.add_edge('A', 'B')
G.add_edge('B', 'C')
# G.add_edge('C', 'A')

# Create a Bokeh plot with the graph
plot = Plot(width=400, height=400, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Clickable Graph"

# Create a graph renderer from the NetworkX graph
mapping = {node_label: index for index, node_label in enumerate(G.nodes())}
H = nx.relabel_nodes(G, mapping)
pos = nx.spring_layout(H)
graph_renderer = from_networkx(H, pos)
# graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

# Customize the nodes
graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

# Customize the edges
graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

# Highlight nodes and edges on selection or hover
graph_renderer.selection_policy = NodesAndLinkedEdges()
graph_renderer.inspection_policy = EdgesAndLinkedNodes()

# Add node labels
x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
node_labels = list(G.nodes())
source = ColumnDataSource({'x': x, 'y': y, 'node_labels': node_labels})
labels = LabelSet(x='x', y='y', text='node_labels', source=source,
                  background_fill_color='white', text_align='center', text_baseline='middle')

# Add the graph renderer to the plot
plot.renderers.append(graph_renderer)
plot.add_layout(labels)

# # Add tools for interaction
# url = "@URL"
# taptool = plot.select(type=TapTool)
# taptool.callback = OpenURL(url=url)
# plot.add_tools(HoverTool(tooltips=[("URL", "@URL")]), TapTool(), BoxZoomTool(), ResetTool())

# Create a hover tool
hover_tool = HoverTool(tooltips=[
    ("Node", "@index"),
    ("URL", "@URL")
])

# Add the hover tool to the plot
plot.add_tools(hover_tool)

# Show the plot
show(plot)