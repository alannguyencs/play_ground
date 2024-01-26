import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add edges with color attributes
G.add_edge('A', 'B', color='blue')
G.add_edge('B', 'C', color='green')
G.add_edge('C', 'A', color='blue')
G.add_edge('D', 'A', color='green')

# Get the colors from the graph
edge_colors = [G[u][v]['color'] for u, v in G.edges()]

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, edge_color=edge_colors, with_labels=True, arrows=True)

# Show the plot
plt.show()