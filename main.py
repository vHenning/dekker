import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
g = nx.DiGraph()

# Add nodes
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

# Add edges with directions
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "D")
g.add_edge("D", "A")

# Draw the graph
pos = nx.spring_layout(g)  # Positions of nodes for visualization
nx.draw(g, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=12, font_color="black", arrows=True)

# Show the graph
plt.axis("off")
plt.show()
