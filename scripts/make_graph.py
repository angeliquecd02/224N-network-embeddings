#currently does nodes as posts and edges as users --> goal is nodes as subreddits and edges as users
import json
import networkx as nx
from collections import defaultdict

def json_to_graph(input_file, output_file, format="graphml"):
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    # Build a mapping of titles to users
    title_to_users = defaultdict(set)
    for entry in data:
        title_to_users[entry["id"]].add(entry["author"])

    # Create an undirected graph
    G = nx.Graph()

    # Add nodes (titles)
    for title in title_to_users:
        G.add_node(title)

    # Add edges based on shared users
    titles = list(title_to_users.keys())
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            title1, title2 = titles[i], titles[j]
            common_users = title_to_users[title1] & title_to_users[title2]  # Set intersection
            if common_users:  # If there are shared users, create an edge
                G.add_edge(title1, title2, weight=len(common_users))

    # Save the graph in the requested format
    if format == "graphml":
        nx.write_graphml(G, output_file)
    elif format == "gexf":
        nx.write_gexf(G, output_file)
    elif format == "adjlist":
        nx.write_adjlist(G, output_file)
    else:
        raise ValueError("Unsupported format. Use 'graphml', 'gexf', or 'adjlist'.")

    print(f"Graph saved to '{output_file}' in {format.upper()} format.")

# Example usage: Convert to GraphML
json_to_graph("raw_data/filtered_data/ActivationSound_submissions.zst", "output.graphml", format="graphml")
