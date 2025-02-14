import matplotlib.pyplot as plt
import networkx as nx

G = nx.read_graphml("../raw_data/sample_1/graphs/output.graphml")  # Load the saved graph
pos = nx.spring_layout(G)  # Layout for better visualization
weights = nx.get_edge_attributes(G, "weight")

nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray", node_size=50, font_size=10)
nx.draw_networkx_edges(G, pos)  # Show edge weights
plt.show()