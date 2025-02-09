import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_graphml("output.graphml")  # Load the saved graph
pos = nx.spring_layout(G)  # Layout for better visualization
weights = nx.get_edge_attributes(G, "weight")

nx.draw(G, pos, with_labels=False, node_color="skyblue", edge_color="gray", node_size=5, font_size=10)
#nx.draw_networkx_edge(G, pos, edge_labels = weights)  # Show edge weights
plt.show()