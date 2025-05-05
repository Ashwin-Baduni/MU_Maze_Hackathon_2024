from maze import MazeGraph

# Create a new graph
graph = MazeGraph()

# Add nodes to the graph
node1 = graph.add_node((0, 0))
node2 = graph.add_node((0, 1))

# Add edges to the graph
edge1 = graph.add_edge(node1, node2, 1)

# Save the graph to a file
graph.save_to_file('graph.pkl')

# Load the graph from a file
new_graph = MazeGraph()
new_graph.load_from_file('graph.pkl')

# Print the nodes and edges of the new graph
print(new_graph)
new_graph.draw()

# Create a new random graph
random_graph = MazeGraph()
random_graph.randomize_maze(10, 10)
random_graph.draw()